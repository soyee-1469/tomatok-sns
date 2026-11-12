#!/usr/bin/env python3
"""Build the local series workspace: python3 tools/build_series_board.py."""
import datetime
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'board_web'
WORLD = ROOT / '00_MASTER_ASSETS/WORLD_PLANNING'
SB = ROOT / '01_EPISODES/EP01R/frames/v08/STORYBOARD'
EPISODES = [
    dict(id='EP01', title='읽음 22', stage='기존 제작본 재검토', next='각본·콘티와 기존 영상의 최종 일치 확인', script='EP01_SCRIPT_FINAL_v07.md', boards='EP01_island_[0-9]*.png'),
    dict(id='EP02', title='싸움은 모국어로', stage='각본·콘티 검토', next='기존 콘티를 검토하고 GPT 기준 이미지 준비', script='EP02_SCRIPT_v08.md', boards='EP02_sofa_board_[0-9]*.png'),
    dict(id='EP03', title='오늘 못 와?', stage='각본·단톡 UI 초안', next='단톡 UI 검수 · 콘티 준비', script='EP03_SCRIPT_v03.md', boards=None, ui='ep03_chat/index.html'),
]


def build():
    OUT.mkdir(exist_ok=True)
    media = OUT / 'series_img'
    media.mkdir(exist_ok=True)
    sources = OUT / 'series_sources'
    sources.mkdir(exist_ok=True)
    ep03_ui = ROOT / 'tools' / 'render_ep03_chat.py'
    if ep03_ui.exists():
        subprocess.run([sys.executable, str(ep03_ui)], check=True)
    episodes = []
    for ep in EPISODES:
        item = dict(ep)
        src = WORLD / ep['script']
        shutil.copy2(src, sources / src.name)
        item['body'] = markdown.markdown(src.read_text(encoding='utf-8'), extensions=['tables', 'fenced_code'])
        item['images'] = []
        for image in sorted(SB.glob(ep['boards'])) if ep['boards'] else []:
            target = media / (image.stem + '.jpg')
            if not target.exists() or target.stat().st_mtime < image.stat().st_mtime:
                subprocess.run(['sips', '-Z', '1400', '-s', 'format', 'jpeg', str(image), '--out', str(target)], check=True, capture_output=True)
            item['images'].append(dict(src='series_img/' + target.name, name=image.stem))
        ui = ep.get('ui')
        item['ui'] = ui if ui and (OUT / ui).exists() else None
        episodes.append(item)
    template = (ROOT / 'tools/series_board.html').read_text(encoding='utf-8')
    data = json.dumps(episodes, ensure_ascii=False).replace('<', '\\u003c')
    (OUT / 'series.html').write_text(template.replace('__EPISODES__', data), encoding='utf-8')
    status = dict(id='SERIES_BOARD', type='SITCOM', title='연남동 3층집 회차 작업실', status='REVIEW',
                  lastCompleted='보드 상단 회차 바로가기 추가 · 전체/1~3화 이동 · 현재 회차 표시 및 작업 탭 유지',
                  nextTask='3화 단톡 UI 검수 · 원문 번역 검수 · 콘티 준비',
                  publishDate=None, platforms=['Local'], updatedBy='Codex',
                  updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  assets={'page': 'board_web/series.html', 'ep03_chat': 'board_web/ep03_chat/index.html', 'generator': 'tools/build_series_board.py'},
                  videoGenerationAuthorized=False)
    (ROOT / 'tools/series_board_status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(OUT / 'series.html')


if __name__ == '__main__':
    build()
