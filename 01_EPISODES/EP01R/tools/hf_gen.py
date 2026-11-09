# -*- coding: utf-8 -*-
"""Higgsfield 생성 전에 견적을 찍고 하루 누계가 HF_MAX_CR 을 넘으면 멈춘다.

usage: python3 01_EPISODES/EP01R/tools/hf_gen.py <out_base> <job_type> [생성 옵션...]
견적 줄이 stdout 첫 줄이다. 상한을 넘으면 exit 3, 생성은 호출하지 않는다.
"""
import csv
import datetime
import json
import os
import re
import subprocess
import sys

DEFAULT_LIMIT = 40.0
COUNTED = set(["success", "fail", "nsfw"])


def episode_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def ledger_path():
    return os.path.join(episode_root(), "video", "v08", "CREDIT_LEDGER.csv")


def limit_credits():
    raw = os.environ.get("HF_MAX_CR", "")
    if raw.strip() == "":
        return DEFAULT_LIMIT
    return float(raw)


def forwarded(args):
    """out_base 를 뺀 생성 옵션. 견적 호출에 그대로 넘긴다."""
    return list(args)


def parse_cost(text):
    for line in text.splitlines():
        chunk = line.strip()
        if not chunk:
            continue
        try:
            data = json.loads(chunk)
        except ValueError:
            data = None
        if isinstance(data, dict):
            for key in ("cost", "credits", "credit", "amount", "estimate"):
                if isinstance(data.get(key), (int, float)):
                    return float(data[key])
        if re.fullmatch(r"\d+(?:\.\d+)?", chunk):
            return float(chunk)
    nums = re.findall(r"\d+(?:\.\d+)?", text or "")
    if not nums:
        raise RuntimeError("견적 숫자를 읽지 못함")
    return float(nums[-1])


def quote_cost(job_type, options):
    cmd = ["higgsfield", "generate", "cost", job_type] + list(options)
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except OSError as exc:
        raise RuntimeError("higgsfield 실행 실패: {0}".format(exc))
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError("견적 실패 ({0}): {1}".format(proc.returncode, err))
    return parse_cost(proc.stdout or "")


def read_ledger(path):
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def today_total(rows, today):
    total = 0.0
    for row in rows:
        stamp = str(row.get("시각") or "")
        if not stamp.startswith(today):
            continue
        if str(row.get("상태") or "") not in COUNTED:
            continue
        try:
            total += float(row.get("견적") or 0)
        except ValueError:
            continue
    return total


def append_ledger(path, job_type, out_base, quote, status):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    new_file = not os.path.isfile(path)
    stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(path, "a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(["시각", "job_type", "out_base", "견적", "상태"])
        writer.writerow([stamp, job_type, out_base, "{0:g}".format(quote), status])


def classify(text):
    low = (text or "").lower()
    if "nsfw" in low:
        return "nsfw"
    return "success"


def run_create(job_type, options):
    cmd = ["higgsfield", "generate", "create", "--wait", job_type] + list(options)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    if proc.returncode != 0:
        return "fail", text
    return classify(text), text


def save_status(out_base, text):
    for line in text.splitlines():
        chunk = line.strip()
        if not chunk or chunk[0] not in "[{":
            continue
        try:
            data = json.loads(chunk)
        except ValueError:
            continue
        dest = out_base + "_status.json"
        with open(dest, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=1)
            handle.write("\n")
        return dest
    return ""


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(
            "usage: python3 hf_gen.py <out_base> <job_type> [--prompt ...] [--duration N] [--mode std] [--aspect_ratio 9:16]\n"
        )
        return 2
    out_base = argv[0]
    job_type = argv[1]
    options = forwarded(argv[2:])
    try:
        quote = quote_cost(job_type, options)
    except RuntimeError as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    sys.stdout.write("견적 {0:g}\n".format(quote))
    path = ledger_path()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    total = today_total(read_ledger(path), today)
    cap = limit_credits()
    if total + quote > cap:
        append_ledger(path, job_type, out_base, quote, "blocked")
        sys.stderr.write(
            "누계 {0:g}+{1:g} 이 HF_MAX_CR {2:g} 보다 커서 생성하지 않음\n".format(total, quote, cap)
        )
        return 3
    status, text = run_create(job_type, options)
    append_ledger(path, job_type, out_base, quote, status)
    if text.strip():
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    saved = save_status(out_base, text)
    if saved:
        sys.stderr.write("status {0}\n".format(saved))
    if status == "fail":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
