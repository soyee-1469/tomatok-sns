# 주인공 리캐스팅 브리프 v8 — "AI 얼굴" 벗어나기

작성일: 2026-10-27
대상: FEMALE_LEAD_01 (베트남 유학생, 약혼녀), MALE_LEAD_01 (한국인 약혼자)
이전 버전: CAST_v2~v7. v8에서 얼굴을 처음부터 다시 뽑는다. v7 시트와 로케이션(LOC_CAFE_v01)은 유지하되 얼굴만 교체.

---

## 1. 왜 전부 비슷하게 나왔나 (v4·v6·v7 진단)

| 증상 | 원인 | v8 대응 |
|---|---|---|
| 매끈한 피부, 완벽 대칭, V라인 턱, 큰 눈 | 프롬프트에 "young, attractive, Korean/Vietnamese" 같은 말만 있으면 모델은 학습된 평균 미인상으로 수렴한다 | 미인 관련 단어 전부 제거. "character actor, not a model" 명시 |
| 두 사람 다 똑같은 "살짝 미소 + 정면 응시" | 표정 지시가 없으면 기본값이 광고 미소 | 표정을 상황 연기로 지정 (생각 중, 입 다묾, 시선 살짝 옆) |
| 스튜디오 회색 배경 + 균일 조명 | 캐스팅 시트 형식 때문에 모든 질감 단서가 사라짐 | 창가 자연광, 폰 카메라 톤. 시트는 얼굴 확정 후 2단계에서만 |
| 나이가 전부 22살 | 나이 지시 없음 | 여 27, 남 31로 고정. "visible signs of late twenties/early thirties" |
| 두 사람 모두 회색 상의 | 의상도 평균값 | 의상으로도 구분 (아래 4절) |
| 뽑을수록 얼굴이 서로 닮아감 | 같은 채팅창에서 연속 생성하면 앞 얼굴이 섞임 | 후보 1명 = 새 채팅 1개. 다른 후보 이미지를 절대 같이 첨부하지 않음 |

핵심 원리: **평범하고 약간 비대칭이며 "결점"이 4~6개 명시된 얼굴**이 기억에 남고, 영상 모델(Seedance/Kling)에서도 동일 인물 유지가 더 잘 된다. 특징이 없는 얼굴은 컷마다 다른 사람으로 바뀐다.

---

## 2. 후보 방향 (각 3안, 서로 다른 유형)

최종은 **F 1안 + M 1안**. 투샷에서 체격·얼굴형·피부톤이 대비되는 조합을 고른다.

### FEMALE_LEAD_01 — 베트남 유학생, 27세, 차분하고 현실적, 은근히 장난기

**F-A "다낭에서 온 대학원생" (추천)**
- 둥근 얼굴, 낮은 코에 콧볼 약간 넓음, 도톰한 입술
- 쌍꺼풀 없는 속쌍꺼풀, 눈꼬리 살짝 처짐
- 골드·올리브 톤 피부, 볼에 옅은 주근깨
- 왼쪽 눈 아래 작은 점
- 머리: 긴 흑발을 낮게 대충 묶음, 잔머리
- 얇은 금속테 안경 (폰 볼 때 안경 올리는 동작이 리액션 소품이 됨)
- 158cm, 보통 체형

**F-B "오토바이 타는 언니"**
- 각진 턱, 높은 광대, 날카로운 홑꺼풀
- 확실히 탄 피부, 진한 일자 눈썹
- 앞니 하나 살짝 겹침
- 턱선 단발 + 뭉툭한 앞머리
- 163cm, 마른 체형
- 장난기가 얼굴에 바로 드러나는 유형

**F-C "시골 장녀"**
- 넓적한 얼굴, 코 위로 주근깨 많음
- 앞니 사이 작은 틈, 깊은 보조개
- 자연 곱슬 웨이브 머리, 어깨 길이
- 입이 커서 웃을 때 얼굴이 다 변함
- 155cm, 통통한 편

### MALE_LEAD_01 — 한국인, 31세, 회사원, 긴장 많고 되묻기 잘함

**M-A "평범한 대리님" (추천)**
- 살짝 통통한 둥근 얼굴, 눈 밑 다크서클과 애굣살
- 홑꺼풀 작은 눈, 두껍고 낮은 눈썹
- 자란 투블럭, 앞머리 이마에 붙음
- 면도 자국 푸른 턱
- 검은 사각 뿔테 안경
- 172cm, 뱃살 조금
- "…지금?" 같은 정적 연기가 얼굴에 잘 붙는 유형

**M-B "코 큰 삼촌형"**
- 긴 얼굴, 콧대에 혹 있는 큰 코
- 깊은 팔자주름, 얇은 입술
- 이마 넓고 M자 헤어라인 시작
- 180cm, 마르고 어깨 좁음
- 멀대 같은 몸으로 당황하면 더 웃김

**M-C "순둥이 곰"**
- 덩치 크고 이중턱 살짝
- 작은 눈, 귀가 크고 바깥으로 벌어짐
- 짧은 스포츠머리, 숱 많은 눈썹
- 178cm, 90kg대
- 큰 몸으로 작은 폰 보는 그림이 자체 개그

---

## 3. 프롬프트

규칙:
- **후보 1명당 새 채팅.** 이미지 첨부 없이 글로만.
- `[ ]` 안은 2절 특징을 영어로 바꿔 채움. 대괄호가 남으면 글자가 그대로 들어감.
- 먼저 **정면 1장(3-1)**만 뽑아 컨펌 → 통과한 얼굴로 **3칸 시트(3-2)** → 시트로 **표정 세트(3-3)**.
- 결과 판단은 사람 눈으로. 3번 뽑아도 미인형으로 돌아오면 특징 문장을 더 과장한다.

### 3-1. 정면 후보 (ChatGPT, 1명씩)

```text
Casting headshot for a low-budget Korean web sitcom. This is a CHARACTER ACTOR, not a model, not an idol, not an influencer. An ordinary person you would pass on the street in Seoul and not look at twice, but with a memorable face.

Subject: a [27]-year-old [Vietnamese] woman, a graduate student living in Korea.
Signature traits (keep every one, exaggerate rather than soften): [round face, low nose bridge with slightly wide nostrils, full lips, hooded eyes without a visible double-eyelid fold and slightly downturned outer corners, warm golden-olive skin with faint freckles on the cheeks, a small dark mole under the left eye, long black hair tied in a low messy bun with loose baby hairs, thin gold wire-frame glasses].
Height impression: [158 cm], average build.

Expression: not smiling. Mouth closed, mid-thought, as if she just read a message and is deciding how to reply. Eyes looking slightly off-camera to the right. Natural, slightly asymmetric face.

Photo: candid, shot on a recent iPhone by a friend, indoors by a cafe window, soft daylight from the left, shallow background. Head and shoulders, eye level, 50 mm look. Real unretouched skin: visible pores, slight shine on the nose, faint under-eye shadows, no skin smoothing, no beauty filter.

Negative: no K-pop idol look, no V-line jaw, no perfectly symmetric face, no big doll eyes, no glass skin, no studio lighting, no gray seamless backdrop, no makeup-ad look, no text, no watermark, no border.
```

남자는 Subject 줄과 특징만 교체:

```text
Subject: a [31]-year-old [Korean] man, an office worker.
Signature traits (keep every one, exaggerate rather than soften): [slightly chubby round face, small monolid eyes, puffy under-eye bags with dark circles, thick low straight eyebrows, grown-out two-block haircut with the fringe stuck flat to the forehead, visible blue-ish shaving shadow on the chin and upper lip, black square acetate glasses].
Height impression: [172 cm], a little soft around the belly.

Expression: not smiling. Mouth slightly open as if about to ask "wait, what?", eyebrows raised a few millimeters, eyes on something just below the lens (a phone screen).
```

### 3-2. 3칸 시트 (컨펌된 정면 1장 첨부)

```text
Use the attached photo as the ONLY identity reference. Same exact person: same face proportions, eye spacing, nose shape, skin tone, hair, glasses. Do not beautify, do not change age, do not slim the face.

Make ONE wide image, 3 equal panels side by side, 3:1 aspect ratio, plain light-gray background, no borders, no labels, no text.
Panel 1: head-and-shoulders, three-quarter angle turned 30 degrees to the left, neutral expression.
Panel 2: full body head to toe, front, standing relaxed, hands natural.
Panel 3: full body head to toe, back view.

Outfit (same in every panel): [olive-green cardigan over a white t-shirt, straight dark-blue jeans, white canvas sneakers, small gold hoop earrings].
Lighting: soft even daylight, no harsh shadows, true colors. Realistic unretouched skin and fabric texture. Full-bleed, edge to edge.
```

### 3-3. 표정 세트 (시트 첨부)

```text
Use the attached 3-panel sheet as the ONLY identity reference. Same person, same outfit, same glasses, same hair.
Make ONE image with 6 equal panels in a 3x2 grid, head-and-shoulders, same framing and same soft window daylight in every panel, light-gray background, no text, no labels.
Row 1: (1) neutral, listening  (2) small genuine smile, teeth barely showing  (3) confused: brows pulled in, head tilted 5 degrees
Row 2: (4) surprised: eyebrows up, lips parted, no wide-open mouth  (5) embarrassed half-smile looking down  (6) deadpan stare, completely still
Subtle sitcom acting, nothing exaggerated. Real skin texture, slight asymmetry kept.
```

---

## 4. 의상 (v04 콘티 수정 사항)

v04 콘티의 "여 회색 후디 / 남 회색 니트"는 두 사람이 한 덩어리로 보이게 한다. 리캐스팅과 함께 의상도 분리하는 것을 권장. 채택 시 `EP01_SHOTLIST_v04.md`의 의상 줄을 v05로 갱신한다.

| | 기존 v04 | v8 제안 | 이유 |
|---|---|---|---|
| 여 | 회색 후디 + 연청 | 올리브 가디건 + 흰 티 + 진청 | 골드 피부톤에 올리브가 살고, 민트 카페와 톤이 이어짐 |
| 남 | 회색 니트 + 네이비 바지 | 연한 체크 셔츠 + 네이비 카라 니트 조끼 또는 베이지 치노 | "회사원 느낌", 민트 배경에서 분리 |

둘 다 토마톡 레드가 없어야 폰 UI의 빨간 포인트가 산다.

---

## 5. 선택 기준 체크리스트

- [ ] 두 후보를 나란히 놓았을 때 얼굴형·체격·피부톤 중 2개 이상이 대비되는가
- [ ] 안경·점·치아·헤어라인처럼 **한 문장으로 설명 가능한 특징**이 각자 3개 이상인가
- [ ] 무표정에서도 "이 사람"이라고 알아볼 수 있는가 (미소를 빼고 판단)
- [ ] 나이가 설정(27 / 31)으로 보이는가
- [ ] 베트남 여성으로 읽히는 단서가 얼굴·피부톤에 있는가 (CAST_RESEARCH 1절 참고). 부족하면 소품(폰 케이스 국기 스티커, 금 귀걸이)으로 보강
- [ ] 영상 테스트: 3-2 시트로 Seedance/Kling 5초 클립 1개를 뽑아 얼굴이 유지되는지 확인 후 확정

---

## 6. 확정 후 할 일

1. 통과한 시트를 `CAST_v8_recast/SHEET_FEMALE_v08.png`, `SHEET_MALE_v08.png`로 저장. 정면 원본은 `FACE_FEMALE_v08.png`, `FACE_MALE_v08.png`.
2. `00_MASTER_ASSETS/01_CHARACTERS/*/character_bible.md`의 빈 외형 항목을 **확정 특징 문장(영어 원문 포함)**으로 채운다. 이 문장이 이후 모든 프롬프트의 IDENTITY LOCK이 된다.
3. 표정 세트에서 잘라 `EXP_*.png` 슬롯을 채운다.
4. `EP01/status.json`의 `characterReference`는 그대로 true, `updatedBy`와 `updatedAt`만 갱신하고 커밋 메시지는 `EP01: cast v8 recast`.
5. 이전 v7 기준 스틸(07_REF_STILLS_v2, EDIT_KIT)은 구도 참고용으로만 쓴다.

---

## 7. 확정 기록 (2026-10-27)

- 1차: 브리프 원안(F-A, M-A) → 특징은 정확했으나 호불호 갈리는 인상. 사용자 피드백 "호감형으로".
- 2차: 다크서클·면도자국·통통함 제거, 식별 요소(안경, 점, 눈매, 귀)만 유지.
- 3차: 여자는 더 또렷하고 밝게, 남자는 더 단정하게. **3차 둘 다 확정.**
- 생성 도구: ChatGPT 이미지 생성 (크롬 확장으로 Claude Code가 조작). 후보 1명 = 새 채팅 규칙 준수.
- 산출물: `FACE_*_v08.png` (1122×1402), `SHEET_*_v08.png` (2172×724, 3칸), `EXP_*_v08.png` (1536×1024, 3×2).
- 슬롯 반영: `01_CHARACTERS/*/` 에 FACE_FRONT, FACE_45_LEFT, FULL_BODY, FULL_BODY_BACK, EXP 6종 크롭 저장. 바이블 외형 항목과 IDENTITY LOCK 채움.
- 의상 확정: 여 아이보리 니트 가디건 + 미드블루 청바지 / 남 네이비 크루넥 니트 + 베이지 치노. → EP01 콘티 v04 의상 줄 갱신 필요(v05).
- 다음: Seedance / Kling에 SHEET + LOC_CAFE_v01 첨부해 테스트 클립 1개.
- 키 수정 (2026-10-27 17:3x): 사용자 피드백 "둘 다 단신으로 보임". 여 165cm/7.5등신, 남 180cm/7.5~8등신, 눈높이 85mm, 패널 높이 채우기로 시트 재생성 → `SHEET_*_v08b.png` 확정. 이전 시트는 `*_v08a_short.png`로 보관. 바이블 키·체형 항목 갱신.
