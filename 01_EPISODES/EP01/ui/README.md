# EP01 v05 폰 UI 렌더 (2026-10-29)

`chat_v05.md` 기준으로 HTML → headless Chrome 캡처 → ffmpeg. 크기 1012×2252 (BASE_CHAT_ROOM.png와 동일). 캡컷에서 폰 화면 네 모서리에 맞춰 합성.
재생성: `node render_ui_v05.mjs` (Chrome + ai-creative-studio의 ffmpeg-static 사용). 메시지·타이밍은 스크립트 상단 배열만 고치면 됨.

| 컷 | 파일 | 내용 |
|---|---|---|
| C2 | `EP01_C2_MALE_23to27_5s.mp4` (+start/end png) | 남자 폰. 인원 23→25→27, 입장 알림 2개, 메시지 4개. 5초 렌더 (실제 UI 노출 3초로 트림) |
| C4 | `EP01_C4_MALE_typing_flood_4s.mp4` (+png) | 남자 폰. 입력창 "안녕하세요, 처음 인사드립니다. 저는" 미전송 + 새 메시지 14개 가속 유입 |
| C5a | `EP01_C5a_FEMALE_send_2s.mp4` (+png) | 여자 폰. 타이핑 → 빨간 말풍선 전송(번역 없음). `EP01_C5a_MALE_her_message.png`는 남자 폰에서 보이는 같은 순간 |
| C5b | `EP01_C5b_MALE_faster_2s.mp4` | 숏리스트상 소리만인 컷. 필요 시 인서트용 |
| C6 | `EP01_C6_MALE_mom_joins_1p5s.mp4`, `*_FEMALE_mom_joined_32.png` | "Mẹ님이 입장" + "조카, 안녕." 인원 32 |

## 결정/가정 (바꿔도 됨)
- 남자 폰: 한국어 번역(흰) 위, 베트남어 원문(회색) 아래. 여자 폰: 베트남어만, 본인 말풍선 빨강.
- C2 이전 맥락 3줄(큰이모가 초대·소개)은 방이 비어 보이지 않게 넣은 것. 여자 이름은 "Linh"으로 임시 표기 (남자 폰 C5a/C6에만 노출).
- C4의 14개 중 뒤 7개는 스크롤용 필러(스크립트에 `filler: true`).
- 인원 23→27은 입장 알림 2개에 각각 +2로 처리.
- 토마톡 로고 에셋이 저장소에 없어 상단바에 로고를 넣지 않음. 에셋 받으면 헤더에 추가.
- C0(잠금화면 알림 스택)은 chat_v05.md에 없어 미렌더.
