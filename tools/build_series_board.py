#!/usr/bin/env python3
"""Build the local series workspace: python3 tools/build_series_board.py."""
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'board_web'
WORLD = ROOT / '00_MASTER_ASSETS/WORLD_PLANNING'
SB = ROOT / '01_EPISODES/EP01R/frames/v08/STORYBOARD'
EPISODES = [
    dict(id='EP01', title='읽음 22', stage='기존 제작본 재검토', next='각본·콘티와 기존 영상의 최종 일치 확인', script='EP01_SCRIPT_FINAL_v07.md', boards='EP01_island_[0-9]*.png'),
    dict(id='EP02', title='싸움은 모국어로', stage='컷별 비교 보드', next='시트2 칸14~17 콘티 스케치 재생성 대기 · 기준 이미지 일부 연결됨', script='EP02_SCRIPT_v08.md', boards='EP02_v01_[0-9]*.png', boards_dir='01_EPISODES/EP02_싸움은모국어로/STORYBOARD'),
    dict(id='EP03', title='오늘 못 와?', stage='각본·단톡 UI 초안', next='단톡 UI 검수 · 콘티 준비', script='EP03_SCRIPT_v03.md', boards=None, ui='ep03_chat/index.html'),
    dict(id='EP04', title='조금만 주세요', stage='각본 초안', next='할머니·수만 음식 교류 각본 검토 · 번역 장면과 콘티 준비', script='EP04_SCRIPT_v02.md', boards=None),
]

VER_RE = re.compile(r'_v(\d+)\.md$', re.I)


def script_version(name: str) -> str:
    m = VER_RE.search(name)
    return f'v{m.group(1)}' if m else name


def iso_from_mtime(path: Path) -> str:
    return datetime.datetime.fromtimestamp(path.stat().st_mtime, tz=datetime.timezone.utc).isoformat()


def build():
    OUT.mkdir(exist_ok=True)
    media = OUT / 'series_img'
    media.mkdir(exist_ok=True)
    sources = OUT / 'series_sources'
    sources.mkdir(exist_ok=True)
    built_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    ep03_ui = ROOT / 'tools' / 'render_ep03_chat.py'
    if ep03_ui.exists():
        subprocess.run([sys.executable, str(ep03_ui)], check=True)

    def wire_cut_videos(cut_map: dict) -> None:
        """board_web에서 재생 가능한 영상 심볼릭 링크(복사 없음)."""
        vid_dir = OUT / 'series_cuts' / 'vid'
        vid_dir.mkdir(parents=True, exist_ok=True)
        for cut in cut_map.get('cuts', []):
            for t in cut.get('video', {}).get('takes', []):
                src = ROOT / t['path']
                if not src.exists():
                    continue
                link = vid_dir / t['name']
                if link.exists() or link.is_symlink():
                    link.unlink()
                try:
                    link.symlink_to(src)
                    t['board_src'] = 'series_cuts/vid/' + t['name']
                except OSError:
                    t['board_src'] = None
            sel = cut.get('video', {}).get('selected')
            if sel:
                name = Path(sel).name
                if (vid_dir / name).exists() or (vid_dir / name).is_symlink():
                    cut['video']['board_src'] = 'series_cuts/vid/' + name
                else:
                    cut['video']['board_src'] = None
            img = cut.get('image') or {}
            if img.get('is_ui_mp4') and img.get('path'):
                src = ROOT / img['path']
                if src.exists():
                    link = vid_dir / ('ui_' + src.name)
                    if link.exists() or link.is_symlink():
                        link.unlink()
                    try:
                        link.symlink_to(src)
                        img['board_src'] = 'series_cuts/vid/' + link.name
                    except OSError:
                        img['board_src'] = None

    cut_maps = {}
    for tool_name, map_name, ep_id in (
        ('series_cut_assets.py', 'ep01_cut_asset_map.json', 'EP01'),
        ('series_cut_assets_ep02.py', 'ep02_cut_asset_map.json', 'EP02'),
    ):
        tool = ROOT / 'tools' / tool_name
        if not tool.exists():
            continue
        subprocess.run([sys.executable, str(tool)], check=True)
        map_path = ROOT / 'tools' / map_name
        if not map_path.exists():
            continue
        cmap = json.loads(map_path.read_text(encoding='utf-8'))
        wire_cut_videos(cmap)
        cut_maps[ep_id] = cmap

    # EP01 콘티: SCRIPT_CONTI_AUDIT 수동 매핑만. EP02 콘티: 현행 시트 칸(C=컷).

    episodes = []
    for ep in EPISODES:
        item = dict(ep)
        src = WORLD / ep['script']
        if not src.exists():
            raise FileNotFoundError(f'각본 없음: {src}')
        shutil.copy2(src, sources / src.name)
        item['body'] = markdown.markdown(src.read_text(encoding='utf-8'), extensions=['tables', 'fenced_code'])
        item['script_version'] = script_version(ep['script'])
        item['script_mtime'] = iso_from_mtime(src)
        item['built_at'] = built_at
        item['images'] = []
        board_dir = ROOT / ep['boards_dir'] if ep.get('boards_dir') else SB
        for image in sorted(board_dir.glob(ep['boards'])) if ep['boards'] else []:
            target = media / (image.stem + '.jpg')
            if not target.exists() or target.stat().st_mtime < image.stat().st_mtime:
                subprocess.run(
                    ['sips', '-Z', '1400', '-s', 'format', 'jpeg', str(image), '--out', str(target)],
                    check=True,
                    capture_output=True,
                )
            item['images'].append(dict(src='series_img/' + target.name, name=image.stem))
        ui = ep.get('ui')
        item['ui'] = ui if ui and (OUT / ui).exists() else None
        item['cuts'] = cut_maps.get(ep['id'])
        episodes.append(item)

    template = (ROOT / 'tools/series_board.html').read_text(encoding='utf-8')
    data = json.dumps(episodes, ensure_ascii=False).replace('<', '\\u003c')
    audit_path = ROOT / 'tools' / 'SCRIPT_CONTI_AUDIT.md'
    links_path = ROOT / 'tools' / 'ep01_conti_links.json'
    meta = json.dumps(
        {
            'built_at': built_at,
            'reviews_file': 'tools/series_board_reviews.json',
            'script_conti_audit': audit_path.exists(),
            'conti_links': 'tools/ep01_conti_links.json' if links_path.exists() else None,
            'note': '콘티는 SCRIPT_CONTI_AUDIT 수동 매핑만 반영. C번호 자동매칭 없음.',
        },
        ensure_ascii=False,
    ).replace('<', '\\u003c')
    page = template.replace('__EPISODES__', data).replace('__BOARD_META__', meta)
    (OUT / 'series.html').write_text(page, encoding='utf-8')

    ep01_stats = (cut_maps.get('EP01') or {}).get('stats') or {}
    ep02_stats = (cut_maps.get('EP02') or {}).get('stats') or {}
    status = dict(
        id='SERIES_BOARD',
        type='SITCOM',
        title='연남동 3층집 회차 작업실',
        status='REVIEW',
        lastCompleted='작업 31·32: 1화 감사 콘티 반영 · 2화 칸14~17 stale 배지',
        nextTask='그록봇 시트2 14~17 재생성 후 flags 삭제 · 작업 30(콘티 1/2화 토글) · EP01 컷30 사용자 확정',
        publishDate=None,
        platforms=['Local'],
        updatedBy='Cursor',
        updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        assets={
            'page': 'board_web/series.html',
            'reviews': 'tools/series_board_reviews.json',
            'ep01_cuts': 'tools/ep01_cut_asset_map.json',
            'ep02_cuts': 'tools/ep02_cut_asset_map.json',
            'ep01_conti_links': 'tools/ep01_conti_links.json',
            'script_conti_audit': 'tools/SCRIPT_CONTI_AUDIT.md',
            'ep03_chat': 'board_web/ep03_chat/index.html',
            'generator': 'tools/build_series_board.py',
            'server': 'tools/serve_series_board.py',
        },
        videoGenerationAuthorized=False,
        scriptContiAudit=audit_path.exists(),
        contiStats={
            'EP01': {
                'linked': ep01_stats.get('conti_linked'),
                'reference': ep01_stats.get('conti_reference'),
                'check': ep01_stats.get('conti_check'),
                'unlinked': ep01_stats.get('conti_unlinked'),
            },
            'EP02': {
                'linked': ep02_stats.get('conti_linked'),
                'with_image': ep02_stats.get('with_image'),
                'with_video': ep02_stats.get('with_video'),
            },
        },
    )
    (ROOT / 'tools/series_board_status.json').write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    print(OUT / 'series.html')
    print('built_at', built_at)


if __name__ == '__main__':
    build()
