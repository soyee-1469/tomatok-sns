# -*- coding: utf-8 -*-
"""애니매틱 행에 clip / clip_in / clip_out 을 넣거나 뺀다.

usage:
  python3 tools/animatic_set_clip.py [json] --set 22 video/v08/E1_22/take.mp4 --out 3.4
  python3 tools/animatic_set_clip.py [json] --clear 22
  python3 tools/animatic_set_clip.py [json] --list
JSON 은 쓰기 전에 <파일>.bak_<시각> 으로 백업한다.
"""
import argparse
import datetime
import json
import os
import shutil
import sys

DEFAULT = os.path.join(
    "01_EPISODES", "EP01R", "edit", "v06", "animatic_E1_v062.json"
)
MAC_ROOT = "/Users/ymy/project/sns"


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def keyn(value):
    text = str(value).strip()
    return int(text) if text.isdigit() else text


def load_rows(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise SystemExit("리스트 json 이 아님: {0}".format(path))
    return data


def save_rows(path, rows):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=1)
        handle.write("\n")


def backup(path):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = "{0}.bak_{1}".format(path, stamp)
    shutil.copy2(path, dest)
    return dest


def find_row(rows, number):
    want = keyn(number)
    for index, row in enumerate(rows):
        if keyn(row.get("n")) == want:
            return index
    raise SystemExit("컷 {0} 없음".format(number))


def resolve_existing(path):
    if os.path.isfile(path):
        return path
    root = repo_root()
    episode = os.path.join(root, "01_EPISODES", "EP01R")
    candidates = []
    if path.startswith(MAC_ROOT + "/") or path.startswith(MAC_ROOT + os.sep):
        candidates.append(os.path.join(root, path[len(MAC_ROOT):].lstrip("/\\")))
    if not os.path.isabs(path):
        candidates.append(os.path.join(episode, path))
        candidates.append(os.path.join(root, path))
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return ""


def cmd_list(rows):
    for row in rows:
        clip = row.get("clip") or ""
        if clip:
            sys.stdout.write(
                "{0}\t{1}\t{2}\t{3}\n".format(
                    row.get("n"), clip, row.get("clip_in", ""), row.get("clip_out", "")
                )
            )
        else:
            sys.stdout.write("{0}\t(없음)\n".format(row.get("n")))


def cmd_set(path, rows, number, clip, clip_out, clip_in):
    if clip_out is None:
        raise SystemExit("--set 에는 --out 초가 필요하다")
    if clip_out <= clip_in:
        raise SystemExit("--out 이 --in 보다 커야 한다")
    if not resolve_existing(clip):
        raise SystemExit("클립 파일 없음: {0}".format(clip))
    index = find_row(rows, number)
    row = rows[index]
    row["clip"] = clip
    row["clip_in"] = float(clip_in)
    row["clip_out"] = float(clip_out)
    dest = backup(path)
    save_rows(path, rows)
    sys.stdout.write("백업 {0}\n".format(dest))
    sys.stdout.write(
        "컷 {0} clip={1} in={2} out={3}\n".format(row["n"], clip, clip_in, clip_out)
    )


def cmd_clear(path, rows, number):
    index = find_row(rows, number)
    row = rows[index]
    for key in ("clip", "clip_in", "clip_out"):
        row.pop(key, None)
    dest = backup(path)
    save_rows(path, rows)
    sys.stdout.write("백업 {0}\n".format(dest))
    sys.stdout.write("컷 {0} clip 제거\n".format(row.get("n")))


def main(argv):
    parser = argparse.ArgumentParser(description="애니매틱 clip 필드 편집")
    parser.add_argument("json_path", nargs="?", default=DEFAULT)
    parser.add_argument("--set", nargs=2, metavar=("N", "MP4"))
    parser.add_argument("--out", type=float)
    parser.add_argument("--in", dest="clip_in", type=float, default=0.0)
    parser.add_argument("--clear", metavar="N")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)
    path = args.json_path
    if not os.path.isabs(path):
        path = os.path.join(repo_root(), path)
    if not os.path.isfile(path):
        raise SystemExit("json 없음: {0}".format(path))
    modes = [bool(args.set), bool(args.clear), bool(args.list)]
    if sum(1 for item in modes if item) != 1:
        raise SystemExit("--set, --clear, --list 중 하나만")
    rows = load_rows(path)
    if args.list:
        cmd_list(rows)
        return 0
    if args.clear is not None:
        cmd_clear(path, rows, args.clear)
        return 0
    number, clip = args.set
    cmd_set(path, rows, number, clip, args.out, args.clip_in)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
