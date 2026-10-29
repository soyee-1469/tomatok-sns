---
name: tomatok-episode
description: TOMATOK 숏폼 시트콤 에피소드 제작 절차와 도구 사용법 (Higgsfield(Kling 3.0) std 생성, whisper 대사 검사, UI 합성, 자막, BGM, 아웃트로). EP02 이후 새 에피소드를 만들거나 EP01 재편집을 이어갈 때 먼저 읽는다.
---

# TOMATOK 에피소드 제작 스킬

기준 문서: `00_MASTER_ASSETS/VIDEO_MAKING_METHOD/EP01_RETRO_2026-10-29.md` (불필요했던 것 / 도구 목록), `00_MASTER_ASSETS/05_STYLE/subtitle_and_line_rule.md` (대사 감정 표기), `01_EPISODES/EP01/video/README.md` (버전 로그).

## 철칙
1. 생성 전 비용(크레딧)을 먼저 보고하고 승인받는다. pro 모드 금지, std 720p만.
2. 대사 컷 3초, 한 컷 한 사람 한 줄. 동작은 무대사 3초로 따로. 투샷에 두 사람 대사 금지.
3. 생성 직후 `python3 01_EPISODES/EP01/tools/transcribe.py <mp4>`로 대사·언어 확인. 틀리면 그 컷만 1회 재생성.
4. 대사 줄에는 항상 (감정, 말투, 끝음↑/↓). 화면 자막은 글자만.
5. 생성 스크립트는 프롬프트 파일 존재와 핵심 문구 포함을 확인하고, 비면 중단한다.
6. 알림음은 띠링, 진동 금지, 연타 금지, Kling 클립에 음악 금지.

## 도구 (01_EPISODES/EP01 기준 경로, EP02는 복사해서 사용)
- 생성: `python3 tools/hf_gen.py <out_base> kling3_0 --prompt "$P" --duration 3 --aspect_ratio 9:16 --mode std --sound on --start-image <upload-uuid|png>` (status json에서 medias url의 uuid 재사용 가능)
- 이미지: `python3 tools/hf_gen.py <out_base> nano_banana_pro --prompt "..." --aspect_ratio 9:16 --resolution 2k --image-references <ref.png>`
- 대사 검사: `python3 tools/transcribe.py a.mp4 b.mp4`
- 점 제거: `python3 tools/remove_spot.py in.mp4 out.mp4 <x> <y> 7 22 [debug.png]`
- UI: `python3 ui/real/render_ui_v2.py C0 C2 C4 C6` → `python3 ui/real/still_anim.py <still> <ui.mp4> <out.mp4> <dur> 'quad=[[..]]' grow_side=0 corner=95 fit=stretch occl_v=120 occl_s=120 zoom=1.05` (검은 폰: white=250 ... occl=display grow_top=0.115 grow_bot=0.127)
- 조립: `python3 edit/assemble_vNN.py edit/out.mp4` (picks: 컷,파일,길이,음소거[,시작[,오디오필터[,비디오필터]]])
- 자막: `python3 tools/subtitles_pass.py edit/out.mp4.json edit/out.mp4 edit/out_subs.mp4` (LINES 표 갱신)
- 마무리 한 번에: `python3 tools/finish.py edit/assemble_vNN.py <tag> --bgm-vol 0.08 --open` (픽처락→자막→BGM 덕킹→템플릿→최종 export). BGM만 끄려면 --no-bgm, 템플릿 없이 --no-template
- 아웃트로: `python3 00_MASTER_ASSETS/08_OUTRO/render_outro.py`
- 크레딧: `higgsfield account status --json`, `account transactions --size 100 --cursor N --json`

## 최종본 보관
`99_FINAL/EPnn_제목_FINAL.mp4` 에피소드당 1개. 최종이 바뀌면 `finish.py ... --final`로 같은 이름에 덮어쓴다(이전 파일 삭제). 사용자 지침 2026-10-29.

## 매치컷
대사 컷 → 동작 컷 연결: `ffmpeg -sseof -0.05 -i line.mp4 -frames:v 1 last.png` 를 동작 컷의 start-image로. 컷 경계에서 크롭·줌 동일.
