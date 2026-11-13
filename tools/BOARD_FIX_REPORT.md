# 회차 작업실 개선 보고

작성: 2026-11-13 · Cursor

## 요약

템플릿·생성기·로컬 서버를 수정해 최신 각본 동기화, 컷별 검토 JSON 영구 저장, 부분 UI 갱신, 장면별 작업 흐름 안내를 반영했다. `tools/SCRIPT_CONTI_AUDIT.md`가 없어 콘티 자동 매칭은 하지 않았다. 원본 각본·승인 에셋은 수정하지 않았다. 유료 영상 생성은 호출하지 않았다.

## 변경 파일

| 파일 | 내용 |
|---|---|
| `tools/series_board.html` | 각본 메타 표시, 검토 UI, 부분 갱신, 장면별 제작 안내 |
| `tools/build_series_board.py` | 각본 copy2 동기화, `script_version`/`script_mtime`/`built_at`, `__BOARD_META__` |
| `tools/serve_series_board.py` | `/api/reviews` GET·PUT·POST, `tools/series_board_reviews.json` 원자 저장 |
| `board_web/serve.py` | gitignore 폴더용 런처(tracked 서버를 실행) |
| `tools/series_board_reviews.json` | 검토 기록 저장소(보드 재생성과 독립) |
| `tools/SERIES_BOARD.md` | 장면별 흐름·저장·콘티 감사 규칙 문서 |
| `tools/series_board_status.json` | 상태 갱신 |
| `board_web/series.html` | 생성 결과(직접 편집 아님) |
| `board_web/series_sources/EP0*.md` | 원본 각본 사본 재동기화 |

기존 미커밋 변경(`series_cut_assets.py`, `ep01_cut_asset_map.json` 등)은 유지했다.

## 목표별 결과

### 1. 최신 각본 반영

- WORLD 원본 ↔ `board_web/series_sources/` 비교: EP01 v07, EP02 v08, EP03 v03, EP04 v02 모두 일치.
- 원본(`00_MASTER_ASSETS/WORLD_PLANNING/`)은 읽기만.
- 이야기 탭에 각본 파일명·버전·원본 수정 시각·화면 생성 시각 표시.
- `SCRIPT_CONTI_AUDIT.md` 없음 → 감사 결과 적용 없음.

### 2. 선택·검토 기록 저장

- 키: 회차 ID + 컷 ID (`episodes.EP01.cuts.3` 형식).
- 필드: `take`, `status`(pending/needs_fix/approved), `memo`, `assignee`(unassigned/claude/cursor/codex), `updatedAt`.
- 저장소: `tools/series_board_reviews.json` (localStorage 전용 아님).
- 저장 실패 시 하단 바에 오류 표시 + 다시 저장 버튼. 화면 `state.reviews`는 유지.
- 담당자 지정은 기록만. 외부 AI 호출 없음.

### 3. 검토 중 화면 유지

- 필터: 컷 `hidden` 토글(전체 재렌더 없음).
- 자막: `body.hide-caps` 클래스.
- 테이크 변경: 해당 컷 영상 `src`만 교체. 다른 `video[data-vid]` 재생 위치·일시정지 상태 복원.
- 지문 `<details>` open 집합 유지. 같은 탭 내 스크롤 유지.

### 4. 작업 흐름 안내

- “각본 전체 확정 후 제작” 문구 제거.
- 장면별 각본 → 임시 제작 → 검토 → 수정 → 승인 안내로 교체.
- 생성 서비스 호출 없음 명시.

### 5. 콘티 연결

- 감사 보고서 없음 → 임의 매칭 안 함.
- 1화 컷 보드 콘티 통계 유지: linked 0 / reference 0 / unlinked 42.

## 검증

| 항목 | 결과 |
|---|---|
| 각본 사본 == WORLD 원본 | 통과 |
| PUT `/api/reviews` 후 파일 반영 | 통과 (컷3 take4·수정요청, 컷7 승인) |
| 잘못된 JSON PUT → 400, 기존 기록 보존 | 통과 |
| 서버 재시작 후 GET 유지 | 통과 |
| `build_series_board.py` 재실행 후 검토 JSON 유지 | 통과 |
| `series.html` / 각본 소스 / EP03 UI / 컷 영상 링크 HTTP 200 | 통과 |
| 반응형 CSS(900·760) · viewport · 자료 링크 | 코드 확인 |
| 브라우저에서 테이크 변경 시 재생 유지 | 로컬 서버 기동 후 UI 로직으로 구현·수동 확인 권장 |

검증용으로 남긴 샘플 기록:

- EP01 컷 3: take 4 · 수정 요청 · 메모 “립싱크 재확인” · 커서
- EP01 컷 7: take 1 · 승인 · 클로드

미리보기: `python3 tools/serve_series_board.py` → http://127.0.0.1:8765/series.html

## 콘티 연결 후속 (2026-11-13, SCRIPT_CONTI_AUDIT 도착 후)

- `tools/ep01_conti_links.json` 추가 — 감사 §3.3 초안 그대로.
- `tools/series_cut_assets.py`가 수동 매핑을 `cuts_island`보다 먼저 적용. `check` 상태 추가.
- 활성 컷 통계: linked **6** (2·11·13·14·15·19) · reference **8** · check **1**(30) · unlinked **27**.
- skip 20·21도 매핑 메타는 유지(보드 활성 목록 제외).
- 검토 JSON·원본 각본·승인 에셋 미수정. 보드 재생성 후 검토 기록 유지 확인.

## 남은 문제

1. 컷 30 `check` — 지문 충돌, 사용자 확정 필요.
2. 감사 3.2 사용자 판단(1막 준호 위치, 네팔어 클립 재생성 범위 등).
3. 작업 30(콘티 1/2화 토글) 미착수.
4. 수만 네팔어 중얼 각본은 보드에 반영됐으나 Kling 클립 음성은 구버전일 수 있음 — 재생성은 별도 지시.
5. 커밋·푸시는 요청하지 않아 수행하지 않음.
