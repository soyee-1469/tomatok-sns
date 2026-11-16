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
    dict(id='EP01', title='읽음 22', stage='완성 후보본 v121 검토', next='v094 전체 시청 판정 · 보류 컷 4·8·10·26 재시도 · 99_FINAL 파일명 확정', script='EP01_SCRIPT_FINAL_v07.md', boards='EP01_island_[0-9]*.png', finals=[('완성 후보 v121 (45 색 보정)','01_EPISODES/EP01R/export/EP01R_FINAL_20261116_v121.mp4'),('컷만 v121 (효과 없음)','01_EPISODES/EP01R/edit/EP01R_PICTURE_LOCK_v121.mp4'),('이전 후보 v120','01_EPISODES/EP01R/export/EP01R_FINAL_20261116_v120.mp4')]),
    dict(id='EP02', title='싸움은 모국어로', stage='컷별 비교 보드', next='시트2 칸14~16 콘티 재생성(그록봇) · 24·30 상자 동작 권장 · 기준 이미지 일부 연결', script='EP02_SCRIPT_v08.md', boards='EP02_v01_[0-9]*.png', boards_dir='01_EPISODES/EP02_싸움은모국어로/STORYBOARD'),
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

    def wire_finals(ep: dict) -> None:
        """완성 후보본 등 최종 영상 파일을 board_web에 링크해 재생 가능하게 (2026-11-16)."""
        vid_dir = OUT / 'series_cuts' / 'vid'; vid_dir.mkdir(parents=True, exist_ok=True)
        out = []
        for label, rel in ep.get('finals', []) or []:
            src = ROOT / rel
            if not src.exists():
                continue
            link = vid_dir / ('final_' + src.name)
            if link.exists() or link.is_symlink():
                link.unlink()
            try:
                link.symlink_to(src); out.append({'label': label, 'src': 'series_cuts/vid/' + link.name, 'path': rel})
            except OSError:
                pass
        ep['finals'] = out

    def build_timeline(ep: dict) -> None:
        """최신 조립본의 실제 순서·시각 표 (애니매틱 JSON 기준, skip 제외). 2026-11-16 사용자: 보드와 합친 영상이 달라서 말하기 어렵다."""
        if ep.get('id') != 'EP01':
            return
        src = ROOT / '01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json'
        if not src.exists():
            return
        rows = [c for c in json.loads(src.read_text(encoding='utf-8')) if not c.get('skip')]
        t = 0.0; out = []
        for i, c in enumerate(rows, start=1):
            d = float(c.get('dur') or 0); clip = c.get('clip') or c.get('src') or ''
            out.append({'idx': i, 'n': str(c.get('n')), 'start': t, 'mmss': f"{int(t//60)}:{int(t%60):02d}", 'dur': round(d, 2), 'who': c.get('who') or '', 'line': (c.get('line') or '')[:40], 'file': Path(clip).name, 'kind': 'video' if clip.endswith('.mp4') else 'still'})
            t += d
        ep['timeline'] = out; ep['timeline_total'] = round(t, 1)

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
                # 선택 클립이 takes 목록 밖(예: _trim 편집본)이어도 재생되게 링크 (2026-11-16)
                if not ((vid_dir / name).exists() or (vid_dir / name).is_symlink()) and (ROOT / sel).exists():
                    try:
                        (vid_dir / name).symlink_to(ROOT / sel)
                    except OSError:
                        pass
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
        wire_finals(item)
        build_timeline(item)
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
        lastCompleted='작업 33 DONE · 32 후속: 17 해제 · 24·30 recommend',
        nextTask='그록봇 시트2 14~16 재생성 · 24·30 상자 동작 · 작업 24 보강/30 · EP01 컷30 사용자 확정',
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
