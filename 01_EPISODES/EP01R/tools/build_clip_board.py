# -*- coding: utf-8 -*-
"""1화 Kling 대사 클립 보드.

usage: python3 01_EPISODES/EP01R/tools/build_clip_board.py
출력: 01_EPISODES/EP01R/board_clips/index.html + board_clips/media/
발행(Artifact)은 하지 않는다.
"""
import datetime
import difflib
import glob
import html
import json
import os
import re
import shutil
import sys

LIMIT = 60 * 1024 * 1024
MAC_ROOT = "/Users/ymy/project/sns"
FACE_KEYS = ("f25", "f50", "f75", "end")


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", ".."))


def episode_root():
    return os.path.join(repo_root(), "01_EPISODES", "EP01R")


def resolve_path(path):
    if not path:
        return ""
    path = os.path.expanduser(str(path))
    if os.path.isfile(path):
        return path
    if path.startswith(MAC_ROOT + os.sep) or path.startswith(MAC_ROOT + "/"):
        alt = os.path.join(repo_root(), path[len(MAC_ROOT):].lstrip("/\\"))
        if os.path.isfile(alt):
            return alt
        return alt
    if not os.path.isabs(path):
        return os.path.join(episode_root(), path)
    return path


def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def norm_text(text):
    text = re.sub(r"ㅋ+|ㅠ+|\.{2,}|…", "", text or "")
    return re.sub(r"[^가-힣0-9a-zA-Z]", "", text)


def whisper_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for seg in value:
            if isinstance(seg, str):
                parts.append(seg)
            elif isinstance(seg, dict):
                parts.append(str(seg.get("text") or ""))
        return "\n".join(parts)
    return str(value)


def match_line(line, whisper):
    whisper = whisper_text(whisper)
    timed = [row for row in whisper.splitlines() if re.match(r"\s*\d", row)]
    if timed:
        said = " ".join(row.split("  ", 1)[-1].strip() for row in timed)
    else:
        said = whisper.strip()
    left, right = norm_text(line), norm_text(said)
    if not right:
        return 0.0, said
    return difflib.SequenceMatcher(None, left, right).ratio(), said


def parse_face(value):
    if value is None or value == "":
        return None
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        try:
            return (float(value[0]), int(value[1]))
        except (TypeError, ValueError):
            return None
    if isinstance(value, dict):
        score = value.get("score", value.get("sim", value.get("similarity")))
        width = value.get("width", value.get("px", value.get("w")))
        if score is None:
            return None
        try:
            return (float(score), int(width or 0))
        except (TypeError, ValueError):
            return None
    match = re.search(r"(\d+\.\d+)\s*\(\s*(\d+)\s*px\s*\)", str(value))
    if not match:
        return None
    return (float(match.group(1)), int(match.group(2)))


def as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in ("1", "true", "yes", "pass", "ok"):
        return True
    if text in ("0", "false", "no", "fail"):
        return False
    return bool(value)


def judge(face_vals, single, ratio, single_known):
    scores = [item[0] for item in face_vals if item]
    widths = [item[1] for item in face_vals if item]
    fmin = min(scores) if scores else 0.0
    wmin = min(widths) if widths else 0
    face_ok = fmin >= 0.45 and wmin >= 180 and all(face_vals)
    said_ok = ratio >= 0.85
    ok = face_ok and single and said_ok and single_known
    why = []
    if not single_known:
        why.append("단일샷 정보 없음")
    elif not single:
        why.append("내부 컷")
    if not face_ok:
        why.append("얼굴 {0:.2f}".format(fmin) if all(face_vals) else "얼굴 미검출")
    if not said_ok:
        why.append("대사 불일치" if ratio > 0 else "무음")
    return {
        "face_ok": face_ok,
        "fmin": fmin,
        "wmin": wmin,
        "single": bool(single) if single_known else False,
        "said_ok": said_ok,
        "verdict": "통과" if ok else "재생성",
        "why": why,
        "single_known": single_known,
    }


def take_num(path):
    match = re.search(r"take(\d+)", os.path.basename(path), re.I)
    return int(match.group(1)) if match else -1


def take_label(path):
    number = take_num(path)
    if number >= 0:
        return "take{0:02d}".format(number)
    return os.path.basename(path)


def video_duration(path):
    try:
        import cv2
    except ImportError:
        return 0.0
    cap = cv2.VideoCapture(path)
    try:
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        if fps <= 1e-3:
            return 0.0
        return float(frames) / float(fps)
    finally:
        cap.release()


def select_under_budget(required, optional, budget):
    """오래된 optional 부터 빼서 required+optional 합이 budget 이하가 되게 한다."""
    kept = sorted(optional, key=lambda item: (item.get("mtime", 0), item.get("take_num", 0)))
    dropped = []

    def total(items):
        return sum(item["size"] for item in required) + sum(item["size"] for item in items)

    while kept and total(kept) > budget:
        dropped.append(kept.pop(0))
    return kept, dropped


def clear_media(media_dir):
    os.makedirs(media_dir, exist_ok=True)
    for old in glob.glob(os.path.join(media_dir, "*")):
        if old.lower().endswith((".mp4", ".jpg", ".jpeg")):
            os.remove(old)


def save_still(src, dest):
    from PIL import Image
    image = Image.open(src).convert("RGB")
    image.thumbnail((540, 960))
    image.save(dest, quality=82)


def discover_takes(cut, clip_path):
    folder = os.path.join(episode_root(), "video", "v08", "E1_{0:02d}".format(cut))
    found = []
    if os.path.isdir(folder):
        found.extend(glob.glob(os.path.join(folder, "*_kling3_take*.mp4")))
    if clip_path and os.path.isfile(clip_path):
        clip_base = os.path.basename(clip_path)
        if all(os.path.basename(path) != clip_base for path in found):
            found.append(clip_path)
    unique = []
    seen = set()
    for path in found:
        base = os.path.basename(path)
        if base in seen:
            continue
        seen.add(base)
        unique.append(path)
    return unique


def dest_video_name(cut, path, used):
    number = take_num(path)
    if number >= 0:
        base = "E1_{0:02d}_take{1:02d}.mp4".format(cut, number)
    else:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.basename(path))
        base = "E1_{0:02d}_{1}".format(cut, safe)
    name = base
    serial = 2
    while name in used:
        stem, ext = os.path.splitext(base)
        name = "{0}_{1}{2}".format(stem, serial, ext)
        serial += 1
    used.add(name)
    return name


def qa_for_take(record, path):
    clip = record.get("_clip") or ""
    if not clip:
        return None
    if os.path.basename(path) == os.path.basename(clip):
        return record
    try:
        if os.path.isfile(clip) and os.path.samefile(path, clip):
            return record
    except OSError:
        return None
    return None


def face_score_text(face_vals):
    parts = []
    for value in face_vals:
        parts.append("{0:.2f}".format(value[0]) if value else "–")
    return " · ".join(parts)


def badges_for(info, face_vals):
    if info is None:
        return [["na", "QA 없음"]]
    ratio = info["ratio"]
    if not info.get("single_known", True):
        shot = ("bad", "단일샷 정보 없음")
    elif info["single"]:
        shot = ("ok", "단일 샷")
    else:
        shot = ("bad", "내부 컷")
    badges = [
        shot,
        (
            "ok" if (info["fmin"] >= 0.45 and all(face_vals)) else "bad",
            "얼굴 {0:.2f}".format(info["fmin"]) if all(face_vals) else "얼굴 미검출",
        ),
        (
            "ok" if ratio >= 0.85 else "bad",
            "대사 {0}%".format(int(round(ratio * 100))) if ratio > 0 else "무음",
        ),
    ]
    if info["wmin"] < 180 and all(face_vals):
        badges[1] = ("bad", "얼굴 {0:.2f}/{1}px".format(info["fmin"], info["wmin"]))
    return badges


def load_cards():
    ep = episode_root()
    anim_path = os.path.join(ep, "edit", "v06", "animatic_E1_v062.json")
    rows = {int(row["n"]): row for row in load_json(anim_path)}
    paths = sorted(glob.glob(os.path.join(ep, "video", "v08", "qa_*.json")))
    if not paths:
        raise SystemExit("qa json 없음: {0}".format(os.path.join(ep, "video", "v08", "qa_*.json")))
    chosen = {}
    for path in paths:
        data = load_json(path)
        if not isinstance(data, dict):
            raise SystemExit("{0}: 객체 json 이 아님".format(path))
        number = data.get("cut", data.get("n"))
        if number is None:
            match = re.search(r"qa_(\d+)", os.path.basename(path))
            if not match:
                raise SystemExit("{0}: cut 번호 없음".format(path))
            number = match.group(1)
        number = int(number)
        stamp = os.path.getmtime(path)
        prev = chosen.get(number)
        if prev is None or stamp >= prev["qmtime"]:
            data["_qa_path"] = path
            data["_qmtime"] = stamp
            chosen[number] = {"data": data, "qmtime": stamp}
    cards = []
    for number in sorted(chosen):
        data = chosen[number]["data"]
        if number not in rows:
            raise SystemExit("애니매틱에 컷 {0} 행이 없음".format(number))
        row = rows[number]
        clip = resolve_path(data.get("clip") or "")
        data["_clip"] = clip
        face = data.get("face") if isinstance(data.get("face"), dict) else {}
        face_vals = [parse_face(face.get(key)) for key in FACE_KEYS]
        ratio, said = match_line(row.get("line") or "", data.get("whisper"))
        single_known = "single_shot" in data
        single = as_bool(data.get("single_shot")) if single_known else False
        info = judge(face_vals, single, ratio, single_known)
        info.update({
            "ratio": ratio,
            "said": said,
            "face_vals": face_vals,
            "take_name": str(data.get("take") or take_label(clip)),
        })
        takes = []
        for src in discover_takes(number, clip):
            takes.append({
                "src": src,
                "take_num": take_num(src),
                "mtime": os.path.getmtime(src),
                "size": os.path.getsize(src),
                "label": take_label(src),
                "qa": qa_for_take(data, src) is not None,
            })
        if not takes:
            folder = os.path.join(ep, "video", "v08", "E1_{0:02d}".format(number))
            raise SystemExit("컷 {0}: mp4 없음 ({1})".format(number, folder))
        latest_i = max(range(len(takes)), key=lambda i: (takes[i]["take_num"], takes[i]["mtime"]))
        for index, take in enumerate(takes):
            take["required"] = index == latest_i
        still_src = resolve_path(row.get("src") or "")
        if not os.path.isfile(still_src):
            raise SystemExit("컷 {0}: 스틸 없음 ({1})".format(number, still_src))
        cards.append({
            "n": number,
            "who": row.get("who") or "",
            "line": row.get("line") or "",
            "act": row.get("dir_override") or row.get("action") or "",
            "frame": row.get("frame") or os.path.basename(still_src),
            "still_src": still_src,
            "verdict": info["verdict"],
            "why": info["why"],
            "info": info,
            "takes": takes,
        })
    return cards


def attach_media(cards):
    ep = episode_root()
    out = os.path.join(ep, "board_clips")
    media = os.path.join(out, "media")
    clear_media(media)
    used_names = set()
    required = []
    optional = []
    for card in cards:
        still_name = "S_{0:02d}.jpg".format(card["n"])
        still_dest = os.path.join(media, still_name)
        save_still(card["still_src"], still_dest)
        card["still"] = "media/" + still_name
        required.append({"size": os.path.getsize(still_dest), "id": still_name})
        for take in card["takes"]:
            take["dest_name"] = dest_video_name(card["n"], take["src"], used_names)
            take["card"] = card["n"]
            if take["required"]:
                required.append(take)
            else:
                optional.append(take)
    kept, dropped = select_under_budget(required, optional, LIMIT)
    keep_ids = set(id(item) for item in kept)
    for card in cards:
        card["takes"] = [take for take in card["takes"] if take["required"] or id(take) in keep_ids]
        for take in card["takes"]:
            dest = os.path.join(media, take["dest_name"])
            shutil.copy2(take["src"], dest)
            take["href"] = "media/" + take["dest_name"]
            take["dur"] = video_duration(dest)
        card["takes"].sort(key=lambda take: (take["take_num"], take["mtime"]), reverse=True)
    total = 0
    for name in os.listdir(media):
        total += os.path.getsize(os.path.join(media, name))
    return out, dropped, total


def take_payload(card, take):
    info = card["info"] if take["qa"] else None
    face_vals = info["face_vals"] if info else []
    return {
        "src": take["href"],
        "label": take["label"],
        "dur": round(float(take["dur"]), 2),
        "qa": bool(take["qa"]),
        "badges": badges_for(info, face_vals) if info else [["na", "QA 없음"]],
        "scores": face_score_text(face_vals) if info else "",
        "said": info["said"] if info else "",
    }


def card_html(card):
    payloads = [take_payload(card, take) for take in card["takes"]]
    current = payloads[0]
    options = []
    for index, payload in enumerate(payloads):
        mark = " selected" if index == 0 else ""
        qa_note = "" if payload["qa"] else " · QA 없음"
        label = "{0} · {1:.1f}s{2}".format(payload["label"], payload["dur"], qa_note)
        options.append(
            '<option value="{0}"{1}>{2}</option>'.format(
                html.escape(payload["src"], quote=True),
                mark,
                html.escape(label),
            )
        )
    blob = json.dumps(payloads, ensure_ascii=False).replace("<", "\\u003c")
    why = (" · " + ", ".join(card["why"])) if card["why"] else ""
    verdict_class = "pass" if card["verdict"] == "통과" else "redo"
    act = '<p class="act">{0}</p>'.format(html.escape(card["act"])) if card["act"] else ""
    said_key = "whisper" if current["qa"] else "QA"
    said_body = html.escape(current["said"]) if current["qa"] and current["said"] else ("(음성 없음)" if current["qa"] else "QA 없음")
    badge_html = "".join(
        '<span class="badge {0}">{1}</span>'.format(html.escape(kind), html.escape(text))
        for kind, text in current["badges"]
    )
    scores = ""
    if current["scores"]:
        scores = '<span class="scores">얼굴 25/50/75/끝 = {0}</span>'.format(html.escape(current["scores"]))
    return """
<article class="cut" data-verdict="{verdict}" id="cut-{n}">
  <header><span class="num">{num}</span><span class="who">{who}</span><span class="line">{line}</span><span class="verdict {vclass}">{verdict}{why}</span></header>
  <div class="pair">
    <figure><img src="{still}" alt="컷 {n} 시작 스틸" loading="lazy"><figcaption>시작 스틸 · {frame}</figcaption></figure>
    <figure>
      <video src="{src}" controls preload="metadata" playsinline></video>
      <label class="take-label">테이크 <select class="take" aria-label="컷 {n} 테이크">{options}</select></label>
      <figcaption class="cap">{cap}</figcaption>
    </figure>
  </div>
  <div class="qa">{badges}{scores}</div>
  <p class="said"><span class="k">{said_key}</span> {said}</p>
  {act}
  <script type="application/json" class="take-data">{blob}</script>
</article>""".format(
        verdict=html.escape(card["verdict"]),
        n=card["n"],
        num="{0:02d}".format(card["n"]),
        who=html.escape(card["who"]),
        line=html.escape(card["line"]),
        vclass=verdict_class,
        why=html.escape(why),
        still=html.escape(card["still"], quote=True),
        frame=html.escape(card["frame"]),
        src=html.escape(current["src"], quote=True),
        options="".join(options),
        cap=html.escape("{0} · {1:.1f}s".format(current["label"], current["dur"])),
        badges=badge_html,
        scores=scores,
        said_key=said_key,
        said=said_body,
        act=act,
        blob=blob,
    )


def page_html(cards, dropped, total):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    passed = sum(1 for card in cards if card["verdict"] == "통과")
    act1 = [card for card in cards if card["n"] <= 21]
    act2 = [card for card in cards if card["n"] >= 22]

    def section(title, group):
        if not group:
            return ""
        ok = sum(1 for card in group if card["verdict"] == "통과")
        body = "".join(card_html(card) for card in group)
        return "<section><h2>{0} <small>{1}/{2} 통과</small></h2>{3}</section>".format(title, ok, len(group), body)

    if dropped:
        names = ", ".join(
            "E1_{0:02d}/{1}".format(item["card"], os.path.basename(item["src"])) for item in dropped
        )
        budget = "용량 한도 60MB를 넘겨 오래된 테이크를 뺌: {0}. 현재 media {1:.1f}MB.".format(
            names, total / 1048576.0
        )
    else:
        budget = "media {0:.1f}MB / 60MB. 제외한 테이크 없음.".format(total / 1048576.0)
        if total > LIMIT:
            budget += " 최신 테이크와 스틸만으로 한도를 넘음."
    style = """
<style>
:root{--bg:#f6f3ee;--card:#fffdf9;--fg:#1f1b16;--mute:#6d655b;--rule:#e2dbd0;--accent:#b8471f;--ok:#2f7a4a;--ok-bg:#e4f2e8;--bad:#a8341c;--bad-bg:#f8e3dc;
 --body:"Noto Sans KR",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#17150f;--card:#211e17;--fg:#f0eae0;--mute:#a69c8d;--rule:#352f26;--accent:#e2794c;--ok:#7fcf98;--ok-bg:#1e3326;--bad:#f09a82;--bad-bg:#3d1f17;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17150f;--card:#211e17;--fg:#f0eae0;--mute:#a69c8d;--rule:#352f26;--accent:#e2794c;--ok:#7fcf98;--ok-bg:#1e3326;--bad:#f09a82;--bad-bg:#3d1f17;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 60px;line-height:1.5}
main{max-width:1040px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 4px;text-wrap:balance} .sub{color:var(--mute);margin:0 0 18px;font-size:.9rem}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.filters button{font:inherit;font-size:.85rem;padding:6px 12px;border-radius:999px;border:1px solid var(--rule);background:var(--card);color:var(--fg);cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.filters button:focus-visible,video:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
h2{font-size:1.05rem;margin:26px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--rule)} h2 small{color:var(--mute);font-weight:400;font-size:.85rem;margin-left:8px}
.cut{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px;margin-bottom:14px}
.cut header{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;margin-bottom:10px}
.num{font-family:var(--mono);font-weight:500;color:var(--accent);font-size:1.05rem} .who{font-weight:700} .line{flex:1 1 260px;min-width:0}
.verdict{font-size:.8rem;padding:2px 10px;border-radius:999px;font-weight:500;white-space:nowrap} .verdict.pass{background:var(--ok-bg);color:var(--ok)} .verdict.redo{background:var(--bad-bg);color:var(--bad)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:620px}
figure{margin:0;min-width:0} figure img,figure video{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:6px;background:#000;display:block;max-width:100%}
figcaption,.take-label{font-family:var(--mono);font-size:.72rem;color:var(--mute);margin-top:4px;overflow-wrap:anywhere}
.take{font:inherit;font-size:.78rem;max-width:100%;margin-left:4px}
.qa{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin-top:10px}
.badge{font-size:.78rem;padding:2px 8px;border-radius:4px;font-family:var(--mono)} .badge.ok{background:var(--ok-bg);color:var(--ok)} .badge.bad{background:var(--bad-bg);color:var(--bad)} .badge.na{background:var(--rule);color:var(--fg)}
.scores{font-family:var(--mono);font-size:.78rem;color:var(--mute);font-variant-numeric:tabular-nums}
.said{margin:8px 0 0;font-size:.9rem} .said .k{font-family:var(--mono);font-size:.72rem;color:var(--mute);margin-right:6px}
.act{margin:4px 0 0;font-size:.82rem;color:var(--mute)}
@media (max-width:480px){.pair{gap:8px} .cut{padding:10px}}
@media (prefers-reduced-motion:no-preference){.filters button{transition:background .15s}}
</style>
"""
    script = """
<script>
const bs=[...document.querySelectorAll(".filters button")];
function apply(f){
  document.querySelectorAll(".cut").forEach(c=>{c.hidden=(f!=="all"&&c.dataset.verdict!==f);});
  bs.forEach(b=>b.setAttribute("aria-pressed", String(b.dataset.f===f)));
  try{localStorage.setItem("clipFilter", f);}catch(e){}
}
bs.forEach(b=>b.addEventListener("click", ()=>apply(b.dataset.f)));
let f="all";
try{f=localStorage.getItem("clipFilter")||"all";}catch(e){}
if(!bs.some(b=>b.dataset.f===f)) f="all";
apply(f);
function paint(card, take){
  const video=card.querySelector("video");
  if(video.getAttribute("src")!==take.src){
    video.pause();
    video.setAttribute("src", take.src);
    video.load();
  }
  card.querySelector(".cap").textContent=take.label+" · "+Number(take.dur).toFixed(1)+"s";
  const qa=card.querySelector(".qa");
  qa.replaceChildren();
  (take.badges||[]).forEach(pair=>{
    const span=document.createElement("span");
    span.className="badge "+pair[0];
    span.textContent=pair[1];
    qa.appendChild(span);
  });
  if(take.scores){
    const span=document.createElement("span");
    span.className="scores";
    span.textContent="얼굴 25/50/75/끝 = "+take.scores;
    qa.appendChild(span);
  }
  const said=card.querySelector(".said");
  said.replaceChildren();
  const key=document.createElement("span");
  key.className="k";
  key.textContent=take.qa?"whisper":"QA";
  said.appendChild(key);
  said.appendChild(document.createTextNode(" "+(take.qa?(take.said||"(음성 없음)"):"QA 없음")));
}
document.querySelectorAll(".cut").forEach(card=>{
  const data=JSON.parse(card.querySelector(".take-data").textContent);
  const sel=card.querySelector("select.take");
  sel.addEventListener("change", ()=>paint(card, data[sel.selectedIndex]));
});
document.querySelectorAll("video").forEach(v=>v.addEventListener("play", ()=>{
  document.querySelectorAll("video").forEach(o=>{if(o!==v) o.pause();});
}));
</script>
"""
    return """<meta charset="utf-8">
<title>토마톡 1화 클립 보드</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{style}<main>
<h1>토마톡 1화 Kling 대사 클립</h1>
<p class="sub">{stamp} 기준 · {count}컷 중 {passed}컷 통과 · 왼쪽 시작 스틸, 오른쪽 테이크 영상. 기준: 단일 샷 · 얼굴 4지점 ≥0.45 · 얼굴 폭 ≥180px · whisper 대사 일치 ≥85%. 기본 재생은 최신 테이크.</p>
<p class="sub" id="budget">{budget}</p>
<div class="filters" role="group" aria-label="필터">
 <button type="button" data-f="all" aria-pressed="true" id="f-all">전체 {count}</button>
 <button type="button" data-f="통과" aria-pressed="false" id="f-pass">통과 {passed}</button>
 <button type="button" data-f="재생성" aria-pressed="false" id="f-redo">재생성 {redo}</button>
</div>
{act1}
{act2}
</main>
{script}""".format(
        style=style,
        stamp=stamp,
        count=len(cards),
        passed=passed,
        redo=len(cards) - passed,
        budget=html.escape(budget),
        act1=section("1막 · 소파 / 아일랜드", act1),
        act2=section("2막 · 아일랜드", act2),
        script=script,
    )


def main():
    cards = load_cards()
    out, dropped, total = attach_media(cards)
    dest = os.path.join(out, "index.html")
    with open(dest, "w", encoding="utf-8") as handle:
        handle.write(page_html(cards, dropped, total))
    passed = sum(1 for card in cards if card["verdict"] == "통과")
    print("{0} cards, {1} pass → {2}".format(len(cards), passed, dest))
    print(" ".join("{0}:{1}".format(card["n"], card["verdict"]) for card in cards))
    print("media {0:.1f}MB".format(total / 1048576.0))
    if dropped:
        print("제외한 오래된 테이크: " + ", ".join(os.path.basename(item["src"]) for item in dropped))
    else:
        print("제외한 테이크 없음")
    if total > LIMIT:
        print("주의: 최신 테이크와 스틸만으로 60MB를 넘김")


if __name__ == "__main__":
    main()
