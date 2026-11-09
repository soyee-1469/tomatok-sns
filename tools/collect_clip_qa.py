# -*- coding: utf-8 -*-
"""컷 번호의 최신 Kling 테이크를 로컬 QA해서 video/v08/qa_<cut>.json 으로 저장한다.

usage: python3 tools/collect_clip_qa.py 3 4 5
face_score.py, clip_qa.py, transcribe.py 를 호출한다. 생성 API는 호출하지 않는다.
"""
import glob
import json
import os
import re
import subprocess
import sys

import cv2

FACE_KEYS = ("f25", "f50", "f75", "end")
MAC_ROOT = "/Users/ymy/project/sns"


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def episode_root():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R")


def tool(*parts):
    return os.path.join(repo_root(), *parts)


def take_num(path):
    match = re.search(r"take(\d+)", os.path.basename(path), re.I)
    return int(match.group(1)) if match else -1


def latest_take(number):
    folder = os.path.join(episode_root(), "video", "v08", "E1_{0:02d}".format(number))
    found = glob.glob(os.path.join(folder, "*_kling3_take*.mp4"))
    if not found:
        raise SystemExit("컷 {0}: mp4 없음 ({1})".format(number, folder))
    found.sort(key=lambda path: (take_num(path), os.path.getmtime(path)))
    return found[-1]


def run_cmd(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or ""), (proc.stderr or "")


def parse_face_text(text):
    match = re.search(r"(\d+\.\d+)\s*\(\s*(\d+)\s*px\s*\)", text or "")
    if not match:
        match = re.search(r"score\s*[:=]\s*(\d+\.\d+).{0,40}?(\d+)\s*px", text or "", re.I)
    if not match:
        return None
    return [float(match.group(1)), int(match.group(2))]


def frame_at(path, fraction, dest):
    cap = cv2.VideoCapture(path)
    try:
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        if frames < 1:
            raise SystemExit("프레임 없음: {0}".format(path))
        index = min(frames - 1, max(0, int(round((frames - 1) * fraction))))
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, frame = cap.read()
        if not ok:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = cap.read()
        if not ok:
            raise SystemExit("프레임을 읽지 못함: {0}".format(path))
        cv2.imwrite(dest, frame)
    finally:
        cap.release()


def score_frame(image_path):
    script = tool("tools", "face_score.py")
    if not os.path.isfile(script):
        return None, "face_score.py 없음"
    code, out, err = run_cmd([sys.executable, script, image_path])
    text = out.strip() or err.strip()
    return parse_face_text(text), text if code != 0 else ""


def clip_qa(path):
    script = tool("tools", "clip_qa.py")
    code, out, err = run_cmd([sys.executable, script, "--json", path])
    if code != 0:
        raise SystemExit("clip_qa 실패: {0}".format(err.strip() or out.strip()))
    data = json.loads(out)
    if not data:
        raise SystemExit("clip_qa 결과 없음")
    return data[0]


def transcribe(path):
    candidates = [
        tool("01_EPISODES", "EP01R", "tools", "transcribe.py"),
        tool("tools", "transcribe.py"),
        tool("01_EPISODES", "EP01", "tools", "transcribe.py"),
    ]
    script = next((item for item in candidates if os.path.isfile(item)), None)
    if script is None:
        return "", "transcribe.py 없음"
    code, out, err = run_cmd([sys.executable, script, path])
    if code != 0:
        return "", err.strip() or out.strip()
    return out.strip(), ""


def rel_clip(path):
    ep = episode_root()
    if path.startswith(ep + os.sep):
        return path[len(ep) + 1:].replace(os.sep, "/")
    if path.startswith(MAC_ROOT + "/"):
        rest = path[len(MAC_ROOT) + 1:]
        marker = "01_EPISODES/EP01R/"
        if marker in rest:
            return rest.split(marker, 1)[1]
    return path


def collect_one(number):
    clip = latest_take(number)
    qa = clip_qa(clip)
    events = qa.get("events") or []
    single = not any(
        item.startswith("HARD_CUT") or item.startswith("WIDE_CUT") or item.startswith("FACE_LOST")
        or item.startswith("CAMERA_MOVE")
        for item in events
    )
    work = os.path.join(episode_root(), "video", "v08", "_qa_frames")
    os.makedirs(work, exist_ok=True)
    face = {}
    notes = []
    fractions = (0.25, 0.50, 0.75, 1.0)
    for key, fraction in zip(FACE_KEYS, fractions):
        image = os.path.join(work, "E1_{0:02d}_{1}.png".format(number, key))
        frame_at(clip, fraction, image)
        parsed, note = score_frame(image)
        face[key] = parsed
        if note:
            notes.append("{0}: {1}".format(key, note))
        if os.path.isfile(image):
            os.remove(image)
    whisper, whisper_note = transcribe(clip)
    if whisper_note:
        notes.append(whisper_note)
    record = {
        "cut": number,
        "clip": rel_clip(clip),
        "take": "take{0:02d}".format(take_num(clip)) if take_num(clip) >= 0 else os.path.basename(clip),
        "single_shot": single,
        "face": face,
        "whisper": whisper,
        "clip_qa": qa,
    }
    if notes:
        record["notes"] = notes
    dest = os.path.join(episode_root(), "video", "v08", "qa_{0}.json".format(number))
    with open(dest, "w", encoding="utf-8") as handle:
        json.dump(record, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return dest, single


def main(argv):
    if not argv:
        sys.stderr.write("usage: python3 tools/collect_clip_qa.py <cut> [<cut> ...]\n")
        return 2
    for token in argv:
        number = int(token)
        dest, single = collect_one(number)
        sys.stdout.write("{0} single={1}\n".format(dest, "yes" if single else "no"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
