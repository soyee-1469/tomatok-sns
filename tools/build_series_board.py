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
    dict(id='EP02', title='싸움은 모국어로', stage='새 콘티 4장 검토', next='시트2 칸 14~17 USB 장면 콘티 재생성 대기(그록봇)', script='EP02_SCRIPT_v08.md', boards='EP02_v01_chatgpt_board_[0-9]*.png', boards_dir='01_EPISODES/EP02_싸움은모국어로/STORYBOARD'),
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


# 3×4. 2화 소파 분할(시트당 12칸)과 blocking_rule 과 같다. 배지 대상 칸 번호는 여기 두지 않는다.
PANELS_PER_SHEET = 12


def ep02_sheet_names(directory, pattern):
    prefix = pattern.split('[', 1)[0]
    found = {}
    if directory.is_dir():
        for path in directory.glob(pattern):
            name = path.name
            if not name.startswith(prefix) or not name.endswith('.png'):
                continue
            middle = name[len(prefix):-4]
            if middle.isdigit():
                found[int(middle)] = name
    return prefix, found


def ep02_panels(media):
    """시트 파일은 ep02_storyboard_status.json 의 pattern·count. 배지는 ep02_conti_flags.json."""
    status = json.loads((ROOT / 'tools/ep02_storyboard_status.json').read_text(encoding='utf-8'))
    assets = status['assets']
    directory = ROOT / assets['directory']
    prefix, found = ep02_sheet_names(directory, assets['pattern'])
    count = int(assets['count'])
    flags = json.loads((ROOT / 'tools/ep02_conti_flags.json').read_text(encoding='utf-8'))
    panels = []
    for sheet_no in range(1, count + 1):
        file_name = found.get(sheet_no) or ('%s%02d.png' % (prefix, sheet_no))
        preview = media / (Path(file_name).stem + '.jpg')
        src = ('series_img/' + preview.name) if preview.is_file() else None
        for pos in range(PANELS_PER_SHEET):
            number = (sheet_no - 1) * PANELS_PER_SHEET + pos + 1
            flag = flags.get(str(number))
            panels.append(dict(
                n=number,
                sheet=sheet_no,
                file=file_name,
                src=src,
                flag=flag if isinstance(flag, dict) else None,
            ))
    stale = [panel['n'] for panel in panels if panel['flag'] and panel['flag'].get('status') == 'stale']
    print('ep02 panels', len(panels), 'stale', stale)
    return panels


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
        if ep['id'] == 'EP02':
            item['panels'] = ep02_panels(media)
        ui = ep.get('ui')
        item['ui'] = ui if ui and (OUT / ui).exists() else None
        episodes.append(item)
    template = (ROOT / 'tools/series_board.html').read_text(encoding='utf-8')
    data = json.dumps(episodes, ensure_ascii=False).replace('<', '\\u003c')
    (OUT / 'series.html').write_text(template.replace('__EPISODES__', data), encoding='utf-8')
    status = dict(id='SERIES_BOARD', type='SITCOM', title='연남동 3층집 회차 작업실', status='REVIEW',
                  lastCompleted='1화 컷 보드 감사 배지 유지 · 2화 시트2 칸 14~17 구 각본 배지',
                  nextTask='1화·2화 보드 발행은 Claude',
                  publishDate=None, platforms=['Local'], updatedBy='Codex',
                  updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  assets={'page': 'board_web/series.html', 'ep03_chat': 'board_web/ep03_chat/index.html', 'generator': 'tools/build_series_board.py'},
                  videoGenerationAuthorized=False)
    (ROOT / 'tools/series_board_status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(OUT / 'series.html')


if __name__ == '__main__':
    build()
