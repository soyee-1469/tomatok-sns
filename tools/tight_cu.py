# -*- coding: utf-8 -*-
"""단독 상반신 스틸을 얼굴 중심 9:16 클로즈업으로 크롭한다.

얼굴 폭이 출력 가로(1080)의 45~50% 가 되게 한다. 원본은 덮어쓰지 않는다.
usage: python3 tools/tight_cu.py
"""
import os
import subprocess
import sys

OUT_W = 1080
OUT_H = 1920
TARGET = 0.475
NAMES = (
    "S_ria_island_act1_cu",
    "S_ria_island_act2_cu",
    "S_suman_island_cu",
    "S_suman_island_look_cu",
    "S_junho_sofa_cu",
    "S_junho_island_r2",
)


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def frames_dir():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R", "frames", "v08")


def plan_crop(img_w, img_h, box):
    """얼굴 박스 (x1,y1,x2,y2) 로 크롭 창을 정한다.

    반환: scale, x, y, crop_w, crop_h (업스케일된 이미지 좌표).
    """
    x1, y1, x2, y2 = [float(v) for v in box]
    face_w = max(1.0, x2 - x1)
    fx = (x1 + x2) / 2.0
    fy = (y1 + y2) / 2.0
    crop_w = face_w / TARGET
    crop_h = crop_w * 16.0 / 9.0
    scale = 1.0
    if crop_w > img_w or crop_h > img_h:
        scale = max(crop_w / float(img_w), crop_h / float(img_h))
    iw = img_w * scale
    ih = img_h * scale
    cw = crop_w * scale
    ch = crop_h * scale
    x0 = fx * scale - cw / 2.0
    y0 = fy * scale - 0.38 * ch
    if x0 < 0:
        x0 = 0.0
    if y0 < 0:
        y0 = 0.0
    if x0 + cw > iw:
        x0 = iw - cw
    if y0 + ch > ih:
        y0 = ih - ch
    if x0 < 0:
        x0 = 0.0
    if y0 < 0:
        y0 = 0.0
    return scale, x0, y0, cw, ch


def render_crop(image, box):
    from PIL import Image
    scale, x0, y0, cw, ch = plan_crop(image.width, image.height, box)
    if scale > 1.0 + 1e-6:
        resized = (
            max(1, int(round(image.width * scale))),
            max(1, int(round(image.height * scale))),
        )
        image = image.resize(resized, Image.Resampling.LANCZOS)
    x = int(round(x0))
    y = int(round(y0))
    w = max(1, int(round(cw)))
    h = max(1, int(round(ch)))
    if x + w > image.width:
        x = max(0, image.width - w)
    if y + h > image.height:
        y = max(0, image.height - h)
    w = min(w, image.width - x)
    h = min(h, image.height - y)
    cropped = image.crop((x, y, x + w, y + h))
    return cropped.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS), scale


def largest_box(frame):
    import io
    from contextlib import redirect_stdout
    from insightface.app import FaceAnalysis
    sink = io.StringIO()
    with redirect_stdout(sink):
        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=0, det_size=(640, 640))
        faces = app.get(frame)
    if not faces:
        return None
    best = max(faces, key=lambda face: float(face.bbox[2] - face.bbox[0]))
    return [float(v) for v in best.bbox]


def face_score_text(path):
    script = os.path.join(repo_root(), "tools", "face_score.py")
    if not os.path.isfile(script):
        return "face_score.py 없음"
    proc = subprocess.run(
        [sys.executable, script, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    text = (proc.stdout or "").strip().replace("\n", " ")
    if proc.returncode != 0:
        err = (proc.stderr or "").strip().replace("\n", " ")
        return "face_score 실패 {0} {1}".format(proc.returncode, err or text)
    return text or "(출력 없음)"


def crop_file(src, dest):
    import cv2
    from PIL import Image
    if os.path.abspath(src) == os.path.abspath(dest):
        raise RuntimeError("원본과 출력이 같음: {0}".format(src))
    frame = cv2.imread(src)
    if frame is None:
        raise RuntimeError("이미지를 열 수 없음: {0}".format(src))
    box = largest_box(frame)
    if box is None:
        raise RuntimeError("얼굴 없음: {0}".format(src))
    image = Image.open(src).convert("RGB")
    out, scale = render_crop(image, box)
    out.save(dest)
    return {
        "face_w": box[2] - box[0],
        "scale": scale,
        "out_w": int(round(OUT_W * TARGET)),
    }


def main():
    folder = frames_dir()
    missing = []
    rows = []
    for name in NAMES:
        src = os.path.join(folder, name + ".png")
        dest = os.path.join(folder, name + "_tight.png")
        if not os.path.isfile(src):
            missing.append(src)
            continue
        info = crop_file(src, dest)
        score = face_score_text(dest)
        rows.append((name, dest, info["out_w"], score))
    if missing:
        for path in missing:
            sys.stderr.write("원본 없음: {0}\n".format(path))
    sys.stdout.write("이름\t출력얼굴폭px\tface_score\t파일\n")
    for name, dest, width, score in rows:
        sys.stdout.write("{0}\t{1}\t{2}\t{3}\n".format(name, width, score, dest))
    if missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
