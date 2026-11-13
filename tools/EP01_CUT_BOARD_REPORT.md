# 1화 컷 보드 — 콘티 연결 (작업 31)

생성: `python3 tools/series_cut_assets.py`
보드: `python3 tools/build_series_board.py` → `board_web/series.html#EP01/images`

수동 매핑 `tools/ep01_conti_links.json` 은 `tools/SCRIPT_CONTI_AUDIT.md` 3.3 초안 그대로다. 판정은 바꾸지 않았다.

## 활성 42컷

- 연결 6: 2, 11, 13, 14, 15, 19
- 참고만 8: 8, 9, 10, 12, 22, 23, 42, 45
- 확인 필요 1: 30
- 없음 27 (UI 6: 6, 16, 25, 28, 36, 38)
- skip 이면서 연결 표시(활성 집계 제외): 20, 21

## 썸네일

활성 상태 행은 15개(연결 6 + 참고만 8 + 확인 필요 1)다. 확인 필요 컷 30은 path가 없어 썸네일이 없다.
그림 경로 고유 13개. 같은 파일을 쓰는 컷은 8·23, 9·42, 13·45라 파일은 한 장만 만든다.
이 실행에서 실제로 쓴 콘티 썸네일: 0. 콘티 PNG는 저장소에 없고(이미지 git 제외) 있는 머신에서 다시 실행하면 채워진다.

## 영상

활성 컷에 지정된 clip 13. 파일이 있는 clip 0.
컷 3 기본 테이크 번호: 1. `_old` 파일은 후보에서 빼고, 영상은 `board_web/series_cuts/vid/` 심볼릭 링크만 만든다.

애니매틱 JSON·각본·frames·video 원본은 수정하지 않았다. 생성 API는 호출하지 않았다.
