# -*- coding: utf-8 -*-
"""컷 번호의 최신 Kling 테이크를 모아 qa_<cut>.json 으로 저장한다.

usage: python3 tools/collect_clip_qa.py 3 4 5
face_score.py, clip_qa.py, transcribe.py 를 로컬에서 호출한다. 외부 생성 API 는 호출하지 않는다.
"""
import glob
import json
import os
import re
import subprocess
import sys

FACE_KEYS = ("f25", "f50", "f75", "end")


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def episode_root():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R")


def keyn(value):
    text = str(value).strip()
    return int(text) if text.isdigit() else text


def tagn(number):
    return "{0:02d}".format(number) if isinstance(number, int) else str(number)


def take_num(path):
    match = re.search(r"take(\d+)", os.path.basename(path), re.I)
    return int(match.group(1)) if match else -1


def latest_take(number):
    folder = os.path.join(episode_root(), "video", "v08", "E1_" + tagn(number))
    found = glob.glob(os.path.join(folder, "*_kling3_take*.mp4"))
    if not found:
        return ""
    found.sort(key=lambda path: (take_num(path), os.path.getmtime(path)))
    return found[-1]


def run_tool(args):
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def first_existing(paths):
    for path in paths:
        if os.path.isfile(path):
            return path
    return ""


def clip_qa(video):
    script = os.path.join(repo_root(), "tools", "clip_qa.py")
    code, out, err = run_tool([sys.executable, script, video, "--json"])
    if code != 0:
        return None, err.strip() or out.strip() or "clip_qa 실패"
    try:
        data = json.loads(out)
    except ValueError:
        return None, out.strip()
    if not data:
        return None, "clip_qa 결과 없음"
    return data[0], ""


def transcribe(video):
    script = first_existing([
        os.path.join(episode_root(), "tools", "transcribe.py"),
        os.path.join(repo_root(), "tools", "transcribe.py"),
        os.path.join(repo_root(), "01_EPISODES", "EP01", "tools", "transcribe.py"),
    ])
    if not script:
        return "", "transcribe.py 없음"
    code, out, err = run_tool([sys.executable, script, video])
    if code != 0:
        return "", err.strip() or "transcribe 실패"
    return out.strip(), ""


def face_score(video):
    script = os.path.join(repo_root(), "tools", "face_score.py")
    if not os.path.isfile(script):
        return {}, "face_score.py 없음"
    import cv2
    cap = cv2.VideoCapture(video)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    points = {}
    if count <= 0:
        cap.release()
        return {}, "프레임 없음"
    wanted = {
        "f25": max(0, int(round((count - 1) * 0.25))),
        "f50": max(0, int(round((count - 1) * 0.50))),
        "f75": max(0, int(round((count - 1) * 0.75))),
        "end": max(0, count - 1),
    }
    folder = os.path.dirname(video)
    base = os.path.splitext(os.path.basename(video))[0]
    scores = {}
    errors = []
    try:
        for key, index in wanted.items():
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ok, frame = cap.read()
            if not ok:
                errors.append(key)
                continue
            dest = os.path.join(folder, "{0}_{1}.png".format(base, key))
            cv2.imwrite(dest, frame)
            code, out, err = run_tool([sys.executable, script, dest])
            points[key] = dest
            if code != 0:
                errors.append(err.strip() or key)
                continue
            scores[key] = out.strip().splitlines()[-1] if out.strip() else ""
    finally:
        cap.release()
    note = ""
    if errors:
        note = " ".join(errors)
    return scores, note


def single_from(row):
    if not row:
        return None
    events = " ".join(row.get("events") or [])
    if any(token in events for token in ("HARD_CUT", "WIDE_CUT", "FACE_LOST")):
        return False
    return bool(row.get("pass"))


def collect_one(number):
    video = latest_take(number)
    if not video:
        raise RuntimeError("컷 {0}: mp4 없음".format(number))
    qa, qa_err = clip_qa(video)
    said, said_err = transcribe(video)
    scores, face_err = face_score(video)
    payload = {
        "cut": number if isinstance(number, int) else str(number),
        "clip": video,
        "take": os.path.basename(video),
        "whisper": said,
        "face": {key: scores.get(key, "") for key in FACE_KEYS},
    }
    flag = single_from(qa)
    if flag is not None:
        payload["single_shot"] = flag
    if qa:
        payload["clip_qa"] = qa
    notes = [item for item in (qa_err, said_err, face_err) if item]
    if notes:
        payload["notes"] = notes
    dest = os.path.join(episode_root(), "video", "v08", "qa_{0}.json".format(tagn(number)))
    with open(dest, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=1)
        handle.write("\n")
    return dest


def main(argv):
    if not argv:
        sys.stderr.write("usage: python3 tools/collect_clip_qa.py <컷> [<컷> ...]\n")
        return 2
    failed = 0
    for token in argv:
        number = keyn(token)
        try:
            dest = collect_one(number)
        except RuntimeError as exc:
            sys.stderr.write(str(exc) + "\n")
            failed += 1
            continue
        sys.stdout.write("{0}\n".format(dest))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
