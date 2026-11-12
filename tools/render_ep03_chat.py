# -*- coding: utf-8 -*-
"""3화 단톡 미리보기 HTML을 데이터에서 만든다. 생성 API와 폰 외곽 디자인은 하지 않는다."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "tools" / "ep03_chat_data.json"
PREVIEW_PATH = ROOT / "tools" / "ep03_chat_preview.html"
BOARD_PREVIEW = ROOT / "board_web" / "ep03_chat" / "index.html"
AVATAR_DIR = ROOT / "00_MASTER_ASSETS" / "04_UI" / "PROFILES" / "CAST"
MOCKUP = ROOT / "00_MASTER_ASSETS" / "04_UI" / "MOCKUP" / "phone_mockup.py"

STATE_TITLES = [
    "공지·참석",
    "메뉴 거절",
    "수만 불참 가능·소고기 합의",
    "참석 번복·김밥",
    "수만 도착·「내가 온다고 해서?」",
    "소고기 식사·수만의 메시지",
]
MENU_ORDER = [
    "그럼 치킨?",
    "튀긴 거 말고.",
    "닭은 오늘 내키지 않소.",
    "피자는?",
    "점심에 빵 먹었어.",
    "저녁은 밥이 좋겠소.",
    "그럼 먹고 싶은 걸 하나씩 써 주세요.",
    "둘이 정해. 나는 진짜 아무거나 괜찮아.",
]
AVATARS = {
    "ria": "BEA_AV.png",
    "junho": "JUNHO_AV.png",
    "hao": "DOYUN_AV.png",
    "miyu": "MIYU_AV.png",
    "suman": "SUMAN_AV.png",
    "sunduk": "BOKRYE_AV.png",
    "hayoung": "SONNYEO_AV.png",
    "siwoo": "DAEHAK_AV.png",
}
ALLOWED_PHOTOS = {"chicken", "pizza"}

TEMPLATE = r"""<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>3화 단톡 · 연남동 3층집</title>
<style>
:root{color-scheme:light;--bg:#e7e2dc;--chat:#f2eeeb;--ink:#241f1c;--muted:#8d8580;--line:#e3ddd8;--pink:#f9dcdc;--white:#fff;--gray:#e7e1dc;--grayink:#5e5854}
*{box-sizing:border-box}
html,body{margin:0;overflow-x:hidden;background:var(--bg);color:var(--ink)}
body{font:15px/1.45 "Noto Sans Devanagari","Droid Sans Fallback","WenQuanYi Micro Hei","Apple SD Gothic Neo",sans-serif}
button,a{font:inherit;touch-action:manipulation}
button{cursor:pointer}
button:focus-visible,a:focus-visible{outline:3px solid #b58a30;outline-offset:2px}
.page{width:100%;max-width:390px;margin:0 auto;padding:12px 12px 28px}
.top{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
.top h1{flex:1 1 180px;min-width:0;margin:0;font-size:18px;line-height:1.35;overflow-wrap:anywhere}
.top p{flex:1 1 100%;margin:0;color:#5c564f;font-size:13px;overflow-wrap:anywhere}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
.controls button{border:1px solid #d5cfc8;background:#fff;border-radius:999px;padding:10px 14px;min-height:44px}
.controls button[aria-pressed=true]{background:#285b45;color:#fff;border-color:#285b45}
.controls button:disabled{opacity:.4;cursor:default}
.state-name{flex:1 1 140px;min-width:0;margin:0;font-size:14px;overflow-wrap:anywhere}
.phone{width:100%;max-width:390px;height:min(720px,calc(100vh - 168px));min-height:520px;background:var(--chat);border:1px solid #ddd6d0;border-radius:16px;display:flex;flex-direction:column;overflow:hidden}
.bar{display:flex;align-items:center;gap:8px;background:#fff;min-height:52px;padding:8px 10px;border-bottom:1px solid var(--line)}
.bar h2{flex:1;min-width:0;margin:0;text-align:center;font-size:16px;font-weight:700;overflow-wrap:anywhere}
.icon{width:36px;height:36px;border:0;background:transparent;color:#3c3835;font-size:22px;flex:0 0 auto}
.notice{margin:10px;background:#fff8e8;border:1px solid #ead9a8;border-radius:12px;padding:10px 12px}
.notice b{display:block;font-size:12px;letter-spacing:.04em}
.notice p{margin:4px 0;overflow-wrap:anywhere}
.notice small{color:#6d6248}
.log{flex:1;overflow:auto;padding:4px 10px 12px}
.msg{display:flex;gap:8px;align-items:flex-start;margin:10px 0;max-width:100%}
.msg.mine{flex-direction:row-reverse}
.av,.fallback{width:36px;height:36px;border-radius:50%;flex:0 0 auto;object-fit:cover;background:#d9d3cc}
.fallback{display:flex;align-items:center;justify-content:center;font-weight:700}
.stack{min-width:0;max-width:calc(100% - 44px);display:flex;flex-direction:column;align-items:flex-start;gap:4px}
.msg.mine .stack{align-items:flex-end}
.who{font-size:12px;color:#3f3a36}
.bubble{max-width:100%;border-radius:14px;padding:8px 10px;overflow-wrap:anywhere;word-break:break-word}
.bubble.ko{background:var(--white)}
.bubble.original{background:var(--gray);color:var(--grayink)}
.bubble.mine{background:var(--pink)}
.food{display:block;width:min(180px,100%);height:auto;border-radius:8px;margin-bottom:6px}
.draft{display:inline-block;margin-left:6px;font-size:10px;letter-spacing:.02em;color:#8a8178;border:1px solid #d9d1ca;border-radius:999px;padding:0 5px;vertical-align:1px}
.timed{display:flex;align-items:flex-end;gap:6px;max-width:100%}
time{color:var(--muted);font-size:11px;flex:0 0 auto}
.composer{display:flex;align-items:center;gap:6px;background:#fff;border-top:1px solid var(--line);padding:8px;min-height:52px}
.composer span{flex:1;min-width:0;color:#9a938e;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.aside{margin:10px 0 0;color:#5c564f;font-size:13px;overflow-wrap:anywhere}
.profile{display:flex;gap:10px;background:#fff;border-radius:12px;padding:10px;margin:8px 0}
.profile h3{margin:0 0 4px;font-size:15px}
.profile p{margin:2px 0;font-size:13px;overflow-wrap:anywhere}
.tag{color:#6d6248}
[hidden]{display:none!important}
</style>
<main class="page">
  <div class="top">
    <h1>3화 단톡 미리보기</h1>
    <p>준호 폰 한국어 뷰. 준호 본인만 연분홍이고, 이 여섯 상태에는 준호가 보낸 문자가 없다. 외국어 원문은 검수 전 초안이다.</p>
  </div>
  <div class="controls">
    <button type="button" id="prev" data-action="prev">이전</button>
    <p class="state-name" id="state-name"></p>
    <button type="button" id="next" data-action="next">다음</button>
    <button type="button" id="view-chat" data-action="chat" aria-pressed="true">대화</button>
    <button type="button" id="view-people" data-action="profiles" aria-pressed="false">프로필</button>
  </div>
  <section class="phone" id="phone" data-viewer="junho">
    <div class="bar">
      <button type="button" class="icon" aria-label="뒤로" tabindex="-1">‹</button>
      <h2 id="room"></h2>
      <button type="button" class="icon" aria-label="검색" tabindex="-1">⌕</button>
      <button type="button" class="icon" aria-label="메뉴" tabindex="-1">☰</button>
    </div>
    <div class="notice" id="notice" data-notice="1"></div>
    <div class="log" id="log"></div>
    <div class="composer" aria-hidden="true"><span>메시지를 입력하세요.</span><span>☺</span></div>
  </section>
  <p class="aside" id="aside"></p>
</main>
<script type="application/json" id="chat-data">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('chat-data').textContent);
let index = 0;
let view = 'chat';
const people = Object.fromEntries(DATA.profiles.map(p => [p.id, p]));

function avatarSrc(file){
  const path = location.pathname.replace(/\\/g, '/');
  const base = path.indexOf('/board_web/ep03_chat/') !== -1
    ? '../../00_MASTER_ASSETS/04_UI/PROFILES/CAST/'
    : '../00_MASTER_ASSETS/04_UI/PROFILES/CAST/';
  return base + file;
}
function esc(s){
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function photo(kind){
  if(kind === 'chicken'){
    return '<svg class="food" viewBox="0 0 160 100" role="img" aria-label="치킨 메뉴 사진 자리"><rect width="160" height="100" rx="10" fill="#f4e2c4"/><ellipse cx="78" cy="62" rx="30" ry="16" fill="#e0a15a"/><rect x="98" y="42" width="12" height="30" rx="5" transform="rotate(28 104 57)" fill="#c9843a"/><text x="12" y="24" font-size="14" fill="#6a4a2a">치킨 사진 자리</text></svg>';
  }
  if(kind === 'pizza'){
    return '<svg class="food" viewBox="0 0 160 100" role="img" aria-label="피자 메뉴 사진 자리"><rect width="160" height="100" rx="10" fill="#f7efe4"/><circle cx="82" cy="62" r="28" fill="#f0c14a"/><circle cx="72" cy="54" r="4" fill="#c14b3a"/><circle cx="92" cy="66" r="4" fill="#c14b3a"/><circle cx="80" cy="74" r="3" fill="#6a8f4e"/><text x="12" y="24" font-size="14" fill="#6a4a2a">피자 사진 자리</text></svg>';
  }
  return '';
}
function avatar(person){
  const alt = esc(person.name);
  return '<img class="av" alt="'+alt+'" src="'+esc(avatarSrc(person.avatar))+'" data-file="'+esc(person.avatar)+'">';
}
function message(msg){
  const person = people[msg.speaker];
  const mine = msg.speaker === DATA.viewer;
  const foreign = person.lang !== DATA.viewer_lang;
  const shot = msg.photo ? photo(msg.photo) : '';
  const ko = '<div class="bubble ko'+(mine?' mine':'')+'" data-kind="ko">'+shot+esc(msg.ko)+'</div>';
  let body = ko;
  if(foreign){
    body += '<div class="timed"><div class="bubble original" data-kind="original" lang="'+esc(person.lang)+'">'+esc(msg.original)+' <span class="draft">초안</span></div><time>'+esc(msg.time)+'</time></div>';
  }else{
    body = '<div class="timed">'+ko+'<time>'+esc(msg.time)+'</time></div>';
  }
  return '<article class="msg'+(mine?' mine':'')+'" data-speaker="'+esc(msg.speaker)+'" data-mine="'+(mine?'1':'0')+'"><div class="av-slot">'+avatar(person)+'</div><div class="stack"><div class="who">'+esc(person.name)+' '+person.flag+'</div>'+body+'</div></article>';
}
function profiles(){
  return DATA.profiles.map(person => {
    return '<article class="profile" data-profile="'+esc(person.id)+'">'+avatar(person)+'<div><h3>'+esc(person.name)+' '+person.flag+'</h3><p class="tag">'+esc(person.avatar_label)+' · '+esc(person.avatar)+' · <span class="av-state">확인 중</span></p><p><b>최종 프로필 연출 제안</b> '+esc(person.proposal)+'</p><p class="tag">사용자 확정 전</p></div></article>';
  }).join('');
}
function bindAvatars(root){
  root.querySelectorAll('img.av').forEach(img => {
    const mark = () => {
      const state = img.closest('.profile') && img.closest('.profile').querySelector('.av-state');
      if(img.naturalWidth > 0){
        if(state) state.textContent = '파일 있음';
        return;
      }
      const fallback = document.createElement('span');
      fallback.className = 'fallback';
      fallback.textContent = (img.alt || '?').slice(0, 1);
      img.replaceWith(fallback);
      if(state) state.textContent = '파일 없음';
    };
    if(img.complete) mark();
    else{
      img.addEventListener('load', mark);
      img.addEventListener('error', mark);
    }
  });
}
function render(){
  const state = DATA.states[index];
  document.getElementById('room').textContent = DATA.room;
  document.getElementById('state-name').textContent = (index + 1) + ' / ' + DATA.states.length + ' ' + state.title;
  document.getElementById('prev').disabled = index === 0;
  document.getElementById('next').disabled = index === DATA.states.length - 1;
  document.getElementById('view-chat').setAttribute('aria-pressed', view === 'chat' ? 'true' : 'false');
  document.getElementById('view-people').setAttribute('aria-pressed', view === 'people' ? 'true' : 'false');
  const notice = DATA.notice;
  const author = people[notice.author];
  document.getElementById('notice').innerHTML = '<b>공지</b><p>'+esc(notice.text)+'</p><small>— '+esc(notice.sign)+' '+author.flag+'</small>';
  document.getElementById('notice').setAttribute('data-author', notice.author);
  const log = document.getElementById('log');
  log.innerHTML = view === 'people' ? profiles() : state.messages.map(message).join('');
  document.getElementById('aside').textContent = state.aside;
  bindAvatars(log);
  if(view === 'chat') log.scrollTop = log.scrollHeight;
}
document.getElementById('prev').addEventListener('click', () => { if(index > 0){ index -= 1; view = 'chat'; render(); }});
document.getElementById('next').addEventListener('click', () => { if(index < DATA.states.length - 1){ index += 1; view = 'chat'; render(); }});
document.getElementById('view-chat').addEventListener('click', () => { view = 'chat'; render(); });
document.getElementById('view-people').addEventListener('click', () => { view = 'people'; render(); });
window.addEventListener('keydown', event => {
  if(event.key === 'ArrowRight') document.getElementById('next').click();
  if(event.key === 'ArrowLeft') document.getElementById('prev').click();
});
render();
</script>
</html>
"""


def embed(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return (
        payload.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def validate(data: dict) -> list[str]:
    errors = []
    if data.get("viewer") != "junho" or data.get("viewer_lang") != "ko":
        errors.append("viewer must be junho / ko")
    if data.get("mine_color") != "#f9dcdc":
        errors.append("mine color must be #f9dcdc")
    if data.get("room") != "연남동 3층집 🏠":
        errors.append("room name mismatch")
    profiles = data.get("profiles") or []
    by_id = {item.get("id"): item for item in profiles}
    if list(by_id) != list(AVATARS):
        errors.append("profile id order mismatch")
    for pid, filename in AVATARS.items():
        person = by_id.get(pid) or {}
        if person.get("avatar") != filename:
            errors.append("avatar mismatch %s" % pid)
        if person.get("name") in ("비아", "도윤", "Bea"):
            errors.append("forbidden display name %s" % pid)
        if "Bea" in person.get("name", "") or "비아" in person.get("name", ""):
            errors.append("forbidden name text %s" % pid)
    if "sunduk" not in by_id:
        errors.append("grandma missing")
    notice = data.get("notice") or {}
    if notice.get("author") != "sunduk":
        errors.append("notice author must be grandma")
    if "저녁값 내기" not in notice.get("text", "") or not notice.get("text", "").startswith("화·목"):
        errors.append("notice text mismatch")
    states = data.get("states") or []
    titles = [state.get("title") for state in states]
    if titles != STATE_TITLES:
        errors.append("state order mismatch: %s" % titles)
    excluded = data.get("excluded_lines") or []
    for state in states:
        for msg in state.get("messages") or []:
            speaker = msg.get("speaker")
            person = by_id.get(speaker) or {}
            blob = " ".join([msg.get("ko") or "", msg.get("original") or "", state.get("aside") or ""])
            if "비아" in blob or "Bea" in blob or "도윤" in blob:
                errors.append("forbidden dialogue in %s" % state.get("id"))
            for line in excluded:
                if line in (msg.get("ko") or "") or line in (msg.get("original") or ""):
                    errors.append("excluded line in message %s" % state.get("id"))
            if speaker == data["viewer"]:
                if person.get("lang") != "ko":
                    errors.append("viewer lang")
            elif person.get("lang") == "ko":
                if msg.get("original"):
                    errors.append("korean incoming must not carry a second original")
            else:
                if not msg.get("original") or msg.get("original_status") != "draft":
                    errors.append("foreign original must stay a draft")
            photo = msg.get("photo")
            if photo and photo not in ALLOWED_PHOTOS:
                errors.append("photo not allowed: %s" % photo)
            if state.get("id") != "menu_no" and photo:
                errors.append("photo outside menu state")
    kos = [msg.get("ko") for msg in (states[1].get("messages") if len(states) > 1 else [])]
    pos = 0
    for needed in MENU_ORDER:
        if needed not in kos[pos:]:
            errors.append("menu order missing %s" % needed)
            break
        pos = kos.index(needed, pos) + 1
    late = " ".join(msg.get("ko") or "" for state in states[2:] for msg in state.get("messages") or [])
    if "내가 온다고 해서?" not in late or "나 오늘 오길 잘했네." not in late:
        errors.append("late lines missing")
    if "할머니, 같이 드세요." in late:
        errors.append("spoken plate line leaked into chat")
    return errors


def avatar_report() -> list[str]:
    lines = []
    missing = 0
    for filename in AVATARS.values():
        path = AVATAR_DIR / filename
        if path.is_file():
            lines.append("AVATAR %s OK" % filename)
        else:
            missing += 1
            lines.append("AVATAR %s MISSING" % path)
    lines.append("AVATAR %s present / %s expected" % (len(AVATARS) - missing, len(AVATARS)))
    if MOCKUP.is_file():
        lines.append("MOCKUP present, not called: no screen png in this run")
    else:
        lines.append("MOCKUP_ABSENT %s" % MOCKUP)
    return lines


def write_preview(data: dict) -> None:
    html = TEMPLATE.replace("__DATA__", embed(data))
    PREVIEW_PATH.write_text(html, encoding="utf-8")
    BOARD_PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    BOARD_PREVIEW.write_text(html, encoding="utf-8")


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors = validate(data)
    for line in avatar_report():
        print(line)
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    write_preview(data)
    print("STATES", len(data["states"]), "OK")
    print("PREVIEW", PREVIEW_PATH)
    print("BOARD", BOARD_PREVIEW)
    return 0


if __name__ == "__main__":
    sys.exit(main())
