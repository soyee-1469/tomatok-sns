# LIGHTING RULE

- soft natural window light
- warm practical household lighting
- natural skin tones
- low-to-medium contrast
- soft highlights
- 얼굴이 선명하게 보여야 한다
- 과도한 역광 금지

## 시간·조명 고정 (2026-11-05 사용자 지적: 거실이 어떨 땐 어둡고 어떨 땐 밝음)
- 시즌 1 거실 장면은 전부 **밤 9시**로 고정. 아치창 네이비, 햇빛 없음.
- 실용 조명 전부 켜짐: 종이 펜던트, 아일랜드 위 구리 펜던트, 테이블 램프, 뒷벽 줄조명. 색온도 약 3000K, 노출은 부드럽고 낮은 대비, 얼굴은 또렷하게.
- 기준 이미지: `SET_LIVINGROOM/LIVINGROOM_master_v14_evening.png` (마스터 v14를 밤으로 바꾼 것). 모든 스틸·Kling 프롬프트에 이 이미지를 참조로 붙이고 LIGHTING 문장(tools/process_checks.py)을 넣는다. 밝기가 기준과 다르면 폐기(체크리스트 8번 강화).

## 세트 각도 참조 세트 v14e (2026-11-05, 사용자: "식탁이 계속 바뀌어 → 장소 더 뽑기")
- `SET_LIVINGROOM/LIVINGROOM_v14e_A1_sofa` 소파 정면 / `A2_island` 아일랜드 / `A3_dining` 식탁+아치창 / `A4_entrance` 현관·계단 / `A5_reverse` 아일랜드에서 본 역앵글 / `A6_sideboard` 암체어·사이드보드. 전부 밤 마스터에서 파생, 9:16.
- 재생성 시 컷 위치의 각도 + 배경에 같이 보이는 각도(EXTRA) + 밤 마스터를 참조로 넣는다 (tools/process_checks.py ROOM/EXTRA). 식탁 = 둥근 오크 + 검정 스핀들 2·빨강 1·오크 1 의자, 아치창 앞 고정.
- 낮 팩 v14d (2026-11-05): 같은 각도 이름으로 `LIVINGROOM_v14d_*` (낮 마스터 v14 조명: 아치창 흰 확산광, 램프·줄조명 켜짐). 애니매틱 row에 `"time":"day"` 를 넣으면 재생성 참조가 낮 팩으로 바뀐다. 식탁 각도: A3 정면, A3b 정면 클로즈, A3f 정면 서서, A3c 소파쪽 사선, A3d 아일랜드쪽 사선, A3g 계단쪽 측면, A3h 아일랜드쪽 측면 (밤·낮 각 7종). 의자 뒤 OTS는 세트가 깨져 폐기.
