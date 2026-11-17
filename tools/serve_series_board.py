#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""회차 작업실 로컬 서버. 생성 API는 호출하지 않는다.

사용: python3 tools/serve_series_board.py
화면: http://127.0.0.1:8765/series.html

/api/reviews 는 컷 단위로 병합한다. 서버 컷의 updatedAt 이 더 최신이면
메모는 합치고, status 는 요청 값을 우선한다. take·image·assignee 는 서버 값을 유지한다.
/api/submit 은 반영 요청을 tools/board_submits/ 와 tools/board_submit_latest.json 에 저장한다.
"""
import json
import os
import re
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP_RE = re.compile(r"^EP\d{2}$")
CUT_RE = re.compile(r"^\d+[a-z]?$")
STATUSES = {"pending", "needs_fix", "approved"}
LOCK = threading.Lock()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def reviews_path():
    raw = os.environ.get("TOMATOK_REVIEWS")
    return Path(raw) if raw else ROOT / "tools" / "series_board_reviews.json"


def board_dir():
    raw = os.environ.get("TOMATOK_BOARD_DIR")
    return Path(raw) if raw else ROOT / "board_web"


def submit_dir():
    raw = os.environ.get("TOMATOK_SUBMIT_DIR")
    return Path(raw) if raw else ROOT / "tools" / "board_submits"


def submit_latest_path():
    raw = os.environ.get("TOMATOK_SUBMIT_LATEST")
    return Path(raw) if raw else ROOT / "tools" / "board_submit_latest.json"


def parse_time(value):
    if not value:
        return 0.0
    text = str(value).strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        return 0.0


def combine_memo(server_memo, user_memo):
    server = "" if server_memo is None else str(server_memo)
    user = "" if user_memo is None else str(user_memo)
    if not user.strip():
        return server
    if not server.strip():
        return user
    if user == server or user in server:
        return server
    if server in user:
        return user
    return server.rstrip() + "\n" + user.strip()


def merge_cut(server_cut, incoming):
    if not isinstance(server_cut, dict):
        out = dict(incoming)
        out.setdefault("updatedAt", now_iso())
        return out
    if parse_time(server_cut.get("updatedAt")) > parse_time(incoming.get("updatedAt")):
        merged = dict(server_cut)
        merged["memo"] = combine_memo(server_cut.get("memo"), incoming.get("memo"))
        if incoming.get("status") in STATUSES:
            merged["status"] = incoming["status"]
        merged["updatedAt"] = now_iso()
        return merged
    merged = dict(server_cut)
    merged.update(incoming)
    return merged


def merge_reviews(store, payload):
    episodes = payload.get("episodes")
    if not isinstance(episodes, dict) or not episodes:
        raise ValueError("episodes 가 필요합니다")
    out_eps = store.setdefault("episodes", {})
    if not isinstance(out_eps, dict):
        raise ValueError("저장 형식이 잘못되었습니다")
    for ep_id, ep in episodes.items():
        if not isinstance(ep_id, str) or not EP_RE.match(ep_id):
            raise ValueError("회차 id 가 잘못되었습니다")
        if not isinstance(ep, dict):
            raise ValueError("회차 형식이 잘못되었습니다")
        cuts = ep.get("cuts")
        if not isinstance(cuts, dict) or not cuts:
            raise ValueError("cuts 가 필요합니다")
        bucket = out_eps.setdefault(ep_id, {})
        if not isinstance(bucket, dict):
            bucket = {}
            out_eps[ep_id] = bucket
        dest = bucket.setdefault("cuts", {})
        if not isinstance(dest, dict):
            dest = {}
            bucket["cuts"] = dest
        for cut_id, rec in cuts.items():
            key = str(cut_id)
            if not CUT_RE.match(key):
                raise ValueError("컷 번호가 잘못되었습니다")
            clean = clean_review(rec)
            dest[key] = merge_cut(dest.get(key), clean)
    store["version"] = store.get("version") or 1
    store["updatedAt"] = now_iso()
    return store


def clean_review(rec):
    if not isinstance(rec, dict):
        raise ValueError("컷 기록이 객체가 아닙니다")
    status = rec.get("status") or "pending"
    if status not in STATUSES:
        raise ValueError("status 값이 잘못되었습니다")
    take = rec.get("take", None)
    if isinstance(take, bool) or (take is not None and not isinstance(take, int)):
        raise ValueError("take 값이 잘못되었습니다")
    image = rec.get("image", None)
    if image is not None and (not isinstance(image, str) or len(image) > 500 or "\n" in image):
        raise ValueError("image 값이 잘못되었습니다")
    memo = rec.get("memo", "")
    if not isinstance(memo, str) or len(memo) > 4000:
        raise ValueError("memo 값이 잘못되었습니다")
    assignee = rec.get("assignee") or "unassigned"
    if not isinstance(assignee, str) or len(assignee) > 40:
        raise ValueError("assignee 값이 잘못되었습니다")
    updated = rec.get("updatedAt")
    if updated is not None and not isinstance(updated, str):
        raise ValueError("updatedAt 값이 잘못되었습니다")
    out = {
        "take": take,
        "image": image,
        "status": status,
        "memo": memo,
        "assignee": assignee,
    }
    if updated:
        out["updatedAt"] = updated
    else:
        out["updatedAt"] = now_iso()
    return out


def clean_submit_cut(rec):
    if not isinstance(rec, dict):
        raise ValueError("컷 기록이 객체가 아닙니다")
    status = rec.get("status") or "pending"
    if status not in STATUSES:
        raise ValueError("status 값이 잘못되었습니다")
    take = rec.get("take", None)
    if isinstance(take, bool) or (take is not None and not isinstance(take, int)):
        raise ValueError("take 값이 잘못되었습니다")
    image = rec.get("image", None)
    if image is not None and (not isinstance(image, str) or len(image) > 500 or "\n" in image):
        raise ValueError("image 값이 잘못되었습니다")
    memo = rec.get("memo", "")
    if memo is None:
        memo = ""
    if not isinstance(memo, str) or len(memo) > 4000:
        raise ValueError("memo 값이 잘못되었습니다")
    return {"status": status, "take": take, "image": image, "memo": memo}


def load_json(path, fallback):
    if not path.exists():
        return fallback
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON 객체가 아닙니다")
    return data


def atomic_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def empty_store():
    return {"version": 1, "updatedAt": now_iso(), "episodes": {}}


def stamp_name(episode, submitted_at):
    moment = datetime.now(timezone.utc)
    parsed = parse_time(submitted_at)
    if parsed:
        moment = datetime.fromtimestamp(parsed, timezone.utc)
    stamp = moment.strftime("%Y%m%dT%H%M%S%fZ")
    return f"{episode}_{stamp}.json"


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print("[board]", fmt % args)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/reviews":
            self.handle_reviews_get()
            return
        if path == "/api/submit":
            self.handle_submit_get()
            return
        self.handle_static(path)

    def do_POST(self):
        if self.path.split("?", 1)[0] == "/api/reviews":
            self.handle_reviews_put()
            return
        self.send_error(404)

    def do_PUT(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/reviews":
            self.handle_reviews_put()
            return
        if path == "/api/submit":
            self.handle_submit_put()
            return
        self.send_error(404)

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > 2_000_000:
            raise ValueError("본문 크기가 잘못되었습니다")
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def send_json(self, code, obj):
        data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def handle_reviews_get(self):
        try:
            with LOCK:
                store = load_json(reviews_path(), empty_store())
            if "episodes" not in store or not isinstance(store.get("episodes"), dict):
                raise ValueError("reviews 형식이 잘못되었습니다")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self.send_json(500, {"ok": False, "error": str(exc)})
            return
        self.send_json(200, store)

    def handle_reviews_put(self):
        try:
            payload = self.read_body()
            if not isinstance(payload, dict):
                raise ValueError("JSON 객체가 필요합니다")
            with LOCK:
                store = load_json(reviews_path(), empty_store())
                if not isinstance(store.get("episodes"), dict):
                    store = empty_store()
                merge_reviews(store, payload)
                atomic_write(reviews_path(), store)
        except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
            self.send_json(400, {"ok": False, "error": str(exc)})
            return
        self.send_json(200, {"ok": True, "store": store})

    def handle_submit_get(self):
        try:
            latest = load_json(submit_latest_path(), None) if submit_latest_path().exists() else None
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self.send_json(500, {"ok": False, "error": str(exc)})
            return
        self.send_json(200, {"ok": True, "latest": latest})

    def handle_submit_put(self):
        try:
            payload = self.read_body()
            if not isinstance(payload, dict):
                raise ValueError("JSON 객체가 필요합니다")
            episode = payload.get("episode")
            if not isinstance(episode, str) or not EP_RE.match(episode):
                raise ValueError("episode 가 필요합니다")
            cuts_in = payload.get("cuts")
            if not isinstance(cuts_in, dict) or not cuts_in:
                raise ValueError("cuts 가 필요합니다")
            cuts = {}
            for cut_id, rec in cuts_in.items():
                key = str(cut_id)
                if not CUT_RE.match(key):
                    raise ValueError("컷 번호가 잘못되었습니다")
                cuts[key] = clean_submit_cut(rec)
            submitted_at = payload.get("submittedAt") or now_iso()
            if not isinstance(submitted_at, str):
                raise ValueError("submittedAt 값이 잘못되었습니다")
            doc = {"episode": episode, "submittedAt": submitted_at, "cuts": cuts}
            folder = submit_dir()
            name = stamp_name(episode, submitted_at)
            target = folder / name
            if target.exists():
                name = stamp_name(episode, now_iso())
                target = folder / name
            with LOCK:
                atomic_write(target, doc)
                atomic_write(submit_latest_path(), doc)
        except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
            self.send_json(400, {"ok": False, "error": str(exc)})
            return
        self.send_json(200, {"ok": True, "file": name, "latest": doc})

    def handle_static(self, path):
        rel = path.lstrip("/") or "series.html"
        root = board_dir().resolve()
        target = (root / rel).resolve()
        if root not in target.parents and target != root:
            self.send_error(403)
            return
        if not target.is_file():
            self.send_error(404)
            return
        kind = "application/octet-stream"
        if target.suffix == ".html":
            kind = "text/html; charset=utf-8"
        elif target.suffix == ".json":
            kind = "application/json; charset=utf-8"
        elif target.suffix == ".js":
            kind = "text/javascript; charset=utf-8"
        elif target.suffix == ".css":
            kind = "text/css; charset=utf-8"
        elif target.suffix == ".mp4":
            kind = "video/mp4"
        size = target.stat().st_size
        start, end = 0, size - 1
        status = 200
        range_h = self.headers.get("Range")
        if range_h and range_h.startswith("bytes=") and "," not in range_h:
            left, _, right = range_h[6:].partition("-")
            try:
                start = int(left) if left else 0
                end = int(right) if right else size - 1
            except ValueError:
                self.send_error(416)
                return
            if start < 0 or end < start or start >= size:
                self.send_error(416)
                return
            end = min(end, size - 1)
            status = 206
        length = 0 if size == 0 else end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with target.open("rb") as fh:
            fh.seek(start)
            remaining = length
            while remaining:
                chunk = fh.read(min(65536, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)


def main():
    port = int(os.environ.get("TOMATOK_BOARD_PORT") or "8765")
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"http://127.0.0.1:{port}/series.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
