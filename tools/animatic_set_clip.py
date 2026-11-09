# -*- coding: utf-8 -*-
"""애니매틱 JSON 행에 clip / clip_in / clip_out 을 넣거나 뺀다.

usage:
  python3 tools/animatic_set_clip.py --set 22 video/v08/E1_22/EP01R_E1_22_kling3_take02.mp4 --out 3.4
  python3 tools/animatic_set_clip.py --clear 22
  python3 tools/animatic_set_clip.py --list
  python3 tools/animatic_set_clip.py --json <animatic.json> ...
기본 JSON: 01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json
쓰기 전에 <파일>.bak_<YYYYMMDD-HHMMSS> 백업을 만든다. --list 는 쓰지 않는다.
"""
import datetime
import json
import os
import shutil
import sys

DEFAULT_REL = os.path.join("01_EPISODES", "EP01R", "edit", "v06", "animatic_E1_v062.json")


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def default_json():
    return os.path.join(repo_root(), DEFAULT_REL)


def load_rows(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise SystemExit("애니매틱 JSON은 리스트여야 함: {0}".format(path))
    return data


def save_rows(path, rows):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = "{0}.bak_{1}".format(path, stamp)
    shutil.copy2(path, backup)
    text = json.dumps(rows, ensure_ascii=False, indent=2)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.write("\n")
    return backup


def find_row(rows, number):
    for row in rows:
        if int(row.get("n")) == int(number):
            return row
    raise SystemExit("컷 {0} 행이 없음".format(number))


def clip_fields(row):
    return {
        "n": row.get("n"),
        "clip": row.get("clip", ""),
        "clip_in": row.get("clip_in", ""),
        "clip_out": row.get("clip_out", ""),
    }


def print_list(rows):
    found = [row for row in rows if row.get("clip")]
    if not found:
        sys.stdout.write("(clip 없음)\n")
        return
    for row in found:
        info = clip_fields(row)
        sys.stdout.write("{n}\t{clip}\t{clip_in}\t{clip_out}\n".format(**info))


def parse_args(argv):
    args = {
        "json": default_json(),
        "set": None,
        "clear": None,
        "list": False,
        "path": None,
        "out": None,
        "in": 0.0,
        "in_set": False,
    }
    index = 0
    while index < len(argv):
        token = argv[index]
        if token == "--json":
            args["json"] = argv[index + 1]
            index += 2
            continue
        if token == "--set":
            args["set"] = int(argv[index + 1])
            args["path"] = argv[index + 2]
            index += 3
            continue
        if token == "--clear":
            args["clear"] = int(argv[index + 1])
            index += 2
            continue
        if token == "--list":
            args["list"] = True
            index += 1
            continue
        if token == "--out":
            args["out"] = float(argv[index + 1])
            index += 2
            continue
        if token == "--in":
            args["in"] = float(argv[index + 1])
            args["in_set"] = True
            index += 2
            continue
        raise SystemExit("알 수 없는 인자: {0}".format(token))
    modes = [args["set"] is not None, args["clear"] is not None, args["list"]]
    if sum(1 for item in modes if item) != 1:
        raise SystemExit("usage: --set N PATH [--in 0 --out SEC] | --clear N | --list")
    if args["set"] is not None and args["out"] is None:
        raise SystemExit("--set 에는 --out 초가 필요함")
    return args


def main(argv):
    args = parse_args(argv)
    path = args["json"]
    if not os.path.isfile(path):
        raise SystemExit("JSON 없음: {0}".format(path))
    rows = load_rows(path)
    if args["list"]:
        print_list(rows)
        return 0
    if args["clear"] is not None:
        row = find_row(rows, args["clear"])
        for key in ("clip", "clip_in", "clip_out"):
            row.pop(key, None)
        backup = save_rows(path, rows)
        sys.stdout.write("cleared {0} backup {1}\n".format(args["clear"], backup))
        return 0
    row = find_row(rows, args["set"])
    row["clip"] = args["path"]
    row["clip_in"] = args["in"]
    row["clip_out"] = args["out"]
    if not os.path.isfile(args["path"]):
        sys.stderr.write("클립 파일이 아직 없음: {0}\n".format(args["path"]))
    backup = save_rows(path, rows)
    sys.stdout.write(
        "set {0} clip={1} in={2} out={3} backup {4}\n".format(
            args["set"], args["path"], args["in"], args["out"], backup
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
