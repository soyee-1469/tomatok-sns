# 커서(Cursor) 작업 지시서 — 2026-11-05

> 이 파일을 통째로 Cursor 에이전트에 붙여 넣으면 된다. 프로젝트 루트: `/Users/ymy/project/sns`

## 공통 규칙 (반드시 지킬 것)
- **건드려도 되는 파일**: `01_EPISODES/EP01R/ui/v06/render_ui_v06.py`, `01_EPISODES/EP01R/ui/v06/render_ui_v062.py`, `01_EPISODES/EP01R/edit/animatic_E1_v062.py`, `tools/build_cast_board.py`
- **읽기만 하는 파일/폴더** (절대 수정·이동·삭제 금지): `01_EPISODES/EP01R/frames/**`, `01_EPISODES/EP01R/edit/v06/*.json`, `01_EPISODES/EP01R/edit/v06/checks_state.json`, `tools/process_checks.py`, `tools/faceswap*.py`, `00_MASTER_ASSETS/**`
- Higgsfield/Kling 등 **외부 생성 API 호출 금지** (크레딧 소모). ffmpeg·Python 렌더만.
- ffmpeg 바이너리: `/Users/ymy/project/ai-creative-studio/node_modules/ffmpeg-static/ffmpeg` (ffprobe 없음 → 길이는 cv2로 프레임 수 세기)
- Python 파일 첫 줄에 `# -*- coding: utf-8 -*-` 유지. 한글 포함 스크립트를 heredoc으로 실행하지 말 것.
- 작업 끝나면 바꾼 파일과 새로 만든 mp4 경로를 목록으로 보고. git commit 하지 않는다.

## UI 렌더 파이프라인 (3개 작업 공통)
1. 렌더: `cd 01_EPISODES/EP01R && python3 ui/v06/render_ui_v06.py U05` 또는 `python3 ui/v06/render_ui_v062.py U21b U33b` → `ui/v06/EP01R_<NAME>.mp4` (830×1800, 30fps)
2. 폰 셸 합성: `tools/ui_compose.sh ui/v06/EP01R_<NAME>.mp4 edit/v06/ui/<NAME>.mp4` → 1080×1920
3. 애니매틱/본편은 `edit/v06/ui/<NAME>.mp4` 의 마지막 프레임(`_end.png`)과 mp4를 그대로 쓴다. 파일명은 바꾸지 말 것.
- `simple_video(name, chromes, lists, dur, anchor)` : `chromes=[(t, 헤더이미지)]`, `lists=[(t, 리스트이미지)]` 를 시간순으로 바꿔 끼우는 방식. 새 상태를 추가하려면 `(t, listimg(...))` 항목을 더 넣으면 된다.

## 작업 1 — E1-06 `U05_READ0` : 안읽음 숫자가 빨리 사라지는 연출 (render_ui_v06.py 69행)
현재: 21 → 14(0.9s) → 6(1.5s) → 없음(2.1s), 총 3.5s. 사용자 요청: "읽음 숫자가 **빠르게** 없어지는 것".
- 전송 직후 0.6s 동안 21 유지 → 0.6~1.4s 사이에 21,19,16,12,8,4,1,없음 순으로 **0.1s 간격**으로 녹아내리듯 줄어든 뒤 → 남은 2.0s는 숫자 없는 상태로 정지(답장 없음 연출). 총 길이 3.5s 유지.
- `L("x",n)` 헬퍼로 상태 이미지를 더 만들어 `lists` 에 추가하면 된다. 말풍선 위치·헤더는 그대로.
- 결과: `edit/v06/ui/U05_READ0.mp4` 재생성 + 마지막 프레임 PNG `edit/v06/ui/EP01R_U05_READ0_end.png` 갱신(기존 방식 그대로: cv2로 마지막 프레임 저장).

## 작업 2 — E1-29 `U21b_DM_QUESTIONS` : 채팅방 숫자가 계속 늘고 최신 메시지가 바뀜 (render_ui_v062.py `U21b`)
현재: 정지 리스트 1장을 4.0s 보여줌. 사용자 지문: "계속 채팅방의 숫자가 늘어난다. 최신 메시지도 바뀐다."
- 4.0s 동안 0.0 / 0.7 / 1.4 / 2.1 / 2.8 / 3.5s 에 리스트 상태를 6단계로 바꾼다. 각 단계마다
  - 배지 숫자 증가: 예) Mama 1→2→4→5→7→9, Chloe 2→3→6→6→8→11, Kyla 1→1→2→3→3→4, Tito Boy 1→1→1→2→2→3, Lola 0→1→2→2→3→3, Papa 0→0→1→1→1→2, Tita Cora 0→1→1→2→2→2
  - 미리보기 문구 교체(영어, 리아 폰 = EN 뷰): 단계가 진행될수록 더 급해지는 질문으로. 예) Mama: "What if I get it wrong." → "Is 'Hello son' too much?" → "Or just 'Hello'?" → "He is awake??" → "Answer me ria" / Chloe: "Can I send HAHAHAHAHA?" → "HAHAHAHA ok?" → "or 😂😂😂?" → "ria pls" …
  - 방금 메시지가 온 방이 **맨 위로 올라오게** 정렬 (실제 메신저처럼). 시간은 `et(10,15)`→`et(10,16)`… 로 1분씩.
- `FAMROW`(가족 단톡방)는 항상 맨 아래 고정, 배지 없음.
- 결과: `edit/v06/ui/U21b_DM_QUESTIONS.mp4` + `_end.png` 갱신.

## 작업 3 — E1-36 `U33b_BEA_REPLIES` : 리아 답장이 하나씩 날아감 (render_ui_v062.py `U33b`)
현재: 이미 전부 "You: OK." 로 바뀐 정지 리스트 2.5s. 사용자: 재렌더 요청.
- 시작 상태 = 작업 2의 마지막 단계(배지 꽉 찬 질문 리스트). 0.3s 간격으로 위에서부터 한 방씩 미리보기가 "You: …" 로 바뀌고 그 방의 배지가 사라진다. 순서: Mama "You: OK." → Tito Boy "You: Skip that one." → Lola "You: OK." → Kyla "You: OK." → Chloe "You: Chloe, that's always OK." → Papa "You: Reviewed. Send." → Tita Cora "You: Not yet."
- 전부 바뀐 뒤 0.4s 정지. 총 길이 2.5s → 필요하면 2.8s까지 허용.
- 결과: `edit/v06/ui/U33b_BEA_REPLIES.mp4` + `_end.png` 갱신.

## 작업 4 (선택) — 애니매틱 생성기 공용화
`01_EPISODES/EP01R/edit/animatic_E1_v062.py` 는 S 리스트가 코드에 박혀 있다. `python3 animatic_E1_v062.py <animatic_json> <out.mp4>` 로 JSON(`edit/v06/animatic_E1_v062.json`, `animatic_E2_v07.json`) 을 읽어 같은 결과를 내도록 바꾼다. row 필드: `n, frame, src, line, situation, emotion, action, dur`(없으면 2.2s). `src` 가 mp4면 그 영상을 그대로, png면 zoompan. 자막은 `tools/subtitle_style.render` 그대로. JSON 파일 자체는 수정 금지.

## 작업 5 (선택) — 보드에 밤/낮 필터
`tools/build_cast_board.py` 세트 탭(`#board` 의 "1층 공용 거실" 섹션)에 [전체 | 밤 v14e | 낮 v14d] 토글 버튼. 파일명에 `v14e_` 포함이면 밤, `v14d_` 포함이면 낮. JS만 추가, DB 코드(`anim_checks`) 는 건드리지 말 것. 수정 후 `node -e` 로 `<script>` 파싱 확인.

---
# 2차 지시서 — 2026-11-05 저녁

> 공통 규칙은 위와 같다. 추가로 `01_EPISODES/EP01R/frames/v09_fs/**` 는 폐기 폴더이니 읽지도 말 것. 페이스스왑·얼굴복원(tools/faceswap*.py, face_restore.py, face_pipeline.sh)은 **절대 호출 금지**(사용자 철칙 9).

## 작업 6 — 얼굴 QA 리포트 도구 `tools/face_qa.py` (새 파일)
목적: 생성된 스틸의 얼굴이 (1) 뭉개졌는지 (2) 마스터 얼굴과 다른 사람인지 자동으로 표를 만든다. 판정 처리 루프가 이 표를 읽는다.
- 입력: `python3 tools/face_qa.py <animatic_json> [<animatic_json> ...] --out <report.md> [--json <report.json>]`
- 메인 파이썬(3.9, `insightface` 1.0.1 + `onnxruntime` 설치됨, 모델 팩 `buffalo_l` 은 `~/.insightface/models` 에 있음). 참고 코드: `tools/faceswap_batch.py` 의 얼굴 검출·임베딩 부분만(스왑 부분은 쓰지 말 것).
- 마스터 얼굴: `00_MASTER_ASSETS/CAST_v8_six/JUNHO_face_C.png`(J), `BEA_MASTER_FACE.png`(B, 표시명 리아), `SUMAN_face.png`(S), `BOKRYE_face.png`(G, 순덕).
- 각 row의 `src`(png만, mp4는 건너뜀)에 대해: 검출된 얼굴마다 폭(px), 마스터 4명과의 코사인 유사도 중 최대값과 그 인물, 얼굴 영역 선명도(그레이 변환 후 `cv2.Laplacian(...).var()`), 그리고 판정.
- 판정 규칙: 얼굴 폭 ≥ 300이면 "클로즈업", 120~299 "미디엄", 그 외 "와이드". 선명도가 같은 구간(클로즈업/미디엄/와이드) 중앙값의 50% 미만이면 `SOFT`, 최대 유사도 < 0.35 이면 `DRIFT`, 둘 다 아니면 `OK`.
- 출력 md: 에피소드·컷 번호·프레임명·인물·폭·유사도·선명도·판정 표, 맨 위에 SOFT/DRIFT 목록 요약. json은 같은 내용 리스트.
- 같은 프레임 파일은 한 번만 계산(캐시). 실행 시간은 56장 기준 2분 이내.

## 작업 7 — 애니매틱 JSON 린트 `tools/lint_animatic.py` (새 파일)
- 입력: `python3 tools/lint_animatic.py 01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json 01_EPISODES/EP01R/edit/v06/animatic_E2_v07.json`
- 검사: (a) `src` 파일 존재 여부 (b) `line`/`situation`/`emotion`/`action` 중 빈 칸 (c) 표시 문자열(line·situation·emotion·action·who)에 "비아" 또는 "Bea" 가 남아 있는지 (파일 경로의 BEA_ 는 정상) (d) `src` 가 `v09_fs` 를 가리키면 오류 (e) 같은 `n` 중복.
- 출력: 문제만 한 줄씩 `E1-07 [missing action]` 형식. 문제 없으면 `OK`. JSON 파일은 **읽기만**, 고치지 말 것.

## 작업 8 — 1화·2화 스틸 애니매틱 빌드 (실행만)
- 작업 4에서 만든 JSON 입력 생성기로 두 편을 만든다:
  - `cd 01_EPISODES/EP01R/edit && python3 animatic_E1_v062.py v06/animatic_E1_v062.json v06/ANIMATIC_E1_v063.mp4`
  - `cd 01_EPISODES/EP01R/edit && python3 animatic_E1_v062.py v06/animatic_E2_v07.json v06/ANIMATIC_E2_v01.mp4`
- 완료 후 각 mp4의 길이(초, cv2 프레임수/fps)와 컷 수를 보고. 길이가 `dur` 합계와 1초 이상 다르면 원인을 적어서 보고(수정은 하지 말 것).
- 프레임이 지금도 재생성 중이라 결과는 "지금 상태 스냅샷"이다. 나중에 같은 명령을 다시 돌릴 수 있게 `tools/build_animatics.sh` 에 두 명령을 넣어 둔다.

## 작업 9 (선택) — 보드 "얼굴 QA" 배지
- `tools/build_cast_board.py` 1화/2화 탭 각 컷 카드에, `tools/face_qa.py --json` 결과 파일(`edit/v06/face_qa.json`, 없으면 배지 없음)을 읽어 `SOFT`/`DRIFT` 배지를 빨간 글씨로 표시. DB 코드(`anim_checks`)는 건드리지 말 것. 수정 후 `node -e` 로 `<script>` 파싱 확인.
