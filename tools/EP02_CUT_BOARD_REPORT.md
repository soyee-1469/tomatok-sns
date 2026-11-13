# 2화 컷별 자산 정리 보고

- 기준 콘티 문서: `01_EPISODES/EP02_싸움은모국어로/STORYBOARD/EP02_STORYBOARD_v01.md`
- 각본: `00_MASTER_ASSETS/WORLD_PLANNING/EP02_SCRIPT_v08.md`
- 활성 컷 42 · 콘티 linked 42 · 이미지 5 · 영상 0
- 콘티 미연결: 없음
- 이미지 연결 컷: [8, 11, 16, 18, 19] (`ep02_image_links.json`)
- 이미지 링크 파일: `tools/ep02_image_links.json`

콘티 C번호는 이 회차 새 시트 기준이라 컷 번호와 같다(1화 구번호 자동매칭과 무관).
시트2 칸 14~17 스케치 그림은 아직 구 영수증 → stale 배지 유지. USB 스틸은 컷16 이미지 열에 연결.

## 재생성

```sh
python3 tools/series_cut_assets_ep02.py
python3 tools/build_series_board.py
```

미리보기: `board_web/series.html#EP02/images`
