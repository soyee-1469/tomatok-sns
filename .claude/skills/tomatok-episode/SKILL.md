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

## 시작 프레임 QA 체크리스트 11항목 (2026-11-04 사용자 지시 — 생성한 이미지는 저장 전에 반드시 아래를 눈으로 확인)
이미지 생성 결과는 **사람처럼 보이는지**보다 **말이 되는지**를 본다. 하나라도 걸리면 그 채팅은 버리고 새 채팅에서 다시 뽑는다(결과를 넣어 고치지 않는다).
1. **몸이 다 있는가** — 머리·상반신 없이 다리만, 팔 하나만, 손가락 6개, 팔다리 추가. 의도적으로 얼굴을 빼는 건 몸통 시트(A)와 세트 컷 레퍼런스(B)뿐. 에피소드 시작 프레임은 대사 컷이면 얼굴, 소품 컷이어도 사람이 나오면 최소 상반신.
2. **가구와 겹치지 않는가** — 사람이 테이블·아일랜드·소파 "안"에 서 있거나, 다리가 가구를 관통하거나, 앉았는데 의자가 없거나.
3. **시선·몸 방향 (눈동자까지)** — 얼굴 방향이 아니라 **눈동자**가 어디를 보는지 확대해서 본다. 상대를 봐야 하는 컷에서 눈이 아래·옆 허공을 보면 폐기 (2026-11-04 F5 비아 사례: 얼굴은 준호 쪽인데 눈은 아래 딴 곳 → 사용자 지적). 대화 상대가 있는 컷은 서로를 보거나 같은 대상(폰 화면)을 본다. 등을 돌리고 말하는 구도 금지. 1인 컷도 컷 리스트의 시선 방향(카메라 왼쪽=소파, 오른쪽=아일랜드)과 맞는지. 프롬프트에 `eyes locked on ...`, `pupils toward ...`처럼 눈동자 대상을 명시한다.
4. **소품 물리 + 손** — 손은 확대해서 본다: 손가락 5개, 엄지 위치, 손목이 꺾인 방향이 팔이 나온 쪽과 맞는지(뒤에서 뻗은 팔이면 손등·손목이 뒤에서 온 각도여야 함). 2026-11-04 F5 v02 사례: 비아가 뒤에서 든 폰인데 손 방향이 앞에서 쥔 것처럼 나옴 → 사용자 지적. **어느 팔인지**도 본다: 사람이 서 있는 위치에서 자연스럽게 나오는 쪽(카메라에 가까운 팔)이어야 하고, 반대팔이 가슴을 가로질러 나오면 폐기(2026-11-04 F5 v03 사례, 사용자 "반대팔로 보여줘야지"). 프롬프트에 어느 팔·어느 어깨 너머·엄지 위치·나머지 손 위치까지 쓴다. 폰 화면이 폰 뒷면에 있는지, 화면이 보이면 안 되는 컷에 화면이 켜져 있는지, 컵·병을 든 손이 반대로 잡고 있는지, 안경이 한쪽만 있는지, 사원증·가방끈이 몸을 뚫는지.
5. **얼굴 일치** — 마스터 얼굴과 나란히 놓고 눈·코·입·머리선 대조. 다르면 폐기.
6. **옷 일치** — 몸통 시트와 상의·하의·신발·소품(열쇠, 안경줄, 사원증) 대조.
7. **세트 일치** — 거실 시그니처 7개(카라멜 소파, 머스타드 암체어, 토마토 트레이, 아치창+깃발, 마블 아일랜드+검은 스툴, 오크 계단+검은 난간, 헤링본 바닥) 중 프레임에 들어온 것이 맞는지. 현관은 빈 벽+문+매트 하나.
8. **조명 일치** — 밤 장면이면 램프·줄조명 켜짐, 창 네이비, 햇빛 없음. 같은 신 안의 프레임끼리 톤이 같은지.
9. **비율** — 9:16(941×1672 또는 1080×1920), 머리 위 여백, 발이 잘리지 않았는지(전신 컷).
10. **소품 연속성** — 같은 신의 프레임끼리 소품이 같은지(담요·쿠션·컵·꽃). 체크무늬 담요처럼 매번 다르게 나오는 소품은 아예 빼거나(2026-11-04 준호 담요: F1·F2·F5 무늬 전부 달라 사용자 지적 → 담요 삭제) 색·무늬를 한 문장으로 못 박고 매 프롬프트에 똑같이 넣는다. 인물 손 위치도 컷 리스트에 고정.
11. **글자·워터마크** — 포스터·화이트보드에 생성된 가짜 글자가 눈에 띄면 폐기.
확인 결과는 컷 리스트 프레임 표에 `QA ✓` 또는 재생성 사유를 적는다. 보드에는 확인본(프레임 + 마스터 얼굴 나란히)을 같이 올린다.

## 최종본 보관
`99_FINAL/EPnn_제목_FINAL.mp4` 에피소드당 1개. 최종이 바뀌면 `finish.py ... --final`로 같은 이름에 덮어쓴다(이전 파일 삭제). 사용자 지침 2026-10-29.

## 매치컷
대사 컷 → 동작 컷 연결: `ffmpeg -sseof -0.05 -i line.mp4 -frames:v 1 last.png` 를 동작 컷의 start-image로. 컷 경계에서 크롭·줌 동일.
