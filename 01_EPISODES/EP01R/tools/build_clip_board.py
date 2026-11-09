#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 1화 Kling 대사 클립 보드: 컷마다 시작 스틸 | 최신 테이크 영상(재생) | QA(얼굴·단일샷·whisper). 2026-11-09
# usage: build_clip_board.py  → board_clips/index.html + board_clips/media/*  (발행은 Claude가 Artifact로)
import json, os, glob, re, shutil, difflib, html, datetime
from PIL import Image
E="/Users/ymy/project/sns/01_EPISODES/EP01R"; OUT=f"{E}/board_clips"; MED=f"{OUT}/media"
os.makedirs(MED, exist_ok=True)
rows={r["n"]:r for r in json.load(open(f"{E}/edit/v06/animatic_E1_v062.json"))}
def norm(t): return re.sub(r"[^가-힣0-9a-zA-Z]","",re.sub(r"ㅋ+|ㅠ+|\.{2,}|…","",t or ""))
def match(line, wh):
    said=" ".join(l.split("  ",1)[-1].strip() for l in wh.splitlines() if re.match(r"\s*\d",l))
    a,b=norm(line),norm(said)
    if not b: return 0.0, said
    return difflib.SequenceMatcher(None,a,b).ratio(), said
cards=[]
for q in sorted(glob.glob(f"{E}/video/v08/qa_*.json")):
    d=json.load(open(q)); n=d["cut"]; r=rows[n]
    mp4=d["clip"]; dst=f"media/E1_{n:02d}.mp4"; shutil.copy2(mp4, f"{OUT}/{dst}")
    still=r["src"]; th=f"media/S_{n:02d}.jpg"
    im=Image.open(still).convert("RGB"); im.thumbnail((540,960)); im.save(f"{OUT}/{th}", quality=82)
    ratio, said=match(r["line"], d["whisper"])
    face_vals=[]
    for t in ("f25","f50","f75","end"):
        m=re.search(r"(\d\.\d\d) \((\d+)px\)", d["face"].get(t,"")); face_vals.append((float(m.group(1)),int(m.group(2))) if m else None)
    fmin=min([v[0] for v in face_vals if v], default=0); wmin=min([v[1] for v in face_vals if v], default=0)
    face_ok=fmin>=0.45 and wmin>=180 and all(face_vals)
    single=d["single_shot"]; said_ok=ratio>=0.85
    verdict="통과" if (face_ok and single and said_ok) else "재생성"
    why=[]
    if not single: why.append("내부 컷")
    if not face_ok: why.append(f"얼굴 {fmin:.2f}" if all(face_vals) else "얼굴 미검출")
    if not said_ok: why.append("대사 불일치" if ratio>0 else "무음")
    frames=0
    try:
        import cv2; cap=cv2.VideoCapture(mp4); frames=int(cap.get(7)); fps=cap.get(5) or 24; dur=frames/fps
    except Exception: dur=0
    cards.append(dict(n=n, who=r["who"], line=r["line"], act=(r.get("dir_override") or r.get("action") or ""), still=th, video=dst, take=d["take"],
                      face=face_vals, fmin=fmin, single=single, said=said, ratio=ratio, verdict=verdict, why=why, dur=dur, frame=r["frame"]))
stamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
n_pass=sum(c["verdict"]=="통과" for c in cards)
def card_html(c):
    face=" · ".join(f"{v[0]:.2f}" if v else "–" for v in c["face"])
    badges=[("ok" if c["single"] else "bad", "단일 샷" if c["single"] else "내부 컷"),
            ("ok" if (c["fmin"]>=0.45 and all(c["face"])) else "bad", f"얼굴 {c['fmin']:.2f}" if all(c["face"]) else "얼굴 미검출"),
            ("ok" if c["ratio"]>=0.85 else "bad", f"대사 {int(c['ratio']*100)}%" if c["ratio"]>0 else "무음")]
    b="".join(f'<span class="badge {k}">{html.escape(t)}</span>' for k,t in badges)
    v=f'<span class="verdict {"pass" if c["verdict"]=="통과" else "redo"}">{c["verdict"]}{(" · "+", ".join(c["why"])) if c["why"] else ""}</span>'
    act=f'<p class="act">{html.escape(c["act"])}</p>' if c["act"] else ""
    return f'''
<article class="cut" data-verdict="{c["verdict"]}" id="cut-{c["n"]}">
  <header><span class="num">{c["n"]:02d}</span><span class="who">{html.escape(c["who"])}</span><span class="line">{html.escape(c["line"])}</span>{v}</header>
  <div class="pair">
    <figure><img src="{c["still"]}" alt="컷 {c["n"]} 시작 스틸" loading="lazy"><figcaption>시작 스틸 · {html.escape(c["frame"])}</figcaption></figure>
    <figure><video src="{c["video"]}" controls preload="metadata" playsinline></video><figcaption>{html.escape(c["take"])} · {c["dur"]:.1f}s</figcaption></figure>
  </div>
  <div class="qa">{b}<span class="scores">얼굴 25/50/75/끝 = {face}</span></div>
  <p class="said"><span class="k">whisper</span> {html.escape(c["said"]) if c["said"] else "(음성 없음)"}</p>
  {act}
</article>'''
act1=[c for c in cards if c["n"]<=21]; act2=[c for c in cards if c["n"]>=22]
def sec(title, cs): return f'<section><h2>{title} <small>{sum(c["verdict"]=="통과" for c in cs)}/{len(cs)} 통과</small></h2>{"".join(card_html(c) for c in cs)}</section>' if cs else ""
page=f'''<title>토마톡 1화 클립 보드</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* layout: one column of cut cards; each card = header row, still|video pair, QA strip */
:root{{--bg:#f6f3ee;--card:#fffdf9;--fg:#1f1b16;--mute:#6d655b;--rule:#e2dbd0;--accent:#b8471f;--ok:#2f7a4a;--ok-bg:#e4f2e8;--bad:#a8341c;--bad-bg:#f8e3dc;
 --body:"Noto Sans KR",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#17150f;--card:#211e17;--fg:#f0eae0;--mute:#a69c8d;--rule:#352f26;--accent:#e2794c;--ok:#7fcf98;--ok-bg:#1e3326;--bad:#f09a82;--bad-bg:#3d1f17;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#17150f;--card:#211e17;--fg:#f0eae0;--mute:#a69c8d;--rule:#352f26;--accent:#e2794c;--ok:#7fcf98;--ok-bg:#1e3326;--bad:#f09a82;--bad-bg:#3d1f17;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 60px;line-height:1.5}}
main{{max-width:1040px;margin:0 auto}}
h1{{font-size:1.5rem;margin:0 0 4px;text-wrap:balance}} .sub{{color:var(--mute);margin:0 0 18px;font-size:.9rem}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}}
.filters button{{font:inherit;font-size:.85rem;padding:6px 12px;border-radius:999px;border:1px solid var(--rule);background:var(--card);color:var(--fg);cursor:pointer}}
.filters button[aria-pressed="true"]{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
.filters button:focus-visible,video:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
h2{{font-size:1.05rem;margin:26px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--rule)}} h2 small{{color:var(--mute);font-weight:400;font-size:.85rem;margin-left:8px}}
.cut{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px;margin-bottom:14px}}
.cut header{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;margin-bottom:10px}}
.num{{font-family:var(--mono);font-weight:500;color:var(--accent);font-size:1.05rem}} .who{{font-weight:700}} .line{{flex:1 1 260px;min-width:0}}
.verdict{{font-size:.8rem;padding:2px 10px;border-radius:999px;font-weight:500;white-space:nowrap}} .verdict.pass{{background:var(--ok-bg);color:var(--ok)}} .verdict.redo{{background:var(--bad-bg);color:var(--bad)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:620px}}
figure{{margin:0;min-width:0}} figure img,figure video{{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:6px;background:#000;display:block;max-width:100%}}
figcaption{{font-family:var(--mono);font-size:.72rem;color:var(--mute);margin-top:4px;overflow-wrap:anywhere}}
.qa{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin-top:10px}}
.badge{{font-size:.78rem;padding:2px 8px;border-radius:4px;font-family:var(--mono)}} .badge.ok{{background:var(--ok-bg);color:var(--ok)}} .badge.bad{{background:var(--bad-bg);color:var(--bad)}}
.scores{{font-family:var(--mono);font-size:.78rem;color:var(--mute);font-variant-numeric:tabular-nums}}
.said{{margin:8px 0 0;font-size:.9rem}} .said .k{{font-family:var(--mono);font-size:.72rem;color:var(--mute);margin-right:6px}}
.act{{margin:4px 0 0;font-size:.82rem;color:var(--mute)}}
@media (max-width:480px){{.pair{{gap:8px}} .cut{{padding:10px}}}}
@media (prefers-reduced-motion:no-preference){{.filters button{{transition:background .15s}}}}
</style>
<main>
<h1>토마톡 1화 Kling 대사 클립</h1>
<p class="sub">{stamp} 기준 · {len(cards)}컷 중 {n_pass}컷 통과 · 왼쪽 시작 스틸, 오른쪽 최신 테이크. 기준: 단일 샷 · 얼굴 동일성 ≥0.45(4지점) · whisper 대사 일치 ≥85%</p>
<div class="filters" role="group" aria-label="필터">
 <button type="button" data-f="all" aria-pressed="true" id="f-all">전체 {len(cards)}</button>
 <button type="button" data-f="통과" aria-pressed="false" id="f-pass">통과 {n_pass}</button>
 <button type="button" data-f="재생성" aria-pressed="false" id="f-redo">재생성 {len(cards)-n_pass}</button>
</div>
{sec("1막 · 소파 / 아일랜드", act1)}
{sec("2막 · 아일랜드", act2)}
</main>
<script>
const bs=[...document.querySelectorAll('.filters button')];
function apply(f){{document.querySelectorAll('.cut').forEach(c=>{{c.hidden=(f!=='all'&&c.dataset.verdict!==f)}});bs.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.f===f)));try{{localStorage.setItem('clipFilter',f)}}catch(e){{}}}}
bs.forEach(b=>b.addEventListener('click',()=>apply(b.dataset.f)));
let f='all';try{{f=localStorage.getItem('clipFilter')||'all'}}catch(e){{}} if(!bs.some(b=>b.dataset.f===f))f='all'; apply(f);
document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{{if(o!==v)o.pause()}})));
</script>'''
open(f"{OUT}/index.html","w").write(page)
print(f"{len(cards)} cards, {n_pass} pass →", f"{OUT}/index.html"); print(" ".join(f"{c['n']}:{c['verdict']}" for c in cards))
