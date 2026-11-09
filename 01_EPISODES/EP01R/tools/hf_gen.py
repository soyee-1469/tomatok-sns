# -*- coding: utf-8 -*-
"""Higgsfield 생성 전에 견적을 확인하고 하루 누계가 HF_MAX_CR을 넘으면 생성하지 않는다.

usage:
  python3 01_EPISODES/EP01R/tools/hf_gen.py <out_base> <job_type> [higgsfield 인자...]
생성 직전 `higgsfield generate cost <job_type> <같은 인자>`를 호출한다.
stdout 첫 줄은 견적. 누계+견적 > HF_MAX_CR(기본 40)이면 생성하지 않고 exit 3.
장부: 01_EPISODES/EP01R/video/v08/CREDIT_LEDGER.csv
날짜가 바뀌면 누계는 0부터. --yes 없이도 동작한다.
"""
import csv
import datetime
import json
import os
import subprocess
import sys

DEFAULT_MAX = 40.0
SPENT_STATUS = ("success", "fail", "nsfw")


def episode_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def ledger_path():
    return os.path.join(episode_root(), "video", "v08", "CREDIT_LEDGER.csv")


def parse_cost(text):
    raw = (text or "").strip()
    if not raw:
        raise SystemExit("견적 출력이 비었음")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = None
    found = _cost_from_json(data)
    if found is not None:
        return found
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            data = None
        found = _cost_from_json(data)
        if found is not None:
            return found
    import re
    match = re.search(r"(\d+(?:\.\d+)?)", raw)
    if not match:
        raise SystemExit("견적 숫자를 읽지 못함")
    return float(match.group(1))


def _cost_from_json(data):
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return float(data)
    if isinstance(data, dict):
        for key in ("cost", "credits", "credit", "estimate", "amount", "total"):
            value = data.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
        for value in data.values():
            found = _cost_from_json(value)
            if found is not None:
                return found
    if isinstance(data, list):
        for value in data:
            found = _cost_from_json(value)
            if found is not None:
                return found
    return None


def format_cost(value):
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return "{:.2f}".format(value)


def read_ledger(path):
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def today_spent(rows, today):
    total = 0.0
    for row in rows:
        stamp = (row.get("시각") or "")[:10]
        status = (row.get("상태") or "").strip()
        if stamp != today or status not in SPENT_STATUS:
            continue
        try:
            total += float(row.get("견적") or 0)
        except ValueError:
            continue
    return total


def append_ledger(path, stamp, job_type, out_base, cost, status):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    new_file = not os.path.isfile(path)
    with open(path, "a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(["시각", "job_type", "out_base", "견적", "상태"])
        writer.writerow([stamp, job_type, out_base, format_cost(cost), status])


def classify(returncode, text):
    blob = (text or "").lower()
    if "nsfw" in blob:
        return "nsfw"
    if returncode == 0:
        return "success"
    return "fail"


def write_outputs(out_base, stdout):
    cli_path = out_base + "_cli.txt"
    with open(cli_path, "w", encoding="utf-8") as handle:
        handle.write(stdout or "")
    raw = (stdout or "").strip()
    if not raw:
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return
    status_path = out_base + "_status.json"
    with open(status_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(
            "usage: python3 01_EPISODES/EP01R/tools/hf_gen.py <out_base> <job_type> [args...]\n"
        )
        return 2
    out_base = argv[0]
    job_type = argv[1]
    rest = argv[2:]
    cost_cmd = ["higgsfield", "generate", "cost", job_type] + rest
    try:
        cost_proc = subprocess.run(cost_cmd, capture_output=True, text=True)
    except OSError as exc:
        sys.stderr.write("higgsfield 실행 실패: {0}\n".format(exc))
        return 1
    if cost_proc.returncode != 0:
        sys.stderr.write(cost_proc.stderr or cost_proc.stdout or "견적 실패\n")
        return 1
    cost = parse_cost((cost_proc.stdout or "") + "\n" + (cost_proc.stderr or ""))
    sys.stdout.write("견적 {0}\n".format(format_cost(cost)))
    sys.stdout.flush()
    now = datetime.datetime.now()
    today = now.date().isoformat()
    stamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    path = ledger_path()
    spent = today_spent(read_ledger(path), today)
    try:
        limit = float(os.environ.get("HF_MAX_CR", DEFAULT_MAX))
    except ValueError:
        limit = DEFAULT_MAX
    if spent + cost > limit:
        append_ledger(path, stamp, job_type, out_base, cost, "over_cap")
        sys.stderr.write(
            "누계 {0} + 견적 {1} > HF_MAX_CR {2}. 생성하지 않음.\n".format(
                format_cost(spent), format_cost(cost), format_cost(limit)
            )
        )
        return 3
    gen_cmd = ["higgsfield", "generate", job_type] + rest
    gen = subprocess.run(gen_cmd, capture_output=True, text=True)
    combined = (gen.stdout or "") + (gen.stderr or "")
    status = classify(gen.returncode, combined)
    append_ledger(path, stamp, job_type, out_base, cost, status)
    if gen.stdout:
        sys.stdout.write(gen.stdout)
        if not gen.stdout.endswith("\n"):
            sys.stdout.write("\n")
    if gen.stderr:
        sys.stderr.write(gen.stderr)
    if status == "success":
        parent = os.path.dirname(os.path.abspath(out_base))
        if parent:
            os.makedirs(parent, exist_ok=True)
        write_outputs(out_base, gen.stdout or "")
    if status == "nsfw":
        return 4
    return 0 if gen.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
