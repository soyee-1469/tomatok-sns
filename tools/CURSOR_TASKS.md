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

---
# 3차 지시서 — 2026-11-06 (콘티→스틸 파이프라인 도구화)

> 공통 규칙은 1차와 같다. 추가 읽기 전용: `01_EPISODES/EP01R/frames/v08/**`, `00_MASTER_ASSETS/05_STYLE/blocking_rule.md`(규칙 원문, 꼭 읽을 것), `01_EPISODES/EP01R/tools/gen_conti_island.py`(참고용 원본, 수정 금지 — 복사해서 새 파일로).
> 건드려도 되는 파일: `tools/build_cast_board.py`, 새로 만드는 `tools/*.py`. **Higgsfield/Kling/ChatGPT 호출 금지.** 생성 도구는 반드시 `--dry`(프롬프트·참조·비용만 출력)로만 테스트한다.
> 작업이 끝나면 이 파일 맨 아래 `
### 작업 17 — 보드 #conti 탭 UX 5건 (2026-11-06, 사용자 검토 의견 그대로)
대상: `tools/build_cast_board.py` 의 콘티·스틸 컨펌 탭(#conti) HTML/JS. 데이터 규약(conti_checks 문서 id `E1-still-<key>` / `E1-island-NN`, 필드 status ok|fix, note)은 바꾸지 말 것. 다른 탭은 건드리지 말 것.
1. **집계 분리**: 상단 OK/수정/미판정 집계가 콘티 12칸 + 사용 중 스틸 + 접힌 「교체됨·미사용」까지 한 통으로 센다. → 집계는 **사용 중 스틸만**, 콘티 칸은 별도 줄로. 접힌 카드(`details.old` 안)는 집계에서 제외.
2. **한 장씩 넘기며 판정**: 카드 그림 클릭 → 크게 보기 모달에 **이전/다음 + OK + 재생성(메모 입력)** 을 넣어 스크롤 없이 컷 순서대로 판정. 1화 탭 재생기의 이전·다음 코드를 재사용해도 됨. 판정하면 자동으로 다음 미판정 카드로.
3. **상단 정리**: 탭 제목 「컷 7~15」를 「1화 스틸 컨펌」으로. 위치 상태표·제작 메모는 `<details>`로 접고, 맨 위에는 「미판정 N장」 + 첫 미판정 카드로 가는 앵커 링크만. 헤더의 얼굴·몸통·세트 숫자는 이 탭에서 숨김.
4. **재생성 버튼 보호**: 고칠 점(note)이 비어 있으면 「재생성」 버튼 disabled. 버튼 라벨에 「재생성 (2cr)」로 크레딧 표시. 「수정」 상태 저장은 note가 있을 때만.
5. **제목 중복 제거**: `[컷 3] 3번 R03b 소파 OTS` → `[컷 3] 소파 OTS` 처럼 번호 한 번만. STILLS 튜플의 title에서 선행 `NN번 ` 을 빌드 시 제거(정규식), 한 줄 설명(desc)은 유지.
완료 후: `python3 tools/build_cast_board.py /tmp/board_test` 로 빌드되는지 확인하고, 변경한 함수/블록 이름과 테스트 방법을 「처리 보고」에 적을 것. 발행(Artifact)은 Claude가 한다.


### 작업 18 — 판정 창구 한 곳으로 (2026-11-06 사용자: "콘티 하단 생성 스틸이랑 애니매틱에 가는 이미지가 동일한데 왜 두 군데서 각각 수정하게 해놨어")
대상: `tools/build_cast_board.py`. 작업 17과 같이 처리해도 됨.
- #conti 탭에서 **생성 스틸 카드(`E1-still-*`)를 모두 제거**. 남기는 것: 콘티 12칸(`E1-island-NN`), 앵커·플레이트 참조 프레임(B13c, B40b, F2c, 플레이트 A1/A2/wide)만 "기준 프레임" 섹션으로(판정 버튼 없이, 보기만).
- 이미지 판정은 **#anim1 탭 한 곳**에서만: 컷 카드의 기존 '이미지' 메모 + 재생성 체크를 그대로 쓴다. 접힌 「교체됨·미사용」 섹션도 삭제(파일은 남김).
- 작업 17의 2번(한 장씩 넘기며 판정 모달)은 #anim1 탭에 구현.
- 기존 conti_checks `E1-still-*` 문서는 건드리지 않는다(이력). 상단 집계는 anim_checks 기준.


### 메모 — 2화 콘티 작업 전에 읽을 것 (2026-11-06)
`.claude/skills/tomatok-episode/SKILL.md`의 「콘티→스틸→보드 컨펌 루프」, 「앵커 감사 6항목」, 「2화 이후 콘티 작업 참고 위치」와 `00_MASTER_ASSETS/05_STYLE/blocking_rule.md` §5~§14. 작업 15(make_storyboard_prompts.py)에는 Fixed positions(§8)·WALL ORDER(§14)·세트 마스터 첨부(§7) 문장이 들어가야 한다.


### 작업 19 — tools/face_strip.py: 얼굴 일관성 띠 + 동일인 점수 (2026-11-06, 사용자 "스틸에 얼굴이 다른 건 괜찮은 거야?")
- 입력: 애니매틱 JSON(skip 제외, kind=still). insightface buffalo_l(이미 설치, tools/face_qa.py 참고)로 각 프레임 얼굴 검출 → 컷 번호 라벨 붙인 띠 이미지(`<json 폴더>/face_strip_<ep>.jpg`, 12열).
- 각 얼굴을 확정 얼굴(`CAST_v8_six/JUNHO_face_C.png`, `BEA_MASTER_FACE.png`, `SUMAN_face.png`)과 코사인 유사도로 매칭해 인물 라벨 + 점수. 점수 < 0.35는 띠에서 빨간 테두리, 보고서 md에 "컷 n <인물> 0.28 ← 재생성 후보"로 나열.
- 사용 예: `python3 tools/face_strip.py 01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json --out 01_EPISODES/EP01R/edit/v06/face_report.md`
- 얼굴 스왑/복원은 절대 하지 말 것(철칙 9). 판정만.

### 작업 20 — tools/gaze_qa.py: 시선·고개 방향 QA (2026-11-06, 사용자 "시선, 눈알 이런 건 괜찮은 거야?")
- insightface의 pose(yaw/pitch/roll)와 2d106 랜드마크로 각 얼굴의 고개 방향(왼/오/정면/아래/위)을 분류.
- 애니매틱 JSON의 dir_override/action 텍스트에서 의도 시선을 규칙으로 뽑는다: "소파 쪽/카메라-LEFT/왼쪽" → 왼쪽, "폰을 보" / "화면" → 아래, "올려다" → 위, "카메라" → 정면, "리아를/준호를 바라" → 상대 방향(자리표: 준호는 리아의 왼쪽).
- 의도와 측정이 다르면 보고서에 "컷 n <인물> 의도=아래 측정=왼쪽" 으로 나열. 눈동자 방향은 랜드마크로 대략만(홍채 중심 vs 눈 중심 오프셋).
- 출력: `<json 폴더>/gaze_report.md`. 생성은 하지 않는다.


### 작업 16 보정 — make_kling_prompts.py 수정 (2026-11-06 Claude 검수, 22번 출력 기준)
1. SCENE CONTEXT가 `cam` 필드를 무시하고 "sofa-axis… corduroy sofa"로 나옴 → `cam=="island"`면 "island-axis camera: the living room on camera-left, the kitchen island, copper shelves and fridge on camera-right; NO window in frame" 문장, `sofa`면 소파 문장.
2. 옛 `situation` 문자열("리아가 폰을 가슴에 엎어 숨긴다: 가족방 아니야")이 들어감 → `situation`은 쓰지 말고 `dir_override`(없으면 `action`)만. "(2026-11-06 판정 지문)" 같은 괄호 메모는 제거.
3. 프레임에 있는 모든 인물을 적을 것: 시작 스틸 키(G40_*, E40_*, B40b 등 2막)면 리아+준호+수만, 1막 아일랜드(G13_*, B13*)면 리아+수만, 소파 키면 준호만. POSITIVE LOCKS에 "the other people in frame stay exactly where they are, no one walks, no one leaves" 추가.
4. DIALOGUE의 "ㅋㅋㅋ/ㅎㅎ"는 발화 텍스트에서 빼고 "(she laughs lightly after the line)"로 바꿀 것. "……"는 그대로 두되 "a short pause" 지시 추가.
5. 수만 복장 문장은 "white chef's jacket with a plain black bib apron, no towel"로(옛 towel 문장 금지).

## 4차 작업 (2026-11-09, Claude) — Kling 대사 클립 QA·조립 도구화. 외부 API 호출 금지, 크레딧 0.
> 배경: 1막 대사 클립 재생성에서 Kling이 클로즈업 중간에 와이드 샷으로 하드 컷을 넣어 얼굴이 바뀜. 통과 기준 = `tools/face_score.py` ≥0.45 & 얼굴 폭 ≥250px(720p 클립 기준 ≥180px), 내부 컷 없음, whisper 대사 일치. 오늘 만든 도구: `01_EPISODES/EP01R/tools/clip_frames.py`(끝·f25/f50/f75·콘택트 추출), `01_EPISODES/EP01R/tools/batch_qa.py`(컷 번호 → 최신 테이크 QA 묶음), `01_EPISODES/EP01R/tools/gen_kling_lines.py`(--dry/--lockend/--omni, CUTS 23컷). 이 세 파일은 **읽기만**, 수정은 작업 21·24에서 지정한 범위만.

### 작업 21 — `tools/clip_qa.py` 내부 컷 판정 고도화 (수정 허용: 이 파일만)
현재 `clip_qa.py`는 프레임 차 >8 스파이크 목록만 찍는다. 와이드 전환을 자동 판정하도록:
1. 각 프레임에서 insightface(`buffalo_l`, CPU)로 가장 큰 얼굴 폭을 재고(매 3프레임), 얼굴 폭이 직전 대비 40% 이상 줄어드는 시각을 `WIDE_CUT@<t>s`로 보고. 얼굴이 사라지면 `FACE_LOST@<t>s`.
2. 프레임 차 스파이크 >40 은 `HARD_CUT@<t>s`, 8~40 연속 10프레임 이상은 `CAMERA_MOVE <t0>-<t1>s`.
3. 출력 한 줄: `<파일> | <길이>s | PASS|FAIL | 사유들 | 사용 가능 구간 0.0-<t>s`(첫 결함 직전까지).
4. `--json` 옵션이면 `{"file","dur","pass","events":[...],"usable_until"}` 배열을 stdout에.
검증: `python3 tools/clip_qa.py 01_EPISODES/EP01R/video/v08/E1_04/EP01R_E1_04_kling3_take03.mp4`(1.75s 하드 컷+와이드 → FAIL, usable 1.7) 와 `E1_12/EP01R_E1_12_kling3_take01.mp4`(PASS) 두 개로 확인.

### 작업 22 — 타이트 클로즈업 크롭기 `tools/tight_cu.py` (새 파일)
단독 상반신 스틸(frames/v08/S_*.png, 1080×1920)에서 얼굴 중심 9:16 크롭을 만든다. 2026-11-06 통과 프레임 J4(얼굴 폭 365px @720p ≈ 550px @1080)와 같은 비율이 목표.
1. insightface로 얼굴 bbox → 얼굴 폭이 출력 가로의 **45~50%** 가 되도록 크롭 폭 결정, 세로는 9:16, 얼굴 중심을 가로 중앙·세로 38% 지점에. 원본 밖으로 나가면 크롭을 안쪽으로 밀고 그래도 안 되면 LANCZOS 업스케일 후 크롭.
2. 출력 `frames/v08/<이름>_tight.png` 1080×1920. 끝에 `tools/face_score.py`로 점수·폭을 찍어 표로 보고.
3. 대상 6장: S_ria_island_act1_cu, S_ria_island_act2_cu, S_suman_island_cu, S_suman_island_look_cu, S_junho_sofa_cu, S_junho_island_r2. 원본은 절대 덮어쓰지 않는다.

### 작업 23 — 보드 「Kling 대사 클립」 탭 테이크 카드 (`tools/build_cast_board.py`)
컷 번호별로 최신 테이크를 카드로: 콘택트 png(`*_contact.png`), mp4 재생, 얼굴 점수 4개(f25/f50/f75/end, `tools/face_score.py` 출력 파싱 또는 미리 저장된 `video/v08/qa_<cut>.json`이 있으면 그것), whisper 텍스트(`video/v08/E1_nn/*_whisper.txt` 있으면), clip_qa 한 줄. PASS/FAIL 배지. 테이크 선택 드롭다운(같은 폴더의 모든 mp4). 데이터 수집 스크립트는 `tools/collect_clip_qa.py`(새 파일)로 분리: `python3 tools/collect_clip_qa.py 3 4 5 …` → `video/v08/qa_<cut>.json` 저장(face_score·clip_qa·transcribe 호출, 모두 로컬). 발행은 Claude가 한다.

### 작업 24 — 애니매틱 클립 끼우기 `tools/animatic_set_clip.py` (새 파일, animatic_set_frame.py 패턴 재사용)
`edit/v06/animatic_E1_v062.json` 행에 `clip`(mp4 경로)·`clip_in`·`clip_out`(초) 필드를 넣고/빼는 CLI: `--set 22 video/v08/E1_22/EP01R_E1_22_kling3_take02.mp4 --out 3.4`, `--clear 22`, `--list`. JSON은 백업(`*.bak_<시각>`) 후 쓴다. `edit/animatic_E1_v062.py` 렌더러가 `clip` 필드가 있으면 스틸 줌 대신 그 구간을 1080×1920로 스케일해 넣도록 분기 추가(오디오 포함, 없는 행은 기존 동작). 검증: 22번 set 후 `ANIMATIC_E1_v090.mp4` 렌더되는지(클립 1개만 들어간 상태).

### 작업 25 — `01_EPISODES/EP01R/tools/hf_gen.py` 비용 사전 견적 + 장부 (수정 허용: 이 파일만, API 호출 중 `generate cost`만 추가 허용 — 크레딧 0)
1. 생성 직전 `higgsfield generate cost <job_type> <같은 파라미터>`를 호출해 견적을 찍고, 환경변수 `HF_MAX_CR`(기본 40)보다 **누계**가 크면 생성하지 않고 exit 3.
2. 누계 장부 `01_EPISODES/EP01R/video/v08/CREDIT_LEDGER.csv`(시각, job_type, out_base, 견적, 상태). 성공·실패·nsfw 모두 기록. 날짜가 바뀌면 누계 0부터.
3. `--yes` 없이도 동작하되, 견적 줄은 반드시 stdout 첫 줄에.
검증: `HF_MAX_CR=1 python3 01_EPISODES/EP01R/tools/hf_gen.py /tmp/x kling3_0 --prompt t --duration 3 --mode std --aspect_ratio 9:16` → 견적 6 출력 후 exit 3(생성 안 함).

### 작업 27 — 1화 Kling 대사 클립 보드 `01_EPISODES/EP01R/tools/build_clip_board.py` (2026-11-09 사용자: "스틸컷 옆에 영상 생성한거 넣어서 짤별로 플레이 해볼수있게") — **작업 23보다 먼저**
Claude가 초안을 써 두었다(미실행, 수정 허용: 이 파일과 `tools/batch_qa.py`의 JSON 저장 부분만). 입력 = `video/v08/qa_<cut>.json`(13개 있음, `python3 01_EPISODES/EP01R/tools/batch_qa.py <컷…>`이 만든다) + `edit/v06/animatic_E1_v062.json`. 출력 = `01_EPISODES/EP01R/board_clips/index.html` + `board_clips/media/`(mp4 복사, 스틸 540px jpg).
1. 실행해서 돌아가게 만들고(cv2·PIL 외 외부 라이브러리 금지), 깨진 부분 고친다. HTML은 `<title>`·`<style>`·본문만(doctype/html/head/body 태그 없음 — Artifact 발행 규격).
2. 컷 카드에 **테이크 선택 드롭다운** 추가: 같은 `video/v08/E1_nn/` 폴더의 모든 `*_kling3_take*.mp4`를 media/로 복사하고 `<select>`로 바꿔 재생. 기본은 최신 테이크. 테이크마다 face/whisper가 있으면(현재는 최신 테이크만 JSON) 표시, 없으면 "QA 없음".
3. 통과 판정은 바꾸지 말 것(단일 샷 & 얼굴 4지점 ≥0.45 & 얼굴 폭 ≥180px & whisper 일치 ≥85%). 필터 버튼(전체/통과/재생성)은 유지.
4. media 총량이 60MB를 넘으면 오래된 테이크부터 제외하고 보고에 적는다(Artifact 1회 발행 상한 64MB).
5. 검증: `python3 01_EPISODES/EP01R/tools/build_clip_board.py` 성공 + `open board_clips/index.html`로 로컬 확인(13카드, 영상 재생, 필터 동작). 발행은 Claude가 한다.

### 작업 27 후속 (2026-11-09 Claude 검수 → 로컬 반영 완료, 커서는 확인만)
- 실제 JSON에는 분할 컷 키 `"4r"`, `"4b"`(문자열)가 있어 `int(row["n"])`에서 죽었다 → `tagn()/keyn()/sort_key()` 헬퍼 추가, `E1_{0:02d}`·`S_{0:02d}`·막 분리 비교를 전부 헬퍼로 교체. **앞으로 컷 번호는 int 또는 '4b'식 문자열 둘 다 온다고 가정할 것(모든 도구 공통).**
- `match_line`: whisper 줄이 `"   0.00-10.00  텍스트"`라 `split("  ",1)`이 들여쓰기에서 잘려 시간 접두가 남음 → 정규식으로 시간 구간 제거. 이 버그로 23카드 중 1장만 통과로 나왔었다(수정 후 29카드 20 통과).
- 발행됨: https://claude.ai/artifact/XUJQa2zH8Q8o1DixuAW3TK . 작업 24(animatic_set_clip)가 다음 우선순위.

### 작업 28 — 보드 「콘티·스틸」 탭을 1화/2화로 나누기 (2026-11-09 사용자: "콘티 1화 2화 나눠줘야지 저렇게 계속 이어서 보게할거야?") — **최우선**
`tools/build_cast_board.py`의 #conti 뷰 안에서 1화 섹션(#conti1)과 2화 섹션(#conti2)이 위아래로 이어져 보인다. 「각본」 탭에 있는 1화/2화 선택 버튼(.ep-pick .ep)과 같은 방식으로 콘티 탭 상단에 **「1화 콘티」「2화 콘티」 토글**을 두고 한 번에 한 화만 보이게 한다. 기본 1화. 선택 상태는 localStorage(try/catch)에 기억. 콘티 판정 저장(conti_checks)과 집계(paintSec)는 그대로 동작해야 한다. 검증: 빌드 → 탭 전환 시 반대쪽 섹션이 hidden, 판정 OK 클릭이 여전히 db에 기록. **빌드 후 처리 보고에 "발행 필요"라고 적을 것** — 커서는 발행 권한이 없고 Claude가 Artifact로 올린다(2화 콘티가 안 보였던 원인).

### 작업 26 — 미처리 작업 17·18·19·20 상태 확인
처리 보고에 17~20 항목이 없다. 끝낸 것이 있으면 보고 절에 적고, 안 한 것은 21~25보다 **뒤**로 미룬다(우선순위: 28 → 24 → 21 → 22 → 25 → 23 → 17~20).

## 처리 보고` 절에 작업 번호·바꾼 파일·검증 방법을 적는다. 5분 주기로 이 파일을 다시 읽고 아직 보고되지 않은 작업만 한다.

## 작업 7 — 콘티 그리드 분할기 `tools/split_storyboard.py` (새 파일)
- 입력: `python3 tools/split_storyboard.py <grid.png> --rows 4 --cols 3 --out <dir> --prefix EP01_island --names C07a,C07b,...`
- 균등 분할이 아니라 **흰 구분선(gutter)을 찾아** 자른다: 행·열 방향 밝기 프로파일에서 밝기 > 240 이 연속된 띠를 구분선으로 보고, 띠 중앙에서 자른다. 못 찾으면 균등 분할로 폴백하고 경고 출력.
- 칸 아래 라벨 띠("1 | CUT 7 – sofa-axis")는 자르지 말고 포함.
- 출력: `<prefix>_NN_<name>.png` + `<prefix>_INDEX.md`(칸 번호·파일명·크기 표).
- 테스트: `01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_board_01.png`(1086×1448, 3×4)로 돌려 기존 `EP01_island_NN_*.png`와 픽셀 차이가 거의 없는지 확인(덮어쓰지 말고 `/tmp` 또는 `--out` 다른 폴더로).

## 작업 8 — 콘티 기반 스틸 생성기 공용화 `tools/gen_from_conti.py` (새 파일)
- `01_EPISODES/EP01R/tools/gen_conti_island.py` 의 CUTS 딕셔너리를 **JSON 파일**로 빼서 읽는다: `python3 tools/gen_from_conti.py <cuts.json> [키 ...] [--dry]`
- cuts.json 스키마: `{ "<key>": {"plate":"sofa|island|dining|door|reverse|sideboard|wide", "sketch": "<STORYBOARD 파일명 or null>", "who": ["J","B","S","G"], "stage": "...", "time": "evening|day"} }`. `time=day` 면 `LIVINGROOM_v14d_*` 플레이트.
- 프롬프트 조립 규칙은 원본과 동일(HEAD + PLATE LOCK + (sketch 있을 때만 STORYBOARD 문장) + stage + LAYOUT + LIGHTING + IDENTITY LOCK). 참조 순서 [플레이트 → (콘티) → 얼굴×2 → 몸통 → 와이드]. JUN/RIA/SUM/SUN/FACE/BODY/ROOM/LAYOUT/LIGHTING 상수는 `tools/process_checks.py` 에서 **import 하지 말고** 그대로 복사(그 파일은 실행 시 sys.argv를 읽어 깨진다).
- `--dry`: 키마다 프롬프트 전문, 참조 파일 존재 여부(없으면 ERROR), 예상 비용(장당 2cr) 을 출력하고 종료. 기본값(비 dry)은 원본처럼 `01_EPISODES/EP01R/tools/hf_gen.py` 를 Popen 병렬 호출 → **너는 절대 비 dry로 실행하지 않는다.**
- 결과 webp → png 변환까지 포함. `_prompt.txt` 저장 유지.
- 샘플 JSON `01_EPISODES/EP01R/frames/v08/STORYBOARD/cuts_island.json` 을 원본 CUTS 그대로 옮겨 만들고 `--dry` 출력이 원본 `_prompt.txt` 와 일치하는지 diff.

## 작업 9 — 가구 배치·각도 QA `tools/layout_qa.py` (새 파일)
목적: 생성 스틸이 플레이트와 가구 배치가 다른지 자동 표시(2026-11-06 J2b r1 사례: 콘티 때문에 소파가 비스듬히 돌아감).
- 입력: `python3 tools/layout_qa.py <still.png> --plate <plate.png> [--out report.md]` 또는 `--batch <dir>`(파일명 규칙으로 플레이트 자동 선택: `J2b*`/`F2*`/`J2*`→A1_sofa, `*island*`/`B*`/`S2*`/`T5*`→A2_island, `J9*`/`*crossing*`→A5_reverse, `W*`→master).
- 방법 (OpenCV, 외부 API 없음): (1) 두 이미지를 같은 크기로 맞추고 상단 55%(벽·창·선반)에서 ORB 특징점 매칭 → RANSAC 호모그래피 인라이어 비율. (2) 하단 45%에서 소파/아일랜드 윗선 각도: Canny + HoughLinesP 로 가장 긴 수평계 선분의 기울기(°)를 플레이트와 비교. (3) 판정: 인라이어 비율 < 0.25 또는 각도 차 > 6° 면 `LAYOUT DRIFT`, 아니면 `OK`. 수치와 판정을 md 표로.
- 검증 세트: `frames/v08/J2b_junho_exit_right_r1.png`(DRIFT가 나와야 함) vs `J2b_junho_exit_right_r2.png`(OK가 나와야 함), `B13_ria_island_start.png`(OK), `T5_ria_suman_look_left_r1.png`(OK). 넷 다 기대값이 나오면 통과. 임계값은 이 넷이 맞게 조정해도 된다(값을 보고에 적을 것).

## 작업 10 — 보드 「콘티·스틸」 탭 분리 (`tools/build_cast_board.py`)
- 지금 `#view-anim1` 안에 끼워 넣은 `<section id="conti1">` 을 새 탭 `#conti`(「콘티·스틸 컨펌」)로 옮긴다. nav에 탭 추가, `show()` 의 허용 해시 목록에 `conti` 추가. `#anim1` 은 원래대로 애니매틱만.
- 콘티 탭 상단에 `01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_STATE_TABLE.md` 의 첫 표(위치 상태표)를 HTML 표로 렌더(간단한 md 표 파서면 됨, 외부 라이브러리 금지).
- `conti_checks` 저장 JS는 그대로(이동만). 콘티 칸 카드와 스틸 카드를 두 묶음(`콘티 12칸` / `생성 스틸`)으로 소제목 구분. 작업 9의 report.json 이 있으면 스틸 카드에 `LAYOUT DRIFT` 배지(기존 `.qa-badge` 클래스 재사용).
- 수정 후 `python3 tools/build_cast_board.py /tmp/board_test` 로 빌드되고 `node -e` 로 `<script>` 문법 통과 확인. **발행(Artifact)은 하지 않는다**(Claude가 한다).

## 작업 11 — 애니매틱 프레임 교체기 `tools/animatic_set_frame.py` (새 파일)
목적: 콘티→스틸로 새로 뽑은 프레임을 애니매틱 JSON의 해당 컷에 안전하게 끼운다(지금은 손으로 JSON을 고침).
- `python3 tools/animatic_set_frame.py <animatic.json> <n> --frame <frame_id> --src <png 경로> [--dur 2.0] [--line "..."] [--action "..."] [--dry]`
- 바꾸기 전 원본을 `<animatic>.bak.<YYYYMMDD-HHMMSS>.json` 으로 백업. `--dry` 면 변경 전/후 row 를 출력만.
- 검사: src 파일 존재, png 9:16(±2%) 여부, 같은 JSON 안에서 같은 frame 이 연속 컷에 반복되면 경고(철칙 8 "같은 인물 연속 컷은 다른 프레임"). `tools/lint_animatic.py` 가 있으면 끝에 호출.
- **JSON 수정은 Claude가 명시적으로 시킬 때만**(지금은 도구만 만들고 `--dry` 로 `01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json` 9번 컷에 `frames/v08/J9d_junho_toward_ria_islandcam.png` 를 넣는 출력이 맞는지만 확인). 실제 JSON은 건드리지 말 것(읽기 전용 목록에 있음).

## 작업 12 — `tools/layout_qa.py` 플레이트 선택 오판 수정 (2026-11-06 Claude 검수)
- 증상: `J9d_junho_toward_ria_islandcam.png` 는 아일랜드 플레이트(A2)로 뽑았는데 파일명 규칙(`J9*`→reverse)으로 A5_reverse와 비교해 `LAYOUT DRIFT`(inlier 0.24, angle 47°)가 나옴. 실제로는 B13과 같은 카메라라 OK여야 함.
- 수정: 플레이트는 파일명이 아니라 **같은 폴더의 `<still>_prompt.txt` 또는 `<still>_status.json`의 image-references 1번**에서 읽는다(status.json의 params에 참조 목록이 있으면 그걸 우선). `frame_ref`로 시작 프레임을 1번에 넣은 경우(`FRAME LOCK` 문구가 프롬프트에 있으면) 2번이 플레이트다. 둘 다 없을 때만 파일명 규칙 폴백.
- 검증: J9d → OK, J2b_r1 → DRIFT, J2b_r2 → OK, T5_r1 → OK, J3_*_r1~r4 → DRIFT(어제 사용자 판정과 일치해야 함). 결과를 `01_EPISODES/EP01R/frames/v08/layout_qa_report.md`(+ .json)로 저장. 보드(작업 10)의 DRIFT 배지가 이 json을 읽는지 확인.

## 작업 13 — `tools/animatic_set_frame.py` 에 행 삽입 모드 추가
- `--insert-after <n>` 옵션: 새 row(n+1)를 끼우고 뒤 row들의 `n`을 +1. 필드는 `--frame --src --dur --line --who --action --situation --emotion --cam`.
- 삽입 시 `edit/v06/anim_checks_renumber.json`에 `{"E1-40":"E1-41",...}` 매핑을 써 둔다(보드 DB 문서 이동은 Claude가 ArtifactData로 한다. 너는 DB를 만지지 않는다).
- `--dry` 로 2026-11-06 삽입(39 뒤 J9d)이 현재 JSON과 같은 결과를 내는지 백업 `.bak.*.insert40.json` 과 diff.

## 작업 14 — 앉은 자리 판정 `tools/seat_qa.py` (새 파일)
목적: 아일랜드 컷에서 리아가 몇 번째 스툴에 앉았는지 자동 판정(2026-11-06 '가운데 스툴' 요청이 생성에서 5번 연속 실패 → 눈 대신 수치로 잡는다).
- 입력: `python3 tools/seat_qa.py <still.png> [--plate <plate.png>] [--batch <dir> --glob "R*|B*|A09*|ISLAND*"]`
- 방법(OpenCV만): (1) 이미지 하단 40%에서 검은 원형 스툴 좌판을 찾는다(어두운 타원 블롭, 가로폭 60~220px, 가로로 늘어선 것만). 플레이트가 주어지면 플레이트의 스툴 좌표를 기준으로 쓴다. (2) 사람 영역은 insightface 얼굴 검출(`tools/face_qa.py` 참고) 얼굴 박스의 x중심을 아래로 내려 가장 가까운 스툴 인덱스를 고른다. (3) 출력: 스툴 개수, 각 인물의 스툴 인덱스(왼쪽=1), 판정 `SEAT 1|2|3|standing`.
- 검증: `frames/v08/ISLAND_MASTER_v2*.png`, `ISLAND_MASTER_v3.png`, `B13_ria_island_start.png` 는 전부 SEAT 1이 나와야 함. 결과를 `frames/v08/seat_qa.md`로.

## 작업 15 — 2막 구조 콘티 프롬프트 생성기 `tools/make_storyboard_prompts.py` (새 파일)
목적: 애니매틱 JSON(현재 기준)에서 ChatGPT 콘티 프롬프트를 자동으로 뽑아 콘티·애니매틱·스틸이 어긋나지 않게 한다(사용자 2026-11-06 "콘티랑 애니매틱이랑 다르다").
- 입력: `python3 tools/make_storyboard_prompts.py 01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json --per 12 --out 01_EPISODES/EP01R/frames/v08/STORYBOARD/prompts_E1/`
- `skip:true` 행 제외, `kind:"ui"` 행은 칸 안에 "UI: <frame>"으로만 표기. 12칸(3×4)씩 묶어 시트 N개. 각 시트 프롬프트는 `00_MASTER_ASSETS/05_STYLE/blocking_rule.md` 6절 템플릿을 뼈대로: 얼굴 없음, 코 쐐기+시선 화살표, 카메라 축 라벨, **Fixed positions 줄**(8절 고정 자리표: 준호 소파 가운데 쿠션 / 리아 아일랜드 스툴 / 수만 카운터 뒤, 2막은 준호 리아 옆), 세트 소품 줄(9절), 그리고 칸마다 `Panel k — CUT n (<막>, <축>): <situation> / <action> / looks at …`.
- 출력: 시트별 `.txt` + 전체 `INDEX.md`(시트↔컷 매핑). 생성 API 호출 없음. 사용자가 ChatGPT에 붙여 넣는다.

## 작업 16 — Kling 대사 컷 프롬프트 생성기 `tools/make_kling_prompts.py` (새 파일, --dry만)
목적: 애니매틱 행(대사 있는 still)에서 `01_EPISODES/EP01R/prompts/v06/E1_02_BEA.txt` 형식(SCENE CONTEXT / FORMAT MODE / CAMERA / ACTION / PERFORMANCE / AUDIO / POSITIVE LOCKS / DIALOGUE)의 Kling 프롬프트를 만든다.
- 입력: `python3 tools/make_kling_prompts.py <animatic.json> --out 01_EPISODES/EP01R/prompts/v08/ [--only 3,8,10]`
- 인물 묘사 문장은 `01_EPISODES/EP01R/tools/gen_conti_island.py`의 JUN/RIA/SUM 상수를 복사. 대사 줄엔 `05_STYLE/subtitle_and_line_rule.md`·`junho_voice_rule.md`·`bea_language_rule.md`의 발화 지시(감정/말투/끝음)를 붙인다. 3초 컷 기준 ACTION 타임라인(0.0~0.5 / 0.5~2.4 / 2.4~3.0). AUDIO는 앰비언스만, 음악·진동 금지(철칙 6).
- 생성 호출은 절대 하지 않는다. 결과 파일만 만들고 `--dry`로 3개 샘플(3·8·10번)을 보고에 붙인다.

## 작업 28 — 새 3화 공동 저녁 단톡방 UI (2026-11-12, Codex → Cursor)

- 상태: TODO. 기존 작업보다 이번 회차 UI를 먼저 진행. 커서 실제 착수 여부는 아직 확인하지 않음.
- 사용자 추가 수정: 한국어가 서툰 입주민들의 소통 수단이 단톡방이다. 메뉴 제안·조건·합의를 채팅으로 표현. 대면 대화로 바꾸자는 장면 삭제, 최신 각본과 UI 브리프의 메뉴 메시지 순서를 사용한다.
- 기준: `tools/EP03_CHAT_UI_BRIEF.md`, 각본 `00_MASTER_ASSETS/WORLD_PLANNING/EP03_SCRIPT_v03.md`. 옛 가스비 3화 v02는 사용하지 않는다.
- 허용 변경: 새 `tools/render_ep03_chat.py`, 새 `tools/ep03_chat_data.json`, 새 `tools/ep03_chat_preview.html`, `tools/build_series_board.py`, `tools/series_board.html`. 이번 작업 결과만 `board_web/ep03_chat/`에 생성 허용. 기존 마스터·각본·프로필·옛 렌더러는 읽기 전용.
- 기존 확정 얼굴 아바타 8명과 할머니 공지를 사용해 한국어 뷰 UI 초안 제작. 인물별 최종 프로필 연출 제안과 임시 기존 아바타를 구분. 리아는 BEA_AV, 하오는 DOYUN_AV이며 중국 국기.
- 각본의 6개 채팅 상태를 데이터로 분리하고 이전/다음 상태 전환 및 프로필 목록 미리보기 제공. 번역 원문은 검수 전 초안으로 표시.
- 3화 작업실에서 UI 미리보기로 이동하는 링크 연결. 기존 1·2화 동작 보존. 새 회차 화면은 `python3 tools/build_series_board.py`, `board_web/series.html#EP03/story`.
- 검증: 아바타 경로 전부 존재, 할머니 참여·공지 표시, 6상태 순서 일치, 준호만 내 메시지 색, 번역/원문 순서, 390px 가로 넘침, 브라우저 이전/다음·프로필 전환, 재빌드 후 링크 유지.
- 외부 이미지·영상·Higgsfield API 호출 금지. 목업은 기존 공용 스크립트 사용. 바이너리 Git 추가 금지. 커서는 처리 보고만 작성하고 커밋하지 않음. Codex가 검수 후 커밋·푸시.

## 처리 보고

작업 7–11. 생성 API는 호출하지 않았다. `gen_from_conti.py` 와 `animatic_set_frame.py` 는 `--dry` 만 실행했다. 애니매틱 JSON은 수정하지 않았다(mtime 1793869535, 25977바이트, 백업 파일 없음).

### 작업 7
- 새 파일 `tools/split_storyboard.py`.
- 검증: `EP01_island_board_01.png` 를 `/tmp/sb_split` 에 분할(원본 칸 파일은 그대로). 밝기 > 240 인 내부 띠 중앙.
- 1–6칸 362×362, 기존 파일과 평균 픽셀 차 0. 7–9칸은 세로 363(구분선 1px가 칸에 포함), 겹치는 영역 차 0. 10–12칸은 세로 361이고 1px 위가 기존 균등 컷. 세 번째 가로 구분선(y 1085–1090) 중앙이 1087이라 기존 1086 컷보다 1px 아래다. 1px 맞춰 겹치면 차 0. 라벨 띠는 칸 안에 있다.

### 작업 8
- 새 파일 `tools/gen_from_conti.py`. 샘플 `01_EPISODES/EP01R/frames/v08/STORYBOARD/cuts_island.json` (원본 CUTS 7키. J9d 만 `frame_ref` 추가).
- 조립은 원본과 같다. `frame_ref` 가 있으면 FRAME LOCK 이 1번 참조가 되고 PLATE 문장은 빠진다. `time=day` 는 `LIVINGROOM_v14d_*` 플레이트.
- `--dry` 프롬프트 7개가 각 `frames/v08/<key>_prompt.txt` 와 일치. 참조 파일 전부 있음. 예상 비용 14cr. 비 dry 는 실행하지 않음.

### 작업 9
- 새 파일 `tools/layout_qa.py`. 리포트 `tools/layout_qa.md`, `tools/layout_qa.json`.
- 임계값: 상단 55% ORB+RANSAC 인라이어 < 0.25, 또는 하단 45% 수평계 선분 각도 차 > 6°. 수평계는 |기울기| ≤ 55° 인 가장 긴 선(돌아간 소파 약 40°를 포함하고 수직 기둥은 버린다).
- 검증: J2b r1 LAYOUT DRIFT (인라이어 0.956, 각도 차 44.99°). r2 OK (0.969, 4.99°). B13 OK (0.899, 0.03°). T5 OK (0.909, 0.96°).

### 작업 10
- `tools/build_cast_board.py`. `#conti` 탭(「콘티·스틸 컨펌」), `show()` 해시에 `conti`. `#view-anim1` 은 애니매틱만. `conti_checks` JS는 이동만.
- 콘티 탭 상단에 위치 상태표 첫 표. 소제목 `콘티 12칸` / `생성 스틸`. `tools/layout_qa.json` 에 DRIFT 가 있으면 해당 스틸에 `.qa-badge`. 이번 보드 스틸(r2, B13, J9d, T5)은 DRIFT 가 아니라 배지가 안 붙는다. r1 은 카드가 없다.
- `python3 tools/build_cast_board.py /tmp/board_test` 성공. 생성 HTML의 script 2개 모두 `node --check` 통과. 발행은 하지 않음.

### 작업 11
- 새 파일 `tools/animatic_set_frame.py`.
- `--dry` 로 E1 9번 컷: frame `J9_junho_crossing_r1_r1_r1` → `J9d_junho_toward_ria_islandcam`, src 는 `frames/v08/J9d_junho_toward_ria_islandcam.png`. 1536×2752, 9:16 오차 2% 안. 앞뒤 컷 프레임과 달라 연속 경고 없음. 이어서 `lint_animatic.py` 호출. JSON은 쓰지 않음.

### 작업 12
- `tools/layout_qa.py`. 플레이트는 status.json params의 로컬 image-references(없으면 prompt.txt의 로컬 경로)에서 고른다. 프롬프트에 FRAME LOCK이 있으면 2번, 아니면 1번. status의 input_images는 클라우드 URL뿐이라 로컬 경로가 없다. 그때 같은 이름의 `cuts_island.json` 참조 순서(frame_ref → plate)를 쓰고, 그것도 없으면 파일명 규칙.
- 각도: 플레이트는 하단 45%에서 |기울기| ≤ 55°인 가장 긴 선. 스틸은 그 각 ±25° 안의 가장 긴 선(45° 인물 윤곽은 제외). 인라이어 < 0.55 또는 각도 차 > 20° 이면 LAYOUT DRIFT. 작업 9의 0.25 / 6°는 이 검증 세트에 맞게 바꾼 값이다.
- 결과 `frames/v08/layout_qa_report.md`, `layout_qa_report.json`. J9d OK (A2, 인라이어 0.885, 각도 차 17.89°). J2b r1 DRIFT (A1, 0.956, 22.02°). J2b r2 OK (0.969, 4.99°). T5 OK (0.909, 0.96°). J3 r1 DRIFT (0.371, 9.98°), r2 DRIFT (0.24, 22.02°), r3 DRIFT (0.246, 11.04°), r4 DRIFT (0.5, 12.01°).
- 보드 배지 경로는 `frames/v08/layout_qa_report.json`. `/tmp/board_test`를 다시 빌드했다. 콘티 탭 스틸(r2, B13, J9d, T5)은 OK라 LAYOUT DRIFT 배지가 없고, J9d 카드에도 배지가 없다. r1과 J3는 그 json에서 DRIFT지만 콘티 스틸 카드가 아니다. script 2개 `node --check` 통과. 발행은 하지 않음.

### 작업 13
- `tools/animatic_set_frame.py`에 `--insert-after`를 넣었다. 새 행은 n+1, 뒤 행의 n은 +1. `--dry`는 JSON과 `anim_checks_renumber.json`을 쓰지 않는다. 실제 삽입은 하지 않았다. 보드 DB는 건드리지 않았다.
- 검증: `animatic_E1_v062.json.bak.20261106-111117.insert40.json`(44컷)의 39번 뒤에 twoact 스냅샷의 J9d 행을 넣으면 45컷이 된다. 새 40번 행은 twoact의 J9d와 같다. 매핑은 `E1-40→E1-41` … `E1-44→E1-45`.
- twoact 스냅샷과 필드 비교는 45행 중 1곳만 다르다. 35번 action이 삽입 백업은 `엄지 빠르게, 준호 뒤에 흐릿`이고 twoact는 자리 고정 문장으로 바뀌어 있다. 삽입 자체와 번호 이동은 같다. 지금 쓰는 `animatic_E1_v062.json`은 그 뒤 2막 재배열(44컷, J9d 없음, 29124바이트)이라 비교 대상이 아니다. dry 전후로 이 파일과 두 백업의 mtime은 그대로였고, renumber 파일은 생기지 않았다.

### 작업 14
- 새 파일 `tools/seat_qa.py`. 플레이트 `LIVINGROOM_v14e_A2_island.png` 하단 40%에서 검은 좌판 가로폭 60–220px. 바닥 쪽 줄만 남겨 스툴 3개, x=522, 712, 844. 더 위의 블롭 1개는 버렸다.
- 얼굴은 insightface buffalo_l. 카운터 쪽으로 기댄 얼굴이 다음 스툴에 더 가까워지므로, 얼굴 x보다 왼쪽(오른쪽 36px 허용)이면서 다음 스툴 간격의 85% 안인 스툴에 배정한다. 화면 아래쪽 얼굴이 그 컷의 판정이다.
- 여섯 장 모두 SEAT 1. 카운터 뒤 얼굴은 standing. `frames/v08/seat_qa.md`. v2 cx624.3, v2b 656.2, v2c 632.8, v2d 674.2, v3 655.1, B13 567.8.

### 작업 15
- 새 파일 `tools/make_storyboard_prompts.py`. 현재 E1 JSON 44컷에서 skip 21·29를 빼고 42칸. 시트 4장(`prompts_E1/sheet_01.txt`–`sheet_04.txt`)과 `INDEX.md`. 생성 API 호출 없음.
- 1–19는 1막, 20은 이동, 22부터 2막. ui 칸은 `UI: <frame>`만. 8절 Fixed positions 문장과 2막(준호는 리아 옆), 9절 소품 문장, Do not flip을 시트마다 넣었다.

### 작업 16
- 새 파일 `tools/make_kling_prompts.py`. 대사가 있는 still 30개를 `prompts/v08/`에 썼다. Kling·힉스필드 호출 없음. 금지어(aggrieved, incredulous, interrogating, pressing, petty, defensive, snapping, whiny, exasperated)는 30개 파일에 없다. 준호 문장의 "never irritated"는 말투 규칙의 고정 문장이다.
- 3번 대사는 JSON 그대로 `오빠, still? 그거 아직도 써?`를 인용했다. 언어 규칙의 확정 대사는 문장 중간 영어를 뺀 `오빠, 그거 아직도 써?`다. JSON은 고치지 않았다.
- `--dry --only 3,8,10` 샘플:

```
SCENE CONTEXT
Evening, island-axis camera, sofa on camera-left and the marble island on camera-right. the woman (27, Filipino-American, warm golden-tan skin, long dark wavy hair with curtain bangs, white poplin shirt with cuffed sleeves, dark-indigo jeans, small gold hoops, no glasses). 리아가 커피를 젓다가 준호를 본다 폰에서 눈 떼고 소파 쪽으로 고개, 눈썹 올림

FORMAT MODE
One continuous shot, no cuts.

CAMERA
Fixed camera on a tripod, exactly the framing of the start image, no zoom, no pan, no handheld sway. Camera axis: sofa on camera-left, island on camera-right. Do not flip. Modern Korean sitcom look: clean, natural warm colors, evening indoor lighting with warm lamps and string lights, window dark navy, no film grain, no over-sharpening.

ACTION
0.0s to 0.5s: hold the start pose, a small breath before the line. 0.5s to 2.4s: 폰에서 눈 떼고 소파 쪽으로 고개, 눈썹 올림 2.4s to 3.0s: hold the last expression, no new gesture.

PERFORMANCE
From the script (놀림, 애정): teasing, affectionate. 폰에서 눈 떼고 소파 쪽으로 고개, 눈썹 올림 Bright and playful. No exaggerated acting, no look at the camera.

AUDIO
Quiet living-room ambience only (soft refrigerator hum). No music, no notification sounds, no vibration, no door sounds.

POSITIVE LOCKS
Continue exactly from the start image. The woman keeps the same face, hair, clothes and position through the whole take. She does not wear glasses. Same room, furniture, lamps and colors. No new people enter. No subtitles, no on-screen text, no watermark.

DIALOGUE
The woman says in fluent Korean with a light Filipino-English accent and an English-like rising rhythm, bright and playful, teasing, affectionate, the question rising at the end: "오빠, still? 그거 아직도 써?". The English word "still" is pronounced natively in English; every other word is Korean. She says only this one line and nothing else; no other words in any language. Natural delivery, visible lip-sync, mouth movements match every word, no subtitles, no on-screen text.
```

```
SCENE CONTEXT
Evening, island-axis camera, sofa on camera-left and the marble island on camera-right. the man (29, Korean, round gold wire glasses, jet-black two-block hair, navy overshirt open over a white T-shirt, company ID badge on a navy lanyard, grey trousers). 리아 옆에 서서 폰을 얼굴 앞에 들이민다 소파 가운데 앉아 폰을 아일랜드 쪽으로 들어 보이며 (1막 소파)

ACTION
0.0s to 0.5s: hold the start pose, a small breath before the line. 0.5s to 2.4s: 소파 가운데 앉아 폰을 아일랜드 쪽으로 들어 보이며 (1막 소파) Throughout the shot he is a nervous, jittery wreck in a funny way: clutching the phone with both hands, bouncing one knee, shifting his weight on the sofa, glancing at the screen and away again, wiping a palm on his trousers, small restless fidgets between and during the words. 2.4s to 3.0s: hold the last expression, no new gesture.

DIALOGUE
The man speaks in natural native Korean, low, calm and quiet, polite and unhurried, never raising his voice, the sentence ending on a soft falling tone; even when flustered his volume stays the same and only the pauses get longer. He says: "리아, 봐봐. 다 읽었어. 근데 아무도 말을 안 해.".
```

```
DIALOGUE
The man speaks in natural native Korean, low, calm and quiet, polite and unhurried, never raising his voice, the sentence ending on a soft falling tone; even when flustered his volume stays the same and only the pauses get longer. Where the line breaks off he trails off, and the question stays quiet. He says: "읽은 건 아는데 왜…… 수만 형, 이거 정상이에요?".
```

8번과 10번의 FORMAT MODE, CAMERA, PERFORMANCE, AUDIO, POSITIVE LOCKS는 3번과 같은 골격이다. 8·10 PERFORMANCE에는 준호 고정 문장(코미디언, 목소리를 높이지 않음)이 들어가 있다.

### 작업 27
- 고친 파일: `01_EPISODES/EP01R/tools/build_clip_board.py`. `batch_qa.py`는 이 클론에 없어 저장 형식은 그대로 두고 읽기만 맞췄다.
- 맥 절대경로(`/Users/ymy/project/sns`)가 이 머신에 없으면 저장소 루트로 다시 찾는다. 컷 폴더 `video/v08/E1_nn/*_kling3_take*.mp4`를 `board_clips/media/`에 복사하고 `<select>`로 바꾼다. 기본 재생은 테이크 번호가 가장 큰 파일. QA JSON의 `clip`과 같은 테이크만 얼굴 4지점·whisper를 보여주고, 나머지는 「QA 없음」.
- 통과 식은 그대로다. 단일 샷이고, 얼굴 4지점 모두 ≥0.45, 얼굴 폭 ≥180px, whisper 일치 ≥85%일 때만 「통과」. 필터는 전체/통과/재생성.
- media 합이 60MB를 넘으면 수정시각이 오래된 테이크부터 빼는다. 최신 테이크와 540px 스틸 jpg는 남긴다. HTML은 `charset`·`title`·`style`·본문만이고 doctype/html/head/body 태그는 없다. 화면 문구에 비아/Bea를 넣지 않았다.
- 검증: 이 클론에는 `qa_*.json`·mp4·스틸 png가 없다. 컷 3·4·5·7·8·9·10·11·12·13·14·19·22 임시 13장으로 `python3 01_EPISODES/EP01R/tools/build_clip_board.py` → `13 cards, 11 pass` (4=내부 컷, 12=얼굴 0.20/100px). 생성 HTML에 article/video/select 각 13, 금지 태그 없음, 기본 선택은 take02, take01 옵션은 QA 없음. 헤드리스 크롬에서 재생성 필터가 4·12만 보이고, 통과 11, 전체 13. 3번 셀렉트를 take01로 바꾸면 문구가 QA 없음이고 영상 src가 바뀐다. take02는 `play()` 후 paused=false, readyState=4, currentTime>0. 390px 폭에서도 가로 스크롤 없이 2열 카드와 재생성 필터가 동작했다. 60MB 제외는 크기 목록으로 확인(가장 오래된 항목부터 탈락, 필수 파일은 유지). 이번 13장 media는 0.1MB라 제외 없음. 임시 파일·jpg·mp4·`board_clips/`는 커밋하지 않았다. 발행은 하지 않았다.
