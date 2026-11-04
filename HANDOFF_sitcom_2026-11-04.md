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
| 비아 | BEA_MASTER_FACE.png | 필리핀 엄마 + 미국 아빠 혼혈, 한국 거주. 가족 단톡에서 영어·타갈로그어·한국어가 섞임. 키 171. 의상 v04(화이트 셔츠+다크진+탄 로퍼, 2026-11-04 B안 확정, 가디건 폐기) |
| 준호 | JUNHO_face_C.png | 키 184. 순박하고 진실한 다정남. 영어 거의 못함(유학파 아님). 동그란 금테 안경. 비아와 한국에서 만남, 토마톡 번역으로 연애 |
| 순덕 할머니 | BOKRYE_face.png | 정규 멤버 |
| 미유 | MIYU_face.png | 정규 멤버 |
| 수만 | SUMAN_face.png | 정규 멤버 |
| 하오 (왕하오, 중국 칭다오) | DOYUN_face.png | 정규 멤버. 2026-11-04 재캐스팅(D안)+중국인 전환. 구 이도윤 |
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
- 몸통 시트 8장 완료: `CAST_v8_six/BODY_<KEY>_v03.png` (미유는 v05 네이비 트랙재킷+러플쇼츠 확정, v03·v04는 _old / 순덕은 v04 네이비 쇼어재킷 '건물주 룩' 확정 15:14, v03 몸뻬는 _old). 프롬프트 `CAST_PROMPTS_v03_body.md`.
- 무표정 정면 얼굴 7/8 완료 (`<KEY>_face_neutral.png`, 도윤만 보류): 프롬프트 `CAST_v8_six/CAST_PROMPTS_v04_neutral_face.md`. Claude가 크롬 ChatGPT로 직접 생성(파일 입력 ref에 file_upload → execCommand insertText → send-button 클릭 → 60s → blob 다운로드).
- 도윤 재캐스팅 확정: D안(태닝 피부·무쌍 큰 눈·페이드컷·보조개) + 중국인 **왕하오**. 얼굴·몸통(v04)·무표정 전부 교체 완료. 기록 `CAST_v8_six/CAST_PROMPTS_v05_doyun_recast.md`.
- 캐릭터별 토마톡 활용 축: `WORLD_PLANNING/CAST_TOMATOK_USAGE_v01.md` (사용자 확정 6명 + 시우·도윤 제안). 제품 요소: 토마톡링(건강), 지니콩즈(AI 비서).
- 거실 앵글1(소파 정면) 재생성: 옛 14:07본 삭제 → `LIVINGROOM_v14_angle1_sofa_v02.png`, `_v03.png`(v03이 쿠션·배경 가장 정확).
- 캐스트·세트 보드(웹): https://claude.ai/artifact/PJEUoc1HUx9K5gaPgv4Hns — `tools/build_cast_board.py <out>` 로 재생성 후 재발행.
- 캐스트 바이블(도윤 성격 + 8명 관계도): `WORLD_PLANNING/CAST_BIBLE_v01.md`. 시우 거주지=2층 창고방 제안(확인 필요).
- 토마톡 단톡 목업 템플릿: `04_UI/TOMATOK_HOUSE_CHAT/render_house_chat.py` (아바타 8명, 모서리 라운드 자동).
- ChatGPT 주의: 일반 채팅은 이전 채팅 기억으로 다른 캐릭터를 섞을 수 있음 → 프롬프트 첫 줄에 'ONLY the one person' 고정. 임시 채팅은 이미지 생성 불가.

## 다음 할 일
0. (완료) 도윤→하오 재캐스팅 확정. (완료) 세트 컷 테스트 `SET_BEA_island_v02.png`(새 의상), `SET_JUNHO_entrance_v02.png`(현관 빈 벽; v01은 후크·가방 지어내서 폐기) — 얼굴+몸통 시트+거실 v14 세 장 첨부로 한 번에 성공, 얼굴·옷·방 전부 유지됨. 이 방식이 EP01 컷 제작 표준. 나머지 6명 세트 컷은 등장 에피소드에서 첫 컷 제작 시 겸함.
1. angle1_sofa를 2~4번 톤에 맞춰 재생성 (v14 + angle2를 함께 첨부).
2. (선택) 2층 공간: 2층 복도는 별도 세트(2층 복도/방 앞)로 따로 만드는 걸 권장. 거실 마스터는 건드리지 않음.
3. **EP01 컷별 제작 (다음 차례)**: 대본·컷 리스트 확정본 `WORLD_PLANNING/EP01_SCRIPT_v04_cutlist.md` (A 월급 번복 / B 나이별 반응, 시작 프레임 7장 F1~F7, Kling 12클립). **F1~F6 최종 (2026-11-04 17:35)** `01_EPISODES/EP01R/frames/` — 사용자 QA 지적으로 여러 번 재생성(F1 다리만/담요, F2 담요, F5 시선·손·팔·위치·담요 7회, F6 재킷색). 최종: 담요 없음, F5는 비아가 카메라 왼쪽에서 오른팔로 폰 들고 둘이 같은 화면 봄. QA 11항목 체크리스트 `.claude/skills/tomatok-episode/SKILL.md`. 타이틀 카드 `09_TITLE/TITLE_EP01_v02.png` = 사용자 공식 로고 `LOGO_yeonnam3f_v01.png` 기반. 의상 색 정리: 미유 블랙 트랙재킷(v07), 순덕 에메랄드 쇼어재킷(v05), 비아 흰 셔츠(v04). **Kling 생성 시작 (2026-11-04 17:40, 사용자 '시작')**: `01_EPISODES/EP01R/` (tools·prompts·frames·video). 3초 std = 6cr, 5초 = ~10cr. 10클립(A8=B7, A10=B10 재사용) 예상 72cr. 배치 `tools/gen_ep01r_batch1.sh`, 로그 `video/batch1.log`. 생성 후 `tools/transcribe.py`로 대사 검사. ffmpeg = `/Users/ymy/project/ai-creative-studio/node_modules/ffmpeg-static/ffmpeg`. UI 인서트 8컷 완료: `EP01R/ui/real/render_ui_ep01r.py`(render_ui_v2 재사용, 방 「Villanueva Fam 💛」, 연령 박스·읽음 카운트 추가) → 830x1800 mp4 → `tools/ui_compose.sh`로 폰 목업 껍데기(`ui/shell_phone_hole.png`, MOCKUP/phone_mockup.py 기반)에 합성 → `edit/ui/{A2,A4,A6,A9,B2,B4,B6,B8}.mp4` 1080x1920. 가족 아바타 9명: ChatGPT 3×3 그리드 1장 → `04_UI/PROFILES/FAM/*.png`. 타이틀 2초 `edit/title_2s.mp4`(로고 카드 + BGM 앞 2초 + 1.5s 차임). 조립 `edit/assemble_A_v01.py`, `assemble_B_v01.py`(컷·차임·룸톤 베드). 자막/마무리 `tools/subtitles_pass.py`, `tools/finish.py` EP01R용 패치 완료(--no-template 권장, 타이틀 카드가 대신함). 전사 통과: A1(무음) A3 A5 A7 A8. **완성 (2026-11-04 18:02)**: `99_FINAL/EP01R_A_월급번복_FINAL.mp4`(39.0s), `99_FINAL/EP01R_B_나이별반응_FINAL.mp4`(39.5s). Kling 10클립 전부 1테이크 통과, 총 66cr(잔액 ~491). 전사 애매: B5 '부동산 해 페소로'→'부동산에 패서로', B9 '비아는'→'비하는' (whisper 특성 가능성, 사용자 청취 확인 필요). 자막 패스 버그 수정: 캡션 컷(B1)에서 대사 자막이 빠지던 것. 재마무리 명령: `cd 01_EPISODES/EP01R && python3 tools/finish.py edit/assemble_A_v01.py v01 --no-template --final --final-name EP01R_A_월급번복_FINAL.mp4` (B: assemble_B_v01.py B_v01 ... EP01R_B_나이별반응_FINAL.mp4).
   - 혼혈 비아, 하영, 시우 설정을 반영해 캐릭터 설명과 기획을 업데이트.
- 2026-11-04 사용자 지시: 할머니 이름 박복례 → **박순덕(순덕 할머니)**. 파일명 BOKRYE_*는 유지.
- 2026-11-04 키 차트: 준호 184 · 시우 178 · 수만 172 · 하오 172 · 비아 171 · 하영 155 · 순덕 155 · 미유 153.
- 2026-11-04 세트 컷 원칙: 세트 컷은 레퍼런스라 얼굴 없음(턱 아래부터). 얼굴은 에피소드 Kling 시작 프레임에만 넣고 마스터와 대조. 전신 9:16은 등장·이동용, 대사 컷은 가슴 위 미디엄으로 따로. 현관은 빈 벽+문+매트 하나(후크·신발장·가방 금지).
