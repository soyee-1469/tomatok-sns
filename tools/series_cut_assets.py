#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1화 컷별 콘티·이미지·영상 맵.

애니매틱 JSON은 읽기만 한다. 콘티 연결은 tools/ep01_conti_links.json 을
cuts_island.json 자동 매칭보다 먼저 쓴다. 생성 API는 호출하지 않는다.

사용: python3 tools/series_cut_assets.py
"""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANIM = ROOT / "01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json"
LINKS = ROOT / "tools/ep01_conti_links.json"
CUTS_ISLAND = ROOT / "01_EPISODES/EP01R/frames/v08/STORYBOARD/cuts_island.json"
MAP_OUT = ROOT / "tools/ep01_cut_asset_map.json"
REPORT_OUT = ROOT / "tools/EP01_CUT_BOARD_REPORT.md"
IMG = ROOT / "board_web/series_cuts/img"
VID = ROOT / "board_web/series_cuts/vid"
VIDEO_ROOT = ROOT / "01_EPISODES/EP01R/video/v08"
STORY = "01_EPISODES/EP01R/frames/v08/STORYBOARD"
AUDIT = "SCRIPT_CONTI_AUDIT 2.4"
TAKE_RE = re.compile(r"_take(\d+)\.mp4$", re.IGNORECASE)
STATUSES = ("linked", "reference", "unlinked", "check")
UI_REASON = "UI, 콘티 대상 아님"
TEXT_REASON = "그림 콘티 없음(prompts_E1 텍스트만)"

EXPECT_LINKED = {2, 11, 13, 14, 15, 19}
EXPECT_REFERENCE = {8, 9, 10, 12, 22, 23, 42, 45}
EXPECT_CHECK = {30}
EXPECT_UI = {6, 16, 25, 28, 36, 38}
EXPECT_SKIP_LINKED = {20, 21}


def to_rel(path):
    if not path:
        return None
    text = str(path).replace("\\", "/")
    for marker in ("01_EPISODES/", "00_MASTER_ASSETS/", "board_web/", "tools/"):
        index = text.find(marker)
        if index >= 0:
            return text[index:]
    if text.startswith("/"):
        return text
    return text


def exists_rel(rel):
    return bool(rel) and (ROOT / rel).is_file()


def clean_name(text):
    if not text:
        return ""
    text = str(text).replace("비아", "리아")
    return re.sub(r"\bBea\b", "리아", text)


def spoken_line(line):
    text = clean_name(line).strip()
    if not text:
        return ""
    if text.startswith("(") and text.endswith(")"):
        return ""
    return text


def direction_of(row):
    override = (row.get("dir_override") or "").strip()
    if override:
        return clean_name(override)
    parts = [(row.get("situation") or "").strip(), (row.get("action") or "").strip()]
    return clean_name(" / ".join(part for part in parts if part))


def take_number(path):
    if not path:
        return None
    match = TAKE_RE.search(Path(path).name)
    return int(match.group(1)) if match else None


def list_takes(folder):
    found = []
    if not folder.is_dir():
        return found
    for path in folder.iterdir():
        if not path.is_file():
            continue
        name = path.name
        if "_old" in name.lower():
            continue
        number = take_number(name)
        if number is None:
            continue
        found.append((number, path))
    found.sort(key=lambda item: (item[0], item[1].name))
    return found


def thumb_name(rel):
    stem = rel.replace("/", "__")
    return stem.rsplit(".", 1)[0] + ".jpg"


def write_jpeg(src, dest, width=540):
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        import cv2
        image = cv2.imread(str(src))
        if image is None:
            return False
        height, wide = image.shape[:2]
        if wide > width:
            new_h = max(1, int(height * width / wide))
            image = cv2.resize(image, (width, new_h), interpolation=cv2.INTER_AREA)
        return bool(cv2.imwrite(str(dest), image, [int(cv2.IMWRITE_JPEG_QUALITY), 80]))
    except ImportError:
        from PIL import Image
        image = Image.open(src).convert("RGB")
        wide, height = image.size
        if wide > width:
            new_h = max(1, int(height * width / wide))
            image = image.resize((width, new_h), Image.Resampling.LANCZOS)
        image.save(dest, "JPEG", quality=80)
        return True


def reset_dir(folder):
    folder.mkdir(parents=True, exist_ok=True)
    for path in folder.iterdir():
        if path.is_symlink() or path.is_file():
            path.unlink()


def link_video(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink() or dest.exists():
        dest.unlink()
    dest.symlink_to(os.path.relpath(src, dest.parent))


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def with_audit_prefix(basis):
    basis = basis or ""
    if AUDIT in basis:
        return basis
    if basis:
        return AUDIT + " — " + basis
    return AUDIT


def conti_for_frame(row, cuts_island):
    """프레임 키가 cuts_island.json 과 같을 때만 연결. C번호 자동 매칭은 하지 않는다."""
    frame = row.get("frame") or ""
    info = cuts_island.get(frame) or {}
    sketch = info.get("sketch")
    if sketch:
        return {
            "status": "linked",
            "path": STORY + "/" + sketch,
            "basis": "cuts_island.json %s.sketch" % frame,
            "source": "frame",
        }
    return {"status": "unlinked", "path": None, "basis": "", "source": "frame"}


def conti_for_row(row, links, cuts_island):
    key = str(row.get("n"))
    if key in links:
        entry = links[key]
        status = entry.get("status")
        if status not in STATUSES:
            raise SystemExit("bad conti status for cut %s" % key)
        return {
            "status": status,
            "path": entry.get("path"),
            "basis": with_audit_prefix(entry.get("basis") or ""),
            "source": "ep01_conti_links",
            "reason": "",
        }
    conti = conti_for_frame(row, cuts_island)
    if conti["status"] == "unlinked":
        reason = UI_REASON if row.get("kind") == "ui" else TEXT_REASON
        conti["basis"] = reason
        conti["reason"] = reason
    else:
        conti["reason"] = ""
    return conti


def attach_conti_preview(conti, written):
    path = conti.get("path")
    if conti["status"] not in ("linked", "reference", "check") or not path:
        conti["preview"] = None
        conti["preview_ready"] = False
        return
    name = thumb_name(path)
    dest = IMG / name
    ready = False
    src = ROOT / path
    if src.is_file():
        ready = write_jpeg(src, dest)
        if ready:
            written.add(name)
    conti["preview"] = "series_cuts/img/" + name
    conti["preview_ready"] = ready and dest.is_file()


def image_info(row):
    rel = to_rel(row.get("src"))
    kind = row.get("kind")
    info = {
        "path": rel,
        "exists": exists_rel(rel),
        "ui": kind == "ui",
        "preview": None,
        "preview_ready": False,
    }
    if not rel or not rel.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return info
    name = thumb_name(rel)
    info["preview"] = "series_cuts/img/" + name
    if info["exists"]:
        info["preview_ready"] = write_jpeg(ROOT / rel, IMG / name) and (IMG / name).is_file()
    return info


def video_info(row):
    number = row.get("n")
    designated = to_rel(row.get("clip"))
    src = to_rel(row.get("src"))
    playback = designated
    if not playback and row.get("kind") in ("ui", "video") and src and src.lower().endswith(".mp4"):
        playback = src
    takes = []
    seen = set()

    def add(rel, take_no):
        if not rel or rel in seen:
            return
        seen.add(rel)
        exists = exists_rel(rel)
        preview = None
        if exists:
            dest = VID / ("E1_%02d_%s" % (int(number), Path(rel).name))
            link_video(ROOT / rel, dest)
            preview = "series_cuts/vid/" + dest.name
        takes.append({
            "take": take_no,
            "path": rel,
            "name": Path(rel).name,
            "exists": exists,
            "src": preview,
        })

    folder = VIDEO_ROOT / ("E1_%02d" % int(number))
    for take_no, path in list_takes(folder):
        add(to_rel(path), take_no)
    if playback:
        add(playback, take_number(playback))
    return {
        "clip": designated,
        "clip_exists": exists_rel(designated),
        "default_take": take_number(designated if designated else playback),
        "takes": takes,
    }


def build_cuts(rows, links, cuts_island):
    reset_dir(IMG)
    reset_dir(VID)
    written = set()
    cuts = []
    for row in rows:
        conti = conti_for_row(row, links, cuts_island)
        attach_conti_preview(conti, written)
        video = video_info(row)
        cuts.append({
            "n": row.get("n"),
            "skip": bool(row.get("skip")),
            "kind": row.get("kind") or "",
            "who": clean_name(row.get("who") or ""),
            "line": clean_name(row.get("line") or ""),
            "spoken": spoken_line(row.get("line") or ""),
            "direction": direction_of(row),
            "emotion": clean_name(row.get("emotion") or ""),
            "frame": row.get("frame") or "",
            "image": image_info(row),
            "video": video,
            "conti": conti,
        })
    return cuts, written


def active(cuts):
    return [cut for cut in cuts if not cut["skip"]]


def stats_of(cuts, written):
    rows = active(cuts)
    def nums(status):
        return [cut["n"] for cut in rows if cut["conti"]["status"] == status]
    linked = nums("linked")
    reference = nums("reference")
    check = nums("check")
    unlinked = nums("unlinked")
    ui = [cut["n"] for cut in rows if cut["conti"]["reason"] == UI_REASON]
    paths = []
    for cut in cuts:
        path = cut["conti"].get("path")
        if cut["conti"]["status"] in ("linked", "reference", "check") and path:
            paths.append(path)
    unique_paths = sorted(set(paths))
    return {
        "rows": len(cuts),
        "active": len(rows),
        "skip": [cut["n"] for cut in cuts if cut["skip"]],
        "conti_linked": len(linked),
        "conti_linked_cuts": linked,
        "conti_reference": len(reference),
        "conti_reference_cuts": reference,
        "conti_check": len(check),
        "conti_check_cuts": check,
        "conti_unlinked": len(unlinked),
        "conti_unlinked_cuts": unlinked,
        "conti_unlinked_ui": len(ui),
        "conti_unlinked_ui_cuts": ui,
        "skip_linked": [cut["n"] for cut in cuts if cut["skip"] and cut["conti"]["status"] == "linked"],
        "clips_designated": sum(1 for cut in rows if cut["video"].get("clip")),
        "clips_exist": sum(1 for cut in rows if cut["video"].get("clip_exists")),
        "thumbnail_planned": len(unique_paths),
        "thumbnail_written": len(written),
        "thumbnail_paths": unique_paths,
        "cut3_default_take": next(cut["video"]["default_take"] for cut in cuts if cut["n"] == 3),
        "preview": "board_web/series.html#EP01/images",
    }


def assert_audit(cuts, stats):
    problems = []
    def same(label, got, expect):
        if set(got) != set(expect):
            problems.append("%s got %s" % (label, sorted(got)))
    same("linked", stats["conti_linked_cuts"], EXPECT_LINKED)
    same("reference", stats["conti_reference_cuts"], EXPECT_REFERENCE)
    same("check", stats["conti_check_cuts"], EXPECT_CHECK)
    same("ui", stats["conti_unlinked_ui_cuts"], EXPECT_UI)
    if stats["conti_unlinked"] != 27 or stats["active"] != 42:
        problems.append("counts linked/ref/check/unlinked/active")
    if stats["conti_linked"] + stats["conti_reference"] + stats["conti_check"] + stats["conti_unlinked"] != 42:
        problems.append("active sum")
    skip_linked = {cut["n"] for cut in cuts if cut["n"] in EXPECT_SKIP_LINKED}
    for cut in cuts:
        if cut["n"] in EXPECT_SKIP_LINKED:
            if not cut["skip"] or cut["conti"]["status"] != "linked":
                problems.append("skip %s" % cut["n"])
            if AUDIT not in (cut["conti"].get("basis") or ""):
                problems.append("skip basis %s" % cut["n"])
        if str(cut["n"]) not in json.loads(LINKS.read_text(encoding="utf-8")):
            if cut["conti"]["status"] != "unlinked" or cut["conti"]["source"] == "ep01_conti_links":
                problems.append("auto match %s" % cut["n"])
        else:
            if cut["conti"]["source"] != "ep01_conti_links":
                problems.append("links unused %s" % cut["n"])
            if AUDIT not in cut["conti"]["basis"]:
                problems.append("basis prefix %s" % cut["n"])
    if stats["thumbnail_planned"] != 13:
        problems.append("planned thumbs %s" % stats["thumbnail_planned"])
    if stats["cut3_default_take"] != 1:
        problems.append("cut3 take %s" % stats["cut3_default_take"])
    if stats["clips_designated"] != 13:
        problems.append("clips %s" % stats["clips_designated"])
    cut3 = next(cut for cut in cuts if cut["n"] == 3)
    cut22 = next(cut for cut in cuts if cut["n"] == 22)
    if cut3["spoken"] == cut22["spoken"] or cut3["video"]["clip"] == cut22["video"]["clip"]:
        problems.append("shared still mixed lines")
    for cut in cuts:
        for key in ("who", "line", "spoken", "direction", "emotion"):
            value = cut.get(key) or ""
            if "비아" in value or re.search(r"\bBea\b", value):
                problems.append("name %s %s" % (cut["n"], key))
        for take in cut["video"]["takes"]:
            if "_old" in take["name"].lower():
                problems.append("old take %s" % take["name"])
    for path in VID.iterdir():
        if not path.is_symlink():
            problems.append("video copied %s" % path.name)
    if len(skip_linked) != 2:
        problems.append("skip set")
    if not any(cut["n"] == 29 and cut["skip"] for cut in cuts):
        problems.append("skip 29")
    # 상태 행 15 = 활성 linked 6 + reference 8 + check 1. check 는 그림이 없다.
    if stats["conti_linked"] + stats["conti_reference"] + stats["conti_check"] != 15:
        problems.append("status slots")
    if problems:
        raise SystemExit("audit check failed: " + "; ".join(problems))


def self_check_takes():
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "EP01R_E1_03_kling3_take01.mp4").write_bytes(b"a")
        (folder / "EP01R_E1_03_kling3_take06.mp4").write_bytes(b"b")
        (folder / "EP01R_E1_03_kling3_take04_old.mp4").write_bytes(b"c")
        (folder / "EP01R_E1_03_kling3_take05_old2.mp4").write_bytes(b"d")
        (folder / "EP01R_E1_03_contact.png").write_bytes(b"e")
        got = [number for number, _path in list_takes(folder)]
        if got != [1, 6]:
            raise SystemExit("take scan failed: %s" % got)
    if take_number("01_EPISODES/EP01R/video/v08/E1_03/EP01R_E1_03_kling3_take01.mp4") != 1:
        raise SystemExit("take number parse failed")


def write_report(stats):
    lines = [
        "# 1화 컷 보드 — 콘티 연결 (작업 31)",
        "",
        "생성: `python3 tools/series_cut_assets.py`",
        "보드: `python3 tools/build_series_board.py` → `board_web/series.html#EP01/images`",
        "",
        "수동 매핑 `tools/ep01_conti_links.json` 은 `tools/SCRIPT_CONTI_AUDIT.md` 3.3 초안 그대로다. 판정은 바꾸지 않았다.",
        "",
        "## 활성 42컷",
        "",
        "- 연결 %d: %s" % (stats["conti_linked"], ", ".join(str(n) for n in stats["conti_linked_cuts"])),
        "- 참고만 %d: %s" % (stats["conti_reference"], ", ".join(str(n) for n in stats["conti_reference_cuts"])),
        "- 확인 필요 %d: %s" % (stats["conti_check"], ", ".join(str(n) for n in stats["conti_check_cuts"])),
        "- 없음 %d (UI %d: %s)" % (
            stats["conti_unlinked"],
            stats["conti_unlinked_ui"],
            ", ".join(str(n) for n in stats["conti_unlinked_ui_cuts"]),
        ),
        "- skip 이면서 연결 표시(활성 집계 제외): %s" % ", ".join(str(n) for n in stats["skip_linked"]),
        "",
        "## 썸네일",
        "",
        "활성 상태 행은 15개(연결 6 + 참고만 8 + 확인 필요 1)다. 확인 필요 컷 30은 path가 없어 썸네일이 없다.",
        "그림 경로 고유 %d개. 같은 파일을 쓰는 컷은 8·23, 9·42, 13·45라 파일은 한 장만 만든다." % stats["thumbnail_planned"],
        "이 실행에서 실제로 쓴 콘티 썸네일: %d. 콘티 PNG는 저장소에 없고(이미지 git 제외) 있는 머신에서 다시 실행하면 채워진다." % stats["thumbnail_written"],
        "",
        "## 영상",
        "",
        "활성 컷에 지정된 clip %d. 파일이 있는 clip %d." % (stats["clips_designated"], stats["clips_exist"]),
        "컷 3 기본 테이크 번호: %s. `_old` 파일은 후보에서 빼고, 영상은 `board_web/series_cuts/vid/` 심볼릭 링크만 만든다." % stats["cut3_default_take"],
        "",
        "애니매틱 JSON·각본·frames·video 원본은 수정하지 않았다. 생성 API는 호출하지 않았다.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    self_check_takes()
    before = (ANIM.stat().st_mtime_ns, ANIM.stat().st_size)
    rows = load_json(ANIM)
    links = load_json(LINKS)
    cuts_island = load_json(CUTS_ISLAND)
    cuts, written = build_cuts(rows, links, cuts_island)
    stats = stats_of(cuts, written)
    assert_audit(cuts, stats)
    after = (ANIM.stat().st_mtime_ns, ANIM.stat().st_size)
    if before != after:
        raise SystemExit("animatic json changed")
    payload = {
        "source": to_rel(ANIM),
        "links": to_rel(LINKS),
        "stats": stats,
        "cuts": cuts,
    }
    MAP_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(stats)
    print("map", MAP_OUT)
    print("active", stats["active"], "linked", stats["conti_linked"], "reference", stats["conti_reference"],
          "check", stats["conti_check"], "unlinked", stats["conti_unlinked"], "ui", stats["conti_unlinked_ui"])
    print("thumbs_planned", stats["thumbnail_planned"], "thumbs_written", stats["thumbnail_written"])
    print("clips", stats["clips_designated"], "exist", stats["clips_exist"], "cut3", stats["cut3_default_take"])
    print("OK")


if __name__ == "__main__":
    main()
