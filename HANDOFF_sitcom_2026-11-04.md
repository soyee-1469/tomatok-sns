# TOMATOK 시트콤 「연남동 3층집」 작업 인수인계 (2026-11-04)

## 기본 규칙
- 모든 결과물은 네이티브 9:16 세로.
- 확정된 마스터 얼굴은 바꾸지 않음, 이후엔 의상만 변경.
- 토마톡 번역 규칙: 상대 말풍선 = 위 번역 + 아래 원문 / 내 말풍선 = 원문만.
- 프롬프트에 film grain, skin pores 넣지 말 것. 처음부터 깨끗하고 선명하게.
- 이미지 생성은 ChatGPT, 이미지 하나당 새 채팅 하나.
- 실제 배우 닮게 만들지 않기 (초상권). 분위기만 참고.
- 만든 파일은 무조건 맥에 저장.
- GitHub(soyee-1469/tomatok-sns)에 push 금지.
- 캐릭터 스타일 가이드: 정면 얼굴은 크게 따로 뽑고, 몸통 앞/뒤 시트는 얼굴 없이 목부터 시작 (일관성 유지용).

## 캐스트 (확정 얼굴 8명) — /Users/ymy/project/sns/00_MASTER_ASSETS/CAST_v8_six/
| 캐릭터 | 파일 | 메모 |
|---|---|---|
| 비아 | BEA_MASTER_FACE.png | 필리핀 엄마 + 미국 아빠 혼혈, 한국 거주. 가족 단톡에서 영어·타갈로그어·한국어가 섞임 |
| 준호 | JUNHO_face_C.png | 순박하고 진실한 다정남. 영어 거의 못함(유학파 아님). 동그란 금테 안경. 비아와 한국에서 만남, 토마톡 번역으로 연애 |
| 순덕 할머니 | BOKRYE_face.png | 정규 멤버 |
| 미유 | MIYU_face.png | 정규 멤버 |
| 수만 | SUMAN_face.png | 정규 멤버 |
| 도윤 | DOYUN_face.png | 정규 멤버 |
| 하영 (17) | SONNYEO_face.png | 순덕 할머니 손녀, K-pop 덕후 고등학생. 자주 놀러 오는 손님 |
| 시우 (22) | DAEHAK_face.png | 2층 사는 한국인 대학생. 하영이 짝사랑해서 할머니 핑계로 기웃거림 |
- 공통 톤: 따뜻한 베이지 벽, 자연광, 4:5 가슴 위 샷. BEA_MASTER_FACE를 스타일 레퍼런스로 첨부.
- 몸통 시트·9:16 세트 컷 프롬프트: `CAST_v8_six/CAST_PROMPTS_v03_body.md` (확정 얼굴 기준, 11-04). `WORLD_PLANNING/CAST_PROMPTS_v01.md`는 옛 설정이라 쓰지 않음.

## 세트: 1층 공용 거실 — /Users/ymy/project/sns/00_MASTER_ASSETS/SET_LIVINGROOM/
- **확정 마스터: LIVINGROOM_master_v14.png**
  - v02(넓은 오크 계단 + 검은 난간)를 기준으로 아치창은 그대로 두고 햇빛만 제거. 창밖은 은은한 단색, 조명은 고르고 부드러운 세트장 느낌.
  - 왼쪽 신발과 신발 선반 제거.
- 세로 앵글 (941×1672):
  - LIVINGROOM_v14_angle1_sofa.png: 톤이 다름 (짙은 녹색 주방, 어두운 테이블) → 다른 컷 톤에 맞춰 재생성 필요.
  - LIVINGROOM_v14_angle2_kitchen.png
  - LIVINGROOM_v14_angle3_stairs.png
  - LIVINGROOM_v14_angle4_window.png
  - 2~4번은 톤이 서로 맞음 (헤링본 바닥, 밝은 원목 원형 테이블, 줄조명과 깃발).
- 탈락안: v03~v13
  - 2층 복도, 신발장, ㄱ자 계단 등을 시도했지만, 이전 결과를 다시 넣어 수정할수록 계단이 이상해져서 폐기.
  - 교훈: 수정은 항상 좋은 원본(v02/v14)에서 한 번에 할 것. 결과를 다시 넣어 고치는 걸 반복하지 말 것.
  - 사용자 의견: 계단 위 2층 공간이 없는 건 아쉬움. 방은 2층 2개 + 부엌 뒤 1개 정도 생각. 방문 크기는 동일해야 함.
- 참고 자료:
  - LAYOUT_BENCHMARK_v01.md: 시트콤·실제 집 구조 조사 결과와 프롬프트.
  - LAYOUT_plan_v01.png: 평면도.
  - refs/: 레퍼런스 사진.
  - SET_LIVINGROOM_PROMPTS_v01.md: Claude가 짠 존 배치.

## 11-04 오후 진행 (Claude)
- 몸통 시트 8장 완료: `CAST_v8_six/BODY_<KEY>_v03.png` (미유는 v05 네이비 트랙재킷+러플쇼츠 확정, v03·v04는 _old). 프롬프트 `CAST_PROMPTS_v03_body.md`.
- 거실 앵글1(소파 정면) 재생성: 옛 14:07본 삭제 → `LIVINGROOM_v14_angle1_sofa_v02.png`, `_v03.png`(v03이 쿠션·배경 가장 정확).
- 캐스트·세트 보드(웹): https://claude.ai/artifact/PJEUoc1HUx9K5gaPgv4Hns — `tools/build_cast_board.py <out>` 로 재생성 후 재발행.
- 캐스트 바이블(도윤 성격 + 8명 관계도): `WORLD_PLANNING/CAST_BIBLE_v01.md`. 시우 거주지=2층 창고방 제안(확인 필요).
- 토마톡 단톡 목업 템플릿: `04_UI/TOMATOK_HOUSE_CHAT/render_house_chat.py` (아바타 8명, 모서리 라운드 자동).
- ChatGPT 주의: 일반 채팅은 이전 채팅 기억으로 다른 캐릭터를 섞을 수 있음 → 프롬프트 첫 줄에 'ONLY the one person' 고정. 임시 채팅은 이미지 생성 불가.

## 다음 할 일
1. angle1_sofa를 2~4번 톤에 맞춰 재생성 (v14 + angle2를 함께 첨부).
2. (선택) 2층 공간: 2층 복도는 별도 세트(2층 복도/방 앞)로 따로 만드는 걸 권장. 거실 마스터는 건드리지 않음.
3. EP01 컷별 제작: 밈 A(월급 번복 문자) + 밈 B(나이별 반응).
   - 혼혈 비아, 하영, 시우 설정을 반영해 캐릭터 설명과 기획을 업데이트.
- 2026-11-04 사용자 지시: 할머니 이름 박복례 → **박순덕(순덕 할머니)**. 파일명 BOKRYE_*는 유지.
