#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    dict(id='EP02', title='싸움은 모국어로', stage='새 콘티 4장 검토', next='새 콘티 확인 · 시트 2의 영수증 장면을 USB 각본과 대조', script='EP02_SCRIPT_v08.md', boards='EP02_v01_chatgpt_board_[0-9]*.png', boards_dir='01_EPISODES/EP02_싸움은모국어로/STORYBOARD'),
    dict(id='EP03', title='오늘 못 와?', stage='각본·단톡 UI 초안', next='단톡 UI 검수 · 콘티 준비', script='EP03_SCRIPT_v03.md', boards=None, ui='ep03_chat/index.html'),
    dict(id='EP04', title='조금만 주세요', stage='각본 초안', next='할머니·수만 음식 교류 각본 검토 · 번역 장면과 콘티 준비', script='EP04_SCRIPT_v02.md', boards=None),
]


def jpeg_preview(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which('sips'):
        subprocess.run(['sips', '-Z', '1400', '-s', 'format', 'jpeg', str(src), '--out', str(dest)], check=True, capture_output=True)
        return
    from PIL import Image
    image = Image.open(src).convert('RGB')
    image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
    image.save(dest, 'JPEG', quality=80)


def load_ep01_cuts():
    script = ROOT / 'tools' / 'series_cut_assets.py'
    subprocess.run([sys.executable, str(script)], check=True)
    return json.loads((ROOT / 'tools' / 'ep01_cut_asset_map.json').read_text(encoding='utf-8'))


def build():
    OUT.mkdir(exist_ok=True)
    media = OUT / 'series_img'
    media.mkdir(exist_ok=True)
    sources = OUT / 'series_sources'
    sources.mkdir(exist_ok=True)
    ep03_ui = ROOT / 'tools' / 'render_ep03_chat.py'
    if ep03_ui.exists():
        proc = subprocess.run([sys.executable, str(ep03_ui)])
        if proc.returncode not in (0, 2):
            raise SystemExit(proc.returncode)
        if proc.returncode == 2:
            print('ep03 avatars missing; series board continues')
    ep01_cuts = load_ep01_cuts()
    episodes = []
    for ep in EPISODES:
        item = dict(ep)
        src = WORLD / ep['script']
        shutil.copy2(src, sources / src.name)
        item['body'] = markdown.markdown(src.read_text(encoding='utf-8'), extensions=['tables', 'fenced_code'])
        item['images'] = []
        board_dir = ROOT / ep['boards_dir'] if ep.get('boards_dir') else SB
        for image in sorted(board_dir.glob(ep['boards'])) if ep['boards'] else []:
            target = media / (image.stem + '.jpg')
            if not target.exists() or target.stat().st_mtime < image.stat().st_mtime:
                jpeg_preview(image, target)
            item['images'].append(dict(src='series_img/' + target.name, name=image.stem))
        if ep['id'] == 'EP01':
            item['cuts'] = ep01_cuts['cuts']
            item['cutStats'] = ep01_cuts['stats']
        ui = ep.get('ui')
        item['ui'] = ui if ui and (OUT / ui).exists() else None
        episodes.append(item)
    template = (ROOT / 'tools/series_board.html').read_text(encoding='utf-8')
    data = json.dumps(episodes, ensure_ascii=False).replace('<', '\\u003c')
    (OUT / 'series.html').write_text(template.replace('__EPISODES__', data), encoding='utf-8')
    status = dict(id='SERIES_BOARD', type='SITCOM', title='연남동 3층집 회차 작업실', status='REVIEW',
                  lastCompleted='1화 컷 보드에 각본·콘티 감사 연결·상태 배지 반영',
                  nextTask='1화 컷 보드 발행은 Claude · 3화 단톡 UI 검수',
                  publishDate=None, platforms=['Local'], updatedBy='Codex',
                  updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  assets={'page': 'board_web/series.html', 'ep03_chat': 'board_web/ep03_chat/index.html', 'generator': 'tools/build_series_board.py'},
                  videoGenerationAuthorized=False)
    (ROOT / 'tools/series_board_status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(OUT / 'series.html')


if __name__ == '__main__':
    build()
