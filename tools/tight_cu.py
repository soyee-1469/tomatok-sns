# -*- coding: utf-8 -*-
"""단독 상반신 스틸을 얼굴 중심 9:16 타이트 크롭으로 만든다.

usage:
  python3 tools/tight_cu.py
  python3 tools/tight_cu.py S_ria_island_act1_cu [이름 ...]
  python3 tools/tight_cu.py still.png --out-dir <dir>
기본 6장을 frames/v08/<이름>_tight.png (1080x1920)로 쓴다. 원본은 덮어쓰지 않는다.
얼굴 폭이 출력 가로의 45~50%가 되도록 크롭하고, 얼굴 중심은 가로 중앙·세로 38%에 둔다.
"""
import contextlib
import os
import subprocess
import sys

import cv2
from PIL import Image

OUT_W = 1080
OUT_H = 1920
RATIO_LO = 0.45
RATIO_HI = 0.50
RATIO_MID = 0.475
FACE_Y = 0.38
DEFAULTS = (
    "S_ria_island_act1_cu",
    "S_ria_island_act2_cu",
    "S_suman_island_cu",
    "S_suman_island_look_cu",
    "S_junho_sofa_cu",
    "S_junho_island_r2",
)


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def frames_dir():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R", "frames", "v08")


def face_score_script():
    return os.path.join(repo_root(), "tools", "face_score.py")


class InsightFaceDetector(object):
    def __init__(self):
        os.environ["TQDM_DISABLE"] = "1"
        from insightface.app import FaceAnalysis
        with contextlib.redirect_stdout(sys.stderr):
            app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=-1, det_size=(640, 640))
        self.app = app

    def bbox(self, bgr):
        with contextlib.redirect_stdout(sys.stderr):
            faces = self.app.get(bgr)
        if not faces:
            return None
        best = max(faces, key=lambda face: float(face.bbox[2] - face.bbox[0]))
        x1, y1, x2, y2 = [float(v) for v in best.bbox[:4]]
        return (x1, y1, x2, y2)


def _crop_at(image_w, image_h, cx, cy, face_w, ratio):
    cw = face_w / ratio
    ch = cw * (float(OUT_H) / float(OUT_W))
    x0 = cx - cw / 2.0
    y0 = cy - FACE_Y * ch
    if cw <= image_w + 1e-6:
        x0 = min(max(0.0, x0), image_w - cw)
    if ch <= image_h + 1e-6:
        y0 = min(max(0.0, y0), image_h - ch)
    fits = x0 >= -1e-6 and y0 >= -1e-6 and x0 + cw <= image_w + 1e-6 and y0 + ch <= image_h + 1e-6
    return x0, y0, cw, ch, fits


def plan_crop(image_w, image_h, bbox):
    """반환: x0, y0, cw, ch, scale. scale>1 이면 원본을 그 배율로 키운 뒤 크롭한다."""
    x1, y1, x2, y2 = bbox
    face_w = max(1.0, float(x2 - x1))
    cx = (float(x1) + float(x2)) / 2.0
    cy = (float(y1) + float(y2)) / 2.0
    chosen = None
    ratio = RATIO_MID
    while ratio <= RATIO_HI + 1e-9:
        x0, y0, cw, ch, fits = _crop_at(image_w, image_h, cx, cy, face_w, ratio)
        if fits and cw >= 2 and ch >= 2:
            chosen = (x0, y0, cw, ch, 1.0)
            break
        ratio = round(ratio + 0.005, 4)
    if chosen is not None:
        return chosen
    x0, y0, cw, ch, _fits = _crop_at(image_w, image_h, cx, cy, face_w, RATIO_HI)
    scale = max(cw / float(image_w), ch / float(image_h), 1.0)
    sx0, sy0, scw, sch, fits = _crop_at(
        image_w * scale, image_h * scale, cx * scale, cy * scale, face_w * scale, RATIO_HI
    )
    if not fits:
        sx0 = max(0.0, sx0)
        sy0 = max(0.0, sy0)
    return sx0, sy0, scw, sch, scale


def crop_image(image, bbox):
    """PIL RGB 이미지와 얼굴 bbox로 1080x1920 RGB를 만든다."""
    width, height = image.size
    x0, y0, cw, ch, scale = plan_crop(width, height, bbox)
    if scale > 1.0 + 1e-6:
        new_size = (max(1, int(round(width * scale))), max(1, int(round(height * scale))))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    left = int(round(x0))
    top = int(round(y0))
    right = int(round(x0 + cw))
    bottom = int(round(y0 + ch))
    left = max(0, min(left, image.size[0] - 1))
    top = max(0, min(top, image.size[1] - 1))
    right = max(left + 1, min(image.size[0], right))
    bottom = max(top + 1, min(image.size[1], bottom))
    cropped = image.crop((left, top, right, bottom))
    return cropped.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS), scale


def output_face_width(path, detector):
    bgr = cv2.imread(path)
    if bgr is None:
        return None
    box = detector.bbox(bgr)
    if box is None:
        return None
    return float(box[2] - box[0])


def run_face_score(path):
    script = face_score_script()
    if not os.path.isfile(script):
        return "face_score.py 없음"
    proc = subprocess.run(
        [sys.executable, script, path],
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    return text.replace("\n", " ")


def resolve_inputs(items, source_dir):
    paths = []
    if not items:
        items = list(DEFAULTS)
    for item in items:
        if item.endswith(".png") and os.path.isfile(item):
            paths.append(os.path.abspath(item))
            continue
        name = item[:-4] if item.endswith(".png") else item
        candidate = os.path.join(source_dir, name + ".png")
        if not os.path.isfile(candidate):
            raise SystemExit("원본 없음: {0}".format(candidate))
        paths.append(candidate)
    return paths


def dest_for(src, out_dir):
    base = os.path.basename(src)
    stem, ext = os.path.splitext(base)
    if stem.endswith("_tight"):
        stem = stem + "_crop"
    name = stem + "_tight" + (ext or ".png")
    dest = os.path.join(out_dir, name)
    if os.path.abspath(dest) == os.path.abspath(src):
        raise SystemExit("원본과 출력이 같음: {0}".format(src))
    return dest


def main(argv):
    args = list(argv)
    out_dir = frames_dir()
    source_dir = frames_dir()
    if "--out-dir" in args:
        index = args.index("--out-dir")
        if index + 1 >= len(args):
            raise SystemExit("--out-dir 경로가 필요함")
        out_dir = args[index + 1]
        del args[index:index + 2]
    if "--source-dir" in args:
        index = args.index("--source-dir")
        if index + 1 >= len(args):
            raise SystemExit("--source-dir 경로가 필요함")
        source_dir = args[index + 1]
        del args[index:index + 2]
    paths = resolve_inputs(args, source_dir)
    os.makedirs(out_dir, exist_ok=True)
    detector = InsightFaceDetector()
    rows = []
    for src in paths:
        bgr = cv2.imread(src)
        if bgr is None:
            raise SystemExit("이미지를 열 수 없음: {0}".format(src))
        box = detector.bbox(bgr)
        if box is None:
            sys.stderr.write("얼굴 없음, 건너뜀: {0}\n".format(src))
            continue
        image = Image.open(src).convert("RGB")
        tight, scale = crop_image(image, box)
        dest = dest_for(src, out_dir)
        tight.save(dest)
        width = output_face_width(dest, detector)
        ratio = (width / float(OUT_W)) if width else 0.0
        score = run_face_score(dest)
        rows.append((os.path.basename(dest), width, ratio, scale, score, dest))
    sys.stdout.write("name\tface_px\tratio\tscale\tface_score\tpath\n")
    for name, width, ratio, scale, score, dest in rows:
        width_text = "{:.0f}".format(width) if width else "-"
        sys.stdout.write("{0}\t{1}\t{2:.3f}\t{3:.3f}\t{4}\t{5}\n".format(
            name, width_text, ratio, scale, score, dest
        ))
    if not rows:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
