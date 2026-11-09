# BLOCKING RULE — 동선·콘티·인물 위치 (2026-11-06 사용자 확정)

배경: 준호 소파→아일랜드 이동 컷에서 (1) 이동 방향이 틀리고 (2) 아일랜드에 앉아 있어야 할 리아가 컷마다 있다 없다 함.
원인은 프롬프트 길이가 아니라 **생성 방식**. 텍스트로 방향을 지시하지 않고, 시작·끝 상태를 스틸로 잠그고 Kling은 그 사이 이동만 시킨다.

## 1. 이동 컷 = 시작 스틸 + 끝 스틸
- 이동 방향을 글로 쓰지 않는다. "walks screen-right" 금지. 목적지는 화면 안 사물로 쓴다: `walks toward the kitchen island and bar stools`.
- Kling에 **시작 프레임 + 끝 프레임** 둘 다 넣는다. 끝 스틸(준호가 아일랜드 옆에 선 장면)을 NB Pro/ChatGPT로 먼저 뽑는다.
- 끝 프레임이 있어도 순간이동·이상한 회전은 남는다 → 한 클립 이동은 **두세 걸음, 3초 이하**. 소파에서 아일랜드까지 한 클립에 넣지 않는다.
- 시작·끝 스틸은 **같은 카메라 축**에서 뽑는다(아래 3).

## 2. 인물 등장은 컷 분할로 해결
- 시작 프레임에 없는 인물은 프롬프트로 통제할 수 없다. "woman sitting at island" 써도 매번 다르게 나온다.
- 표준 분할:
  - CUT A (소파 축): 준호 일어남 → 화면 오른쪽으로 퇴장. 리아 프레임 밖.
  - CUT B (아일랜드 축): **리아가 이미 앉아 있는 스틸**이 시작 프레임. 준호 화면 왼쪽에서 진입.
  - CUT C (아일랜드 투샷): 둘 다 프레임 안, 대화.
- 둘 다 처음부터 프레임 안에 있으면 사라질 수 없다. 한 컷 와이드로 둘을 다 넣는 방법은 얼굴이 무너지므로 쓰지 않는다.

## 3. 카메라 축 고정
- 거실 기준 축: **카메라 왼쪽 = 소파, 오른쪽 = 아일랜드.** 소파→아일랜드 이동이 걸린 컷은 전부 이 축.
- 축이 바뀌면 같은 "오른쪽"이 공간상 다른 곳이 되어 이동이 이어지지 않는다(2026-11-06 1번·2번 이미지 사례).
- 아일랜드 모서리가 프레임에 걸리는 앵글이면 리아가 **보여야** 정상. 안 보이면 오류.

## 4. 컷별 인물 위치 상태표 (컷 리스트에 열 추가)
| 컷 | 카메라 축 | 준호 위치 | 리아 위치 | 리아 가시성 | 소품 | 이동 |
|---|---|---|---|---|---|---|
| A | 소파 방향 | 소파→일어남 | 아일랜드 착석 | 프레임 밖 | 준호 폰 | 오른쪽 퇴장 |
| B | 아일랜드 방향 | 왼쪽 진입 | 아일랜드 착석 | 보임 | 준호 폰, 리아 컵 | 아일랜드 접근 |
| C | 아일랜드 투샷 | 아일랜드 옆 정지 | 아일랜드 착석 | 보임 | 동일 | 없음 |
- **"프레임 밖"과 "공간에 없음"은 다른 상태.** 프레임 밖이어도 공간 위치는 유지하고 스틸 프롬프트에 `Ria is seated at the island, out of frame to the right`처럼 쓴다.
- 카메라 축과 가시성은 한 세트로 적는다.

## 5. 콘티(스토리보드) 단계 — 대본 잠금 후, 스틸 전 (2026-11-06 사용자: 여러 씬을 한 장에)
- ChatGPT(크롬, 0cr)로 **에피소드(또는 여러 씬)를 한 장의 그리드**에 뽑는다. 씬당 한 장이 아니다. 한 번의 생성 안에서 같은 인물·같은 세트를 그리므로 칸끼리 일관성이 따로 뽑는 것보다 높다. 이게 이 방식의 핵심 이점.
- 칸 수: 3×4 = 12칸까지. 그 이상이면 칸이 작아져 시선·손이 안 보인다. 12컷이 넘는 에피소드는 2장으로 나누되, 2장째 프롬프트에 1장째 이미지를 첨부해 인물·세트를 잇는다.
- 칸 비율 9:16. 회색 연필 스케치/단색 선화. 최종에 쓰는 이미지가 아니라 **구도·동선·인물 위치 참고용**이므로 해상도는 상관없다.
- 칸 안에 씬·컷 번호, 카메라 축, 인물 위치를 글자로 → 그 자체가 위치 상태표.
- 저장: `01_EPISODES/EPnn/frames/vNN/STORYBOARD/EPnn_board_01.png` (원본 그리드) + 칸별 분할 `EPnn_Snn_Cnn.png`.
- 스틸 생성 시 첨부 3종: 해당 콘티 칸 + 세트 마스터(`LIVINGROOM_master_v14.png`) + 캐릭터 레퍼런스. 프롬프트에 반드시:
  `Use the sketch for composition and blocking only. Render photoreal, match the supplied set master and character references.`
- **얼굴은 그리지 않는다**(2026-11-06 사용자). 마네킹/크로키 인체처럼 얼굴 빈 머리로 뽑는다. 이유: 콘티 얼굴이 스틸에 번지는 걸 원천 차단하고, ChatGPT가 캐릭터 생김새를 틀리게 그리는 문제도 없앤다. 몸통 시트(A)와 같은 관례.
- **고개·시선은 두 겹으로 잠근다**(사용자 질문 "시선·얼굴 방향은 어떻게 고정?"):
  1. 콘티(그림): 얼굴 없는 머리에 **코 방향 쐐기(▶)** 하나 + 머리에서 보는 대상까지 **시선 화살표** + 글자 `looks at Ria` / `looks at phone`. 이걸로 고개 방향·몸 방향·보는 대상이 고정된다.
  2. 스틸 프롬프트(글): `head turned toward ..., eyes locked on ..., pupils toward ...` (QA 3번 문장). 눈동자는 그림으로 못 잠그므로 글이 맡는다.
  3. QA 3번: 생성된 스틸에서 눈동자를 확대해 콘티 화살표와 같은 대상인지 확인.
- 콘티의 세트 디테일도 무시. 위치·앵글·고개 방향·시선 대상·동작만 본다.
- 사용자 확인은 콘티 한 장에서 한 번. 통과 후 스틸. 동선·인물 누락은 여기서 걸러진다.

## 6. ChatGPT 콘티 프롬프트 템플릿
```
Storyboard for one sitcom episode, 3x4 grid (12 panels), each panel 9:16 portrait. Grey pencil sketch, no color, no shading detail, loose lines. Same two characters and same apartment in every panel.
Draw characters as faceless croquis figures: blank oval heads, NO facial features. Show head direction with a single small wedge for the nose, and draw an arrow from the head to whatever the character is looking at, with a label like "looks at Ria" or "looks at phone".
Set: Korean apartment living room. Left = caramel corduroy sofa + round coffee table. Right = white marble kitchen island with black bar stools. Arched window on back wall.
Characters: JUNHO (man, glasses, navy shirt, phone in hand). RIA (woman, seated at island with a mug).
Camera axis for all panels: sofa on camera-left, island on camera-right. Do not flip.
Panel 1 — CUT A: medium, sofa side. Junho rising from sofa, phone in right hand, looking toward camera-right. Ria out of frame (she is at the island).
Panel 2 — CUT A end: Junho exiting frame right. Sofa empty.
Panel 3 — CUT B start: island side. Ria seated at island, mug, looking down at her phone. Junho not yet in frame.
Panel 4 — CUT B: Junho entering from frame-left, two steps from the island. Ria still seated, looks up.
Panel 5 — CUT C: two-shot, Junho standing beside island, Ria seated, eye contact.
Panel 6 — CUT C reaction: close-up Ria, eyes on Junho.
Panels 7-12 — (다음 씬 컷을 같은 형식으로 이어 쓴다: 씬 번호, 카메라 축, 누가 어디, 시선, 동작)
Label each panel with scene/cut number and "sofa-axis" or "island-axis" in small text.
```
에피소드에 맞게 패널 내용만 바꾼다. 축 문장과 "Do not flip"은 지우지 않는다.

## 7. 교훈 2026-11-06 — 콘티가 가구 각도를 끌고 간다
- 사례: 콘티 칸 2가 소파를 비스듬히 그렸고, J2b r1이 플레이트가 아니라 콘티의 소파 각도를 따라감(사용자 지적 "창문을 등진 소파가 비틀어졌다").
- 규칙 A (콘티 생성): ChatGPT에 **세트 마스터 v14 + 해당 앵글 플레이트를 첨부**하고 프롬프트에 `Furniture layout and angles must match the attached set photos exactly: the sofa faces the camera squarely with its back to the arched window; do not rotate or move furniture` 를 넣는다. 콘티가 틀리면 그 칸은 스틸 참조로 쓰지 않는다.
- 규칙 B (스틸 생성): 1인·단순 배치 컷은 콘티 이미지를 **참조에서 뺀다**. 플레이트 1번 + 글 배치만으로 충분하고 더 안전하다. 콘티 이미지는 2인 이상·동선이 복잡한 칸에만 붙인다.
- 규칙 C (프롬프트): 소파 컷은 `THE SOFA GEOMETRY IS FIXED: faces the camera squarely with its back to the arched window, exactly as in image 1, not rotated` 를 명시. QA 12에 "소파 각도" 항목 추가.

## 8. 고정 자리표 (2026-11-06 사용자: "이런 것도 콘티 때 저장해 놔야겠네")
사례: 1화 소파 컷 15장에서 준호 자리가 왼쪽 끝(W1)·가운데(J1b·F2·J2b)·오른쪽 끝(F1·J2)으로 오갔다. 가구 배치는 잠겼는데 **사람 자리**는 잠그지 않아서다.

규칙: 세트마다 인물별 기본 자리를 한 줄로 정해 두고, (1) 콘티 프롬프트, (2) 위치 상태표, (3) 스틸 프롬프트(SEAT LOCK 문장) 세 곳에 똑같이 넣는다. 자리를 바꾸는 컷은 상태표에 "이동" 열로 명시한다.

| 인물 | 세트 | 기본 자리 | 소품 | 비고 |
|---|---|---|---|---|
| 준호 | 거실 소파 | 3인 소파 **가운데 쿠션** (2026-11-06 사용자 확정) | 폰, 좌탁 토마토 트레이 바로 앞 | 일어날 땐 소파 바로 앞에서 → 아일랜드 쪽으로 |
| 리아 | 아일랜드 | 거실 쪽(카메라 왼쪽) **첫 번째(끝) 검은 스툴** (2026-11-06 사용자 확정: 가운데 스툴 시도 5회 실패 후 끝 스툴로 확정) | 폰 (컵 없음) | 소파 쪽으로 올 때만 이동 |
| 수만 | 아일랜드 | **카운터 뒤**, 리아보다 오른쪽 | 피클병 | 고개 숙임 기본 |
| 순덕 | 현관 | 현관문 안쪽 매트 | 반찬통 | |
| 미유 | 창가 벤치 | 아치창 아래 벤치 왼쪽 | 줄자·스케치북 | |
| 하오 | 계단 | 계단 아래 칸 | 삼각대 | |

- 콘티 프롬프트에 넣는 문장: `Fixed positions in every panel: Junho sits on the CENTER cushion of the sofa; Ria sits on the END black stool nearest the living room (the first of three stools); Suman stands behind the island counter to her right. Do not move anyone unless the panel says so.`
- 스틸 프롬프트 SEAT LOCK: `SEAT LOCK: the man sits on the CENTER cushion of the three-seat sofa, the coffee table tray directly in front of him; not on either end.` + 자리 마스터 프레임(정한 자리에 앉은 확정 스틸 1장)을 1번 참조.
- QA 15: 소파 컷은 자리 마스터와 나란히 놓고 쿠션 위치 대조. 다르면 폐기.
- 상태표 열 추가: `자리(기본/이동)`.

### 2화 「싸움은 모국어로」 자리 (1화 문장과 따로, 2026-11-06)
1화 문장(준호 가운데 쿠션, 리아 끝 스툴, 수만 카운터 뒤)을 2화 콘티·스틸에 넣지 않는다. 극본 `WORLD_PLANNING/EP01_PROSE_SCRIPT_v06.md` 2화. 콘티 프롬프트, 위치 상태표, 스틸 SEAT LOCK 세 곳에 아래만 넣는다.

| 인물 | 기본 자리 | 소품 |
|---|---|---|
| 준호 | 소파 **한쪽 끝**. 가운데 쿠션 금지 | 폰은 주머니. 칸이 꺼낼 때만 |
| 리아 | 소파 **반대쪽 끝**. 아일랜드 스툴로 보내지 않음 | 폰은 손 |
| 가운데 쿠션 | 둘 사이의 국경. 칸이 치우거나 숨기라고 할 때만 이동 | |
| 순덕 | 현관 밖. 칸이 들어온다고 할 때만 반찬통을 들고 등장 | 반찬통 |
| 수만·하오 | 이 화에 없음 | |

- 콘티 프롬프트 문장: `Fixed positions in every panel of episode 2: Junho and Ria sit on OPPOSITE ENDS of the sofa; one cushion stays in the MIDDLE as a border between them. Do not sit Junho on the center cushion. Do not move Ria to the island. Sundeok stays outside until a panel says she enters, carrying banchan containers. Suman is not in this episode. Do not move anyone unless the panel says so.`
- 스틸 SEAT LOCK: `SEAT LOCK episode 2: the man and the woman sit on opposite end cushions of the three-seat sofa, one cushion between them as a border; the man is not on the center cushion; the woman is not on an island stool.`
- QA: 준호가 가운데 쿠션이거나 리아가 스툴에 있으면 폐기. 순덕이 칸 지문 없이 나오면 폐기.

## 9. 세트 소품 고정표 (2026-11-06 사용자: "아일랜드 위 꽃이 없다가 생겼어")
원칙: **플레이트에 올라가 있는 것이 전부다.** 플레이트를 참조로 넣어도 모델은 작은 소품을 빼거나 보태므로, 표면별 소품을 글로 세어서 프롬프트에 넣는다(SET DRESSING LOCK). 표에 없는 물건이 생기거나 있는 물건이 빠지면 폐기.

| 표면 (플레이트) | 고정 소품 | 금지 |
|---|---|---|
| 아일랜드 상판 (A2) | 레몬 볼 1 + 분홍 꽃 작은 꽃병 1 (상판 안쪽) | 그 외 아무것도 없음. 인물 소품(컵·폰)은 상태표에 적은 것만 |
| 좌탁 (A1) | 토마토 레드 트레이 1 + 안개꽃 작은 꽃병 1 + 책 2권 | 리모컨·잔·접시 금지 |
| 소파 | 쿠션: 킬림 무늬 1 + 흰 니트 1 + 갈색 줄무늬 1, 왼쪽 팔걸이 크림 담요 | 담요 무늬 변경 금지(2026-11-04 교훈) |
| 창가 벤치 | 흰·회색 쿠션 3, 몬스테라 화분 왼쪽 | |
| 사이드보드 (A6) | 라디오 + 지구본 + 늘어진 덩굴 + 책 | |
| 식탁 (A3) | 분홍 꽃병 1 | |
| 주방 선반 | 구리 통 5, 유리병 3, 소스병 2, 빨간 통 1, 구리 팬 4 | |

- 프롬프트 문장(아일랜드 컷): `SET DRESSING LOCK: on the island counter there are exactly one bowl of lemons and one small vase of pink flowers, exactly as in the set plate; nothing else on the counter except the props listed for the characters.`
- 프롬프트 문장(소파 컷): `SET DRESSING LOCK: on the coffee table exactly the tomato-red tray, a small vase of baby's breath and two books, as in the set plate; nothing else.`
- 상태표에 `표면 소품` 행을 씬마다 한 줄 넣는다(컵·폰처럼 인물이 가져오는 소품은 인물 열에).
- QA 16: 플레이트와 나란히 놓고 표면 위 물건 개수를 센다.
- 2026-11-06 기록: B13·J9d·T5 r1은 아일랜드 꽃병이 **빠진** 상태(레몬만). 사용자 승인으로 그대로 사용. 이 씬 안에서는 "꽃병 없음"으로 통일하고, 다음 아일랜드 씬부터 플레이트대로 꽃병 포함.

## 10. 씬 안에서 인물 자리는 고정 (2026-11-06 사용자: "말을 하고 있는데 왜 앞에 있다 뒤에 있다 해")
- 한 씬(같은 장소·연속 시간) 안에서 인물이 **대사 중이면 그 자리에 그대로** 있다. 반응 컷·상대 컷에서 그 인물을 뒤로 보내거나 흐리게 하거나 프레임 밖으로 빼지 않는다. 옛 지문("준호 뒤에 흐릿")처럼 자리를 바꾸는 문구가 있으면 지문을 고친다.
- 구현: 씬의 기준 프레임(예: J9d) 하나를 정하고, 그 씬의 모든 컷을 FRAME LOCK(기준 프레임을 1번 참조, "same camera, same positions, the only change: …")으로 뽑는다. 바뀌는 건 표정·손·시선만.
- 상태표의 `자리(기본/이동)` 열에 "이동"이 없는 컷에서 자리가 바뀌면 QA 15 폐기.

## 11. FRAME LOCK 컷에서 카메라를 바꾸지 않는다 (2026-11-06 교훈)
FRAME LOCK(1번 참조 = 같은 샷의 이전 프레임) 프롬프트에 "camera slightly closer", "medium close-up" 같은 카메라 변경 문구를 넣으면 모델이 3분할 콜라주(R13b r1)나 증명사진(B37b r0)을 낸다. 사이즈를 바꾸고 싶으면 (a) 2k 스틸을 크롭하거나(0cr) (b) 플레이트 기반으로 새 컷을 뽑는다. FRAME LOCK 컷 첫 문장은 항상 "ONE SINGLE photograph, same camera as image 1".
- 복장 소품(수만 수건)은 "The only change" 문장과 별개로 매번 "NO towel on his shoulder"를 다시 적는다. 앵커에 없어도 모델이 되살린다.

## 12. 앵커 프레임은 재잠금 전에 복장·소품을 먼저 감사한다 (2026-11-06 교훈, 사용자: "이런 것도 미리 맞춰 놨으면 재생성을 안 했을 텐데")
2막 앵커를 B40b로 바꾸면서 수만 앞치마가 **검정**인 것을 확인하지 않고 15컷을 잠갔다. 1막 앵커 B13b는 **회색**. 결과: 막 사이 앞치마 색이 다르고, 24·30은 수건·앞치마 유무까지 흔들림.
규칙:
1. 앵커 후보가 정해지면 **생성 전에** 캐릭터별 복장 체크리스트(재킷·앞치마 색·수건·신발)와 상판 소품을 앵커 1장에서 먼저 대조한다. 틀리면 앵커부터 고친다(2cr), 절대 종속 컷을 먼저 뽑지 않는다.
2. 복장은 프롬프트 글이 아니라 **바디 시트**로 잠근다. 수만 = BODY_SUMAN에 앞치마가 없어서 글과 참조가 싸웠다 → 앞치마 입은 바디 시트(v04)를 만들어 참조로 쓴다.
3. 막이 둘 이상이면 앵커끼리 먼저 나란히 놓고 복장·소품을 대조한 뒤 종속 컷을 뽑는다.

## 13. 가구 치수 고정 (2026-11-06 사용자: "아일랜드 식탁 폭이 너무 좁아짐, 넓이도 고정")
2막 앵커 B40b 계열에서 아일랜드 상판이 1막(B13b, A2 플레이트)보다 좁고 길게 나왔다. 모델은 플레이트를 참조해도 가구 비율을 바꾼다.
규칙: 세트 플레이트마다 핵심 가구의 **치수와 비율을 글로** 적어 SET DRESSING LOCK 앞에 넣는다(FURNITURE SIZE LOCK). 앵커 감사(§12) 항목에 "가구 폭·깊이 플레이트와 같은가"를 추가한다.
| 가구 | 치수(고정) | 비율 단서 |
|---|---|---|
| 아일랜드 | 상판 2.4 m × 1.0 m, 높이 0.9 m, 두꺼운 흰 대리석 상판(두께 5 cm), 오크 몸체 | 스툴 3개가 긴 변에 여유 있게 놓이고 상판 깊이는 스툴 좌판 지름의 약 2.5배 |
| 바 스툴 | 좌판 지름 35 cm, 높이 65 cm, 검정 철제 | 스툴 간격 = 좌판 지름 1개 |
| 소파 | 3인, 폭 2.2 m, 깊이 0.95 m | 쿠션 3개 동일 폭 |
| 좌탁 | 원형 지름 0.9 m | 소파 폭의 약 40% |
프롬프트 문장: `FURNITURE SIZE LOCK: the island is a deep, wide block, 2.4 m long and 1.0 m deep with a thick white marble top; the counter depth is about 2.5 stool-seat diameters; never a narrow bar or a slim ledge.`

## 14. 플레이트끼리 벽 순서가 맞아야 한다 (2026-11-06 사용자: "창문 옆이 액자인데 아일랜드 식탁에서 창문이 보이는 바람에 달리 보여")
아일랜드 플레이트(A2)는 아치창 바로 오른쪽에 구리 선반을 붙였다. 마스터 와이드에서는 창 → 액자 벽 → 주방 선반·냉장고 순서다. 플레이트가 틀리면 그 위에 잠근 컷 전부(1화 아일랜드 23장)가 틀린다.
규칙:
1. 세트 플레이트 프롬프트에 **벽 순서 문장**을 고정으로 넣는다: `WALL ORDER (left to right, as in the master wide): front door and staircase → arched window with the window bench → framed-pictures wall (bus, pagoda, map) → kitchen shelves, copper pans, stove, fridge. Never put the kitchen shelves directly beside the window.`
2. 플레이트를 뽑으면 **마스터 와이드와 나란히 놓고** 같은 벽이 같은 순서로 보이는지 대조한다. 창이 보이는 플레이트라면 창 옆에 액자가 있어야 한다.
3. 플레이트가 틀렸으면 플레이트 → 앵커 → 종속 컷 순서로만 고친다. 컷부터 고치지 않는다.
4. 비용 예시: A2 수정 = 플레이트 1 + 앵커 2 + 종속 23 = 26장 52cr. 플레이트 단계에서 잡았으면 2cr.

### §14 보충 — A2 아일랜드 플레이트 vs 마스터 와이드 대조 결과 (2026-11-06, 사용자 "앵커가 거기만 틀린 게 아니잖아")
A1 소파 플레이트 = 마스터와 일치. A2 아일랜드 플레이트가 다른 곳 7가지(앵커 B13c·B40b가 전부 물려받음):
1. 창 오른쪽 액자 벽(버스·탑·지도·산) 누락, 구리 선반이 창에 바로 붙음
2. 창 위 타르초(오색 기도 깃발) 누락
3. 창 아래 윈도 벤치(쿠션) → 낮은 오크 수납장으로 바뀜, 그 위에 라디오·지구본 (마스터: 라디오·램프는 창 오른쪽 사이드보드 위)
4. 선반 왼쪽 벽 덩굴 화분 추가됨 (마스터: 창가 바닥 몬스테라만)
5. 지구본 추가됨 (마스터에 없음)
6. 주방 천장 낮은 보(단차) 추가됨 (마스터: 평천장)
7. 아일랜드 각도 사선 (마스터: 오른쪽 벽과 나란히). B40b는 폭까지 좁음(§13)
맞는 것: 구리 펜던트 3, 헤링본 바닥, 냉장고 자석, 레몬 볼+꽃병, 검정 스툴 3.
A2 재생성 프롬프트에 넣을 문장: `Reference image 1 is the evening master wide; this plate is the same room seen from the sofa side toward the island. Keep EXACTLY: prayer flags over the arched window, the cushioned window bench under the window, the framed-pictures wall between the window and the kitchen shelves, flat ceiling, the island parallel to the right wall. Do NOT add a globe, a hanging vine plant, a cabinet under the window, or a dropped beam.`

### §13 보충 — 키·가구 높이 잠금 (2026-11-06 사용자: "수만이가 마지막 컷에서 식탁이 가슴까지 올라와 있어")
키 차트(CAST_PROMPTS_v03_body.md): 준호 184 · 시우 178 · 수만 172 · 하오 172 · 리아 171 · 하영 155 · 순덕 155 · 미유 153.
가구 높이: 아일랜드 상판 0.9 m, 바 스툴 좌판 0.65 m, 소파 좌판 0.45 m, 좌탁 0.4 m.
→ 서 있는 사람에게 상판은 **골반·벨트 높이**(준호 184: 허벅지 위/골반, 수만 172: 벨트). 절대 가슴·명치가 아니다. 스툴에 앉은 리아는 어깨가 상판보다 한 뼘 이상 위, 팔꿈치가 상판에 편하게 놓인다.
프롬프트 문장(HEIGHT LOCK): `HEIGHT LOCK: the island counter top is 0.9 m high; on the standing men it reaches the belt line / hip (Junho 184 cm: upper thigh to hip; Suman 172 cm: belt), never the chest. The woman (171 cm) on the 65 cm stool has her shoulders well above the counter and rests her forearms on it.`
QA 17: 서 있는 인물 옆에 상판이 가슴까지 오면 폐기. 앵커 감사(§12) 항목에 추가.

## 15. 가구 디자인 잠금 — 플레이트 재생성 때 직전 플레이트를 참조에 넣는다 (2026-11-06 사용자: "식탁이 왜 다 바뀌었어")
A2d 플레이트를 벽 순서만 고치려고 마스터 와이드+글로 다시 뽑았더니 모델이 **식탁 디자인·스툴·창**을 바꿨다(오크 몸체 → 통대리석 워터폴, 둥근 좌판 스툴 → 톨릭스, 아치창 → 문형 창). 앵커 감사 6항목에 "가구 디자인"이 없어서 통과시켰다.
규칙:
1. 플레이트를 다시 뽑을 때는 **마스터 와이드 + 직전 플레이트** 둘 다 참조로 넣는다. 고칠 것(벽 순서 등)만 글로 적고, 나머지는 "exactly as in reference image 2(직전 플레이트)".
2. FURNITURE DESIGN LOCK 문장: `FURNITURE DESIGN LOCK: the island has a light OAK body with a 5 cm white marble top only (NO waterfall marble sides); the three bar stools are black metal with ROUND seats and a foot ring (not square Tolix stools); the window is the tall ARCHED window with black mullions and a cushioned bench, as in the master wide.`
3. 앵커 감사 7번째 항목 = 가구 디자인(재질·형태·창 모양). 마스터와 나란히 놓고 식탁 옆면·스툴 좌판·창 모양을 본다.
4. 예정: A2e = 마스터 + 옛 A2 참조 + §14 벽 순서 + §15 디자인 잠금 → E13/E40 마스터 → 동작 컷. 약 16cr, 2026-11-14 갱신 후.

### §14·§15 결론 — 아일랜드 플레이트 A2e (2026-11-06 사용자 제안 "부엌에서 창문 대신 액자 우측만")
아일랜드 카메라에서는 창이 안 보이고 **액자 벽 오른쪽 끝(지도·탑 액자) + 라디오 사이드보드 → 구리 선반 → 주방**이 보인다. 사용자가 준 그림(`SET_LIVINGROOM/LIVINGROOM_v14e_A2e_island_userref.png`, 9:16 크롭 = `..._A2e_island.png`)이 마스터 디자인(오크 몸체+대리석 상판, 둥근 스툴, 구리 선반, 라디오) 그대로라 이것을 플레이트로 쓴다. 앵커 생성 시 참조 = [A2e 플레이트, 마스터 와이드] + DESIGN/SIZE/HEIGHT LOCK.

## 16. 수만 피클병 상태표 (2026-11-06 사용자: "수만이는 피클을 너무 좋아해서 계속 꺼내 먹고, 얘기가 끝났을 때는 한 통이 비워진 걸로")
러닝 개그. 피클병은 **상태가 변하는 소품**이라 §9 고정표의 예외. 막별 상태를 프롬프트에 적는다.
| 구간 | 병 상태 | 수만 동작 |
|---|---|---|
| 1막 (3~18) | 가득(피클이 병 입구까지) | 뚜껑 열고 한 개씩 꺼내 먹음(11·13 등) |
| 2막 전반 (22~35) | 절반 | 대사 사이사이 하나씩 꺼내 씹음 |
| 2막 후반 (37~43) | 바닥에 두세 개 | 병을 기울여 꺼냄 |
| 엔딩 (44·45) | **빈 병**, 뚜껑 옆에 | 빈 병을 내려놓고 둘을 보며 절레절레 |
프롬프트 문장: `PICKLE JAR STATE: the glass pickle jar on the counter is <FULL / HALF-EMPTY / NEARLY EMPTY / EMPTY with the lid beside it>.` Kling ACTION에 "he fishes out another pickle spear and eats it while listening" 추가(대사 없는 구간).
적용: 다음 2막 마스터/엔딩 재생성 때 반영. 현재 G13/G40/H44는 전부 가득 찬 병.

## 17. 얼굴 동일성은 수치로 판정한다 (2026-11-06 사용자: "얼굴이 왜 기준 얼굴이랑 다른 거 같지")
insightface(buffalo_l) 코사인 유사도, 확정 얼굴(JUNHO_face_C / BEA_MASTER_FACE / SUMAN_face) 대비. 1화 측정: CU(얼굴 750px) 0.66 ↔ 미디엄(100~220px) 0.2~0.3, Kling 클립 중간 프레임은 더 낮음(0.1~0.3). 즉 **미디엄 스틸의 얼굴은 기준 얼굴이 아니다.** 원인: 참조 9장 중 얼굴은 2장, 얼굴이 프레임의 1/15라 모델이 정체성을 못 잡음.
기준: 얼굴 폭 ≥200px에서 유사도 ≥0.45 통과, <0.35 폐기. 작업 19(face_strip.py)가 보고.
대책 순서: (1) 마스터 생성 시 참조 1·2번을 얼굴로, 세트 참조는 뒤로 (2) 통과한 CU(≥0.45)를 FRAME LOCK 1번 참조로 미디엄을 뽑아 얼굴을 끌고 간다 (3) 영상은 Kling 3.0 Omni(image_references, kling_o3_image_reference)로 얼굴 참조를 같이 넣는 방식을 테스트 (4) 얼굴 스왑 금지(철칙 9).

### §17 결론 (2026-11-06 측정) — 대사 시작 스틸은 1인 단독
- 다인 프레임(전신·허리 위 모두) 동일인 점수 0.2~0.40, 1인 단독 상반신 0.49~0.64. 얼굴 참조를 1·2번에 두고(`face_first`) 한 사람만 그리면 통과한다.
- 절차: 인물×상황별 단독 스틸 1장 → 2k 얼굴 중심 9:16 크롭(얼굴 ≥450px, `tools/face_score.py` ≥0.45) → 그 크롭이 그 인물의 모든 대사 컷 시작 프레임. 다인 마스터는 등장·리액션·동작·엔딩 전용.
- 1화 단독 세트: S_ria_island_act1_cu / S_ria_island_act2_cu / S_suman_island_cu / S_suman_island_look_cu / S_junho_sofa_cu / S_junho_island_r2.

## 18. 샷 사이즈·얼굴 크기 표 (2026-11-06 사용자: "핸드폰 화면비라 투샷까지는 얼굴 크기를 정해 놔야겠다. 다른 영상들 보니 상반신 컷이 많네")
9:16 세로 화면 기준. 얼굴 폭은 1080px 출력 기준(2k 스틸이면 ×1.42).
| 샷 | 쓰임 | 얼굴 폭(1080 기준) | 프레임 높이 대비 |
|---|---|---|---|
| 단독 CU (어깨 위) | 감정 리액션, 짧은 대사 | ≥500px | 얼굴이 높이의 1/3~1/2 |
| 단독 상반신 (가슴 위) | **대사 기본 샷** | ≥400px | 1/4~1/3 |
| 투샷 (허리 위, 두 사람) | 주고받는 대사, 같이 폰 보기 | 각 ≥260px | 1/6 이상 |
| 3인샷·전신 | 등장·이동·동작·엔딩만 (대사 없음) | 제한 없음 | — |
- 대사 컷은 단독 상반신이 기본, 투샷은 "같이 보는" 순간에만. 전신 3인샷에서 대사 금지(§14).
- 생성 프롬프트에 "the face fills about one third of the frame height"를 넣어도 모델이 덜 당기므로, 2k로 뽑고 얼굴 중심 크롭으로 맞춘다(0cr). 투샷은 두 얼굴 중심으로 크롭.
- QA: `tools/face_score.py`가 폭·점수를 출력. 표 미달이면 시작 스틸로 쓰지 않는다.

### §18 보충 — 줌아웃으로 와이드를 만들지 않는다 (2026-11-06 사용자 질문)
Kling은 시작 스틸에 있는 것만 이어 그린다. 상반신 스틸에서 줌아웃하면 바깥 공간을 지어내 세트가 바뀐다. 와이드·3인샷은 **그 사이즈의 스틸을 따로** 만들고(G13·G40·H 시리즈), 대사 없는 등장·동작·엔딩(1.5~3초)에만 쓴다. 줌은 안쪽으로(푸시인)만 허용. 와이드에서 대사가 꼭 필요하면 "와이드 1초 → 단독 컷"으로 편집한다.
- 단독 CU 배경 규칙: 다인 마스터에서 그 인물 뒤에 보이는 벽을 그대로 적는다(준호 아일랜드 = 뒤 액자 벽·라디오, 오른쪽 허리에 상판·리아 어깨 / 리아 = 뒤 구리 선반 / 수만 = 뒤 선반·타일 / 준호 소파 = 뒤 소파 등받이·아치창).

## §19 Kling 대사 컷 ACTION 작성 규칙 (2026-11-09, 사용자 지시)
- ACTION에는 **관찰 가능한 동작만** 쓴다. 감정어(sulky, fond, hopeful…)는 PERFORMANCE 한 줄에만.
- 비트마다 `초 구간: on '대사 구절' + 무엇이 어떻게 움직이는지`. 부위는 눈·눈썹·입·고개 중 2~3개만.
- 머뭇거림은 길이와 상태로: "0.3~0.5s, lips parted but silent".
- 크기를 못 박는다: 고개 "a few degrees", 시선 "flick … and back", 어깨 "a few centimetres".
- 손·소품(폰 기울이기, 뺨 만지기, 폰 들기)은 움직이지 않는다 → 카메라 리프레이밍 원인(E1_22 take02).
- 마지막 비트는 항상 "no new movement; …" 로 끝낸다. ACTION 머리말: "(only the movements listed below happen; nothing else moves)".
- 프레임 밖 인물·공간을 언급하지 않는다("the man on the sofa off-frame" 금지) → Kling이 보여주려고 와이드 컷 삽입(1막 묶음 38cr 손실).
- 클로즈업 컷은 SCENE CONTEXT에 방 전체를 쓰지 않고 시작 스틸에 보이는 것만 + end_image = 시작 스틸(--lockend). A/B 5번으로 확정.
