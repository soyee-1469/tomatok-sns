# -*- coding: utf-8 -*-
"""클립 내부 컷·와이드 전환 QA.

usage: python3 tools/clip_qa.py [--json] <mp4> [<mp4> ...]
한 줄: <파일> | <길이>s | PASS|FAIL | 사유들 | 사용 가능 구간 0.0-<t>s
--json: {"file","dur","pass","events","usable_until"} 배열을 stdout에.
길이는 cv2 프레임 수 / fps. ffprobe는 쓰지 않는다.
"""
import contextlib
import json
import math
import os
import sys

import cv2

DIFF_W = 320
HARD_CUT = 40.0
MOVE_LOW = 8.0
MOVE_HIGH = 40.0
MOVE_FRAMES = 10
FACE_EVERY = 3
WIDE_RATIO = 0.60


def fmt_num(value):
    value = round(float(value), 2)
    if abs(value - round(value, 1)) < 1e-6:
        return "{:.1f}".format(value)
    return "{:.2f}".format(value)


def usable_before(t):
    tenths = int(math.floor((float(t) - 1e-6) * 10.0))
    if tenths < 0:
        tenths = 0
    return tenths / 10.0


def events_from_diffs(diffs):
    """diffs: [(t, score), ...] 현재 프레임과 직전 프레임의 평균 절대차."""
    events = []
    run = []

    def flush():
        if len(run) >= MOVE_FRAMES:
            events.append({
                "t": run[0][0],
                "text": "CAMERA_MOVE {0}-{1}s".format(fmt_num(run[0][0]), fmt_num(run[-1][0])),
            })
        run.clear()

    for t, score in diffs:
        if score > HARD_CUT:
            flush()
            events.append({"t": t, "text": "HARD_CUT@{0}s".format(fmt_num(t))})
        elif MOVE_LOW <= score <= MOVE_HIGH:
            run.append((t, score))
        else:
            flush()
    flush()
    return events


def events_from_faces(samples):
    """samples: [(t, width or None), ...] 매 3프레임. 직전 검출 대비 폭 40% 이상 감소면 WIDE_CUT."""
    events = []
    prev = None
    missing = False
    for t, width in samples:
        if width is None:
            if prev is not None and not missing:
                events.append({"t": t, "text": "FACE_LOST@{0}s".format(fmt_num(t))})
                missing = True
            continue
        missing = False
        if prev is not None and width <= prev * WIDE_RATIO:
            events.append({"t": t, "text": "WIDE_CUT@{0}s".format(fmt_num(t))})
        prev = width
    return events


class InsightFaceMeasurer(object):
    def __init__(self):
        os.environ["TQDM_DISABLE"] = "1"
        from insightface.app import FaceAnalysis
        with contextlib.redirect_stdout(sys.stderr):
            app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=-1, det_size=(640, 640))
        self.app = app

    def width(self, bgr):
        with contextlib.redirect_stdout(sys.stderr):
            faces = self.app.get(bgr)
        if not faces:
            return None
        best = max(faces, key=lambda face: float(face.bbox[2] - face.bbox[0]))
        return float(best.bbox[2] - best.bbox[0])


def _small_gray(frame):
    height, width = frame.shape[:2]
    if width < 1 or height < 1:
        raise RuntimeError("빈 프레임")
    new_h = max(1, int(round(height * (DIFF_W / float(width)))))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray, (DIFF_W, new_h), interpolation=cv2.INTER_AREA)


def analyze(path, measurer=None):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError("영상을 열 수 없음: {0}".format(path))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    if fps <= 1e-3:
        cap.release()
        raise RuntimeError("fps를 읽을 수 없음: {0}".format(path))
    diffs = []
    samples = []
    prev = None
    index = 0
    own_measurer = measurer is None
    if own_measurer:
        measurer = InsightFaceMeasurer()
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            t = index / fps
            small = _small_gray(frame)
            if prev is not None:
                diffs.append((t, float(cv2.absdiff(small, prev).mean())))
            prev = small
            if index % FACE_EVERY == 0:
                samples.append((t, measurer.width(frame)))
            index += 1
    finally:
        cap.release()
    if index < 1:
        raise RuntimeError("프레임 없음: {0}".format(path))
    dur = index / fps
    events = events_from_diffs(diffs) + events_from_faces(samples)
    events.sort(key=lambda item: (item["t"], item["text"]))
    passed = not events
    if passed:
        usable = round(dur, 2)
    else:
        usable = usable_before(events[0]["t"])
    return {
        "file": path,
        "dur": round(dur, 3),
        "pass": passed,
        "events": [item["text"] for item in events],
        "usable_until": usable,
    }


def format_line(row):
    reasons = ", ".join(row["events"])
    verdict = "PASS" if row["pass"] else "FAIL"
    return "{0} | {1}s | {2} | {3} | 사용 가능 구간 0.0-{4}s".format(
        row["file"], fmt_num(row["dur"]), verdict, reasons, fmt_num(row["usable_until"])
    )


def main(argv):
    args = list(argv)
    as_json = False
    if "--json" in args:
        as_json = True
        args = [item for item in args if item != "--json"]
    if not args:
        sys.stderr.write("usage: python3 tools/clip_qa.py [--json] <mp4> [<mp4> ...]\n")
        return 2
    rows = []
    for path in args:
        if not os.path.isfile(path):
            sys.stderr.write("파일 없음: {0}\n".format(path))
            return 1
        rows.append(analyze(path))
    if as_json:
        sys.stdout.write(json.dumps(rows, ensure_ascii=False))
        sys.stdout.write("\n")
    else:
        for row in rows:
            sys.stdout.write(format_line(row))
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
