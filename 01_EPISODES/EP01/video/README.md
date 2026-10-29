# EP01 v05 영상 컷 1차 (2026-10-29, Higgsfield Kling 3.0 std 720x1280 24fps, 내장 음성)

| 컷 | 파일 | 길이 | 대사 처리 | 1차 판정 | 비고 |
|---|---|---|---|---|---|
| C0 | C0/EP01_C0_PHONE_INSERT_kling3_v05_take01.mp4 | 3s | 없음 | OK | 스틸 없이 텍스트→영상. 흰 폰 face-up 빈 화면, 알림 스택 UI 합성 |
| C1 | C1/EP01_C1_TWOSHOT_kling3_v05_take01.mp4 | 5s | 여·남 Kling 내장 | OK (사용자 승인) | 여자 목소리 너무 한국식 → 이후 컷부터 베트남 억양 지정 |
| C2 | C2/EP01_C2_OTS_PHONE_kling3_v05_take01.mp4 | 5s | 남 Kling / 여 OS→TTS | OK | 3초쯤 폰을 돌려 빈 화면이 카메라 쪽 → UI 합성 가능 |
| C3a | C3/EP01_C3a_MAN_CU_kling3_v05_take02.mp4 | 3s | 남 Kling | OK (사용자 요청: 폰 보면서 대사) | take01은 옆을 보다 말함 → 폐기 |
| C3b | C3/EP01_C3b_WOMAN_CU_kling3_v05_take01.mp4 | 3s | 여 Kling (베트남 억양 지정 첫 컷) | OK, 목소리 확인 필요 | 웃음 살짝 큰 편 |
| C4 | C4/EP01_C4_HANDS_PHONE_kling3_v05_take01.mp4 | 5s | 없음 → 남 VO + 여 OS TTS | OK | 줌인 후 화면에 희미한 앱 상단바 생김 → UI 풀 합성으로 가림 |
| C5a | C5/EP01_C5a_WOMAN_PHONE_kling3_v05_take01.mp4 | 3s | 없음 → 남 OS + 여 VO TTS | OK | 빈 화면 카메라 쪽 유지 |
| C5b | C5/EP01_C5b_MAN_CU_kling3_v05_take01.mp4 | 3s | 남 Kling / 여 OS→TTS | OK | C7 스틸로 생성 |
| C6 | C6/EP01_C6_TWOSHOT_MOM_kling3_v05_take03.mp4 | 5s | 4줄 모두 Kling 내장 | 확인 필요 | 대사 변경: "우리 엄마~" / "다 이모랑 사촌이었어" (take01·02는 구 대사) |
| C7 | C7/EP01_C7_MAN_FREEZE_kling3_v05_take01.mp4 | 3s | 없음 | OK | 정지 홀드, 눈 1회 깜빡 |

크레딧: 1차 66 + 재생성 C6×2(20) + C3a(6) = 92. 효과음/앰비언스 Mirelo 약 13.
전체 프레임 시트: EP01_ALL_CUTS_take01_contact_sheet.png

## 남은 작업 (2026-10-29 픽처락 v24 이후)
1. 자막: C0 "여자친구 가족방에 초대된 지 40초" + 대사 자막 스타일 결정(폰트/위치/세이프존), 전 컷 삽입
2. BGM: 07_BGM/BGM_EP01_playful_sitcom_sonilo_take01.mp4(60s) 깔고 대사 구간 덕킹, 아웃트로 엔딩 처리
3. 폰 화면 인서트 연출 결정: 번역이 읽히는 풀스크린 인서트 1개 추가 여부(크레딧 0)
4. 9:16 세이프존(상단 UI/하단 캡션 영역) 점검 후 최종 내보내기(1080x1920, H.264)
5. EP02: 대본 → 스틸 → 컷당 1테이크 + whisper 검사 → 조립. 예산 200크레딧 이내

## 알려진 연속성 이슈
- 남자 폰 색: C1·C3a·C4는 검정, C2·C5a·C5b·C6·C7·C0은 흰색(투명 케이스). 스틸 단계 불일치. 편집에서 티 안 나면 두되, 재생성 시 흰색으로 통일 권장.
- 좌석: C1·C6 나란히, C2·C5a 마주보기 (숏리스트 메모 그대로).

## 가편집
- edit/EP01_ROUGHCUT_v01_untrimmed.mp4 — 그대로 이어붙임 (38s)
- edit/EP01_ROUGHCUT_v02c_bed_chimes.mp4 — 트림 + 카페 앰비언스 베드 + 단일 띠링 (TTS 없음)
- edit/EP01_ROUGHCUT_v03_c3a-t02_c6-t03.mp4 — v02c + C3a take02 + C6 take03 (현재 기준본)
- 사용자 규칙: 알림은 진동 말고 소리. 연타 효과음(burst) 금지. TTS 프리셋(Hana/Marcus)은 어색해서 보류.
- edit/EP01_ROUGHCUT_v04_opening_c7line.mp4 — v06 대본: N1(투샷 "토마톡 가족톡방에 초대했어… 여섯 명/귀엽네/귀여워?/응. 작아서") + N2(여 CU "자, 이제 우리 가족방") + C0~C6 + C7 take02("한 분씩 인사드리려면… 하루 걸리겠는걸"). 앰비언스는 AMB_CAFE_LIVELY (take01 룸톤은 웅웅거려 슬프게 들림 → 폐기). 44.4s.
- edit/EP01_ROUGHCUT_v05_n0n1_c1t02_c7t03.mp4 — 현재 기준본. N0(남 "우리는 엄마, 아빠, 나, 동생 4명이야. 들어왔지?") + N1 take03(여 "우리집 토마톡 대화방에 초대했어. 링크 갔지?") + C0 + C1 take02(여 밝은 톤) + C2 + C3a t02 + C3b t01 + C4 + C5a + C5b + C6 t03 + C7 take03(쉼 없이). 42.4s. N1 t01/t02, N2 t01은 폐기(파일 보존).
- edit/EP01_ROUGHCUT_v06_newlines.mp4 — 현재 기준본. N0 t03("네 명이야", 손동작 없음) + N1 t04("토마톡 메신저 가족 대화방에 초대했어.") + C0 + C1 t03(남 "응~ 가족이 엄청 많구나~" 당황) + C2 t02("근데 계속 사람이 늘고 있는데?") + C3a t04("그동안 어떻게 참으셨지?", 폰만 봄) + C3b t02("알지~ 질문 많이 하지 말라 그랬는데…" 밝게) + C4 + C5a + C5b + C6 t03 + C7 t04(이마 짚기). 42.4s.
- edit/EP01_ROUGHCUT_v07_c6split_n1lipsync.mp4 — 현재 기준본. v06 + N1 take05(4s, 립싱크 보강) + C6를 C6a 투샷/C6b 남 CU/C6c 여 CU 3컷으로 분할(얼굴 드리프트 해결). 47.4s.
- edit/EP01_ROUGHCUT_v08_script_v07_order.mp4 — script_v07.md 순서(N0 N1 C0 C1 C2 C4 C5a C5b C3a C3b C6a C6b C6c C7). N1 t06("응, 오빠도 가족방에 초대했어"), C3b t03("아 진짜… 질문 많이 하지 말라 그랬는데" 당황), C6b t02("어머님?"). 46.4s.
- 크레딧 메모: 울트라 결제 후 Kling 생성은 먼저 부스트 200크레딧에서 차감됐고(잔액 표시 안 줄던 이유), 2026-10-29 오후 소진 → 이후 월 크레딧에서 차감.
- edit/EP01_ROUGHCUT_v08b_c1full_c6ahold.mp4 — v08 + C1 5초 전체(대사 잘림 수정) + C6a t02 5초(우리 엄마~ 뒤 2초 정적). 50s.
- edit/EP01_ROUGHCUT_v08c_c6b_hair.mp4 — v08b + C6b t03(머리 고정). 50s.
- edit/EP01_ROUGHCUT_v08d_c5b_nomusic_omni_c6b.mp4 — v08c + C5b t02(음악 금지) + C6b를 Kling 3.0 Omni 얼굴참조 테이크로 교체 + C6c t02(시선 고정 시도). 50s.
- edit/EP01_ROUGHCUT_v08e_no_omni.mp4 — v08d에서 Omni C6b → kling3_0 C6b t03으로, C6c → t01로 되돌림(영어 발화 의심 컷 제거). 50s.
- edit/EP01_ROUGHCUT_v09_pro_firstpick.mp4 — v08 pro 배치 1순위 테이크(video/v08/SELECTION_v09.md), C5c 인서트 포함, 1080x1920. 조립 스크립트: scratchpad/assemble.py
- edit/EP01_ROUGHCUT_v09b_n0take13.mp4 — v09 + N0 take13 (사용자 선택). 52.5s.
- edit/EP01_ROUGHCUT_v10_std_takes.mp4 — 사용자 결정(2026-10-29): pro 일괄 배치는 대사 오류·영어 섞임으로 폐기. pro 배치 전 std 테이크로 복귀 + N0 pro take13("우리집은 4명. 들어왔지?") + C5c pro take02 인서트. 조립: scratchpad/assemble_std.py (파일 목록이 곧 선택표). 1080p 업스케일. 52.5s.
- edit/EP01_ROUGHCUT_v10b_all_std.mp4 — v10 + N0도 std take03으로 복귀(pro take13은 '그건 사실이야' 환청 대사). 전 컷 std, C5c만 pro. 52.5s.
- edit/EP01_ROUGHCUT_v11_c4_after_c5b.mp4 — v10b에서 C4(손+폰)를 C5b 뒤로 이동, C5c 제외. 50s.
- edit/EP01_ROUGHCUT_v12_c6a_short_c8_end.mp4 — v11 + N0 take06(치아) + C6a 3.6s(어머님? 앞 정적 단축) + C6c v08 take04(시선) + C8 엔딩 여 '그래도 바로 번역돼서 다행이다~' take02. 51.6s. A/B: edit/N0_std_takes05_06_AB.mp4, edit/C6c_takes03_04_AB.mp4, edit/C8_takes01_02_AB.mp4
- edit/EP01_ROUGHCUT_v12b_c6a_4p3.mp4 — v12 + C6a 4.3s(우리 엄마~ 끝까지 + 0.5s). 52.3s.
- edit/EP01_ROUGHCUT_v12c_c6a_full_c8t01.mp4 — C6a 4.8s(대사 끝 4.5s + 여유), C8 take01. 52.8s. C8 목소리 비교: edit/C8_voice_match_C6c_then_t01_t03_t04.mp4 (기준 C6c → C8 t01 → t03 → t04)
- edit/EP01_ROUGHCUT_v12d_c1t05.mp4 — v12c + C1 take05(눈 고정, 흰 폰 스틸). A/B: edit/C1_takes04_05_AB.mp4. 52.8s.
- edit/EP01_ROUGHCUT_v12e_c1t04.mp4 — C1 take04 (take05는 남자 대사 누락). 추가 C1 t06/t07 비교: edit/C1_takes04_06_07_AB.mp4
- C1 미디엄 투샷 스틸(v09 nbp)은 얼굴 이탈로 폐기(사용자). C1은 images/v08/EP01_C1_TWOSHOT_v08_nbp_take02.png(원본 얼굴, 흰 폰) 기준.
- edit/EP01_ROUGHCUT_v12f_c1t06.mp4 — C1 take06 (사용자 선택). 52.8s.
- edit/EP01_ROUGHCUT_v12g_c1_t06v_t03a.mp4 — C1 = take06 영상 + take03 남자 음성(2.3s부터 '응~ 가족이 엄청 많구나~') 합성. 52.8s.
- edit/EP01_PICTURE_LOCK_v12g.mp4 — 사용자 승인 픽처락 (2026-10-29). 조립 목록: edit/assemble_v12g_LOCKED.py
- edit/EP01_ROUGHCUT_v15_inserts.mp4 — 실제 토마톡 레이아웃 UI(ui/real/)를 합성 전용 인서트 스틸(images/inserts/, 화면 정면·순백)에 얹고 살짝 줌인(scratchpad still_anim.py). C2 3.4s + C2i 2s, C5a/C4 인서트 교체. 이전 트래킹 합성(video/comp/*_comp_*, *_tk, *_big, STILLANIM)은 폐기.
- edit/EP01_ROUGHCUT_v16_c1split.mp4 — C1 투샷 → C1a 여 CU '들어갔어?'(t01, 2.4s) + C1b 남 CU '응… 가족이 엄청 많네'(t01, 3s). 입모양·얼굴·폰 뒷면 문제 해결. 53.6s.
- edit/EP01_ROUGHCUT_v17_c0lock.mp4 — C0를 인서트 스틸(테이블 위 폰, 정면) + 실제 토마톡 알림 배너 스택 잠금화면 + 미세 흔들림으로 교체. 53.6s.
- edit/EP01_ROUGHCUT_v18_ui_v2_c6a_t03.mp4 — v17 + C6a v08 take03("…또 들어왔어" / "어! 우리 엄마~ 이제 들어왔네", 4.6s; take04는 비교본 edit/C6a_takes03_04_AB.mp4) + 폰 UI 전면 재렌더(ui/real/render_ui_v2.py → ui/real/*_v2.mp4 → still_anim.py fit=stretch 합성). 날짜 알약 없이 처음부터 꽉 찬 채팅창이 새 메시지마다 실제 앱처럼 밀려 올라감(연속 스크롤). C5a는 손가락 없는 여자 스틸 take01 + 입력창에 적힌 문장이 0.4s에 바로 전송. C0 잠금화면은 시계를 아래로 내리고(화면 비율에 맞춰 렌더해 잘림 없음) 실제 배너 6장 스택. 영어 쓰는 호주 사촌 Emily 🇦🇺 추가 → 남자 폰(한국어 번역+영어 원문)·여자 폰(베트남어 번역+영어 원문) 둘 다 번역 UI 노출. 띠링은 UI 도착 타이밍에 맞춤(C0 6회, C2i 3회, C4 8회). 53.4s.
- edit/EP01_ROUGHCUT_v18b_c6a_t04.mp4 — v18에서 C6a를 v08 take04(4.8s)로 교체. take03은 1.5초부터 남자 뺨에 점이 생기고 당황 대신 웃는 표정이라 폐기(프롬프트의 여자 '눈 밑 점' 묘사가 남자에게 옮겨간 것으로 추정 → 다음 C6a 재생성 때 "the man has no moles" 추가). 53.6s.
- edit/EP01_ROUGHCUT_v18c_corners.mp4 — 사용자 지적(모든 인서트에서 UI 직각 모서리가 베젤 위로 삐져나옴, 여자 폰은 UI 각도·크기 어색): still_anim.py에 둥근 모서리 마스크(corner=95, UI 좌표계에서 그려 함께 워프), 정확한 화면 쿼드(white=250 폴리곤 검출 또는 quad 직접 지정, grow_side=0), 여자 스틸은 흰 영역 위아래 검은 띠까지 화면으로 확장(grow_top=0.115 grow_bot=0.127, 캔버스 830x1958)하고 손가락만 가리는 occl=skin 모드 추가. 흰 폰(남자·테이블)은 흰 베젤 때문에 자동 검출이 안 되므로 쿼드를 직접 지정: 남자 [[577,860],[965,860],[965,1658],[577,1658]], 테이블 [[493,884],[1033,884],[1033,2064],[493,2064]]. 53.6s.
- edit/EP01_ROUGHCUT_v18d_nail.mp4 — v18c에서 C5a만 재합성: occl=skin은 손톱(저채도)을 화면으로 오인해 UI가 덮었음 → occl=display 모드 추가(스틸에서 순백 화면 픽셀 또는 검은 띠 픽셀만 UI로 교체, 손가락·손톱은 전부 보존). 여자 C5a 합성 명령: still_anim.py ... white=250 grow_side=0 grow_top=0.115 grow_bot=0.127 corner=95 occl=display fit=stretch zoom=1.06. 53.6s.
- edit/EP01_ROUGHCUT_v18e_c1b_clean_c6a_trim.mp4 — C1b take01의 왼뺨 점(시작 스틸부터 있던 환각, take02도 동일)을 ui/real/remove_spot.py(템플릿 추적 + 인페인팅)로 지운 _nomole.mp4 사용. C6a take04는 앞 0.5초에 영어 중얼거림("did you see that")이 있어 0.95초부터 3.85초 사용(남 대사 0.3초 뒤 시작). 조립 스크립트 picks 5번째 값 = 시작 오프셋. 52.65s.
- edit/EP01_ROUGHCUT_v18f_no_c5a_no_c6a.mp4 — 사용자 지시: C5a(여자 폰 인서트 19~22초) 삭제, C6a(영어 섞인 투샷 36~40초) 삭제. C6a 자리에는 남자 폰 "Mẹ님이 입장했습니다" 인서트 1.5초(comp/EP01_C6_INSERT_mom.mp4, 띠링 0.35s)를 넣어 C6b "어머님이 지금?"의 앞 상황을 유지. 47.3s.
- edit/EP01_ROUGHCUT_v19_profiles_c8sip.mp4 — v18f + C8 재생성(prompts/v08/EP01_C8_v08b_sip.txt: 대사 후 아이스 아메리카노 빨대를 물고 민망하게 시선 피함, 5s, std 2테이크 20크레딧) take02 사용. A/B: edit/C8_sip_takes01_02_AB.mp4. 채팅 인서트 프로필을 실사 사진으로 교체(00_MASTER_ASSETS/04_UI/PROFILES/*.png, Nano Banana Pro 1k, 2크레딧×8: Dì Hai 부겐빌레아, Dì Ba 식탁, Dì Tư 아오자이+연꽃, Dì Năm 손주, Cậu Sáu 맥주, Dì Bảy 다낭 셀카, Emily 멜버른 카페, Mẹ 매화). 생성 헬퍼: tools/hf_gen.py (CLI generate create --wait → _status.json + curl 다운로드). 49.3s.
- edit/EP01_ROUGHCUT_v19b_c8line_c1a_gate.mp4 — C8 v08b 5초 2테이크는 음성 인식(tools/transcribe.py, faster-whisper small) 결과 둘 다 대사가 바뀜("야, 드디어 왔어" / "내가 달래줄게") → 폐기. C8은 승인된 v08 take01(3s)로 복귀. C1a "들어갔어?" 밑에 Kling이 넣은 낮은 지속음 → afftdn + 대사 구간(1.1~2.3s) 외 무음 처리(picks 6번째 값 = 추가 오디오 필터). v19b의 대사 컷 11개 전부 whisper로 대사 일치 확인.
- edit/EP01_ROUGHCUT_v20_sip_outro.mp4 — v19b + C8b 무대사 빨대 클립(prompts/v08/EP01_C8b_sip_nodialogue.txt, 3s std 2테이크 12크레딧, take01: 빨대 물고 눈 옆으로 굴리며 민망) + 공통 아웃트로(00_MASTER_ASSETS/08_OUTRO/render_outro.py → TOMATOK_OUTRO_v01.mp4 4.5s: 엄마 베트남어 메시지 → 한국어 번역 말풍선 → 앱 아이콘 + "실시간 번역 메신저, 토마톡 / 말이 달라도 가족이니까"). 교훈: 대사 컷에 동작까지 5초로 시키면 Kling이 대사를 바꿈 → 대사 3초 + 동작 3초 분리 생성. 54.8s.
- edit/EP01_ROUGHCUT_v20b_sip_outro.mp4 — 아웃트로를 사용자 제공 로고(~/작업/로고관련/토마톡로고토마톡로고1@4x.png → 04_UI/TOMATOK_LOGO_4x.png, 840w 축소본)로 교체, 겹침 검사(세로 밴드: 말풍선 380~700 / 로고 900~1283 / 문구 1344~1394 / 부제 1432~1464). TOMATOK_OUTRO_v02.mp4.
- edit/EP01_ROUGHCUT_v21_eyes_end.mp4 — 사용자 지시: C2i(17~19초)·C6i(33~34초) 폰 화면 삭제, "또 들어왔어/어? 우리 엄마" 투샷 복구 = v07 take02(whisper 한국어 확인; v08b take03/04는 말레이어 발화 "Awak nampak itu?"라 폐기). 엔딩 = C8 대사 → C8c 눈 클로즈업 눈알 굴리기(images/v08/EP01_C8c_EYES_ECU_nbp_take02.png를 NB Pro로 만들고 Kling 3s 무대사 2테이크 12크레딧, take01 사용; A/B edit/C8c_eyes_takes01_02_AB.mp4) → 아웃트로. 빨대 클립(C8b)은 제외. 폰 인서트는 C0·C4만 남음. 51.6s.
- edit/EP01_ROUGHCUT_v22_sip_end.mp4 — 사용자: 눈 클로즈업(C8c)이 야외처럼 보임 → 제외. 엔딩 = C8 대사 → C8b 빨대 커피 + 눈 옆으로 굴리기(take01, 0.5s부터 2.5s, 1.12배 펀치인 크롭으로 점프컷 완화; picks 7번째 값 = 추가 비디오 필터) → 아웃트로. 55.6s.
- edit/EP01_ROUGHCUT_v23_c8_zoom.mp4 — 사용자: 엔딩 유지, "번역돼서 다행이다"(C8)는 1.2배 줌인(얼굴 쪽 크롭), 커피 빨대 컷(C8b)은 1.12배에서 시작해 2.5초 동안 전체 프레임으로 줌아웃(zoompan). 55.6s.
- edit/EP01_ROUGHCUT_v23b_logo.mp4 — v21~v23이 아웃트로 v01(작은 앱 아이콘 확대본)을 참조하고 있던 실수 수정 → TOMATOK_OUTRO_v02(사용자 제공 4x 로고). 55.6s.
- edit/EP01_ROUGHCUT_v24_newlines_matchcut.mp4 — C2 대사 "그런데 계속 누가 들어오는데?"(v08c take03, 3s; whisper 확인. v08b/v08c take01~02는 프롬프트 파일 누락으로 빈 프롬프트 제출된 불량분, 영어 발화 → 폐기, 약 24크레딧 손실). C6b 대사 "질문 제일 많이 하신 분이 어머님 아니셨어?"(v08b take01 4.2s; whisper는 끝을 '어머니 많이셨어'로 들음 → 사용자 청취 확인 필요, A/B edit/C6b_newline_takes01_02_AB.mp4). C8b 커피 컷을 C8 마지막 프레임(images/v08/EP01_C8_LASTFRAME_take01.png)에서 생성(v09 take01, prompts/v08/EP01_C8b_v09_from_lastframe.txt)해 매치컷; C8 1.2배 크롭 → C8b 1.2배에서 1.0으로 줌아웃. 아웃트로 v03 부제 "언어가 달라도 대화는 바로바로". 56.0s.
- edit/EP01_PICTURE_LOCK_v24.mp4 — 사용자 승인 픽처락 2차 (2026-10-29 저녁, "오케이 완료"). 조립 목록: edit/assemble_v24_LOCKED.py. 이전 픽처락 v12g는 대체됨.
- edit/EP01_PICTURE_LOCK_v24b.mp4 — 픽처락 v24 + C0 잠금화면 날짜↔배너 간격 확대(배너 시작 0.27H→0.34H). 조립: edit/assemble_v24b.py
- edit/EP01_v25b_subs_B.mp4 — 자막 B안(흰 글자 + 반투명 검정 바, 72% 높이; C0 상황 자막은 폰 아래 80%) 전 대사 삽입. 타이밍 = tools/subtitles_pass.py(faster-whisper 단어 시간, 텍스트는 대본 기준). 자막 목록: *.subs.json. 자막 스타일 렌더: tools/subtitle_style.py
  (remove_spot.py는 tools/로 이동)
- edit/EP01_PICTURE_LOCK_v24d.mp4 / edit/EP01_v25d_subs_B.mp4 — C6a1 "누가 또 들어오셨어."를 당황(눈 커짐) 버전으로 교체(v08c take01, 6크레딧, whisper 통과). C6c 자막을 실제 발화 "그동안은 다 이모랑 사촌이었어."로 수정. 조립: edit/assemble_v24d.py
- edit/EP01_PICTURE_LOCK_v24e.mp4 / v25e_subs_B / v26e_subs_bgm — C6a1을 "누가… 또 들어오시네?"(얼떨떨, 끝음↑, v08d take01, 6크레딧, whisper 통과)로 교체. v26 = 자막본 + BGM(07_BGM playful sitcom, volume 0.16, 대사 사이드체인 덕킹 threshold 0.06 ratio 6, 1s 페이드인/55.5s부터 2.5s 페이드아웃). BGM 믹스 명령은 이 줄의 파라미터 참고(스크립트화 예정: tools/finish_pass.py).
- export/EP01_FINAL_20261029_v27_title.mp4 — 최종 출력본. v26e(자막+BGM) + 고정 템플릿(상단 왼쪽 알약: 로고 + "가족방이 안 멈춰요 EP.01", y=290, 본편 0~아웃트로 시작까지, 0.4s 페이드) → 1080x1920 24fps H.264 High, AAC 48k 192k, loudnorm -14 LUFS. 템플릿 에셋: 00_MASTER_ASSETS/09_TEMPLATE/EP01_TITLE_topleft.{png,html}. 세이프존 점검: edit/SAFEZONE_CHECK_v26e.png (상단 250 / 하단 420 / 우측 180 밖 확인).
- edit/EP01_PICTURE_LOCK_v24f / v25f / v26f, export/EP01_FINAL_20261029_v28_c2.mp4 — C2를 "계속 들어오시는데?"(얼떨떨, 끝음↑, v08d take01, 6크레딧, whisper 통과)로 교체한 최종 출력본. 이전 최종(v27)은 보관.
- export/EP01_FINAL_20261029_v28b_bgmlow.mp4 — 사용자: 배경음 너무 큼 → BGM volume 0.16→0.08, 덕킹 threshold 0.05 ratio 8 release 600. (edit/EP01_v26g_subs_bgm_low.mp4)
- tools/finish.py — 마무리 체인 자동화(조립→자막→BGM→템플릿→export). 예: python3 tools/finish.py edit/assemble_v24f.py v28c --bgm-vol 0.08 --open
