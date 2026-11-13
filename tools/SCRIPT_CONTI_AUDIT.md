# 각본·콘티 대조 감사 (2026-11-13)

작성: Claude Code. 범위: 이 보고서 한 파일만 생성. 각본·페이지·생성 코드·승인 에셋·JSON은 읽기만 했고 수정하지 않았다.
읽은 규칙: `PROJECT_WORKFLOW.md`, `00_MASTER_ASSETS/05_STYLE/blocking_rule.md`(§5 콘티, §7, §8), `00_MASTER_ASSETS/05_STYLE/suman_language_rule.md`, `tools/EP01_CUT_BOARD_PLAN.md`, `tools/CURSOR_TASKS.md` 작업 29·30.

---

## 1. 각본 대조 — `00_MASTER_ASSETS/WORLD_PLANNING/` vs `board_web/series_sources/`

### 1.1 요약

| 회차 | 원본 (WORLD_PLANNING) | 보드 사본 (series_sources) | 결과 | 최신성 |
|---|---|---|---|---|
| 1화 | `EP01_SCRIPT_FINAL_v07.md` (수정 11-13 11:18, **미커밋**) | `EP01_SCRIPT_FINAL_v07.md` (11-09 11:27) | **차이 3곳** (컷 11·12·13) | 원본이 최신. 사본 = git HEAD(`fb8dce2`)와 바이트 동일 |
| 2화 | `EP02_SCRIPT_v08.md` | `EP02_SCRIPT_v08.md` | 동일 | (대조 대상 외, 참고) |
| 3화 | `EP03_SCRIPT_v03.md` (수정 11-13 11:19, **미커밋**) | `EP03_SCRIPT_v03.md` (11-12 17:14) | **차이 1곳** (172행) | 원본이 최신. 사본 = HEAD와 동일 |
| 3화 (구) | `EP03_SCRIPT_v02.md` | `EP03_SCRIPT_v02.md` | 동일 | 보드가 쓰지 않는 사본(아래 1.3) |
| 4화 | `EP04_SCRIPT_v02.md` (수정 11-13 11:19, **미커밋**) | `EP04_SCRIPT_v02.md` (11-12 18:16) | **차이 3곳** (13·58·70행) | 원본이 최신. 사본 = HEAD와 동일 |
| 4화 (구) | `EP04_SCRIPT_v01.md` | `EP04_SCRIPT_v01.md` | 동일 | 보드가 쓰지 않는 사본 |

공통 원인: 세 파일의 차이는 전부 **2026-11-13 수만 언어 규칙**(`05_STYLE/suman_language_rule.md`, "사용자 확정 2026-11-13") 반영분이다. 원본은 오늘 고쳐졌고 아직 커밋되지 않았으며(`git status`: M), `board_web/`은 `.gitignore` 30행으로 제외된 로컬 빌드 산출물이라 빌드 전 상태(= HEAD)에 머물러 있다.

### 1.2 회차별 차이 상세

**1화 `EP01_SCRIPT_FINAL_v07.md`** (사본 기준 행 번호)

| 행 | 사본 (보드) | 원본 (최신) |
|---|---|---|
| 41–42 | **11.** (아무렇지 않다는 듯이 피클 뚜껑을 열며) / **수만**: 우리 집도 그래~ 읽기만 해... | **11.** (… 네팔어로 중얼거린다. 한국어 대사 없음) / **수만 — 네팔어 중얼거림의 뜻:** 우리 집도 그래. 읽기만 해. |
| 44 | **12.** (다행이라는 듯이, 기대하는 눈빛) | **12.** (… — 단어는 못 알아도 톤은 안다) |
| 47–48 | **13.** (피클 한입 씹으며 말한다. '새벽 4시에' 뒤 3초 정적…) / **수만**: 우리 엄마는 전화로만 하셔.. 새벽 4시에.. | **13.** (피클 한입 씹으며 네팔어로 중얼. 중얼 뒤 3초 정적…) / **수만 — 네팔어 중얼거림의 뜻:** 우리 엄마는 전화로만 해. 새벽 4시에. |

**3화 `EP03_SCRIPT_v03.md`**

| 행 | 사본 | 원본 |
|---|---|---|
| 172 | **수만** (어리둥절, 폰을 들어 보이며, 끝↑): "소고기는?" | 수만이 어리둥절한 얼굴로 폰을 들어 보인다. 네팔어로 짧게 중얼거린다. (뜻: 소고기는?) 말은 한국어로 하지 않는다. |

**4화 `EP04_SCRIPT_v02.md`**

| 행 | 사본 | 원본 |
|---|---|---|
| 13 | 수만은 간단한 한국어 인사·감탄은 할 수 있다. 재료·조리 순서처럼 길어지는 말은 어렵다. 순덕은 네팔어를 못한다. | 수만은 대면에서 네팔어로 중얼거리거나 손짓한다(2026-11-13). 한국어 장문·설명은 하지 않는다. 재료·조리 이야기는 토마톡 번역. 「감사합니다」처럼 짧은 인사만 예외. 순덕은 네팔어를 못한다. 상세: `05_STYLE/suman_language_rule.md`. |
| 58 | **수만** (바로 고개를 끄덕이며, 입 안의 밥을 삼키고, 끝↓): "네. 진짜 맛있어요." | 수만이 입 안의 밥을 삼키고 바로 고개를 끄덕인다. 엄지를 치켜 올려 보인다. 말은 없다. |
| 70 | **수만** (소개하고 싶어, 접시와 자기를 번갈아 가리키며, 끝↓): "아차르. 네팔… 제가 만들었어요." | 수만이 반가워하며 접시를 조금 밀어 보인다. 접시와 자기를 번갈아 가리키며 네팔어로 중얼거린다. (뜻: 아차르. 네팔 음식. 내가 만들었어요.) |

### 1.3 버전·최신성 확인 (근거)

확인된 사실
- `board_web/series_sources/*.md` 6개는 모두 `git show HEAD:…`와 diff 결과 동일. 즉 보드 사본은 "마지막 커밋 시점의 원본"이고, 오늘 작업분만 빠져 있다.
- `tools/build_series_board.py` 18–21행이 회차별 기준 각본을 고정한다: EP01 → `EP01_SCRIPT_FINAL_v07.md`, EP02 → `EP02_SCRIPT_v08.md`, EP03 → `EP03_SCRIPT_v03.md`, EP04 → `EP04_SCRIPT_v02.md`. `series_sources`의 `EP03_SCRIPT_v02.md`, `EP04_SCRIPT_v01.md`는 이 목록에 없는 **이전 빌드의 잔재**다(빌드 스크립트가 지우지 않음).
- 1화 v07 머리글: "STATUS: FINAL for animatic v06.2. 애니매틱 1화 JSON과 1:1. 산문(EP_PROSE_SCRIPT_v08.md 1화)과도 동기." 이 1:1 관계를 점검한 결과:
  - `01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json` 컷 11·13 `line`은 아직 한국어 발화("우리 집도 그래~ 읽기만 해...", "우리 엄마는 전화로만 하셔.. 새벽 4시에..") → 오늘 각본 변경(네팔어 중얼)이 **JSON에 반영되지 않음**.
  - `EP_PROSE_SCRIPT_v08.md`(11-12 16:46)에는 '네팔어' 0회 → 산문 v08도 미반영. 반면 `EP01_PROSE_SCRIPT_v06.md`는 오늘 같이 고쳐짐(미커밋, 68·74행).
  - 리아 영어 단어 4줄(31 "Yes." / 33 "Mom?" / 40 "Yep." / 42 "Wait.")은 각본 v07과 JSON이 일치(JSON `line_old_v07`에 이전 대사 보관). 11-09 저녁 "리아 영어 6줄 취소" 기록(STATE_TABLE)과 달리 이 4줄은 유지된 상태로 양쪽이 동기돼 있다.
- 3화: `EP03_SCRIPT_v02.md`「그건 우리가 따져요」와 `EP03_SCRIPT_v03.md`「오늘 못 와?」는 **같은 이야기의 버전이 아니라 다른 이야기**다(제목·로그라인·무대가 다름). v03 머리글 "사용자 확정 소재", 250행 "이 초안은 최종 확정 아님". 보드는 v03만 쓴다.
- 4화: `EP04_SCRIPT_v01.md`「반찬통 돌려주세요」→ `EP04_SCRIPT_v02.md`「조금만 주세요」. v02에 STATUS 줄 없음, 208행 "이미지·영상은 아직 생성하지 않음". 보드는 v02만 쓴다.
- 2화 v08: 양쪽 동일. 수만은 2화에 등장하지 않아("수만·하오는 없음(2층)") 오늘 규칙의 영향 없음.

불분명 (표시만, 판단은 사용자)
- [불분명] 1화 v07.1 머리글의 STATUS가 여전히 "FINAL"인데 오늘 컷 11·13 발화 방식이 바뀌었다. 이 변경이 FINAL 재확정인지, 적용 전 제안인지 각본에 표기가 없다.
- [불분명] 3화 v02(다른 이야기)와 4화 v01(구 제목)을 보관(참고)으로 두는지, 폐기 표시를 하는지 어디에도 적혀 있지 않다. 보드 사본에도 남아 있어 혼동 소지가 있다.
- [불분명] `EP_PROSE_SCRIPT_v08.md`가 여전히 1화의 "동기 대상 산문"인지, 아니면 `EP01_PROSE_SCRIPT_v06.md`(오늘 수정)가 대체했는지. v07 머리글은 v08을, 오늘 수정은 v06을 건드렸다.

---

## 2. 1화 콘티 대응 — `tools/ep01_cut_asset_map.json` 42컷 vs 기존 콘티

### 2.1 기준과 현재 상태
- 기준: `tools/ep01_cut_asset_map.json` (원본 `01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json`, 45행, 활성 42, skip 20·21·29). 이 맵의 `conti` 필드는 `tools/series_cut_assets.py`가 `cuts_island.json` 키 일치 또는 프롬프트/파일명 근거로만 채우며, 현재 **linked 0 · reference 0 · unlinked 42**(작업 29 의도: C번호 자동매칭 금지).
- 이 감사는 번호가 아니라 **인물·장소·행동·대사**로 대조했다. 번호 추적이 필요한 곳은 JSON의 `n_old`/`frame_old`/`src_old`/`line_prev` 필드와 `EP01_island_STATE_TABLE.md` "기존 프레임" 열을 근거로 썼다.

### 2.2 기존 콘티 자료 목록 (1화에 쓸 수 있는 것 전부)

| ID | 파일 | 생성 | 내용 | 비고 |
|---|---|---|---|---|
| A. 아일랜드 콘티 12칸 | `01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_01_C07a.png` … `_12_C15.png` (원본 그리드 `EP01_island_board_01.png`, 보드 사본 `board_web/series_img/EP01_island_*.jpg`) | 11-06 10:05 | 칸1 CUT7 준호 소파에서 반쯤 일어남(시선 아일랜드) / 칸2 CUT7 end 오른쪽 퇴장 / 칸3 CUT8 start 리아 스툴+수만 피클병 / 칸4 CUT8 enter 준호 왼쪽 진입 / 칸5 CUT8 준호 아일랜드 옆에서 폰 보여줌 / 칸6 CUT9 OTS 리아→준호 / 칸7 CUT10 준호→수만 / 칸8 CUT11 수만 피클병 뚜껑 / 칸9 CUT12 준호 아일랜드 쪽 기울임 / 칸10 CUT13 수만 CU 씹기 / 칸11 CUT14 준호 CU 폰 / 칸12 CUT15 리아·수만 투샷, 둘 다 프레임 밖 준호 봄 | **C번호 = `cutlist_v08_plan.md`(극본 v06.2) 번호**이며 현재 JSON 번호가 아님. 얼굴이 그려져 있음(11-06 "얼굴 없는 콘티" 규칙 이전) → 스틸 참조 시 "composition only" 필수(STATE_TABLE 검수 메모). 칸5·7·9는 준호가 아일랜드에 서 있는 **구 1막 동선**(11-06 오후 "2막 구조" 변경으로 1막 준호는 소파에 남음) |
| B. 컷 2 단칸 콘티 | `…/STORYBOARD/EP01_cut02_board.png` | 11-06 15:32 | "CUT 2 sofa-axis" 얼굴 없는 준호, 소파 가운데, 폰 타이핑→삭제, 머리 긁기, looks at phone | 현행 규칙(얼굴 없음·시선 화살표)으로 만든 유일한 1화 칸. `prompts_E1/sheet_01.txt` Panel 2의 실현본 |
| C. ChatGPT 시트 프롬프트 4장 | `…/STORYBOARD/prompts_E1/sheet_01.txt`~`sheet_04.txt`, `INDEX.md` (`tools/make_storyboard_prompts.py` 출력) | 11-06 12:43 | 현재 JSON 번호로 42칸(1~44, skip 21·29 제외) 프롬프트 | **이미지 없음**(프로젝트 안에서 해당 시트 PNG 미발견, B 한 칸만 존재). 45번(엔딩 CU) 칸 없음(44컷 시점 생성). 여러 칸이 옛 상황+새 지문을 함께 담아 자기모순(2.5 참조) |
| D. `cuts_island.json` | `…/STORYBOARD/cuts_island.json` | 11-06 10:39 | 생성 스틸 ↔ 콘티 칸 매핑: `J2b_junho_exit_right_r1`→C07b, `B13_ria_island_start`→C08a, `J9b_junho_crossing_shoes`→C08b, `T5_ria_suman_look_left_r1`→C15 (r2·J9c·J9d는 sketch 없음) | 현재 JSON의 `frame` 키(S_*, H*, G13 등)와 하나도 겹치지 않아 자동 매칭 0건이 된 원인 |
| E. 2화 소파 콘티 | `…/STORYBOARD/EP02_sofa_board_01~04.png`, `EP02_sofa_panels/` | 11-09 | 2화 | 1화 자료 아님. `01_EPISODES/EP02_싸움은모국어로/STORYBOARD/EP02_STORYBOARD_v01.md`가 "참고만, 본 파일이 대체"로 표기 |
| F. 구 프로젝트 콘티 | `01_EPISODES/EP01/storyboard.md` (SUPERSEDED 10-27, 카페·구 캐스트), `01_EPISODES/EP001_FAMILY_GROUP_CHAT/02_STORYBOARD/` | 10월 | 다른 캐스트·다른 무대 | 현재 1화와 무관. 자료로 치지 않음 |

### 2.3 번호 추적 근거 (A 콘티 ↔ 현재 컷)

`EP01_island_STATE_TABLE.md` 첫 표의 "기존 프레임" 열과 JSON의 이전 프레임 필드가 같은 프레임 ID를 가리킨다.

| 콘티 칸 | 콘티 프레임 ID (STATE_TABLE) | 현재 컷 | JSON 근거 |
|---|---|---|---|
| C07a | J2 | 19 (활성), 20 (skip) | 19 `src_old` = frames/v07/J2_junho_halfstand.png / 20 `src_old` = J2_junho_halfstand_r2, `n_old` 8 |
| C07b | J2b | 20 (skip) | `cuts_island.json["J2b_junho_exit_right_r1"].sketch` = C07b |
| C08a / C08b | B13 / J9d | 21 (skip) | `cuts_island.json` B13→C08a, J9b→C08b; 21 `frame_old` J9_junho_crossing, `n_old` 9 |
| C08 | J3 | 8 | `n_old` 10, `frame_old` J3_junho_at_island_r2, `line_prev` "리아 봐봐. 다들 읽으셨는데……" |
| C09 | B5 (OTS) | 9 | `n_old` 11, `frame_old` B5_ots_island_r2_r1 |
| C10 | J3 변형 | 10 | `n_old` 12, `frame_old` J3_junho_at_island_r3, `line_prev` "…수만 형, 이거 정상이에요?" |
| C11 | F4 | 11 | `n_old` 13, `frame_old` EP01R_F4_suman_island_med_r2_r1 |
| C12 | J3 변형 | 12 | `n_old` 14, `line_prev` "그럼 대답은 언제 와요?…" |
| C13 | S2 | 13 | `n_old` 15, `frame_old` S2_suman_chew_r1 |
| C14 | J4 | 14 | `n_old` 16, `frame_prev` J4_junho_cu_r2, `line_prev` "……저 알람 맞출게요." |
| C15 | F4+B3 → 신규 투샷 | 15 | `n_old` 17, `frame_old` T5_ria_suman_look_left_r1 (C15에서 생성) |

단, 번호가 이어진다고 바로 연결하지 않았다. 아래 표에서 **위치·샷·행동이 현재 지문과 다르면 '참고만 가능'**으로 내렸다.

### 2.4 컷별 판정 (45행, 활성 42 + skip 3)

판정 기준: 연결 가능 = 인물·장소·행동(+대사 비트)이 현재 지문과 일치 / 참고만 가능 = 같은 비트나 공통 구도이지만 위치·샷·행동 중 하나가 다름 / 자료 없음 = 그림 콘티 없음(프롬프트 텍스트만 있어도 '없음') / 확인 필요 = 지문·각본 자체가 모순이라 콘티를 정할 수 없음.

| 컷 | 인물 | 현재 내용 (JSON) | 현재 프레임 | 콘티 식별자 | 판정 | 근거·메모 |
|---|---|---|---|---|---|---|
| 1 | — | 오프닝 와이드, 준호 혼자 소파 | W1c_opening_junho_only | (sheet_01 P1 텍스트만) | 자료 없음 | |
| 2 | 준호 | 인사말 여섯 번째 지우는 중 (CU) | R02c_junho_cu_typing_crop | **EP01_cut02_board.png** (CUT 2 sofa-axis) | **연결 가능** | 준호·소파 가운데·폰 타이핑/삭제·머리 긁기·시선 폰 일치. 콘티는 미디엄, 현재 프레임은 CU 크롭(샷 사이즈만 다름) |
| 3 | 리아 | "오빠, 인사말 정리됐어? 지금 초대할게?" | S_ria_island_act2_cu | (sheet_01 P3) | 자료 없음 | |
| 4 | 준호 | "남자친구? 예비신랑? …" | S_junho_sofa_cu | (sheet_01 P4, 옛 대사 '22명 첫인상') | 자료 없음 | |
| 5 | 리아 | "내가 잘 말해뒀어…" | S_ria_island_act1_cu | (sheet_01 P5) | 자료 없음 | |
| 6 | UI | U05_READ0 | — | — | 자료 없음 (UI, 콘티 대상 아님) | |
| 7 | 준호 | "어....." 눈 ECU | F2E_junho_eyes | (sheet_01 P7) | 자료 없음 | |
| 8 | 준호 | "다들 읽으셨는데… 아무도 답변을 안 해주셔…" **소파** | S_junho_sofa_cu | EP01_island_05_C08 (칸5) | 참고만 가능 | 같은 대사 비트(`line_prev` "리아 봐봐. 다들 읽으셨는데", `frame_old` J3 = 칸5 프레임). 콘티는 준호가 **아일랜드 옆에 서서** 폰을 보여줌, 현재 지문은 소파 착석 → 위치 불일치 |
| 9 | 리아 | "다들 뭐라고 답장할까 고민 중이실 거야." | S_ria_island_act1_cu | EP01_island_06_C09 (칸6 OTS) | 참고만 가능 | 같은 비트(`frame_old` B5_ots). 현재 지문(sheet_01 P9) "OTS 아님(1막)" → 샷 불일치 |
| 10 | 준호 | "수만이 형.. 기다리면 되겠죠?" 소파에서 고개 | S_junho_sofa_cu | EP01_island_07_C10 (칸7) | 참고만 가능 | 같은 비트(`line_prev` "수만 형, 이거 정상이에요?"). 콘티 준호 아일랜드 옆 / 현재 소파 |
| 11 | 수만 | 피클 뚜껑 열며 (원본 각본 11-13: 네팔어 중얼, 한국어 대사 없음) | S_suman_island_cu | **EP01_island_08_C11** (칸8) | **연결 가능** | 수만·카운터 뒤·피클병 뚜껑·고개 안 듦·시선 병 일치(`frame_old` F4). 콘티 왼쪽 가장자리의 준호 팔은 현재 단독 프레임에 없음(무시). 오늘 각본 변경은 발화 방식만 바뀌고 동작 동일 |
| 12 | 준호 | "누구 한 분은 답변해 주시겠죠?" CU | J4_junho_cu_r1 | EP01_island_09_C12 (칸9) | 참고만 가능 | 같은 비트(`line_prev` "그럼 대답은 언제 와요"). 콘티 준호 아일랜드 위로 기울임 / 현재 소파 CU |
| 13 | 수만 | 피클 씹으며 "새벽 4시" (원본 11-13: 네팔어 중얼) + 3초 씹기 | S_suman_island_look_cu | **EP01_island_10_C13** (칸10) | **연결 가능** | 수만 CU·피클 씹기·시선 준호(카메라 왼쪽) 일치(`frame_old` S2_suman_chew_r1). 동작 동일 |
| 14 | 준호 | "…아… 전화가 오면 어쩌지…" CU | J4_junho_cu_r1 | **EP01_island_11_C14** (칸11) | **연결 가능** | 준호 CU·폰 불빛·시선 폰 일치(같은 비트, `line_prev` "저 알람 맞출게요"). 메모: 칸11은 얼굴 디테일(안경·머리) 있음 → "composition only"(STATE_TABLE 검수 메모). 11-09 기록의 "J4 축 불일치(S_junho_sofa_cu와 배경 다름)" 지적은 프레임 문제이지 콘티 문제는 아님 |
| 15 | — | 수만 처음 고개 듦, 리아 폰에서 눈 뗌 | G13_island_master_act1 | **EP01_island_12_C15** (칸12 투샷) | **연결 가능** | 리아·수만 둘 다 프레임 밖 왼쪽(준호) 봄 일치. 콘티에서 생성한 T5_ria_suman_look_left_r1이 `frame_old`로 남아 있고 현재 프레임은 G13 마스터 → 어느 프레임을 쓸지는 사용자 판단(3절) |
| 16 | UI | U11_WEATHER | — | — | 자료 없음 (UI) | |
| 17 | — | 폰 뒤집어 둠, 리아 폰 띠링 | F1c_phone_table_center | (sheet_02 P5) | 자료 없음 | |
| 18 | — | 리아 웃음 참기 | H18_ria_laugh_hand | (sheet_02 P6) | 자료 없음 | |
| 19 | 준호 | "어? 뭐야 뭐야, 뭔데? 나도 보여줘." 벌떡 | J2c_halfstand_curious | **EP01_island_01_C07a** (칸1) | **연결 가능** | 준호 소파에서 반쯤 일어남·폰 오른손·시선 아일랜드(리아·수만) 일치(`src_old` J2_junho_halfstand). cutlist_v08_plan에서도 7·19 모두 J2 프레임 |
| 20 | skip | 준호 일어나 오른쪽 퇴장 | J2b_junho_exit_right_r2 | EP01_island_02_C07b (칸2) | 연결 가능 (skip) | `cuts_island.json` J2b_r1.sketch = C07b. r2는 콘티 소파 각도 오류로 콘티 참조를 빼고 재생성(STATE_TABLE 생성 결과 칸2). 렌더·보드 제외 컷 |
| 21 | skip | 이동 Kling (B13 → J9d) | E1_08_WALK take01 | EP01_island_03_C08a + 04_C08b (칸3·4) | 연결 가능 (skip) | `cuts_island.json` B13→C08a, J9b→C08b. 사용자 "굳이 없어도" → skip |
| 22 | 리아 | "다들 준호한테 무슨 말 할지 나한테 다 물어보고있어" 걸어오는 준호에게 폰 보여줌 | S_ria_island_act2_cu | EP01_island_04_C08b (칸4) | 참고만 가능 | 준호 진입·리아 고개 들어 준호 봄 구도 일치. 콘티엔 리아 대사·폰 보여주기 없음. sheet_02 P9 프롬프트는 옛 상황("폰을 가슴에 엎어 숨긴다: 가족방 아니야") |
| 23 | 준호 | "편하게 말하시지.." 리아 폰 함께 봄 | S_junho_island_r2 | EP01_island_05_C08 (칸5) | 참고만 가능 | 준호 아일랜드 옆·리아 스툴·수만 뒤 배치 일치. 콘티는 준호가 **자기 폰**을 보여줌, 현재는 **리아 폰**을 같이 봄 → 행동 다름 |
| 24 | 리아 | "다들 궁금한게 많긴 하신가봐" 서로 쳐다봄 | S_ria_island_act2_cu | — | 자료 없음 | 2막 3인 배치는 칸7(C10)·칸9(C12) 참고 가능하나 행동 불일치 |
| 25 | UI | U18b_DMLIST | — | — | 자료 없음 (UI) | |
| 26 | 준호 | "……이게 뭐야." | S_junho_island_r2 | (sheet_03 P1) | 자료 없음 | |
| 27 | 리아 | "보내도 괜찮을지 체크해달래" | S_ria_island_act1_cu | (sheet_03 P2, 옛 대사 '검사') | 자료 없음 | |
| 28 | UI | U20b_MAMA_DM | — | — | 자료 없음 (UI) | |
| 29 | skip | U21b_DM_QUESTIONS | — | — | 자료 없음 (skip, UI) | |
| 30 | 준호 | "……스물한 명이 지금 나한테 물어볼 걸 너한테 검사받는 중이라고?" | S_junho_island_r2 | — | **확인 필요** | JSON·각본 v07 지문 "준호 다시 쇼파로 돌아간다."가 같은 각본의 무대 설명("준호는 소파로 돌아가지 않는다"), 컷 37 지문("소파로 돌아가지 않음"), sheet_03 P4("리아 옆에 그대로 서 있음")와 충돌. 동선이 정해져야 콘티 대응이 가능 |
| 31 | 리아 | "Yes. 단톡방에 쓰면 다들 보니까…" | S_ria_island_act2_cu | (sheet_03 P5, 옛 대사) | 자료 없음 | |
| 32 | 준호 | "어머님 아버님도?" | S_junho_island_r2 | (sheet_03 P6) | 자료 없음 | |
| 33 | 리아 | "Mom? 엄마가 제일 무서워해." | S_ria_island_act2_cu | (sheet_03 P7) | 자료 없음 | |
| 34 | 준호 | "……나만 무서운 줄 알았는데." 입꼬리 | S_junho_island_r2 | (sheet_03 P8) | 자료 없음 | |
| 35 | 리아 | "오빠, 나 빨리 답변해드려야해~" | S_ria_island_act1_cu | (sheet_03 P9, 옛 대사 '대기 열한 명') | 자료 없음 | |
| 36 | UI | U33b_BEA_REPLIES | — | — | 자료 없음 (UI) | |
| 37 | — | 준호 아일랜드 옆에서 자기 폰 꺼냄 | S_junho_island_r2 | (sheet_03 P11) | 자료 없음 | |
| 38 | UI | U25b_MAMA_EAT | — | — | 자료 없음 (UI) | |
| 39 | 준호 | "리아! 어머니가 밥 먹었냬!" 폰 번쩍 | H39_junho_joy | — | 자료 없음 | `frame_old` J2_junho_halfstand_r2(소파 반쯤 일어남)는 칸1(C07a) 구도와 같지만 현재 위치는 아일랜드(2막) → 콘티로 쓸 수 없음 |
| 40 | 리아 | "Yep. 방금 그렇게 보내시라고…" CU | S_ria_island_act2_cu | (sheet_04 P2) | 자료 없음 | |
| 41 | 준호 | "나 밥 먹었어. 먹었다고 보내도 돼?" | S_junho_island_r2 | (sheet_04 P3) | 자료 없음 | |
| 42 | 리아 | "……Wait. 오빠도 검사받게?" OTS, 준호 올려다봄 | S_ria_island_act2_cu | EP01_island_06_C09 (칸6 OTS) | 참고만 가능 | 지문 "OTS, 리아가 준호를 올려다봄" = 칸6 구도(준호 어깨 너머 리아 looks at Junho), `frame_old` B5_ots_island. 콘티 의도는 1막 "읽었잖아"였으므로 구도만 |
| 43 | 준호 | "응." 폰 두 손으로 내밈 | H43_junho_submits_phone | (sheet_04 P5) | 자료 없음 | |
| 44 | — | 엔딩 와이드, 수만 절레절레 + 빈 피클병 | H44e_suman_headshake_emptyjar | (sheet_04 P6, 옛 엔딩 자막) | 자료 없음 | |
| 45 | 수만 | 수만 CU 절레절레, 대사 없음 | H44e_crop_suman_cu | EP01_island_10_C13 (칸10) | 참고만 가능 | 수만 CU·피클병·아일랜드 샷 사이즈만 참고. 행동(씹기 ↔ 절레절레)·소품(빈 병) 다름. sheet_04에 45 칸 없음 |

### 2.5 집계

| 판정 | 활성 컷 | 컷 번호 |
|---|---|---|
| 연결 가능 | 6 | 2, 11, 13, 14, 15, 19 (+ skip 20, 21) |
| 참고만 가능 | 8 | 8, 9, 10, 12, 22, 23, 42, 45 |
| 확인 필요 | 1 | 30 |
| 자료 없음 | 27 | 1, 3, 4, 5, 6(UI), 7, 16(UI), 17, 18, 24, 25(UI), 26, 27, 28(UI), 31, 32, 33, 34, 35, 36(UI), 37, 38(UI), 39, 40, 41, 43, 44 |

자료 없음 27컷 중 UI 6컷을 빼면 **그림 콘티가 없는 인물 컷은 21컷**이다. 이 21컷 전부 `prompts_E1/sheet_01~04.txt`에 프롬프트는 있으나 이미지는 만들어지지 않았다.

### 2.6 `prompts_E1` 시트 프롬프트의 문제 (이미지 생성 전 확인용)

`tools/make_storyboard_prompts.py`가 JSON의 `situation`+`action`+`dir_override`를 그대로 이어 붙여서, 한 칸에 옛 상황과 새 지문이 같이 들어간 칸이 있다. 그대로 ChatGPT에 넣으면 칸이 모순된다.

| 시트/칸 | 컷 | 모순 내용 |
|---|---|---|
| sheet_01 P4 | 4 | "22명이면 첫인상 22개라는 논리"(옛 대사) vs 현재 "남자친구? 예비신랑?…" |
| sheet_01 P8 | 8 | "리아 옆에 서서 폰을 얼굴 앞에 들이민다" vs "소파 가운데 앉아 폰을 아일랜드 쪽으로 들어 보이며 (1막 소파)" |
| sheet_01 P11 | 11 | 같은 문장 3회 반복 + "그옆에 서서 쩔쩔매는 준호"(1막엔 준호가 소파) |
| sheet_02 P9 | 22 | "폰을 가슴에 엎어 숨긴다: 가족방 아니야"(옛) vs "핸드폰을 보여주며 말한다"(현재) |
| sheet_02 P10 | 23 | "가족방은 묵념 중이잖아, 그럼 뭔데"(옛 대사) |
| sheet_03 P2 | 27 | "리아: 검사"(옛 대사) |
| sheet_03 P4 | 30 | "리아 옆에 그대로 서 있음" ↔ JSON 지문 "다시 쇼파로 돌아간다" (2.4 컷 30) |
| sheet_03 P5·P9 | 31, 35 | 옛 대사("응, 다들 틀릴까 봐…", "대기 열한 명") |
| sheet_04 P6 | 44 | 엔딩 자막 옛 문구("당신 가족도 단톡방에 쓰기 전에 검사받나요?") vs 각본 "느낌표 개수 고민하신 적 있나요?"; 45 칸 없음 |
| 공통 | 11, 13 | 수만 발화가 한국어로 적혀 있음(오늘 각본: 네팔어 중얼). 콘티엔 말풍선이 없어 그림엔 영향 없지만 라벨 문구는 갱신 필요 |

---

## 3. 확인된 사실 / 사용자 판단 필요

### 3.1 확인된 사실 (근거 파일로 재현 가능)
1. 1·3·4화 보드 사본은 git HEAD와 동일하고, 원본과의 차이는 전부 11-13 수만 언어 규칙 반영분(1화 3곳, 3화 1곳, 4화 3곳)이다. 2화는 동일.
2. 오늘 각본 변경은 1화 애니매틱 JSON(컷 11·13 line)과 `EP_PROSE_SCRIPT_v08.md`에 반영되지 않았다. `EP01_PROSE_SCRIPT_v06.md`에는 반영됐다(미커밋).
3. 1화 그림 콘티는 세 종류뿐이다: 아일랜드 12칸(구 번호, 얼굴 있음), 컷 2 단칸(현행 규칙), 그리고 이미지 없는 프롬프트 42칸.
4. 아일랜드 콘티의 C번호는 `cutlist_v08_plan.md` 번호이며 현재 JSON 번호와 다르다. JSON `n_old`·`frame_old`로 추적하면 C07a→19/20, C07b→20, C08a·b→21, C08→8, C09→9, C10→10, C11→11, C12→12, C13→13, C14→14, C15→15로 이어지지만, 그중 8·9·10·12는 11-06 오후 "준호 1막 소파 고정" 변경으로 **위치·샷이 달라져** 콘티로 쓸 수 없다.
5. 42컷 중 콘티를 바로 연결할 수 있는 컷은 6개(2·11·13·14·15·19), 구도 참고만 8개, 그림 콘티 없음 27개(UI 6 포함), 지문 모순 1개(30).
6. `series_cut_assets.py`의 자동 매칭(`cuts_island.json` 키 = JSON `frame`)은 현재 프레임 키 체계(S_*/H*/G13/J2c/R02c)와 겹치는 키가 없어 앞으로도 0건이다. 위 판정을 보드에 올리려면 수동 매핑 입력이 필요하다(3.3).

### 3.2 사용자 판단이 필요한 항목
1. **1막 준호 위치 확정**: 현재 JSON·각본은 1막 소파 고정. 이대로면 아일랜드 콘티 칸5·6·7·9(C08·C09·C10·C12)는 1화에서 은퇴시키고 컷 8·9·10·12는 새 콘티가 필요하다. 반대로 콘티대로 아일랜드에 서게 되돌리면 11-06 테이크(소파 CU 클립)와 어긋난다.
2. **컷 30 지문 충돌**: "다시 쇼파로 돌아간다" vs "소파로 돌아가지 않는다". 어느 쪽인지 각본에서 확정해야 콘티·스틸·클립 판단이 가능하다. (각본은 수정하지 않았다.)
3. **컷 15 프레임**: 콘티 C15와 일치하는 컷이지만 현재 프레임은 G13 마스터, 콘티에서 뽑은 T5 투샷은 `frame_old`로 밀려 있다. 어느 프레임을 기준으로 둘지.
4. **컷 11·13 발화 방식 변경의 적용 범위**: 오늘 각본(네팔어 중얼)을 JSON·보드 자막·11-06 take01(한국어 발화 클립)에도 적용할지, 아니면 각본만 바꾼 상태로 둘지. 적용하면 두 클립은 재생성 대상이 되고 콘티는 그대로 쓸 수 있다(동작 동일).
5. **빠진 콘티 21컷(인물 컷)의 생성 여부·방식**: `prompts_E1` 시트를 그대로 쓰지 말고 2.6의 모순을 정리한 뒤 ChatGPT 시트(얼굴 없음, 12칸 그리드)로 뽑을지. `EP01_CUT_BOARD_PLAN.md` 기준 새 콘티 생성은 그록봇 담당.
6. **아일랜드 콘티의 얼굴**: 11-06 "얼굴 없는 콘티" 규칙 이전 자료다. 연결 가능 컷(11·13·14·15·19)에 쓰더라도 "composition only" 참조로 제한할지, 얼굴 없는 버전으로 다시 뽑을지.
7. **보드 사본 정리**: `series_sources`의 `EP03_SCRIPT_v02.md`(다른 이야기)·`EP04_SCRIPT_v01.md`(구 제목)를 남길지. 그리고 1·3·4화 보드 사본을 오늘 원본으로 갱신(빌드 재실행)할지 — 미커밋 상태라 빌드 전 커밋 여부도 포함.
8. **1화 각본 STATUS**: v07.1 "FINAL" 표기를 오늘 변경 이후에도 유지할지, v07.2로 올릴지.

### 3.3 커서 반영 안내 (제안, 코드 변경은 하지 않음)
- 자동 매칭 대신 수동 매핑 파일을 하나 두고 `series_cut_assets.py`가 `cuts_island.json`보다 먼저 읽게 하면 위 판정을 보드 "콘티" 열에 그대로 올릴 수 있다. 제안 파일명 `tools/ep01_conti_links.json`. 상태값은 기존 `linked / reference / unlinked`에 `check`(확인 필요) 하나만 추가.
- 아래는 이 보고서의 판정을 그대로 옮긴 초안이다(경로는 저장소 루트 기준, 모두 존재 확인함).

```json
{
  "2":  {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_cut02_board.png",      "basis": "SCRIPT_CONTI_AUDIT 2.4 — 준호·소파·타이핑/삭제·시선 폰 일치"},
  "8":  {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_05_C08.png",   "basis": "같은 비트(line_prev, frame_old J3) — 콘티 준호 아일랜드, 현재 소파"},
  "9":  {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_06_C09.png",   "basis": "같은 비트(frame_old B5) — 현재 지문 OTS 아님"},
  "10": {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_07_C10.png",   "basis": "같은 비트(line_prev) — 콘티 준호 아일랜드, 현재 소파"},
  "11": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_08_C11.png",   "basis": "수만·카운터 뒤·피클 뚜껑·고개 안 듦 일치(frame_old F4). composition only"},
  "12": {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_09_C12.png",   "basis": "같은 비트 — 콘티 준호 아일랜드, 현재 소파 CU"},
  "13": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_10_C13.png",   "basis": "수만 CU·씹기·시선 준호 일치(frame_old S2). composition only"},
  "14": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_11_C14.png",   "basis": "준호 CU·폰 불빛·시선 폰 일치(frame_prev J4). composition only(얼굴 디테일)"},
  "15": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_12_C15.png",   "basis": "리아·수만 둘 다 프레임 밖 준호 봄 일치(frame_old T5는 C15에서 생성)"},
  "19": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_01_C07a.png",  "basis": "준호 소파 반쯤 일어남·폰·시선 아일랜드 일치(src_old J2)"},
  "20": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_02_C07b.png",  "basis": "cuts_island.json J2b_r1.sketch (skip 컷)"},
  "21": {"status": "linked",    "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_03_C08a.png",  "basis": "cuts_island.json B13.sketch; 끝 프레임 C08b (skip 컷)"},
  "22": {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_04_C08b.png",  "basis": "준호 진입·리아 고개 듦 구도만. 콘티에 리아 대사·폰 없음"},
  "23": {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_05_C08.png",   "basis": "3인 배치 일치 — 콘티 준호 자기 폰, 현재 리아 폰 함께 봄"},
  "30": {"status": "check",     "path": null,                                                                  "basis": "지문 충돌: '다시 쇼파로 돌아간다' vs 무대 '소파로 돌아가지 않는다'"},
  "42": {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_06_C09.png",   "basis": "OTS 리아→준호 구도 일치, 콘티 의도는 1막 대사"},
  "45": {"status": "reference", "path": "01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_10_C13.png",   "basis": "수만 CU 샷 사이즈만. 행동·소품 다름"}
}
```

- 위 파일에 없는 컷은 지금처럼 `unlinked`로 두되 reason을 "그림 콘티 없음(prompts_E1 텍스트만)"로 바꾸면 UI와 인물 컷이 구분된다(UI 컷 6·16·25·28·36·38은 "UI, 콘티 대상 아님").
- 보드 각본 탭을 오늘 원본과 맞추려면 `python3 tools/build_series_board.py` 재실행이 필요하다(사용자 판단 7번 뒤에).

---

## 부록 — 읽은 파일
- 각본: `00_MASTER_ASSETS/WORLD_PLANNING/EP01_SCRIPT_FINAL_v07.md`, `EP01_PROSE_SCRIPT_v06.md`, `EP_PROSE_SCRIPT_v08.md`, `EP02_SCRIPT_v08.md`, `EP03_SCRIPT_v02.md`, `EP03_SCRIPT_v03.md`, `EP04_SCRIPT_v01.md`, `EP04_SCRIPT_v02.md`; `board_web/series_sources/*.md`(6)
- 규칙: `PROJECT_WORKFLOW.md`, `05_STYLE/blocking_rule.md`, `05_STYLE/suman_language_rule.md`, `tools/EP01_CUT_BOARD_PLAN.md`, `tools/EP01_CUT_BOARD_REPORT.md`, `tools/CURSOR_TASKS.md`
- 컷·콘티: `tools/ep01_cut_asset_map.json`, `01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json`, `01_EPISODES/EP01R/cutlist_v06.md`, `cutlist_v08_plan.md`, `frames/v07/INDEX.md`, `frames/v08/STORYBOARD/{EP01_island_STATE_TABLE.md, cuts_island.json, EP01_island_01..12_*.png, EP01_island_board_01*.png, EP01_cut02_board.png, prompts_E1/*}`, `video/v08/board_default_takes.json`
- 코드(읽기만): `tools/series_cut_assets.py`, `tools/build_series_board.py`, `tools/make_storyboard_prompts.py`, `tools/split_storyboard.py`, `tools/gen_from_conti.py`, `01_EPISODES/EP01R/tools/gen_conti_island.py`
