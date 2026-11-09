# -*- coding: utf-8 -*-
"""애니매틱 JSON을 1080x1920 mp4로 렌더한다.

usage: python3 animatic_E1_v062.py <animatic_json> <out.mp4>
row.clip 이 있으면 clip_in~clip_out 구간을 스케일하고 오디오를 넣는다.
없으면 src가 mp4면 그 영상, png면 느린 줌. dur이 없으면 2.2초.
자막은 tools/subtitle_style.render 가 있을 때만 호출한다.
길이는 cv2로 센다. ffprobe는 쓰지 않는다.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import cv2

MAC_ROOT = "/Users/ymy/project/sns"
FFMPEG_MAC = "/Users/ymy/project/ai-creative-studio/node_modules/ffmpeg-static/ffmpeg"
WIDTH = 1080
HEIGHT = 1920
FPS = 30


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", ".."))


def episode_root():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R")


def ffmpeg_bin():
    if os.path.isfile(FFMPEG_MAC) and os.access(FFMPEG_MAC, os.X_OK):
        return FFMPEG_MAC
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise SystemExit("ffmpeg 없음")


def resolve_path(path):
    if not path:
        return ""
    path = os.path.expanduser(str(path))
    if os.path.isfile(path):
        return path
    if path.startswith(MAC_ROOT + "/") or path.startswith(MAC_ROOT + os.sep):
        alt = os.path.join(repo_root(), path[len(MAC_ROOT):].lstrip("/"))
        if os.path.isfile(alt):
            return alt
    if not os.path.isabs(path):
        local = os.path.join(episode_root(), path)
        if os.path.isfile(local):
            return local
    return path


def load_rows(path):
    import json
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise SystemExit("애니매틱 JSON은 리스트여야 함")
    rows = []
    for row in data:
        if row.get("skip"):
            continue
        rows.append(row)
    return rows


def duration_of(path):
    cap = cv2.VideoCapture(path)
    try:
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        if fps <= 1e-3:
            return 0.0
        return float(frames) / float(fps)
    finally:
        cap.release()


def has_audio(ffmpeg, path):
    proc = subprocess.run([ffmpeg, "-hide_banner", "-i", path], capture_output=True, text=True)
    return "Audio:" in (proc.stderr or "")


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or "")[-2000:]
        raise SystemExit("ffmpeg 실패\n{0}".format(tail))


def encode_clip(ffmpeg, src, dest, start, dur):
    vf = "scale={0}:{1}:force_original_aspect_ratio=increase,crop={0}:{1},setsar=1,fps={2}".format(
        WIDTH, HEIGHT, FPS
    )
    cmd = [
        ffmpeg, "-y", "-i", src, "-ss", "{:.3f}".format(start), "-t", "{:.3f}".format(dur),
        "-vf", vf, "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast",
        "-r", str(FPS),
    ]
    if has_audio(ffmpeg, src):
        cmd += ["-map", "0:v:0", "-map", "0:a:0", "-c:a", "aac", "-ac", "2", "-ar", "48000"]
    else:
        cmd += [
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-shortest",
        ]
    cmd.append(dest)
    run(cmd)


def encode_still(ffmpeg, src, dest, dur):
    frames = max(1, int(round(dur * FPS)))
    vf = (
        "scale={0}:{1}:force_original_aspect_ratio=increase,crop={0}:{1},"
        "zoompan=z='min(zoom+0.0010,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        "d={2}:s={0}x{1}:fps={3},setsar=1"
    ).format(WIDTH, HEIGHT, frames, FPS)
    cmd = [
        ffmpeg, "-y", "-loop", "1", "-i", src,
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", vf, "-frames:v", str(frames),
        "-map", "0:v:0", "-map", "1:a:0",
        "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast",
        "-c:a", "aac", "-shortest", dest,
    ]
    run(cmd)


def try_subtitle(segment, row, work):
    tools = os.path.join(repo_root(), "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    try:
        import subtitle_style
    except ImportError:
        return segment
    render = getattr(subtitle_style, "render", None)
    if not callable(render):
        return segment
    dest = os.path.join(work, "sub_{0}.mp4".format(row.get("n")))
    try:
        result = render(segment, dest, row.get("line") or "")
    except TypeError:
        try:
            result = render(segment, row.get("line") or "")
        except Exception as exc:
            sys.stderr.write("subtitle_style.render 건너뜀: {0}\n".format(exc))
            return segment
    except Exception as exc:
        sys.stderr.write("subtitle_style.render 건너뜀: {0}\n".format(exc))
        return segment
    if isinstance(result, str) and os.path.isfile(result):
        return result
    if os.path.isfile(dest):
        return dest
    return segment


def segment_for(row, ffmpeg, work, warned):
    number = row.get("n")
    dest = os.path.join(work, "seg_{0}.mp4".format(number))
    if row.get("clip"):
        src = resolve_path(row.get("clip"))
        if not os.path.isfile(src):
            raise SystemExit("컷 {0} 클립 없음: {1}".format(number, src))
        start = float(row.get("clip_in") or 0.0)
        end = row.get("clip_out")
        if end is None:
            end = start + float(row.get("dur") or 2.2)
        dur = float(end) - start
        if dur <= 0:
            raise SystemExit("컷 {0} clip 길이가 0 이하".format(number))
        encode_clip(ffmpeg, src, dest, start, dur)
    else:
        src = resolve_path(row.get("src"))
        if not os.path.isfile(src):
            raise SystemExit("컷 {0} src 없음: {1}".format(number, src))
        dur = float(row.get("dur") or 2.2)
        if src.lower().endswith(".mp4"):
            encode_clip(ffmpeg, src, dest, 0.0, dur)
        else:
            encode_still(ffmpeg, src, dest, dur)
    if not warned["sub"] and not _subtitle_module_exists():
        sys.stderr.write("subtitle_style 없음. 자막 없이 렌더한다.\n")
        warned["sub"] = True
    return try_subtitle(dest, row, work)


def _subtitle_module_exists():
    return os.path.isfile(os.path.join(repo_root(), "tools", "subtitle_style.py"))


def concat(ffmpeg, segments, dest):
    listing = dest + ".concat.txt"
    with open(listing, "w", encoding="utf-8") as handle:
        for path in segments:
            handle.write("file '{0}'\n".format(path.replace("'", "'\\''")))
    run([
        ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", listing,
        "-c", "copy", dest,
    ])
    os.remove(listing)


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: python3 animatic_E1_v062.py <animatic_json> <out.mp4>\n")
        return 2
    json_path, out_path = argv
    rows = load_rows(json_path)
    if not rows:
        raise SystemExit("렌더할 행이 없음")
    ffmpeg = ffmpeg_bin()
    work = tempfile.mkdtemp(prefix="animatic_")
    warned = {"sub": False}
    try:
        segments = []
        for row in rows:
            segments.append(segment_for(row, ffmpeg, work, warned))
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
        concat(ffmpeg, segments, out_path)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    dur = duration_of(out_path)
    sys.stdout.write("{0} cuts {1}s {2}\n".format(len(rows), round(dur, 2), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
