# -*- coding: utf-8 -*-
"""스틸 애니매틱 렌더.

usage: python3 animatic_E1_v062.py <animatic.json> <out.mp4>
clip 이 있는 행은 그 구간을 1080x1920 으로 넣고 오디오를 포함한다.
없는 행은 src 가 mp4 면 그 영상, png 면 느린 줌이다. skip 행은 빼 둔다.
길이는 cv2 로 센다. ffprobe 는 쓰지 않는다.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

MAC_ROOT = "/Users/ymy/project/sns"
MAC_FFMPEG = "/Users/ymy/project/ai-creative-studio/node_modules/ffmpeg-static/ffmpeg"
WIDTH = 1080
HEIGHT = 1920
FPS = 30


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", ".."))


def episode_root():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R")


def ffmpeg_bin():
    if os.path.isfile(MAC_FFMPEG) and os.access(MAC_FFMPEG, os.X_OK):
        return MAC_FFMPEG
    found = shutil.which("ffmpeg")
    if not found:
        raise SystemExit("ffmpeg 없음")
    return found


def resolve_path(path):
    if not path:
        return ""
    path = os.path.expanduser(str(path))
    if os.path.isfile(path):
        return path
    root = repo_root()
    episode = episode_root()
    if path.startswith(MAC_ROOT + "/") or path.startswith(MAC_ROOT + os.sep):
        alt = os.path.join(root, path[len(MAC_ROOT):].lstrip("/\\"))
        if os.path.isfile(alt):
            return alt
    if not os.path.isabs(path):
        for base in (episode, root, os.getcwd()):
            alt = os.path.join(base, path)
            if os.path.isfile(alt):
                return alt
    return path


def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace")[-2000:]
        raise SystemExit(err or "ffmpeg 실패")
    return proc


def has_audio(ff, path):
    proc = subprocess.run([ff, "-hide_banner", "-i", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return b"Audio:" in proc.stderr


def video_filter():
    return (
        "scale={w}:{h}:force_original_aspect_ratio=decrease,"
        "pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps={fps},format=yuv420p"
    ).format(w=WIDTH, h=HEIGHT, fps=FPS)


def encode_tail(dest):
    return [
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
        dest,
    ]


def render_clip(ff, src, t0, t1, dest):
    dur = max(0.05, float(t1) - float(t0))
    filt = video_filter()
    if has_audio(ff, src):
        graph = (
            "[0:v]{filt}[v];"
            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=0:{dur}[a]"
        ).format(filt=filt, dur=dur)
        cmd = [
            ff, "-y", "-ss", str(t0), "-t", str(dur), "-i", src,
            "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
        ] + encode_tail(dest)
    else:
        graph = "[0:v]{filt}[v]".format(filt=filt)
        cmd = [
            ff, "-y", "-ss", str(t0), "-t", str(dur), "-i", src,
            "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex", graph, "-map", "[v]", "-map", "1:a:0",
        ] + encode_tail(dest)
    run(cmd)


def render_still(ff, src, dur, dest):
    frames = max(1, int(round(float(dur) * FPS)))
    hold = frames / float(FPS)
    zoom = (
        "scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
        "zoompan=z='min(1.0+0.06*on/{frames},1.06)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={fps},"
        "format=yuv420p"
    ).format(w=WIDTH, h=HEIGHT, frames=frames, fps=FPS)
    cmd = [
        ff, "-y", "-loop", "1", "-i", src,
        "-f", "lavfi", "-t", str(hold), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-filter_complex", "[0:v]{0}[v]".format(zoom),
        "-map", "[v]", "-map", "1:a:0", "-frames:v", str(frames),
    ] + encode_tail(dest)
    run(cmd)


def row_duration(row):
    try:
        return float(row.get("dur") or 2.2)
    except (TypeError, ValueError):
        return 2.2


def render_row(ff, row, dest):
    if row.get("clip"):
        src = resolve_path(row.get("clip"))
        if not os.path.isfile(src):
            raise SystemExit("컷 {0}: clip 없음 ({1})".format(row.get("n"), row.get("clip")))
        t0 = float(row.get("clip_in") or 0.0)
        t1 = row.get("clip_out")
        t1 = float(t1) if t1 is not None else t0 + row_duration(row)
        render_clip(ff, src, t0, t1, dest)
        return
    src = resolve_path(row.get("src"))
    if not os.path.isfile(src):
        raise SystemExit("컷 {0}: src 없음 ({1})".format(row.get("n"), row.get("src")))
    if src.lower().endswith(".mp4"):
        dur = row_duration(row)
        render_clip(ff, src, 0.0, dur, dest)
        return
    render_still(ff, src, row_duration(row), dest)


def concat(ff, parts, dest):
    if len(parts) == 1:
        shutil.copy2(parts[0], dest)
        return
    folder = os.path.dirname(parts[0])
    listing = os.path.join(folder, "list.txt")
    with open(listing, "w", encoding="utf-8") as handle:
        for part in parts:
            handle.write("file '{0}'\n".format(part.replace("'", "'\\''")))
    run([ff, "-y", "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", dest])


def duration_seconds(path):
    import cv2
    cap = cv2.VideoCapture(path)
    try:
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
    finally:
        cap.release()
    if fps <= 1e-3:
        return 0.0
    return float(frames) / float(fps)


def load_rows(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise SystemExit("리스트 json 이 아님")
    return data


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: python3 animatic_E1_v062.py <animatic.json> <out.mp4>\n")
        return 2
    src_json, dest = argv
    rows = [row for row in load_rows(src_json) if not row.get("skip")]
    if not rows:
        raise SystemExit("렌더할 행이 없음")
    ff = ffmpeg_bin()
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="animatic_") as folder:
        parts = []
        for index, row in enumerate(rows):
            part = os.path.join(folder, "p{0:03d}.mp4".format(index))
            render_row(ff, row, part)
            parts.append(part)
        concat(ff, parts, dest)
    sys.stdout.write("{0} cuts, {1:.2f}s → {2}\n".format(len(rows), duration_seconds(dest), dest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
