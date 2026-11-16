#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""보드 반영 큐를 읽는다. processedAt 기록은 Claude가 한다.

사용: python3 tools/board_requests.py
tools/board_submit_latest.json 을 먼저 본다. 없으면 tools/board_submits/ 의 최신 파일.
승인된 take 는 tools/series_board_reviews.json 에 남아 있으므로
python3 tools/animatic_set_clip.py <animatic.json> --from-reviews tools/series_board_reviews.json
으로 애니매틱에 연결할 수 있다. 이 스크립트는 JSON을 수정하지 않는다.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = Path(os.environ["TOMATOK_SUBMIT_LATEST"]) if os.environ.get("TOMATOK_SUBMIT_LATEST") else ROOT / "tools" / "board_submit_latest.json"
FOLDER = Path(os.environ["TOMATOK_SUBMIT_DIR"]) if os.environ.get("TOMATOK_SUBMIT_DIR") else ROOT / "tools" / "board_submits"


def load_latest():
    if LATEST.exists():
        data = json.loads(LATEST.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data, LATEST
    if not FOLDER.exists():
        return None, None
    files = sorted(FOLDER.glob("EP*.json"), key=lambda p: p.stat().st_mtime)
    if not files:
        return None, None
    path = files[-1]
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return None, path
    return data, path


def main():
    data, path = load_latest()
    if not data:
        print("미처리 제출 없음")
        return 0
    if data.get("processedAt"):
        print(f"미처리 제출 없음 (processedAt={data.get('processedAt')})")
        return 0
    cuts = data.get("cuts") if isinstance(data.get("cuts"), dict) else {}
    episode = data.get("episode") or "?"
    when = data.get("submittedAt") or "?"
    print(f"{episode} {when} 미처리 {len(cuts)}컷")
    if path:
        try:
            shown = path.resolve().relative_to(ROOT)
        except ValueError:
            shown = path
        print(f"파일 {shown}")
    for cut_id in sorted(cuts, key=lambda k: (len(str(k)), str(k))):
        rec = cuts[cut_id] if isinstance(cuts[cut_id], dict) else {}
        memo = (rec.get("memo") or "").replace("\n", " / ")
        image = rec.get("image") or ""
        take = rec.get("take")
        take_s = "없음" if take is None else str(take)
        print(
            f"- {cut_id} status={rec.get('status') or 'pending'} "
            f"take={take_s} image={image} memo={memo}"
        )
    print(
        "승인 take 연결: python3 tools/animatic_set_clip.py "
        "<animatic.json> --from-reviews tools/series_board_reviews.json"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"읽기 실패: {exc}", file=sys.stderr)
        sys.exit(1)
