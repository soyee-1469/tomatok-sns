# -*- coding: utf-8 -*-
"""스틸 얼굴 띠와 마스터 대비 동일인 점수.

usage: python3 tools/face_strip.py <animatic.json> --out <report.md>
얼굴 스왑이나 복원은 하지 않는다. skip 행은 빼고 kind=still 만 본다.
점수 0.35 미만은 띠에서 빨간 테두리, 보고서에는 재생성 후보로 적는다.
"""
import argparse
import io
import os
import sys
from contextlib import redirect_stdout

MASTERS = (
    ("준호", "00_MASTER_ASSETS/CAST_v8_six/JUNHO_face_C.png"),
    ("리아", "00_MASTER_ASSETS/CAST_v8_six/BEA_MASTER_FACE.png"),
    ("수만", "00_MASTER_ASSETS/CAST_v8_six/SUMAN_face.png"),
)
DRIFT = 0.35
COLS = 12


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
    if path.startswith(mac + "/"):
        alt = os.path.join(repo_root(), path[len(mac):].lstrip("/"))
        if os.path.isfile(alt):
            return alt
    if not os.path.isabs(path):
        alt = os.path.join(repo_root(), path)
        if os.path.isfile(alt):
            return alt
    return path


def load_app():
    from insightface.app import FaceAnalysis
    sink = io.StringIO()
    with redirect_stdout(sink):
        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def faces_of(app, path):
    import cv2
    frame = cv2.imread(path)
    if frame is None:
        return None, []
    sink = io.StringIO()
    with redirect_stdout(sink):
        found = app.get(frame)
    return frame, list(found)


def embedding(face):
    import numpy as np
    vec = getattr(face, "normed_embedding", None)
    if vec is None:
        vec = getattr(face, "embedding", None)
    if vec is None:
        return None
    arr = np.asarray(vec, dtype="float32")
    norm = float(np.linalg.norm(arr))
    if norm <= 1e-8:
        return None
    return arr / norm


def cosine(left, right):
    import numpy as np
    return float(np.dot(left, right))


def master_bank(app):
    bank = []
    missing = []
    for label, rel in MASTERS:
        path = resolve(os.path.join(repo_root(), rel))
        if not os.path.isfile(path):
            missing.append(rel)
            continue
        _frame, found = faces_of(app, path)
        if not found:
            missing.append(rel + " (얼굴 없음)")
            continue
        best = max(found, key=lambda face: float(face.bbox[2] - face.bbox[0]))
        vec = embedding(best)
        if vec is None:
            missing.append(rel + " (임베딩 없음)")
            continue
        bank.append((label, vec))
    return bank, missing


def match_person(bank, face):
    vec = embedding(face)
    if vec is None or not bank:
        return "미상", 0.0
    scored = [(label, cosine(vec, ref)) for label, ref in bank]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[0]


def still_rows(path):
    import json
    with open(path, encoding="utf-8") as handle:
        rows = json.load(handle)
    chosen = []
    for row in rows:
        if row.get("skip"):
            continue
        if row.get("kind") != "still":
            continue
        src = str(row.get("src") or "")
        if not src.lower().endswith(".png"):
            continue
        chosen.append(row)
    chosen.sort(key=lambda row: sort_key(row.get("n")))
    return chosen


def episode_tag(json_path):
    base = os.path.basename(json_path)
    if "E2" in base:
        return "E2"
    return "E1"


def build_strip(items, dest):
    from PIL import Image, ImageDraw
    cell_w, cell_h = 180, 220
    cols = COLS
    rows = max(1, (len(items) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (24, 22, 18))
    draw = ImageDraw.Draw(sheet)
    for index, item in enumerate(items):
        col = index % cols
        row = index // cols
        x = col * cell_w
        y = row * cell_h
        crop = item["crop"]
        crop.thumbnail((cell_w - 16, cell_h - 36))
        px = x + (cell_w - crop.width) // 2
        py = y + 28
        sheet.paste(crop, (px, py))
        draw.text((x + 8, y + 6), "컷 {0}".format(item["n"]), fill=(240, 232, 220))
        if item["score"] < DRIFT:
            draw.rectangle((x + 2, y + 2, x + cell_w - 3, y + cell_h - 3), outline=(200, 48, 32), width=4)
    sheet.save(dest, quality=85)


def crop_face(frame, box):
    from PIL import Image
    import cv2
    x1, y1, x2, y2 = [int(round(float(v))) for v in box]
    h, w = frame.shape[:2]
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)
    chip = frame[y1:y2, x1:x2]
    if chip.size == 0:
        chip = frame
    rgb = cv2.cvtColor(chip, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    rows = still_rows(args.json_path)
    try:
        app = load_app()
    except Exception as exc:
        sys.stderr.write("insightface 를 쓸 수 없음: {0}\n".format(exc))
        return 2
    bank, missing_masters = master_bank(app)
    lines = ["# 얼굴 띠", ""]
    if missing_masters:
        lines.append("마스터 없음: " + ", ".join(missing_masters))
        lines.append("")
    items = []
    flagged = []
    for row in rows:
        number = keyn(row.get("n"))
        src = resolve(str(row.get("src")))
        if not os.path.isfile(src):
            lines.append("- 컷 {0} 파일 없음".format(number))
            continue
        frame, found = faces_of(app, src)
        if frame is None or not found:
            lines.append("- 컷 {0} 얼굴 없음".format(number))
            continue
        for face in found:
            label, score = match_person(bank, face)
            items.append({
                "n": number,
                "crop": crop_face(frame, face.bbox),
                "score": score,
                "label": label,
            })
            if score < DRIFT:
                flagged.append((number, label, score))
    folder = os.path.dirname(os.path.abspath(args.json_path))
    strip_path = os.path.join(folder, "face_strip_{0}.jpg".format(episode_tag(args.json_path)))
    if items:
        build_strip(items, strip_path)
        lines.append("띠: {0} ({1}얼굴)".format(os.path.basename(strip_path), len(items)))
    else:
        lines.append("띠를 만들 얼굴이 없음")
    lines.append("")
    lines.append("## 재생성 후보")
    if not flagged:
        lines.append("없음")
    for number, label, score in flagged:
        lines.append("컷 {0} <{1}> {2:.2f} ← 재생성 후보".format(number, label, score))
    out = args.out
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    sys.stdout.write("{0}\n".format(out))
    if missing_masters or not items:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
