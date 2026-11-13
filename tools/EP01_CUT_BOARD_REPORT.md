# 1화 컷별 자산 정리 보고

- 기준: `01_EPISODES/EP01R/edit/v06/animatic_E1_v062.json`
- 콘티 수동 매핑: `tools/ep01_conti_links.json` (SCRIPT_CONTI_AUDIT)
- 전체 행 45 / 활성 42 / skip [20, 21, 29]
- 이미지 있음 42 · 영상(선택 클립 존재) 13
- 콘티 linked 6 [2, 11, 13, 14, 15, 19] · reference 8 [8, 9, 10, 12, 22, 23, 42, 45] · check 1 [30] · unlinked 27
- 이미지 없음 컷: 없음
- 선택 클립 경로 있으나 파일 없음: 없음

## 컷3 검증

- 이미지: `01_EPISODES/EP01R/frames/v08/S_ria_island_act2_cu.png` exists=True
- 선택 클립: `01_EPISODES/EP01R/video/v08/E1_03/EP01R_E1_03_kling3_take01.mp4` exists=True
- default_take: 1 (take01이어야 함)
- takes: [1, 4, 5, 6]
- 콘티: unlinked / 그림 콘티 없음(prompts_E1 텍스트만)
- 컷2 콘티: linked path=`01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_cut02_board.png` basis=SCRIPT_CONTI_AUDIT 2.4 — 준호·소파·타이핑/삭제·시선 폰 일치
- 컷11 콘티: linked path=`01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_08_C11.png` basis=수만·카운터 뒤·피클 뚜껑·고개 안 듦 일치(frame_old F4). composition only
- 컷15 콘티: linked path=`01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_12_C15.png` basis=리아·수만 둘 다 프레임 밖 준호 봄 일치(frame_old T5는 C15에서 생성)
- 컷30 콘티: check path=`None` basis=지문 충돌: '다시 쇼파로 돌아간다' vs 무대 '소파로 돌아가지 않는다'
- 컷8 콘티: reference path=`01_EPISODES/EP01R/frames/v08/STORYBOARD/EP01_island_05_C08.png` basis=같은 비트(line_prev, frame_old J3) — 콘티 준호 아일랜드, 현재 소파

## 재생성

```sh
python3 tools/series_cut_assets.py
python3 tools/build_series_board.py
```

미리보기: `board_web/series.html#EP01/images`

바이너리·아바타·목업 PNG는 로컬 전용. 맵 JSON만 Git.
