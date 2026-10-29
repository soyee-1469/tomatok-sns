# Nano Banana Pro 캐스트 일관성 테스트 (2026-10-29, 힉스필드 CLI, 0크레딧)
참조: FACE_FRONT + FACE_45_LEFT (두 캐릭터) + LOC_CAFE_v01. 프롬프트에 IDENTITY LOCK 문장 그대로 포함.
- TWOSHOT_CAFE_nbp_take01.png: 풀샷. 얼굴이 작아 판정 어려움, 카페·의상·폰 OK.
- TWOSHOT_CAFE_MEDIUM_nbp_take01.png: 50mm 미디엄 투샷. 둥근 금테 안경·주근깨·점·로우 포니테일 / 검정 사각 안경·투블럭 모두 유지. ChatGPT 스틸과 동급 → 스틸 생성 도구로 사용 가능 판단(사용자 확인 필요).
교훈: 스틸용 프롬프트는 "medium shot, faces large and readable"을 넣어야 함.
