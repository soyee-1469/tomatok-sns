# 3화 단톡 UI 검수 — 2026-11-12

검수: Codex. 원격 참고 커밋: `origin/cursor/ep03-chat-ui` / `116ca3d`.
원격 브랜치는 기능 초안이다. 로컬의 공지 바·번역 스택·최신 대사·하오 아바타 수정본을 기준으로 보완하여 main에 코드로 반영한다. 원격 커밋을 그대로 merge한 것은 아니다.

## 반영

- 노란 공지 카드 대신 흰 확성기 공지 바, 클릭·키보드로 펼침.
- `render_ui_v2.py`를 참고한 흰 한국어 번역 + 회색 원문 스택. 준호만 내 메시지 색.
- CAST 아바타 8개를 로컬 `board_web/ep03_chat/avatars`로 복사. 리아 BEA, 하오 DOYUN 및 중국 국기. 오늘 수정된 로컬 DOYUN_AV를 보존하며 새 얼굴을 생성하지 않음.
- 원본·템플릿·렌더러가 파일로 분리되어 재생성 시 로컬 스타일이 사라지지 않음.
- `--screens` 옵션으로 830×1800 앱 화면 6장과 기존 `phone_mockup.py` 공용 셸 목업 6장 출력. 생성 API 호출 없음.
- UI 상태별 화면 PNG·목업 링크. 390px에서 가로 넘침 수정.
- 시리즈 빌드에서 UI 렌더 실패를 무시하지 않도록 check=True.

## 실행과 로컬 결과

```sh
python3 tools/render_ep03_chat.py --screens
python3 tools/build_series_board.py
```

- 앱 미리보기: `board_web/ep03_chat/index.html`
- 화면: `board_web/ep03_chat/screens/S1.png` ~ `S6.png`
- 공용 목업: `board_web/ep03_chat/screens/S1_MOCKUP.png` ~ `S6_MOCKUP.png` (1122×2164)
- 작업실: `board_web/series.html#EP03/story`
- PNG와 얼굴 사진은 로컬 전용이며 Git에 추가하지 않음. 클라우드에서 코드만 받으면 아바타 파일도 별도로 필요. 없는 파일을 승인된 실사 프로필로 취급하지 않음.

## 검증

- 6상태·8아바타 경로·리아/하오 매핑 및 제외 대사 검사 통과.
- 실제 Chrome에서 390px iframe 검증: 가로폭 390/390, 공지 흰색·펼침, 1~6상태 순회, 끝 버튼 비활성화, 이전 이동, 프로필 모드·실사 이미지 8개 로딩 모두 통과.
- JavaScript 문법 검사, diff whitespace 검사 통과.
- S3 공용 폰 목업 육안 확인: 하오 새 아바타, 흰 공지 바, 원문·번역 스택, 공용 셸 반영.

## 남은 범위

- 외국어 원문 번역 검수 필요. 음식 사진은 자리표시자.
- 실제 앱 헤더·입력창 스크린샷의 픽셀 단위 크롭 합성은 아직 아님. 현재 HTML은 실제 규칙을 참고한 재현본.
- 긴 상태는 스크롤 가능한 대화이며 PNG는 마지막에 보이는 화면만 담음. 최종 인서트는 콘티 확정 후 메시지별로 분할/스크롤 연출.
- 1화 컷별 기존 자료 정리는 CURSOR_TASKS 작업 29, 계속 TODO.
