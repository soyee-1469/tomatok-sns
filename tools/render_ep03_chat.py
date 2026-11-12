#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3화 「연남동 3층집」 단톡 UI 초안을 board_web/ep03_chat/ 에 만든다.
사용: python3 tools/render_ep03_chat.py
생성 API·페이스스왑 호출 없음. 기존 CAST 아바타만 복사."""
import json
import shutil
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "ep03_chat_data.json"
TMPL = ROOT / "tools" / "ep03_chat_preview.html"
PROF = ROOT / "00_MASTER_ASSETS" / "04_UI" / "PROFILES" / "CAST"
OUT = ROOT / "board_web" / "ep03_chat"
AV_OUT = OUT / "avatars"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--screens', action='store_true', help='기존 공용 폰 셸로 6상태 PNG와 목업 렌더')
    args = parser.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    data['exports'] = [dict(id=state['id'], screen='screens/' + state['id'] + '.png',
                            mockup='screens/' + state['id'] + '_MOCKUP.png')
                       for state in data['states']
                       if (OUT / 'screens' / (state['id'] + '_MOCKUP.png')).is_file()
                       and (OUT / 'screens' / (state['id'] + '.png')).is_file()]
    OUT.mkdir(parents=True, exist_ok=True)
    AV_OUT.mkdir(parents=True, exist_ok=True)

    missing = []
    for p in data["profiles"]:
        src = PROF / p["av"]
        if not src.exists():
            missing.append(str(src))
            continue
        shutil.copy2(src, AV_OUT / p["av"])

    # 상태·인물 교차 검사
    ids = {p["id"] for p in data["profiles"]}
    bad_who = []
    for st in data["states"]:
        for m in st["messages"]:
            if m.get("type") == "notice":
                continue
            if m.get("who") not in ids:
                bad_who.append(f"{st['id']}:{m.get('who')}")

    html = TMPL.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    html = html.replace("__DATA__", payload)
    (OUT / "index.html").write_text(html, encoding="utf-8-sig")
    shutil.copy2(DATA, OUT / "ep03_chat_data.json")

    print("out", OUT / "index.html")
    print("states", len(data["states"]))
    print("profiles", len(data["profiles"]))
    print("avatars_copied", len(list(AV_OUT.glob("*_AV.png"))))
    if missing:
        print("MISSING_AVATARS")
        for m in missing:
            print(" ", m)
        raise SystemExit(2)
    if bad_who:
        print("BAD_WHO", bad_who)
        raise SystemExit(3)
    # 공지 + 프로필에 순덕. 제외 대사(브리프) 없는지.
    banned = ("기다릴게요", "오는 길에 뛰지 마라", "다음에 하오 없는 날", "나 이제 안 빠져요", "할머니 다음에도 오세요")
    found_banned = [
        f"{st['id']}:{m.get('ko')}"
        for st in data["states"]
        for m in st["messages"]
        if any(b in (m.get("ko") or "") for b in banned)
    ]
    grandma_profile = any(p["id"] == "sundeok" for p in data["profiles"])
    notice_ok = bool(data.get("notice")) and "순덕" in data["notice"]
    print("notice_ok", notice_ok, "grandma_profile", grandma_profile)
    if found_banned:
        print("BANNED_LINES", found_banned)
        raise SystemExit(4)
    if not notice_ok or not grandma_profile:
        raise SystemExit(5)
    # S6는 수만 「나 오늘 오길 잘했네.」만 (리아 채팅 제외)
    s6 = next(s for s in data["states"] if s["id"] == "S6")
    if not (len(s6["messages"]) == 1 and s6["messages"][0].get("who") == "suman" and "오길 잘했네" in s6["messages"][0].get("ko", "")):
        print("BAD_S6", s6["messages"])
        raise SystemExit(6)
    print("OK")
    if args.screens:
        chrome = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        mockup = ROOT / '00_MASTER_ASSETS/04_UI/MOCKUP/phone_mockup.py'
        screens = OUT / 'screens'
        screens.mkdir(exist_ok=True)
        for index, state in enumerate(data['states'], 1):
            screen = screens / (state['id'] + '.png')
            url = (OUT / 'index.html').as_uri() + '?export=1&state=' + str(index)
            subprocess.run([str(chrome), '--headless=new', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', '--window-size=830,1800',
                            '--virtual-time-budget=1500', '--screenshot=' + str(screen), url],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([sys.executable, str(mockup), str(screen),
                            str(screens / (state['id'] + '_MOCKUP.png'))], check=True)
        print('SCREENS', len(data['states']), 'MOCKUPS', len(data['states']))


if __name__ == "__main__":
    main()
