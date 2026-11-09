# -*- coding: utf-8 -*-
"""클립 내부 컷·와이드 전환 판정.

usage: python3 tools/clip_qa.py <clip.mp4> [<clip.mp4> ...] [--json]
얼굴 폭은 insightface buffalo_l (CPU), 3프레임마다. 길이는 cv2로 센다.
"""
import json
import math
import os
import sys

DIFF_W = 160
DEFECTS = ("HARD_CUT", "WIDE_CUT", "FACE_LOST")


def frame_diff(prev, frame):
    import cv2
    if prev.shape[:2] != frame.shape[:2]:
        frame = cv2.resize(frame, (prev.shape[1], prev.shape[0]))
    gray_prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height = max(1, int(round(DIFF_W * gray.shape[0] / float(gray.shape[1]))))
    small_prev = cv2.resize(gray_prev, (DIFF_W, height))
    small = cv2.resize(gray, (DIFF_W, height))
    return float(cv2.absdiff(small_prev, small).mean())


def floor_tenth(value):
    return math.floor(float(value) * 10.0 + 1e-9) / 10.0


class InsightFaceMeter(object):
    """가장 큰 얼굴의 가로 폭(px). 검출이 없으면 None."""

    def __init__(self):
        import io
        from contextlib import redirect_stdout
        from insightface.app import FaceAnalysis
        sink = io.StringIO()
        with redirect_stdout(sink):
            self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            self.app.prepare(ctx_id=0, det_size=(640, 640))
        self._silence = redirect_stdout

    def __call__(self, frame):
        import io
        sink = io.StringIO()
        with self._silence(sink):
            faces = self.app.get(frame)
        if not faces:
            return None
        best = max(faces, key=lambda face: float(face.bbox[2] - face.bbox[0]))
        return float(best.bbox[2] - best.bbox[0])


def _fmt_t(value):
    return "{0:.2f}".format(float(value))


def analyze(path, measure):
    import cv2
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError("영상을 열 수 없음: {0}".format(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    if fps <= 1e-3:
        cap.release()
        raise RuntimeError("fps 없음: {0}".format(path))
    prev = None
    diffs = []
    widths = []
    index = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            when = index / float(fps)
            if prev is not None:
                diffs.append((when, frame_diff(prev, frame)))
            if index % 3 == 0:
                widths.append((when, measure(frame)))
            prev = frame
            index += 1
    finally:
        cap.release()
    if index == 0:
        raise RuntimeError("프레임 없음: {0}".format(path))
    dur = index / float(fps)

    events = []
    run = []

    def flush():
        if len(run) >= 10:
            t0 = run[0][0]
            t1 = run[-1][0]
            events.append(("CAMERA_MOVE", t0, "CAMERA_MOVE {0}-{1}s".format(_fmt_t(t0), _fmt_t(t1))))
        del run[:]

    for when, value in diffs:
        if value > 40.0:
            flush()
            events.append(("HARD_CUT", when, "HARD_CUT@{0}s".format(_fmt_t(when))))
        elif value >= 8.0:
            run.append((when, value))
        else:
            flush()
    flush()

    prev_w = None
    saw_face = False
    for when, width in widths:
        if width is None:
            if prev_w is not None:
                events.append(("FACE_LOST", when, "FACE_LOST@{0}s".format(_fmt_t(when))))
            prev_w = None
            continue
        saw_face = True
        if prev_w is not None and width <= prev_w * 0.60:
            events.append(("WIDE_CUT", when, "WIDE_CUT@{0}s".format(_fmt_t(when))))
        prev_w = width
    if not saw_face:
        t0 = widths[0][0] if widths else 0.0
        events.append(("FACE_LOST", t0, "FACE_LOST@{0}s".format(_fmt_t(t0))))

    events.sort(key=lambda item: (item[1], item[0]))
    defects = [item for item in events if item[0] in DEFECTS]
    passed = not defects
    usable = floor_tenth(defects[0][1]) if defects else round(dur, 2)
    return {
        "file": path,
        "dur": round(dur, 2),
        "pass": passed,
        "events": [item[2] for item in events],
        "usable_until": usable,
    }


def format_line(row):
    flag = "PASS" if row["pass"] else "FAIL"
    why = ", ".join(row["events"]) if row["events"] else "-"
    return "{file} | {dur:.2f}s | {flag} | {why} | 사용 가능 구간 0.0-{usable:.1f}s".format(
        file=row["file"],
        dur=row["dur"],
        flag=flag,
        why=why,
        usable=row["usable_until"],
    )


def main(argv):
    args = list(argv)
    as_json = False
    if "--json" in args:
        as_json = True
        args = [item for item in args if item != "--json"]
    if not args:
        sys.stderr.write("usage: python3 tools/clip_qa.py <clip.mp4> [...] [--json]\n")
        return 2
    try:
        measure = InsightFaceMeter()
    except Exception as exc:
        sys.stderr.write("insightface buffalo_l 를 쓸 수 없음: {0}\n".format(exc))
        return 2
    rows = []
    try:
        for path in args:
            if not os.path.isfile(path):
                raise RuntimeError("파일 없음: {0}".format(path))
            rows.append(analyze(path, measure))
    except RuntimeError as exc:
        sys.stderr.write(str(exc) + "\n")
        return 1
    if as_json:
        sys.stdout.write(json.dumps(rows, ensure_ascii=False) + "\n")
    else:
        for row in rows:
            sys.stdout.write(format_line(row) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
