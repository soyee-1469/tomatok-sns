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

## 남은 작업
1. 사용자 시청: C3b·C6 여자 목소리(베트남 억양), C6 4줄 타이밍
2. OS/VO 대사 TTS: C2 여, C4 남+여, C5a 남+여, C5b 여 (목소리 선택 필요: `higgsfield voices list`)
3. BGM 30초 (sonilo_music)
4. 캡컷: UI 합성(ui/ 폴더), 자막, 효과음, 세이프존 확인, 9:16 내보내기
5. 최종본은 pro(1080p) 재렌더 검토 (3s 7.5 / 5s 12.5 크레딧)

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
