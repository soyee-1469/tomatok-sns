#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the local series workspace: python3 tools/build_series_board.py."""
import datetime
import html
import json
from pathlib import Path
import shutil
import subprocess

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'board_web'
WORLD = ROOT / '00_MASTER_ASSETS/WORLD_PLANNING'
SB = ROOT / '01_EPISODES/EP01R/frames/v08/STORYBOARD'
EPISODES = [
    dict(id='EP01', title='읽음 22', stage='기존 제작본 재검토', next='각본·콘티와 기존 영상의 최종 일치 확인', script='EP01_SCRIPT_FINAL_v07.md', boards='EP01_island_[0-9]*.png'),
    dict(id='EP02', title='싸움은 모국어로', stage='각본·콘티 검토', next='기존 콘티를 검토하고 GPT 기준 이미지 준비', script='EP02_SCRIPT_v08.md', boards='EP02_sofa_board_[0-9]*.png'),
    dict(id='EP03', title='오늘 못 와?', stage='새 각본 초안', next='공동 저녁 각본 검토 · 단톡방 UI 초안 검수', script='EP03_SCRIPT_v03.md', boards=None),
]


def build():
    OUT.mkdir(exist_ok=True)
    media = OUT / 'series_img'
    media.mkdir(exist_ok=True)
    sources = OUT / 'series_sources'
    sources.mkdir(exist_ok=True)
    episodes = []
    for ep in EPISODES:
        item = dict(ep)
        src = WORLD / ep['script']
        shutil.copy2(src, sources / src.name)
        item['body'] = markdown.markdown(src.read_text(), extensions=['tables', 'fenced_code'])
        item['images'] = []
        for image in sorted(SB.glob(ep['boards'])) if ep['boards'] else []:
            target = media / (image.stem + '.jpg')
            if not target.exists() or target.stat().st_mtime < image.stat().st_mtime:
                subprocess.run(['sips', '-Z', '1400', '-s', 'format', 'jpeg', str(image), '--out', str(target)], check=True, capture_output=True)
            item['images'].append(dict(src='series_img/' + target.name, name=image.stem))
        item['chat_preview'] = None
        if ep['id'] == 'EP03':
            preview = ROOT / 'tools/ep03_chat_preview.html'
            chat_dir = OUT / 'ep03_chat'
            chat_dir.mkdir(parents=True, exist_ok=True)
            if preview.is_file():
                shutil.copy2(preview, chat_dir / 'index.html')
                item['chat_preview'] = 'ep03_chat/index.html'
        episodes.append(item)
    template = (ROOT / 'tools/series_board.html').read_text()
    data = json.dumps(episodes, ensure_ascii=False).replace('<', '\\u003c')
    (OUT / 'series.html').write_text(template.replace('__EPISODES__', data))
    status = dict(id='SERIES_BOARD', type='SITCOM', title='연남동 3층집 회차 작업실', status='REVIEW',
                  lastCompleted='3화 단톡방 UI 초안 6상태를 회차 작업실에 연결',
                  nextTask='3화 단톡 원문 검수와 각본 사용자 검토',
                  publishDate=None, platforms=['Local'], updatedBy='Codex',
                  updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  assets={'page': 'board_web/series.html', 'ep03_chat': 'board_web/ep03_chat/index.html', 'generator': 'tools/build_series_board.py'},
                  videoGenerationAuthorized=False)
    (ROOT / 'tools/series_board_status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n')
    print(OUT / 'series.html')


if __name__ == '__main__':
    build()
