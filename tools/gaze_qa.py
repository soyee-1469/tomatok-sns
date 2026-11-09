# -*- coding: utf-8 -*-
"""시선·고개 방향 QA. 생성은 하지 않는다.

usage: python3 tools/gaze_qa.py <animatic.json> [--out <report.md>]
insightface pose 는 (pitch, yaw, roll) 도 단위. yaw 가 양수면 화면 왼쪽을 보는 쪽으로 적는다.
눈동자는 2d106 에서 눈 영역 중심과 그 안의 가장 안쪽 점의 오프셋으로 대략만 본다.
"""
import argparse
import io
import os
import sys
from contextlib import redirect_stdout

YAW_MIN = 12.0
PITCH_MIN = 12.0


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def keyn(value):
    text = str(value).strip()
    return int(text) if text.isdigit() else text


def sort_key(number):
    import re
    match = re.match(r"(\d+)(.*)", str(number))
    if not match:
        return (9999, str(number))
    return (int(match.group(1)), match.group(2))


def resolve(path):
    if os.path.isfile(path):
        return path
    mac = "/Users/ymy/project/sns"
    if str(path).startswith(mac + "/"):
        alt = os.path.join(repo_root(), str(path)[len(mac):].lstrip("/"))
        if os.path.isfile(alt):
            return alt
    if path and not os.path.isabs(path):
        alt = os.path.join(repo_root(), path)
        if os.path.isfile(alt):
            return alt
    return path


def intended(text):
    text = text or ""
    if "폰을 보" in text or "화면" in text:
        return "아래"
    if "올려다" in text:
        return "위"
    if "소파 쪽" in text or "카메라-LEFT" in text or "왼쪽" in text:
        return "왼쪽"
    if "리아를" in text or "준호를 바라" in text:
        return "상대"
    if "카메라" in text:
        return "정면"
    return ""


def resolve_intent(who, direction):
    if direction != "상대":
        return direction
    who = who or ""
    if "리아" in who:
        return "왼쪽"
    if "준호" in who:
        return "오른쪽"
    return "상대"


def load_app():
    from insightface.app import FaceAnalysis
    sink = io.StringIO()
    with redirect_stdout(sink):
        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def pupil_offset(face):
    """눈 중심 대비 안쪽 점 오프셋. (dx, dy) 는 눈 너비로 나눈 값. 오른쪽·아래가 양수."""
    import numpy as np
    pts = getattr(face, "landmark_2d_106", None)
    if pts is None:
        return None
    arr = np.asarray(pts, dtype="float32")
    if arr.ndim != 2 or arr.shape[0] < 20:
        return None
    x1, y1, x2, y2 = [float(v) for v in face.bbox]
    height = max(1.0, y2 - y1)
    mid = (x1 + x2) / 2.0
    upper = arr[(arr[:, 1] >= y1 + 0.18 * height) & (arr[:, 1] <= y1 + 0.55 * height)]
    if len(upper) < 6:
        return None
    offsets = []
    for side in (upper[upper[:, 0] < mid], upper[upper[:, 0] >= mid]):
        if len(side) < 3:
            continue
        center = side.mean(axis=0)
        dists = np.linalg.norm(side - center, axis=1)
        iris = side[int(np.argmin(dists))]
        rest = side[dists > 1.0]
        eye = rest.mean(axis=0) if len(rest) else center
        width = max(1.0, float(side[:, 0].max() - side[:, 0].min()))
        offsets.append(((iris[0] - eye[0]) / width, (iris[1] - eye[1]) / width))
    if not offsets:
        return None
    dx = sum(item[0] for item in offsets) / len(offsets)
    dy = sum(item[1] for item in offsets) / len(offsets)
    return dx, dy


def measure_dir(pose, pupil):
    pitch, yaw = 0.0, 0.0
    if pose is not None and len(pose) >= 2:
        pitch = float(pose[0])
        yaw = float(pose[1])
    horiz = ""
    vert = ""
    if yaw >= YAW_MIN:
        horiz = "왼쪽"
    elif yaw <= -YAW_MIN:
        horiz = "오른쪽"
    if pitch >= PITCH_MIN:
        vert = "아래"
    elif pitch <= -PITCH_MIN:
        vert = "위"
    if pupil is not None:
        dx, dy = pupil
        if abs(dy) >= 0.15 and not vert:
            vert = "아래" if dy > 0 else "위"
        if abs(dx) >= 0.15 and not horiz:
            horiz = "오른쪽" if dx > 0 else "왼쪽"
    if vert and (not horiz or abs(pitch) >= abs(yaw)):
        return vert, pitch, yaw
    if horiz:
        return horiz, pitch, yaw
    return "정면", pitch, yaw


def person_label(row, face, index):
    who = str(row.get("who") or "").strip()
    if who and index == 0:
        return who
    if who and "," in who:
        parts = [part.strip() for part in who.split(",") if part.strip()]
        if index < len(parts):
            return parts[index]
    return who or "얼굴{0}".format(index + 1)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    import json
    with open(args.json_path, encoding="utf-8") as handle:
        rows = json.load(handle)
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.json_path)), "gaze_report.md")
    try:
        app = load_app()
    except Exception as exc:
        sys.stderr.write("insightface 를 쓸 수 없음: {0}\n".format(exc))
        return 2
    import cv2
    lines = ["# 시선 QA", ""]
    mismatches = []
    checked = 0
    for row in sorted(rows, key=lambda item: sort_key(item.get("n"))):
        if row.get("skip"):
            continue
        if row.get("kind") not in (None, "", "still"):
            continue
        src = resolve(str(row.get("src") or ""))
        if not src.lower().endswith(".png"):
            continue
        number = keyn(row.get("n"))
        if not os.path.isfile(src):
            lines.append("- 컷 {0} 파일 없음".format(number))
            continue
        frame = cv2.imread(src)
        if frame is None:
            lines.append("- 컷 {0} 파일 없음".format(number))
            continue
        sink = io.StringIO()
        with redirect_stdout(sink):
            found = app.get(frame)
        text = " ".join([str(row.get("dir_override") or ""), str(row.get("action") or "")])
        intent = resolve_intent(str(row.get("who") or ""), intended(text))
        found = sorted(found, key=lambda face: float(face.bbox[2] - face.bbox[0]), reverse=True)
        for index, face in enumerate(found):
            checked += 1
            measured, pitch, yaw = measure_dir(getattr(face, "pose", None), pupil_offset(face))
            label = person_label(row, face, index)
            if intent and measured != intent:
                mismatches.append((number, label, intent, measured, yaw, pitch))
    lines.append("검사한 얼굴 {0}".format(checked))
    lines.append("")
    lines.append("## 어긋남")
    if not mismatches:
        lines.append("없음")
    for number, label, intent, measured, yaw, pitch in mismatches:
        lines.append(
            "컷 {0} <{1}> 의도={2} 측정={3} (yaw {4:.1f}, pitch {5:.1f})".format(
                number, label, intent, measured, yaw, pitch
            )
        )
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    sys.stdout.write("{0}\n".format(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
