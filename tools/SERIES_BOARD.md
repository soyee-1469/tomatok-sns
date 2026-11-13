# 회차 작업실

생성: `python3 tools/build_series_board.py`

미리보기: `python3 tools/serve_series_board.py` 실행 후 http://127.0.0.1:8765/series.html

첫 화면에서 회차를 고르고 이야기 / 콘티·기준 이미지 / 최종 제작으로 이동한다.
각본과 콘티는 어느 쪽부터 시작해도 된다. **장면(컷) 단위**로 각본 → 임시 제작 → 검토 → 수정 → 승인 흐름을 쓴다. 각본 전체가 확정돼야만 제작하는 구조가 아니다.

이미지 준비는 GPT 이미지가 기본이며 영상은 최종 확정과 사용자 명시 지시 이후 힉스필드에서 진행한다. **이 화면과 `tools/serve_series_board.py`는 생성 서비스를 호출하지 않는다.** (`board_web/serve.py`는 동일 서버 런처.)

## 검토 기록

컷별 테이크 선택·검토 상태(미검토/수정 요청/승인)·수정 메모·담당자(미지정/클로드/커서/코덱스)는
`tools/series_board_reviews.json`에 서버 API(`/api/reviews`)로 영구 저장된다.
브라우저 localStorage만 쓰지 않는다. 보드 HTML을 다시 생성해도 검토 기록은 유지된다.
담당자 지정은 기록 기능이며 외부 AI를 호출하지 않는다.

## 각본 동기화

생성기는 `00_MASTER_ASSETS/WORLD_PLANNING/`의 지정 각본을 `board_web/series_sources/`에 복사해 표시한다.
원본 각본은 수정하지 않는다. 화면에는 각본 파일명·버전·원본 수정 시각·화면 생성 시각을 표시한다.
회차 추가와 원문 경로는 `tools/build_series_board.py`의 EPISODES에서 관리한다.

- 1화: `EP01_SCRIPT_FINAL_v07.md`
- 2화: `EP02_SCRIPT_v08.md`
- 3화: `EP03_SCRIPT_v03.md`
- 4화: `EP04_SCRIPT_v02.md`

기존 EP02/status.json·1화 과거 상태 파일은 다른 제목/제작 단계의 옛 기록이므로 새 화면에서 자동 승인으로 해석하지 않는다.

## 콘티

2화: 컷별 비교 보드(`#EP02/images`) — 콘티·이미지·영상 3열. 맵 `tools/ep02_cut_asset_map.json`.
원본 시트 `EP02_v01_chatgpt_board_01~04.png` → 칸 `EP02_v01_01_C01.png` … `_42_C42.png` (INDEX: `EP02_v01_INDEX.md`).
이미지·영상 제작본은 아직 없어 콘티만 채워진다. 예전 `EP02_sofa_board_*`는 보존하되 새 화면에 표시하지 않는다.

1화 컷 보드 콘티 연결: `tools/SCRIPT_CONTI_AUDIT.md` → `tools/ep01_conti_links.json` → `series_cut_assets.py`.
C번호=컷번호 자동 매칭은 하지 않는다. `check`(컷 30)는 사용자 지문 확정 전.

다음 작업: 컷 30 지문 확정, 감사 3.2 사용자 판단, 작업 30(콘티 1/2화 토글). 영상 생성 권한은 부여되지 않았다.
