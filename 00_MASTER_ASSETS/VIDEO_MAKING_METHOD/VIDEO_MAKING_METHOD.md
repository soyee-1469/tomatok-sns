# 영상 만드는 방법 (실사풍 AI 영상) — 정리본

> 출처: Notion 「만화 속 동네를 진짜로 찍어온 것처럼 — 검정고무신 현실판 AI 영상 만드는 법」 (blake.exe, 2026-10-16 기준)
> https://rust-quiet-4bf.notion.site/AI-3f59a775569781b4b283c91c882ffe51
> 정리일: 2026-10-20 (KST). 원문 전체(STEP 1~5, 프롬프트 7개, 표, 토글)를 읽고 정리했어요. 할인/제휴 링크 내용은 뺐어요.

---

## 1. 한눈에 보기

```
① 참고 캡처 → ② 캐릭터 실사 사진/시트 → ③ 장소 사진/시트 → ④ 클립 뽑기 → ⑤ 편집
                 (ChatGPT)                (ChatGPT)          (힉스필드 Seedance 2.5)  (캡컷)
```

- **핵심은 ④.** 프롬프트마다 "누가 찍고 있는지"(예: 부모님이 캠코더를 한 손에 들고 찍음)를 정해준다. 그러면 AI가 일부러 흔들고, 초점을 놓치고, 급 줌인하면서 인물을 프레임 밖으로 반쯤 내보내서 AI 티가 덜 난다.
- 급하면 ④만: 캐릭터 사진 1장 + 장소 사진 1장 + 클립 1개면 한 장면이 나온다.
- 결과물: 클립 6개(5~8초) → 21초 릴스. 클립마다 "동작 하나 + 반전 하나".

## 2. 준비물과 비용

| 서비스 | 용도 | 비용 |
|---|---|---|
| ChatGPT (이미지 생성 가능 계정, 원작자는 Plus) | 캐릭터 사진, 장소 사진 | 무료 계정은 하루 생성 한도에 걸릴 수 있음 |
| 힉스필드 Seedance 2.5 | 영상 클립 | 720p 기준 초당 7크레딧 (5초 35 · 6초 42 · 7초 49 · 8초 56). 1편 6클립 273, 2편 8클립 266 크레딧 |
| 캡컷 | 컷 편집, 음악, 색보정, 자막 | 무료 |
| (선택) 클로드 코드 + 크롬 확장 / 힉스필드 MCP | 캡처 수집, ChatGPT 조작, 기획안·프롬프트 작성, 힉스필드 실행 대행 | 크레딧은 손으로 돌릴 때와 같음 |

⚠️ 한 번에 다 돌리지 말고 **"먼저 하나만 뽑아서 보여 줘"** — 8개를 한 번에 시키면 266크레딧이 한 번에 나간다.

## 3. 단계별 요약

### STEP 1. 참고 캡처 모으기 (5분)
- 캐릭터마다 얼굴이 잘 보이는 장면 1장. 옷·소품이 중요하면 그 부분 장면 1장 더.
- 소품은 실물 사진을 따로 구한다(예: 엿가위, 770ml 콜라병).
- **만화 그림만** 넣는다. 다른 사람 실사 사진을 같이 붙이면 그 얼굴이 섞인다.
- 원작 캡처는 참고용. 원작 화면을 영상에 넣어 배포하지 않는다.

### STEP 2. 캐릭터 실사 사진 (한 명당 5분)
- ChatGPT에 캡처 1장 + 프롬프트(아래 원문). [ ] 안은 영어로 바꿔 쓰기(남으면 글자가 그대로 들어감).
- 성공 기준: 머리~신발 전신, 적은 특징 절반 이상이 보임.
- 안 닮으면 특징 문장을 더 과장 → 그래도 안 되면 상반신 먼저 만들고 "같은 얼굴로 전신".
- 가장자리 누런 테두리/먼지는 3~5% 잘라내기(영상에 번짐).
- 2편부터는 **3칸 시트**(1칸 얼굴 클로즈업 / 2칸 목 아래 정면 전신 / 3칸 목 아래 뒷모습, 가로 3:1). 얼굴 급 줌인이 많을 때 유리.

### STEP 3. 장소 사진 (한 곳당 3분)
- 장소 사진이 두 번째로 중요. 먼저 만들어서 모든 클립에 같이 넣어야 같은 동네가 나온다.
- 기준 사진(집) 1장을 **글로만** 만든다(만화 그림 넣으면 미니어처 구도). 한 이미지 2칸, 둘 다 눈높이, 사람 0명, 테두리 없음.
- 3D/미니어처처럼 보이면 "구도 그대로, 질감과 빛만" 수정 프롬프트.
- 나머지 장소는 기준 사진을 통째로 첨부하고 **한 장씩 따로** 돌린다(한꺼번에 시키면 룩이 갈림).
- 영상에 쓸 땐 필요한 칸만 반으로 잘라서 올린다.

### STEP 4. 클립 뽑기 (한 개당 3분)
- 힉스필드 → Video → Create Video → Seedance 2.5(없으면 가장 높은 번호).
- 설정 4개: **화면비 9:16 / 길이(프롬프트별 5~8초) / 해상도 720p 또는 1080p / 오디오(켜면 현장음, 대사 어색하면 끄고 편집에서)**.
- 사진을 **먼저**, 프롬프트에 적힌 **순서대로** 올린다(첫 장 = @image1). 그다음 프롬프트 붙여넣기 → 초록 @Image 칩이 사진 개수만큼 보여야 정상. 순서가 바뀌면 장소가 사람이 된다.
- 프롬프트 구조: `SCENE CONTEXT → ACTIVE REFERENCES → LOCATION MAP → FIRST FRAME / BLOCKING → FORMAT MODE → OPTICS → CAMERA → ACTION(초 단위) → PERFORMANCE → PHYSICS → LIGHTING → AUDIO → STYLE → OUTPUT SETTINGS → POSITIVE LOCKS`
- 지우면 안 되는 줄: `A parent films with a handheld camcorder`(홈비디오화 핵심), `Rough handheld shake / Focus hunts / fast lens zoom-in`(손떨림·초점 놓침·줌인), `No music`.
- 내 캐릭터로 바꿀 땐 ACTIVE REFERENCES의 사람 설명 줄만 교체, @image 번호는 그대로.
- 합격한 클립을 다음 클립에 **@video1(룩·모션 레퍼런스)**로 같이 올리면 질감이 이어진다("Do not copy its ... action").
- 시트를 올릴 땐 `three-panel reference sheet`, `never show the sheet layout` 줄 유지.

### STEP 5. 편집 (30분, 캡컷)
- 앞뒤 허술한 부분 자르고 제일 좋은 순간만. 음악은 편집에서(상업 이용 가능한 음원). 색보정·그레인·자막도 캡컷. 9:16으로 내보내기.
- 성공 기준: 클립이 넘어가도 같은 인물, 같은 옷, 같은 장소로 보임.

### 🆘 안 될 때
| 증상 | 원인 | 해결 |
|---|---|---|
| 캐릭터가 안 닮음 | 특징 문장이 약함 | 특징을 더 과장, 안 되면 상반신 → 전신 |
| 친구 얼굴이 주인공을 닮아감 | 다른 캐릭터 실사 사진을 같이 첨부 | 그림 1장만 첨부 |
| 사진 가장자리 누런 테두리·먼지 | soft edges, scan dust 같은 옛날 사진 문구 | 문구 빼고 Full-bleed ... no border 줄 추가, 이미 생겼으면 3~5% 크롭 |
| 장소가 미니어처/3D 같음 | 내려다보는 각도, 너무 깨끗·고채도 | eye level, no aerial view, no tilt-shift + 수정 프롬프트 |
| 장소가 만화 구도 | 만화 그림 첨부 | 글로만 쓰기 |
| 장소가 오려 붙인 듯 | 사람 사진 같이 첨부 | 장소엔 사람 사진 X, 사람은 영상 단계에서 |
| 초록 칩이 안 생김 | 프롬프트부터 붙임 | 사진 먼저, @로 직접 선택 |
| 사람과 장소가 뒤섞임 | 업로드 순서 바뀜 | 적힌 순서대로 재업로드 |
| 영상이 너무 깔끔하고 AI 같음 | 손떨림 약함 | shake 10–15cm → 15–20cm, 줌인 시점 1초 앞당기기 |

### ✅ 돌리기 전 체크리스트
- [ ] 캐릭터 사진에 참고 그림만 첨부(다른 실사 X)
- [ ] 캐릭터 사진 가장자리 3~5% 크롭
- [ ] 장소 사진에 사람 0명, 쓸 칸만 잘라 올림
- [ ] 설정 9:16 / 해상도 / 길이 확인
- [ ] 사진을 적힌 순서로 올림, 초록 칩 개수 확인
- [ ] 영상 레퍼런스가 필요한 클립은 앞 클립 먼저 뽑아 같이 올림
- [ ] 전부 돌리기 전 1개만 먼저 돌려 얼굴 확인

### 자주 묻는 것
- 캐릭터 1명이어도 됨(캐릭터 1 + 장소 1 + 클립 1 = 한 장면). 내가 만든 캐릭터도 STEP 2 특징 문장만 바꾸면 됨.
- 클립 길이가 제각각인 이유: 동작 하나 + 반전 하나에 필요한 시간이 달라서(5~8초).
- 마음에 안 들면 같은 프롬프트로 한 번 더, 또는 고칠 점을 설명하고 수정된 프롬프트를 다시 받기.
- **결과 판단(OK/다시)은 사람이 직접 눈으로.** 원작자도 얼굴을 세 번 고쳤다.

---

## 4. 토마톡 시트콤 적용법

### 4-1. 기본 원칙 (기존 규칙 유지)
- **세로 9:16 네이티브만** (1080×1920). 가로 버전·아웃페인트 없음.
- **세이프존:** 위 200px, 아래 350px, 오른쪽 180px, 왼쪽 90px 안에는 얼굴·자막·중요한 화면을 두지 않는다.
- 깔끔한 광고 퀄리티, 과샤픈("지글지글") 금지. → 원문의 1990년대 캠코더 STYLE(테이프 노이즈, 오버샤픈 헤일로, 바랜 색)은 **그대로 쓰지 않고**, "요즘 폰으로 찍은 자연스러운 영상" 톤으로 바꾼다.
- 대사: 인물은 자기 언어로 말하고 **영어 자막 크게 + 한국어 자막 작게**.

### 4-2. 단계별 매핑
| 원문 단계 | 토마톡에서는 |
|---|---|
| ① 캡처 | 참고 영상 스틸(07_REF_STILLS_v2) + 콘티. 남의 영상은 **구도·연기 참고만**, 화면을 그대로 쓰지 않음 |
| ② 캐릭터 시트 | **ChatGPT**로 국제커플 모델 시트: 정면 / 옆면 / 3/4 / 감정(기본·웃음·당황·놀람·멋쩍음) / 의상 전신. 의상까지 미영 님 컨펌 후 확정 → 이후 모든 컷의 얼굴 기준(IDENTITY LOCK) |
| ③ 장소 시트 | **ChatGPT**로 카페 로케이션 시트 1장(같은 카페 두 각도: ①창가 2인 테이블 투샷 방향 ②맞은편에서 본 방향), 사람 0명, 눈높이, 테두리 없음. 이후 모든 클립에 첨부해 배경 통일 |
| ④ 클립 | **Higgsfield Seedance** 또는 **Kling 3.0** — 1컷 먼저 테스트해서 얼굴·시선·화질·비용 비교 후 더 나은 쪽(비슷하면 저렴한 쪽). 9:16, 1080p |
| ⑤ 편집 | 캡컷: 폰 화면 합성, 자막, 효과음(띠링), 음악 |

### 4-3. "누가 찍고 있는지" 카메라 설정 (핵심 적용)
캠코더 대신 **친구가 테이블 맞은편에서 폰으로 몰래 찍는** 설정을 기본으로 한다.

```text
CAMERA
A friend sitting at the next table films the couple on a smartphone held vertically in one hand at table height. Light natural handheld sway of 2 to 4 cm, slight re-framing when someone moves, a short focus hunt when the lens moves from a face to a phone screen, one quick digital zoom-in at the reaction beat. Modern phone video: clean, natural colors, no over-sharpening, no film grain.
```
- 폰 화면 컷(어깨 너머): `The friend leans behind @image1's shoulder and films over her shoulder down onto the phone screen, the screen faces up toward her face and the camera, never toward the opposite person.`
- 리액션 컷: 줌인은 "당황/귀엽다고?/23명" 같은 반전 순간에 한 번만.

### 4-4. 시선과 폰 방향은 프롬프트에 매번 명시 (지난 실수 교훈)
- 사진→영상 방식: 손이 굳고, 시선·폰 화면 방향이 틀어짐(화면이 카메라 쪽, 인물이 뒤를 봄).
- 스톡 영상 모션 컨트롤: 원본이 각자 메뉴를 보는 구간이라 두 사람 시선이 따로 놂.
- 그래서 ACTION/PERFORMANCE에 반드시 적는다:
  - 누가 누구를 보는지: `@image1 looks at @image2's eyes`, `both look down at the same phone`.
  - 폰 화면 방향: `the phone screen faces @image1 (the holder)` / `he turns the screen toward her`.
  - 폰 개수: `only one phone in frame` 등 POSITIVE LOCKS에 고정.
  - `no look at the camera` 유지.

### 4-5. 폰 화면은 나중에 합성
- 생성 단계에서는 폰 화면을 **빈 화면(밝은 단색)**으로 두고(`the phone screen is a plain bright blank screen`), 편집에서 토마톡 기본 UI(`00_MASTER_ASSETS/04_UI/BASE_SCREENS/`)로 만든 채팅 화면을 네 모서리에 맞춰 합성.
- **번역 규칙:** 다른 사람 말풍선은 **번역(내 언어)이 위, 원문이 아래**. 내가 보낸 말풍선은 **번역하지 않음**.
- 친척 프로필은 실제 사진 느낌 또는 회색 사람 아이콘(알파벳 아이콘 X). 단체방 인원 수는 대본과 맞추기(예: 22명 → 23명).

### 4-6. 작업 순서 (권장)
1. 콘티 확정(비트별 초, 대사, 시선, 폰 방향).
2. ChatGPT 모델 시트 → 컨펌 → 카페 시트 → 컨펌.
3. 첫 클립 1개만 Seedance/Kling으로 테스트 → 얼굴·시선·화질 확인 → 비교 후 툴 결정.
4. 합격 클립을 @video 레퍼런스로 다음 클립에 연결해 톤 통일.
5. 캡컷에서 화면 합성 + 자막 + 효과음. 9:16 내보내기, 세이프존 확인.

---

## 5. 원문 프롬프트 (그대로 인용)

### STEP 2~3 프롬프트 원문

### STEP 2. 캐릭터 실사 사진 만들기 (한 명당 5분)
ChatGPT 채팅창에 만화 이미지 1장을 첨부하고 아래를 복붙하세요.

```text
Turn the attached cartoon character into a real 1970s Korean boy, as if casting a live-action film. He must be instantly recognizable as this exact character. Push the likeness toward the cartoon's proportions rather than toward a typical cute model.

Signature traits to keep: [여기에 만화 특징 4개에서 6개. 머리 모양, 얼굴 비율, 눈, 입, 귀]. Outfit: [여기에 옷 설명. 색, 무늬, 신발]. About [나이] years old.

Photo style: a candid full-body snapshot from 1972 on cheap color negative film, hard afternoon sun, visible heavy film grain, faded colors. Location: a dusty Korean village alley with a rough cement block wall and a stone wall behind him.

Real skin: uneven tan, visible pores, dust on his legs, no retouching, no skin smoothing, no beauty lighting. Clothes worn, faded, stretched, hand-me-down. One single full-body photo.
Full-bleed image edge to edge: no border, no frame, no vignette, no dust specks, no vintage overlay. No text, no logos, no watermark.
```
대괄호 [ ] 안의 한국어 안내는 지우고 본인 캐릭터에 맞게 영어로 다시 쓰세요. 대괄호가 남아 있으면 그 글자가 그대로 들어가요. 남자 어른이면 boy를 man으로, 여자아이면 girl로 바꾸세요. 영어가 어려우면 한국어로 특징을 적어서 ChatGPT에 "이걸 영어 문장으로 써줘"라고 시키세요.

소품이 중요한 캐릭터(엿장수)는 이 프롬프트 말고 아래 두 번째 토글의 프롬프트를 쓰세요.


**▸ 제가 실제로 쓴 특징 문장 (복붙해서 고쳐 쓰세요)**

기영이

```text
oversized squarish head, short flat-top hair with a few stubborn spiky tufts at the crown, big round wide-set eyes, round cheeks. Outfit: faded orange short-sleeve tee with a small T mark on the chest, short blue-purple shorts, black rubber shoes. About 8 years old.
```
초록 티 친구 (승철이)

```text
oversized tall domed head with a very high wide forehead, nearly shaved head with only a few thin long wisps of hair combed back from the crown, big ears sticking out, thin high eyebrows, small nose, wide laughing open mouth, eyes looking down and to the side. Outfit: faded green short-sleeve tee with a darker green horizontal band across the chest, worn gray shorts, both hands tucked into the pockets, flat black rubber shoes. About 8 years old.
```
보라 셔츠 친구 (도승이)

```text
black straight bowl cut with a blunt fringe sitting low and flat across the forehead, a wide round face, ears showing, calm half-lidded eyes glancing to the side, closed mouth with a faint smile. Outfit: faded violet short-sleeve button shirt with a white Peter Pan collar and three buttons, dark navy shorts, one hand resting on his stomach, the other hanging at his side, flat black rubber shoes. About 8 years old.
```

**▸ 소품이 중요한 캐릭터는 이렇게 (엿장수 + 엿가위)**

만화 얼굴 장면, 만화 하체 장면, 엿가위 실물 사진 3장을 한 번에 첨부하고 아래를 복붙했어요.

```text
Use the attached images as references. Image 1 (cartoon face) is the character: make him a real person in a real photograph, in the Korean countryside of 1972, keeping the cartoon's signature traits and pushing the proportions toward the cartoon: a long, bony face with a big wide grin showing his upper teeth, thick arched eyebrows, a slightly hooked nose, a tanned weathered face, small ears, a floppy brown bucket hat pulled down low.
Image 2 (cartoon lower body) is the outfit: a plain white short-sleeve cotton undershirt, loose and sweat-stained, dark navy baggy trousers that are wide and slightly too long, and worn black rubber shoes (gomusin, boat-shaped). Thin tanned arms.
Image 3 (real photo) is only the object reference for his candy scissors (yeot-gawi): copy it exactly. Hand-forged dark iron scissors, about 40 cm long, with two large teardrop-shaped finger loops, two very wide flat rectangular blunt blades with squared-off ends, a single large hex bolt in the middle, rusty dark metal with scratches and uneven forging marks. Do not copy the hand or background from image 3.
He is a candy (yeot) peddler. He holds the giant scissors in one hand, one finger through a loop, raised at chest height, laughing mid-sales-pitch. The scissors are always in his hand.
Full-body shot at human eye level, seen head to toe, standing in front of an old fieldstone wall on a dusty dirt lane. Beside him a wooden candy tray box with sheets of candy and a cloth cover, resting on a wooden stand.
Look: a 1972 candid snapshot on cheap 35mm color negative film, bright hazy summer sky, slightly overexposed highlights, muted natural colors, uneven tan skin, heavy grain, deep focus, no retouching, no HDR.
Full-bleed image edge to edge: no border, no frame, no vignette, no dust specks, no vintage overlay. No text, no logos, no other people.
```
실물 사진은 소품의 모양만 복사하라고 적었어요. 손이나 배경까지 따라오지 않게요.

✅ 성공: 머리부터 신발까지 다 나오고, STEP 1에서 적은 특징 중 절반 넘게(머리 모양, 옷 색, 신발 같은 것)가 사진에서 보이면 성공이에요.

안 닮으면: 얘가 특징을 못 읽은 거라, 특징 문장을 더 만화처럼 과장해서 쓰고 다시 돌리세요. 그래도 안 되면 먼저 상반신 사진을 만들고, 그 사진을 첨부해서 "같은 얼굴로 전신 사진을 만들어줘"라고 시키세요.

사진 가장자리에 누런 테두리나 먼지 자국이 있으면 3에서 5%만 잘라내고 쓰세요. 영상에 그대로 번져요. 맥은 미리보기, 윈도우는 사진 앱의 자르기로 돼요.


---

### STEP 3. 장소 사진 만들기 (한 곳당 3분)
장소 사진이 두 번째로 중요해요. 장소 사진을 먼저 만들어서 모든 클립에 같이 넣어야 컷마다 같은 동네가 나와요.


#### 3-1. 집 한 장을 먼저 (기준 사진)
만화 집 그림은 넣지 마세요. 만화 그림을 붙이면 위에서 내려다보는 만화 구도를 따라가서 미니어처처럼 나와요. 글로만 쓰세요.

```text
A real 1970s Korean house, photographed at eye level. Single-story L-shaped house with a dark gray ceramic tile roof (a few cracked and mossy tiles, one crooked), gray-white plaster walls stained with rain streaks and peeling in patches, wood-framed windows with sun-faded paper, a raised wooden veranda with a worn low wooden bench, a packed-earth yard with weeds along the wall, a clothesline with a few faded sheets and old clothes, large earthen jars (one chipped, one with a stone on its lid), a concrete water trough with a tap, a broom, a rubber basin, firewood stacked by the wall, a pair of old rubber shoes by the veranda, a tilted TV antenna on the roof, a rough cement block wall and a wooden plank gate.
ONE image, two panels side by side, same house, both at human eye level, no aerial view. Left: from the gate looking across the yard toward the veranda. Right: from the veranda looking back toward the yard and the gate.
Photo style: an amateur snapshot by a family member with a cheap 35mm camera in 1972, slightly crooked framing, bright hazy summer sky, sun slightly overexposed, muted natural colors, fine film grain. Deep focus everywhere, no tilt-shift, no miniature effect.
IMPORTANT: full-bleed image, edge to edge. No border, no frame, no white or yellow edge, no torn edges, no vignette, no dust specks, no scratches, no vintage-photo overlay. No people, no text, no logos.
```
✅ 성공: 눈높이에서 찍은 것 같은 사진이 두 칸으로 나오고, 사람이 0명이고, 가장자리에 테두리가 없으면 돼요.

사진이 3D 그림이나 미니어처처럼 보이면 그 사진을 첨부하고 아래 수정 프롬프트를 쓰세요. 구도는 그대로 두고 질감과 빛만 바꿔요.

```text
Edit this image. Keep the exact same composition, camera angle, house layout, and every object in place. Change only the rendering so it looks like a real photograph instead of a 3D render or miniature:

1. Remove any border, torn edges, vignette and dust specks. Full-bleed image, edge to edge.
2. Remove the miniature and tilt-shift look: no blurred foreground, deep focus everywhere, with only slight natural atmospheric haze toward the distance.
3. Lighting: bright hazy summer sky, slightly overexposed highlights on the plaster and the yard, softer natural shadows, muted natural colors instead of a saturated grade. Neutral white balance.
4. Textures: real rain-stained and peeling plaster, mossy and uneven roof tiles, weathered gray wood, dusty packed earth with footprints and small stones, uneven weeds, rusty and chipped metal and concrete. Slightly irregular, imperfect surfaces everywhere.
5. Camera feel: an ordinary 35mm film snapshot, subtle fine grain, natural lens softness, no oversharpening, no HDR, no glow.

Do not add or remove any objects. No people, no text, no logos.
```

#### 3-2. 나머지 장소 3곳
방금 만든 집 사진을 두 칸 그대로(통째로) 첨부하고, 아래 프롬프트를 한 장씩 따로 돌리세요. 집 사진을 붙이면 같은 동네, 같은 빛으로 나와요. 세 장을 한꺼번에 시키면 룩이 갈려요.

① 대문 앞 사진 (딱지치기와 대문 장면)

```text
Use the attached image as the exact house and look reference: same gray-white stained plaster, dark mossy tile roofs, weathered wood, cement block walls, same plank gate in the wall. Photograph the area just outside the gate of this house, as a real photograph.
A packed-earth lane and flat dirt patch in front of the plank gate: dusty ground with footprints, small stones and tufts of weeds along the wall bases, a rough cement block wall on one side, an old fieldstone wall on the other, a wooden utility pole with sagging wires, an old rusty bicycle leaning on the wall, a few clay pots, a stack of firewood by the wall.
ONE image, two panels, both at human eye level, no aerial view. Left: from the lane looking at the gate. Right: from low near the ground looking along the wall, showing the open dirt patch.
Look: ordinary 35mm film snapshot, bright hazy summer sky, slightly overexposed highlights, soft natural shadows, muted natural colors, neutral white balance, fine grain, deep focus, natural lens softness, no oversharpening, no HDR, no miniature or tilt-shift look. Imperfect real surfaces everywhere.
Full-bleed image edge to edge: no border, no frame, no vignette, no dust specks, no vintage overlay. No people, no text, no logos.
```
② 방 안과 마루 사진 (바나나와 콜라 장면)

```text
Use the attached image as the exact house and look reference. Photograph the interior of this house as a real photograph: the room seen through the veranda doors, with the same wood-framed windows and sliding doors.
A small room with yellowed oiled-paper floor worn at the edges, a low round wooden dining table in the center, faded floral wallpaper with water stains and peeling corners, a wooden wardrobe with a mirror, a bare lightbulb hanging on a cord, wood-framed paper sliding doors, folded quilts on a shelf, a wall clock, a small cabinet, a rubber basin and a kettle in the corner.
ONE image, two panels, both at human eye level, no aerial view. Left: from the doorway toward the table and the wardrobe. Right: from the table toward the sliding doors and the sunlit veranda outside.
Look: ordinary 35mm film snapshot, soft bright daylight coming through the doors, slightly overexposed highlights near the doors, muted natural colors, neutral white balance, fine grain, deep focus, natural lens softness, no oversharpening, no HDR. Imperfect real surfaces: scuffed floor, stained walls, worn wood.
Full-bleed image edge to edge: no border, no frame, no vignette, no dust specks, no vintage overlay. No people, no text, no logos.
```
③ 골목과 공터 사진 (굴렁쇠와 엿장수 장면)

```text
Use the attached image as the exact look reference for the same village: same gray-white stained plaster, dark mossy tile roofs, cement block walls, dusty earth, same hazy bright light. Photograph a lane of this village as a real photograph.
A gently curved dusty lane with wheel marks and footprints, a long fieldstone wall on one side, a rough cement block wall on the other, a wooden utility pole with sagging wires, a few clay pots against a wall, weeds growing from wall bases, and at the end of the lane an open dirt clearing where children gather, with the fieldstone wall behind it.
ONE image, two panels, both at human eye level, no aerial view. Left: the lane seen from its entrance. Right: the open dirt clearing with the fieldstone wall behind it.
Look: ordinary 35mm film snapshot, bright hazy summer sky, slightly overexposed highlights, soft natural shadows, muted natural colors, neutral white balance, fine grain, deep focus, natural lens softness, no oversharpening, no HDR, no miniature or tilt-shift look. Imperfect real surfaces everywhere.
Full-bleed image edge to edge: no border, no frame, no vignette, no dust specks, no vintage overlay. No people, no text, no logos.
```
✅ 성공: 장소 4장 모두 눈높이에서 찍은 사진처럼 보이고, 하늘이 뿌옇게 밝고, 색이 흐릿하고, 사람이 0명이면 돼요. 같은 동네처럼 보이는지는 회벽 색과 기와 색으로 보세요.

장소 사진은 두 칸짜리라서, 영상에 쓸 때는 그 클립에 필요한 칸만 잘라서 올려요. 어느 칸을 쓰는지는 STEP 4 프롬프트마다 적어놨어요. 사진을 정확히 반으로 가르면 왼쪽 칸, 오른쪽 칸이 돼요. 맥은 미리보기, 윈도우는 사진 앱의 자르기로 돼요.


---

### 클로드 활용 방법(원문)

### 🤖 저는 클로드한테 이렇게 시켰어요 (클로드 코드 쓰시는 분)
영상 속 작업 순서예요. 저는 방향 정하기, 결과 보고 OK 또는 다시, 캡컷 편집, 업로드만 했고 나머지는 클로드가 했어요. 아래 "시킨 말"은 제가 실제로 한 말을 복붙하기 좋게 다듬은 거예요.

이 절은 클로드 코드(Claude Code, 클로드 Pro 이상)가 깔려 있고 크롬 확장(Claude in Chrome)이 켜져 있어야 돼요. 둘 다 처음이면 ‣ 가이드의 설치와 "크롬 직접 조작시키기"부터 하고 오세요. 다른 곳엔 없어요. 크롬에는 ChatGPT에 로그인된 탭이 하나 열려 있어야 하고요.


#### 시킨 말 1. 원작 캡처 모으기
클로드 코드 채팅창에 이렇게 쳤어요. 작품 이름과 인물 이름만 바꾸세요.

```text
유튜브에서 검정고무신 영상 중에 조회수 높은 걸 골라서 실제로 봐. 보면서 기영이, 기철이, 다혜, 경주 얼굴이 잘 보이는 장면이랑, 집, 골목, 교실처럼 배경으로 쓸 만한 장면을 스크린샷으로 찍어서 바탕화면에 "검정고무신 원작 캡처" 폴더를 만들고 정리해 줘. 파일명에 인물 이름이나 장소, 몇 화인지 적어 주고, 출처 메모 파일도 하나 만들어 줘.
```
✅ 성공: 바탕화면에 폴더가 생기고, 안에 기철이 전신 01.jpg, 교실 원작 02 칠판 정면 (3기 15화).jpg 같은 이름의 캡처가 인물과 장소별로 들어 있으면 돼요.

🆘 "영상을 볼 수 없다"고 하면: 크롬 확장이 꺼진 거예요. 위 설치 가이드의 "크롬 직접 조작시키기"를 확인하세요. 


#### 시킨 말 2. 실사 시트 만들기
```text
(크롬에 열려 있는)ChatGPT로 가서, 방금 모은 원작 캡처를 올리고 실사 캐릭터 시트를 만들어 줘. 형식은 가로로 긴 한 장을 3칸으로 나눠서 1번 칸은 얼굴 클로즈업, 2번 칸은 목 아래 정면 전신, 3번 칸은 목 아래 뒷모습. 1970년대 한국 시골에서 찍은 바랜 컬러 필름 사진처럼. 기영이, 기철이, 다혜, 경주 한 명씩 따로 만들고, 다 되면 바탕화면 "검정고무신 시트" 폴더에 저장해 줘.
```
장소와 소품도 같은 식이에요. "만둣집, 교실, 개울가는 같은 장소를 두 각도로 찍은 2칸 로케이션 시트로, 옥수수빵, 빈 병, 유리구슬은 정사각형 소품 사진으로 만들어 줘"라고 덧붙이면 돼요. 소품은 실물 사진을 한 장 같이 주면 훨씬 정확해요.

ChatGPT 데스크탑 앱을 사용하시거나 클로드에게 연결을 시켜줬다면 (크롬에 열려 있는) 은 안넣으셔도 되요. 

✅ 성공: 시트 폴더에 인물마다 가로로 긴 3칸 시트 한 장이 생기고, 1번 칸 얼굴이 원작의 머리 모양과 옷 색을 따라가면 돼요. 세 칸의 얼굴이 같은지는 보지 마세요. 2번, 3번 칸은 일부러 얼굴을 잘라요.


**▸ 클로드가 ChatGPT에 실제로 넣은 캐릭터 시트 프롬프트 (한국어 그대로)**

첫 번째 이미지로 기존 시트 한 장(형식 기준), 두 번째 이미지로 원작 캡처를 올리고 아래를 넣었어요. 마지막 문단만 인물별로 바꿨어요.

```text
첫 번째 이미지는 내가 쓰는 캐릭터 시트 형식이야. 이 형식과 사진 스타일을 그대로 따라서 새 인물의 캐릭터 시트 한 장을 만들어 줘.

형식: 가로로 긴 한 장(3:1 비율)을 3칸으로 나눈다. 1970년대 한국 시골에서 찍은 바랜 컬러 필름 스냅, 한낮 직사광, 첫 번째 이미지와 같은 콘크리트 담벼락과 흙바닥, 같은 낡은 필름 테두리.
1번 칸: 얼굴 클로즈업(어깨 위). 포즈를 잡지 않은 자연스러운 표정.
2번 칸: 정면 전신. 목 아래부터 발끝까지만 프레임에 넣고 얼굴은 보이지 않게 자른다.
3번 칸: 같은 차림의 뒷모습. 역시 목 아래부터 발끝까지만.
세 칸의 머리 모양, 체형, 옷은 완전히 같게.

인물: 두 번째 이미지의 만화 캐릭터를 실제 한국 아이로 옮긴다. 머리 모양, 옷, 색은 두 번째 이미지를 그대로 따르고, 얼굴은 만화 비율이 아니라 실제 사람 비율로. 피부는 보정 없이 자연스럽게, 실제 필름 사진처럼. 글자와 로고는 넣지 않는다.
```
기존 시트가 없으면 첫 문단을 빼고 "형식:"부터 넣으세요.


**▸ 로케이션 시트 프롬프트 (교실. 다른 장소는 "장소" 문단부터만 바꿨어요)**

첫 번째 이미지로 기존 로케이션 시트 한 장(형식 기준), 두 번째 이미지로 원작 교실 캡처 여섯 컷을 한 장에 붙여서 올렸어요.

```text
첫 번째 이미지는 내가 쓰는 로케이션 시트 형식이야. 이 형식과 사진 스타일을 그대로 따라서 새 장소의 로케이션 시트 한 장을 만들어 줘.

형식: 가로로 긴 한 장(2:1 비율)을 좌우 2칸으로 나눈다. 같은 교실을 두 각도에서 찍은 실제 사진. 1970년 무렵 한국 국민학교, 바랜 컬러 필름, 여름 낮 창으로 들어오는 자연광. 사람은 한 명도 없다.

장소: 두 번째 이미지는 만화 「검정고무신」에 나오는 3학년 5반 교실 장면 여섯 컷이다. 이 교실을 실제 교실 사진으로 옮긴다. 벽 색, 바닥, 칠판, 책걸상, 문, 창, 게시판의 모양과 배치는 두 번째 이미지를 그대로 따르고, 만화의 선과 색면은 실제 재질로 바꾼다. 두 번째 이미지 속 인물은 모두 뺀다.

교실 공통: 벽 위쪽은 하늘빛이 도는 흰 페인트, 아래 3분의 1은 파란 페인트 띠(허리벽). 페인트가 군데군데 벗겨지고 손때가 묻었다. 바닥은 노르스름한 갈색의 긴 나무 널마루. 천장은 격자로 나뉜 흰 천장판. 책상은 짙은 갈색 나무로 만든 2인용 책상이고, 의자는 등받이가 있는 나무 의자다. 책상이 줄 맞춰 놓여 있다.

왼쪽 칸(교실 맨 뒤에서 앞을 본 모습): 앞 벽에 나무 틀을 두른 짙은 남색 칠판과 분필받이. 칠판 오른쪽 벽에 나무 막대에 건 격자 달력. 칠판 앞에 낮은 나무 교단이 있고 그 위에 짙은 갈색 나무 교탁. 왼쪽 벽에 나무틀 여러 칸 유리창이 줄지어 있고 낮 빛이 책상 위로 들어온다.

오른쪽 칸(창가 쪽에서 교실 뒤쪽 구석과 복도 쪽 벽을 본 모습): 화면 앞에 맨 뒷줄 2인용 책상 하나와 의자 둘. 그 뒤 복도 쪽 벽에 짙은 갈색 나무 뒷문이 있고, 문 위쪽 절반은 유리 두 칸, 아래는 나무판이다. 문 유리 너머로 밝은 복도가 보인다. 문 옆 복도 쪽 벽에 나무틀 유리창 하나. 뒷벽에는 아이들 그림을 줄 맞춰 붙인 초록색 게시판과 작은 네모 액자. 뒷벽과 복도 쪽 벽이 만나는 구석에 검은 양동이와 대걸레 자루.

글자, 로고, 워터마크는 넣지 않는다. 달력과 게시판 그림에도 읽을 수 있는 글자는 넣지 않는다. 세트장처럼 깨끗하지 않게, 오래 쓴 실제 교실로.
```

#### 시킨 말 3. 기획안과 프롬프트
```text
이 시트들로 30초 안팎 릴스 구성안을 짜 줘. 장면마다 몇 초인지, 어떤 시트를 쓰는지 표로 정리해 줘. 카메라는 부모님이 한 손으로 든 캠코더 느낌이고, 배경음악은 넣지 말고 현장음만. 구성이 정해지면 장면마다 시댄스 2.5용 영어 프롬프트를 써 줘.
```
✅ 성공: 장면표와, 장면마다 SCENE CONTEXT로 시작해서 POSITIVE LOCKS로 끝나는 영어 프롬프트가 나오면 돼요. 아래 🎬 프롬프트 7개가 그렇게 나온 거예요.

저는 여기서 "C2는 4초로 줄여", "만찐두빵의 배경과 계절은 겨울로 바꿔" 같은 말만 했어요. 


#### 시킨 말 4. 클립 뽑기
손으로 하실 분은 STEP 4예요. 2편은 클로드한테 이렇게 시켰어요.

```text
이번에는 네가 힉스필드를 직접 돌려서 만들어 봐. 720p, 시댄스 2.5로.
```
이게 되려면 클로드 앱의 설정(Settings) → 커넥터(Connectors) 에서 Higgsfield MCP를 먼저 연결해 둬야 해요. 잘 모르시겠다면 클로드에게 직접 물어봐도 상세하게 알려줘요! ( “클로드에서 힉스필드 MCP 연결하는 방법을 아주 쉽게 알려줘” 이런식으로만 해도 되요)

✅ 성공: 클로드가 클립마다 크레딧(5초 35, 6초 42)을 먼저 알려 주고, 다 되면 mp4 파일 위치를 적어 주면 돼요. 크레딧은 손으로 돌릴 때와 똑같이 나가요. 돌리기 전에 "먼저 하나만 뽑아서 보여 줘"라고 하세요. 8개를 한 번에 시키면 266크레딧이 한 번에 나가요.


#### 클로드가 못 하는 것
- 결과가 마음에 드는지는 못 정해요. 시트와 클립은 꼭 눈으로 보고 "OK" 또는 "다시" 하세요. 저는 2편 기철이 얼굴을 세 번 고쳤어요
- 캡컷 편집과 업로드는 제가 해요
- 원작 캡처는 참고용이에요. 영상이나 자료에 원작 화면을 넣어 배포하진 마세요

---

### 🎬 프롬프트 7개
순서는 최종 영상에 나오는 순서예요. 위에서부터 차례로 뽑으시면 돼요. 단, 06번은 01번 클립이 먼저 있어야 해요. 07번은 2편 장면이라 따로예요.


#### 01. 굴렁쇠 몰고 달리기
길이 7초

올리는 순서: 기영이 사진 → @image1 · 초록 티 친구 사진 → @image2 · 골목과 공터 사진(왼쪽 칸, 골목) → @image3

```text
SCENE CONTEXT
A dusty village lane on a bright summer afternoon in Korea. A parent films two boys with a handheld camcorder while jogging behind them. @image1 runs ahead pushing a metal hoop with a hooked iron rod, @image2 runs two steps behind him.

ACTIVE REFERENCES
@image1: young boy, spiky short dark hair, orange t-shirt with a mustard T mark, navy shorts, black rubber shoes, 100% matches the reference.
@image2: young boy, thin hair strands on a large forehead, big round eyes, green t-shirt with a darker green horizontal stripe, gray shorts, black rubber shoes, 100% matches the reference.
@image3: the dusty lane with the fieldstone wall on the left and the cement block wall on the right, 100% matches the reference.

LOCATION MAP
Foreground: packed dirt with wheel marks and small stones. Midground: the lane running away between the two walls. Background: tiled roofs and hazy hills. The sun sits high behind frame-left.

FIRST FRAME / BLOCKING
The frame opens already moving: @image1 is at the left edge of the frame, only his back and the blur of the hoop inside the frame, @image2 is half hidden behind the frame edge.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
MS at 63° FOV. At 1.5s a fast lens zoom-in narrows the FOV from 63° to 29° in 0.3s onto @image1. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator holds a consumer camcorder at chest height with one hand while jogging at 8 km/h. Rough handheld shake of 10 to 15 cm, the framing wanders so the boys sit off-center and drift partly out of frame, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the near stones and the far wall before it locks.

ACTION
0.0s to 1.5s: the camera trails the boys, @image1 runs at 12 km/h and the hoop rings against the rod, focus sits on the stone wall behind and then slides onto his back.
1.5s to 2.5s: a fast zoom-in onto @image1, the image soft for 0.3s and then sharp on his profile, tongue between his teeth, eyes locked on the hoop.
2.5s to 4.5s: the operator keeps pace, the frame bounces, @image2 runs into frame breathing hard and goes soft, then sharp. Exposure brightens on the bright dirt.
4.5s to 5.5s: the hoop hits a stone, jumps 30 cm and tumbles off the lane into the weeds with a metal rattle. The camera arrives late and sees only weeds and the rattling hoop, then pans 25 degrees back to the boys.
5.5s to 7.0s: @image1 has stopped dead with the hooked rod still held out in front of him and his mouth slightly open, @image2 bumps into his back. Both stand still and look at the fallen hoop while the focus re-locks.

PERFORMANCE
Unposed child effort: shoulders rising with breath, sweat at the hairline, eyes tracking the hoop only, no look at the camera.

PHYSICS
The hoop keeps its momentum, wobbles before it falls. Dust rises under the shoes and settles slowly in the sun.

LIGHTING
Hard overhead sun at 5600K with a blown-out white sky, short contact shadows under the feet, bright bounce from the pale dirt.

AUDIO
Wind hitting the camcorder microphone, handling rustle, the camcorder motor whirr, iron hoop ringing against the rod, scuffing shoes, cicadas, a distant dog, the operator's short breathy laugh at the fall. No music.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded to a warm yellow-green cast with weak blacks, white sky blown out to pure white, auto-exposure that pumps when the lens swings between bright dirt and shade, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores, uneven tan and dust on the knees.

OUTPUT SETTINGS
9:16 vertical, 7 seconds, 24fps, real-time speed.

POSITIVE LOCKS
Both boys keep the same faces, hair and clothes through the whole take. The lane, walls and utility pole stay identical. The hoop stays metal and round.
```
✅ 성공: 아이 둘이 골목을 뛰고, 굴렁쇠가 돌에 튕겨 풀숲으로 굴러가고, 마지막에 둘이 멈춰서 굴렁쇠를 보고 있으면 돼요.


---

#### 02. 바나나 앞에서 "우와"
길이 6초

올리는 순서: 기영이 사진 → @image1 · 초록 티 친구 사진 → @image2 · 방 안과 마루 사진(왼쪽 칸, 방 전체) → @image3

```text
SCENE CONTEXT
Inside a small Korean house, midday. A parent films with a handheld camcorder from a crouch near the sliding doors. @image1 and @image2 kneel at a low round wooden table in the middle of the room. A single banana is about to be placed on the table.

ACTIVE REFERENCES
@image1: young boy, spiky short dark hair, orange t-shirt with a mustard T mark, navy shorts, 100% matches the reference.
@image2: young boy, thin hair strands on a large forehead, big round eyes, green t-shirt with a darker green horizontal stripe, gray shorts, 100% matches the reference.
@image3: the room with the oiled-paper floor, low round table, wooden wardrobe, paper sliding doors, 100% matches the reference.

LOCATION MAP
Foreground: the round table edge. Midground: @image1 frame-left and @image2 frame-right at the table. Background: the wooden sliding doors with sunlit paper panes and the wardrobe. The key light comes from the doors on frame-right.

FIRST FRAME / BLOCKING
The frame opens pointing at the table edge and the floor, the boys only half in frame at the top.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
MS at 47° FOV. At 1.5s a fast lens zoom-in narrows the FOV from 47° to 18° in 0.3s onto the banana. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator holds a consumer camcorder at chest height with one hand while crouching. Rough handheld shake of 10 to 15 cm, the framing wanders so the boys drift off-center and partly out of frame, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the table edge and the boys before it locks. Exposure pumps between the bright doors and the dark room.

ACTION
0.0s to 1.5s: the camera wobbles over the table edge, a woman's weathered forearm in a rolled cotton sleeve enters from frame-left and sets a plate with one banana on the table, yellow with brown speckles. The plate clinks on the wood and the arm leaves.
1.5s to 2.5s: a fast zoom-in onto the banana, soft and then sharp.
2.5s to 4.0s: the operator tilts up and the top of @image1's head is cut off at first, then the frame corrects. His eyes widen following the banana, his mouth opens into a round shape and he whispers softly "우와".
4.0s to 6.0s: a quick pan to the right, @image2 reaches a hand toward the banana. Without moving his eyes from the banana, @image1 smacks the hand away with his palm in one quick motion. @image2 pulls his hand to his chest and both boys lean in toward the banana and hold still.

PERFORMANCE
Deadpan reverence: held breath, unblinking eyes, a small swallow from @image1 before the whisper, no look at the camera.

PHYSICS
The plate settles with a small wobble, the banana skin shows soft brown speckles, the table surface reflects the door light.

LIGHTING
Strong daylight at 5600K from the sliding doors on frame-right, blown-out white at the door panes, warm bounce from the yellow floor, the room in shade.

AUDIO
Handling rustle, the camcorder motor whirr, plate clink on wood, the whispered "우와", palm slap, cicadas outside, a faint clock tick, the operator's stifled laugh. No music.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded to a warm yellow-green cast with weak blacks, white doors blown out to pure white, auto-exposure that pumps when the lens swings between the bright doors and the dark room, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores and uneven tan.

OUTPUT SETTINGS
9:16 vertical, 6 seconds, 24fps, real-time speed.

POSITIVE LOCKS
Both boys keep the same faces and clothes through the whole take. The banana stays whole and unpeeled. The room layout stays identical.
```
✅ 성공: 접시 위에 바나나가 놓이고, 기영이가 놀란 입 모양을 하고, 친구 손이 바나나로 뻗었다가 밀려나면 돼요.


---

#### 03. 마루에서 몰래 콜라 마시기
길이 5초

올리는 순서: 기영이 사진 → @image1 · 콜라병 실물 사진 → @image2 · 방 안과 마루 사진(오른쪽 칸, 툇마루 쪽) → @image3

```text
SCENE CONTEXT
Inside a small Korean house, midday. A parent films with a handheld camcorder, peeking through a gap in the wooden sliding doors. @image1 sits cross-legged on the wooden floor near the open doorway with a big glass cola bottle between his knees, looking over his shoulder to check that nobody is coming.

ACTIVE REFERENCES
@image1: young boy, spiky short dark hair, orange t-shirt with a mustard T mark, navy shorts, 100% matches the reference.
@image2: a 770 ml glass Coca-Cola bottle with green-tinted glass, a metal crown cap, dark cola inside and a white Korean label reading 코카·콜라, about 30 cm tall, nearly as long as the boy's forearm and hand together. Use only the bottle, ignore the wallpaper and the table behind it, 100% matches the reference.
@image3: the doorway with wooden-framed paper sliding doors opening onto the sunlit veranda, 100% matches the reference.

LOCATION MAP
Foreground: the blurred edge of the wooden door frame on the left 20% of the frame. Midground: @image1 on the floor, centered. Background: the room in shade with the low round table and the wardrobe, the veranda doorway glowing white on frame-right.

FIRST FRAME / BLOCKING
The frame opens through the door gap with the door frame out of focus on the left, @image1 small and low in the frame, the bottle at his knees.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
MS at 47° FOV. At 1.0s a fast lens zoom-in narrows the FOV from 47° to 18° in 0.3s onto the bottle. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator crouches behind the door and holds a consumer camcorder at chest height with one hand. Rough handheld shake of 10 to 15 cm, the framing wanders so the boy drifts partly behind the door frame, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the near door frame and the boy before it locks.

ACTION
0.0s to 1.0s: @image1 holds still, his head turns toward the off-screen kitchen on frame-left and back, the focus sliding from the door frame onto him.
1.0s to 1.8s: a fast zoom-in onto the bottle, soft and then sharp: dark cola, green glass, the white label.
1.8s to 3.2s: he raises the bottle with both hands and takes a tiny sip, his eyes squeeze shut, his nose scrunches and his cheeks puff from the fizz.
3.2s to 3.8s: a floorboard creaks off-screen. His eyes snap sideways toward the sound.
3.8s to 5.0s: he shoves the bottle behind his back with both hands, sits upright with a stiff face and looks up at the ceiling, a small hiccup pushes his cheeks out and he clamps his lips shut.

PERFORMANCE
A sneaking child: hunched shoulders, eyes sliding sideways before every move, a held breath, a stiff innocent face at the end, no look at the camera.

PHYSICS
The cola bubbles rise in the bottle and the glass picks up the door light. A thin fizz mist rises from the neck when he lowers the bottle.

LIGHTING
Strong daylight at 5600K from the veranda doorway on frame-right, blown-out white in the doorway, the room in shade, a sharp glint on the glass.

AUDIO
Handling rustle, the camcorder motor whirr, a fizz hiss at the sip, glass tapping his teeth, a floorboard creak, a muffled hiccup, cicadas, the operator's stifled breathy laugh. No music, no dialogue.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded to a warm yellow-green cast with weak blacks, white sky blown out to pure white, auto-exposure that pumps when the lens swings between bright and shade, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores, uneven tan and dust on the knees.

OUTPUT SETTINGS
9:16 vertical, 5 seconds, 24fps, real-time speed.

POSITIVE LOCKS
@image1 keeps the same face and clothes through the whole take. The bottle stays one glass bottle with the white Korean label, the label text stays as in the reference, the cola stays dark. The room layout stays identical.
```
✅ 성공: 문틈으로 훔쳐보는 화면에서 기영이가 병을 들어 한 모금 마시고, 소리에 놀라 병을 등 뒤로 숨기면 돼요. 병 라벨 한글이 조금 깨져도 영상은 쓸 수 있어요.


---

#### 04. 엿장수와 고무신으로 엿 바꾸기
길이 7초

올리는 순서: 엿장수 사진 → @image1 · 기영이 사진 → @image2 · 골목과 공터 사진(오른쪽 칸, 공터) → @image3

⚠️ 이 클립만 엿장수가 @image1 이에요. 다른 클립과 순서가 달라요.

그 시절엔 돈을 내고 엿을 산 게 아니라 낡은 고무신 같은 걸 가져가서 엿으로 바꿨어요. 그래서 이 장면은 동전이 아니라 고무신이에요.

```text
SCENE CONTEXT
At the dirt clearing at the end of a village lane in Korea, with a fieldstone wall behind. A parent films with a handheld camcorder from 3 m away. @image1 stands beside his wooden candy tray on a stand. @image2 stands in front of him holding out a worn-out old black rubber shoe, cracked and patched, to trade for candy. Nobody pays with money.

ACTIVE REFERENCES
@image1: thin man in his forties, brown floppy bucket hat, big wide grin with upper teeth, white short-sleeve undershirt, dark navy baggy trousers, black rubber shoes, a pair of hand-forged dark iron scissors with two teardrop loops and wide flat blunt blades always in his right hand, 100% matches the reference.
@image2: young boy, spiky short dark hair, orange t-shirt with a mustard T mark, navy shorts, black rubber shoes, 100% matches the reference.
@image3: the clearing with the fieldstone wall, hazy hills and tiled roofs, 100% matches the reference.

LOCATION MAP
Foreground: the tray with sheets of golden-brown candy and a cloth cover. Midground: the two characters facing each other, @image1 frame-right, @image2 frame-left. Background: the fieldstone wall and hazy hills. The sun sits high behind frame-right.

FIRST FRAME / BLOCKING
The frame opens searching: the wall and the tray, @image1 only half in frame at the right edge.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
MS at 47° FOV. At 1.0s a fast lens zoom-in narrows the FOV from 47° to 12° in 0.3s onto the scissors and candy, and at 4.5s a second fast zoom-in narrows it from 47° to 18° onto @image2's face. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator holds a consumer camcorder at chest height with one hand. Rough handheld shake of 10 to 15 cm, the framing wanders so the subjects drift partly out of frame, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the tray and the faces before it locks.

ACTION
0.0s to 1.0s: the frame wanders over the wall and the tray, the focus slides from the wall to the candy sheets.
1.0s to 2.5s: a fast zoom-in onto the tray as @image1's right hand opens the iron scissors and snips a corner off a brittle slab of golden-brown candy dusted with white starch. The blades close with a metallic clack and the piece drops onto the cloth.
2.5s to 4.5s: the operator tilts up, the frame catches @image1's grin under the bucket hat late. He swaps the candy piece for the worn-out shoe in @image2's hand, takes the shoe with his left hand and tosses it into a burlap sack beside the tray with a dull thump. The scissors stay in his right hand.
4.5s to 7.0s: a fast zoom-in onto @image2 as he bites the candy and his jaw stops. Strands of candy stretch 10 cm between his teeth and fingers. He tries to open his mouth, eyebrows climb, eyes cross toward the candy. Behind him @image1 tilts his head, grin widening. The camera holds the stuck jaw, the focus hunting once and re-locking.

PERFORMANCE
@image1: unhurried showman, the grin never drops. @image2: a child discovering his teeth are glued, silent and wide-eyed, no look at the camera.

PHYSICS
The candy is brittle when cut, then sticky and elastic when bitten, starch powder puffs lightly from the slab.

LIGHTING
Hard sun from behind frame-right at 5600K, a rim on the bucket hat, blown-out white sky, warm bounce from the dirt, soft shadow under the hat brim.

AUDIO
Wind on the microphone, the camcorder motor whirr, scissors clack, the dull thump of the shoe into the sack, cicadas, a wet sticky chew, the operator's stifled laugh. No music, no dialogue.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded to a warm yellow-green cast with weak blacks, white sky blown out to pure white, auto-exposure that pumps when the lens swings between bright dirt and shade, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores and uneven tan.

OUTPUT SETTINGS
9:16 vertical, 7 seconds, 24fps, real-time speed.

POSITIVE LOCKS
@image1 keeps the same face, hat, undershirt, trousers and the same iron scissors in his right hand through the whole take. @image2 keeps the same face and clothes and keeps wearing his own shoes, the traded shoe is a separate old cracked one. The tray and wall stay identical.
```
✅ 성공: 엿장수가 고무신을 받아 자루에 던지고, 기영이가 엿을 무는 장면이 나오면 되요. 


---

#### 05. 딱지치기
길이 8초

올리는 순서: 기영이 사진 → @image1 · 초록 티 친구 사진 → @image2 · 보라 셔츠 친구 사진 → @image3 · 대문 앞 사진(왼쪽 칸, 대문 쪽) → @image4

```text
SCENE CONTEXT
In front of the plank gate of a village house on a summer afternoon in Korea. A parent films with a handheld camcorder while crouching at the edge of the dirt. @image1 and @image2 crouch facing each other over two ddakji, flat square slap cards hand-folded from old newspaper, on the packed dirt, @image3 squats at the side and watches.

ACTIVE REFERENCES
@image1: young boy, spiky short dark hair, orange t-shirt with a mustard T mark, navy shorts, black rubber shoes, 100% matches the reference.
@image2: young boy, thin hair strands on a large forehead, big round eyes, green t-shirt with a darker green horizontal stripe, gray shorts, black rubber shoes, 100% matches the reference.
@image3: small boy, black bowl-cut bangs, lavender short-sleeve shirt with a white round collar and three navy buttons, navy shorts, black rubber shoes, 100% matches the reference.
@image4: the stone gate pillar with the wooden plank door, the cement block wall and the dirt lane, 100% matches the reference.

LOCATION MAP
Foreground: bare packed dirt with two ddakji, each a palm-sized square about 9 cm wide folded from old newsprint and scrap paper: thin and floppy, soft worn rounded corners, a cross-shaped fold crease at the center, faded gray-beige with smudged illegible newsprint marks and frayed edges, one slightly yellower than the other. Midground: the boys. Background: the plank gate and stone wall with a clothesline over it. The sun sits high behind frame-left.

FIRST FRAME / BLOCKING
The frame opens on the dirt and the two ddakji, @image1's hand and knee at the edge of the frame, the other boys out of frame.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
MS at 47° FOV. At 1.5s a fast lens zoom-in narrows the FOV from 47° to 29° in 0.3s onto the ddakji. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator holds a consumer camcorder at knee height with one hand. Rough handheld shake of 10 to 15 cm, the frame jolts on each slam, the framing wanders so faces drift partly out of frame, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the ddakji and the faces before it locks.

ACTION
0.0s to 1.5s: the ddakji lie on the dirt, @image1's right hand grips his ddakji and lifts it out of the top of the frame while the focus slides from the dirt to his knee.
1.5s to 4.0s: @image1 swings and slams his ddakji down, a puff of dust blows into the lens and blurs it, the other ddakji trembles and stays flat. The camera whips up to @image2, who smirks, then drifts to @image3, who squats with his hands on his knees and looks on without expression.
4.0s to 8.0s: @image1 exhales, pushes his sleeve above the elbow and slams again with his whole body behind it at 40 km/h. A dust ring blasts outward, @image2's ddakji flips fully over in the air and lands face-up. The operator whips to @image2 with a late refocus, his smirk drops and his mouth slowly opens, then a short pan to @image3, who turns his head slowly toward @image2.

PERFORMANCE
Small serious faces: narrowed eyes on the ddakji, a held breath before each slam, a delayed reaction from @image2, no look at the camera.

PHYSICS
Dust leaves the ground at the impact and falls back slowly, the thin paper ddakji flexes and flips in the air blast of the slam, knees scuff the dirt.

LIGHTING
Hard high sun at 5600K from behind frame-left, contact shadows under each boy, bright bounce off the pale dirt, blown-out white sky.

AUDIO
Wind on the microphone, the camcorder motor whirr, paper slap on dirt, a soft dust whoosh, children's breathing, cicadas, a distant rooster, the operator's stifled laugh. No music.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded to a warm yellow-green cast with weak blacks, white sky blown out to pure white, auto-exposure that pumps when the lens swings between bright dirt and shade, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores, uneven tan and dust on the knees.

OUTPUT SETTINGS
9:16 vertical, 8 seconds, 24fps, real-time speed.

POSITIVE LOCKS
All three boys keep the same faces, hair and clothes through the whole take. The gate, wall and dirt stay identical. The ddakji count stays at two, both stay square folded newspaper, never round cards or coins.
```
✅ 성공: 딱지를 내리쳐서 먼지가 일고, 두 번째에 친구 딱지가 뒤집히고, 친구 표정이 굳으면 돼요. 딱지가 두꺼운 카드나 동전처럼 나오면 프롬프트 끝에 paper stays paper-thin, floppy, no thick cardboard를 덧붙이세요.


---

#### 06. 대문으로 우르르
길이 6초

올리는 순서: 기영이 사진 → @image1 · 초록 티 친구 사진 → @image2 · 보라 셔츠 친구 사진 → @image3 · 대문 앞 사진(왼쪽 칸, 대문 쪽) → @image4 · 01번 굴렁쇠 클립(영상 파일) → @video1

01번 클립을 영상 레퍼런스로 같이 올려요. 달리는 아이들의 움직임과 영상 질감을 그대로 가져오거든요. 01번 결과 영상을 내려받은 파일을, 사진 올리던 그 업로드 버튼으로 올리세요. 사진을 다 올린 다음에 영상을 올리세요.

```text
SCENE CONTEXT
In front of the plank gate of a village house on a summer afternoon in Korea. A parent films with a handheld camcorder, standing in the lane next to the gate. Three boys run down the lane toward the camera and the gate: @image2 leads, @image1 is in the middle, small @image3 trails behind.

ACTIVE REFERENCES
@image1: young boy, spiky short dark hair, orange t-shirt with a mustard T mark, navy shorts, black rubber shoes, 100% matches the reference.
@image2: young boy, thin hair strands on a large forehead, big round eyes, green t-shirt with a darker green horizontal stripe, gray shorts, black rubber shoes, 100% matches the reference.
@image3: small boy, black bowl-cut bangs, lavender short-sleeve shirt with a white round collar and three navy buttons, navy shorts, black rubber shoes, 100% matches the reference.
@image4: the stone gate pillar with the wooden plank door standing open, the cement block wall and the dirt lane, 100% matches the reference.
@video1: a previously generated outdoor camcorder-style clip of boys running down a lane, used only as the look and motion reference: copy its handheld shake, focus hunting, exposure pumping, color cast, tape noise and the loose bouncing way the children run. Do not copy its hoop, its lane or its action.

LOCATION MAP
Foreground: packed dirt with small stones. Midground: the open plank gate on frame-right in the stone pillar wall. Background: the lane running away to frame-left with the cement block wall, tiled roofs and hazy hills. The sun sits high behind frame-left.

FIRST FRAME / BLOCKING
The frame opens on the far end of the lane with the three boys small and soft, already running toward the camera.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
WS at 63° FOV. At 1.0s a fast lens zoom-in narrows the FOV from 63° to 29° in 0.3s onto the three runners. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator holds a consumer camcorder at chest height with one hand while standing still. Rough handheld shake of 10 to 15 cm, the framing wanders so the boys drift partly out of frame, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the far lane and the boys before it locks. Exposure pumps between the bright dirt and the shade of the gate.

ACTION
0.0s to 1.0s: the three boys run down the lane toward the camera at 15 km/h, small and soft, the frame bouncing.
1.0s to 1.3s: a fast zoom-in onto the runners.
1.3s to 3.0s: the boys close in, @image2 with his mouth wide open, @image1 laughing out loud, @image3 trailing with his bowl cut bouncing. The operator whips the camera 30 degrees right late, so the boys sweep partly out of frame toward the gate.
3.0s to 4.0s: at the gate all three try to squeeze through at once, shoulder to shoulder, and jam in the doorway for half a second, then pop through one after another.
4.0s to 6.0s: the plank door swings and bangs against the wall, dust rises. @image3 runs in last with his arms flapping. The camera holds on the empty gate and the swaying door, the focus re-locking.

PERFORMANCE
Unposed pure rush: heaving breath, shoulders jostling, wide open mouths, eyes only on the gate, no look at the camera.

PHYSICS
Shoes slap and kick up dust at 15 km/h, the old plank door swings on its hinge and bangs with a wooden thud, dust hangs in the sun beam.

LIGHTING
Hard high sun at 5600K from behind frame-left, blown-out white sky, contact shadows under each boy, bright bounce off the pale dirt, the gate in shade.

AUDIO
Wind on the microphone, the camcorder motor whirr, shoes slapping on dirt, unintelligible whooping and laughing with no words, the door's wooden bang, cicadas, the operator's laugh. No music.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded to a warm yellow-green cast with weak blacks, white sky blown out to pure white, auto-exposure that pumps when the lens swings between bright and shade, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores, uneven tan and dust on the knees.

OUTPUT SETTINGS
9:16 vertical, 6 seconds, 24fps, real-time speed.

POSITIVE LOCKS
All three boys keep the same faces, hair and clothes through the whole take. The gate, wall and lane stay identical. The boy count stays at three.
```
✅ 성공: 프롬프트 칸에 초록 칩 5개(@Image 1에서 @Image 4, @Video 1)가 보이고, 결과에서 세 아이가 대문으로 우르르 들어가고 문이 쾅 흔들리면 돼요.


---

#### 07. 만찐두빵 (2편, 겨울 만둣집)
길이 5초

올리는 순서: 기영이 겨울옷 시트 → @image1 · 기철이 시트 → @image2 · 만둣집 시트(오른쪽 칸, 가게 안) → @image3 · 마음에 든 1편 클립 하나(영상 파일) → @video1

2편은 전신 사진 대신 3칸 시트를 올렸어요. 그래서 프롬프트에 three-panel reference sheet와 never show the sheet layout 줄이 들어 있어요. 시트를 쓰실 땐 이 줄을 지우지 마세요. 겨울 장면이라 기영이 옷이 긴소매로 바뀌었고, 그래서 겨울옷 시트를 한 장 더 만들었어요.

```text
SCENE CONTEXT
Inside a small village dumpling shop in Korea on a cold winter afternoon, a few days after snow. A parent films with a handheld camcorder from across a small table. @image1 sits behind the table facing the camera, his older brother @image2 sits on a stool at the right end of the table. An old woman's hands set down a plate of steaming buns.

ACTIVE REFERENCES
@image1: a three-panel reference sheet of one young boy: spiky short dark hair, freckles and red cheeks, mustard-yellow long-sleeve shirt with a black T mark on the chest, brown long trousers, black rubber shoes. Use the sheet only for his face, hair, body and clothes, never show the sheet layout or its wall, 100% matches the reference.
@image2: a three-panel reference sheet of one teenage boy: round soft face, black peaked school cap, black stand-collar school uniform with gold buttons. Use the sheet only for his face, cap, body and clothes, never show the sheet layout or its wall, 100% matches the reference.
@image3: the shop interior: the wooden table with the pale blue cloth, the small round wooden stools, the two vertical paper signs on the yellowed plaster wall and the four-pane window with snowy roofs outside, 100% matches the reference.
@video1: a previously generated camcorder-style clip, used only as the look reference: copy its handheld shake, focus hunting, exposure pumping and tape noise. Do not copy its characters, room, season or action.

LOCATION MAP
Foreground: the near edge of the table with the pale blue cloth and a water glass. Midground: @image1 behind the table, slightly left of center, @image2 at the right edge of the frame. Background: the plaster wall with the two vertical paper signs on frame-left, the window on frame-right full of gray winter light.

FIRST FRAME / BLOCKING
The frame opens as two wrinkled hands lower a white plate with five round white steamed buns onto the table, steam already rising. @image1 sits behind the plate, @image2 is cut off by the right edge, only his cap and one shoulder in frame.

FORMAT MODE
One continuous shot, the camera does not cut on its own.

OPTICS
MS at 47° FOV. At 2.0s a fast lens zoom-in narrows the FOV from 47° to 18° in 0.3s onto @image1's face. The lens zoom only narrows the FOV, the camera position stays and the subjects' proportions stay natural.

CAMERA
The operator sits across the table and holds a consumer camcorder at chest height with one hand. Rough handheld shake of 10 to 15 cm, the framing wanders so the boy drifts off-center, then the operator re-aims within 0.4s with a late refocus. Focus hunts between the rising steam and the boy before it locks. Exposure pumps toward the bright window.

ACTION
0.0s to 0.8s: the plate lands on the table and steam rolls up. @image1 throws both hands in the air with his mouth wide open.
0.8s to 2.0s: he grabs one bun with both hands and takes a huge bite.
2.0s to 2.4s: a fast zoom-in onto his face, soft and then sharp.
2.4s to 4.2s: the bun is far too hot. His eyes squeeze shut, his eyebrows tilt up in the middle, his mouth hangs wide open and he pants out fast hot breaths, white steam puffing from his mouth. He holds the half-eaten bun in both hands in front of his chest, steam rising from the dark red bean filling.
4.2s to 5.0s: his cheeks bulge, he opens his eyes and grins with his mouth full.

PERFORMANCE
A hungry child with no manners left: grabbing hands, eyes only on the bun, a pained happy face at the heat, no look at the camera.

PHYSICS
Steam rises from the buns and drifts toward the window light, breath shows white in the cold room, the soft white bun dents under his fingers and tears open on dark red bean filling, the plate knocks on the table.

LIGHTING
Soft gray winter daylight at 6500K from the window on frame-right, the room dim and cool, steam glowing where it crosses the window light, no direct sun.

AUDIO
Handling rustle, the camcorder motor whirr, the plate knocking on wood, a steamer hissing outside, fast hot panting breaths, chewing, the operator's stifled breathy laugh. No music, no dialogue.

STYLE
Low-bitrate consumer camcorder video from the 1990s: deep focus with no background blur, small sensor, soft edges with slight over-sharpening halos, colors faded with weak blacks, the window blown out to pure white, auto-exposure that pumps when the lens swings between the bright window and the dim room, interlaced ghosting on fast motion, fine tape noise. Natural unretouched skin with pores, freckles and chapped red winter cheeks.

OUTPUT SETTINGS
9:16 vertical, 5 seconds, 24fps, real-time speed.

POSITIVE LOCKS
@image1 keeps the same face, hair and yellow long-sleeve shirt with the black T through the whole take. @image2 keeps his cap and black uniform. The buns stay round and white with red bean filling. The room layout and the two paper signs stay identical.
```
✅ 성공: 접시가 놓이고 기영이가 두 손을 들고, 한입 물고, 급 줌인 뒤에 눈을 질끈 감고 입을 벌린 채 김을 뿜으면 돼요. 찐빵이 주름 잡힌 왕만두로 나오면 five round white steamed buns 뒤에 , smooth and plain with no pleats를 붙여서 다시 돌리세요. 저도 처음에 그렇게 나왔어요.

