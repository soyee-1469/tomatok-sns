# 토마톡 캐스트 프롬프트 v03 — 확정 얼굴 8명 기준 몸통 시트 + 9:16 세트 컷

작성 2026-11-04. `CAST_PROMPTS_v01.md`(2026-11-03)는 확정 얼굴과 안 맞아 폐기(리아 번·점, 준호 은테 사각 안경, 미유 히메컷·덧니, 순덕 금니 전부 옛 설정). 이 파일이 현재 기준.

## 공통 규칙
- 키 차트 (2026-11-04 사용자 지시: 준호 180+, 리아 170+, 하영·미유 작게): 준호 184 · 시우 178 · 수만 172 · 하오 172 · 리아 171 · 하영 155 · 순덕 155 · 미유 153. 2인 이상 컷에서는 이 차이가 보이게 프롬프트에 두 사람 키를 함께 적는다.
- 확정 얼굴(`*_face.png`, `BEA_MASTER_FACE.png`)은 바꾸지 않는다. 몸통 시트의 상의는 **확정 얼굴 사진에 보이는 상의 그대로** 이어받는다. 그래야 얼굴 컷과 몸통 컷이 한 사람으로 붙는다.
- 이미지 1장 = ChatGPT 새 채팅 1개. (임시 채팅은 이미지 생성 불가.) 일반 채팅은 이전 채팅 기억을 끌어와 다른 캐릭터를 한 장에 합쳐 버릴 수 있다(11-04 수만 사례) → 프롬프트 맨 앞에 반드시 `Generate ONE image of ONLY the one person in the attached photo. Ignore any other people, previous images or conversations.`를 붙인다. 해당 캐릭터 확정 얼굴을 첨부하고 그 뒤에 아래 줄을 붙인다.
  ```
  Use the attached photo as the exact identity and wardrobe reference. Same person, same hair, same top, same lighting and wall.
  ```
- 몸통 시트(A)는 얼굴 없이 목부터. 앞면은 쇄골부터 발끝, 뒷면은 뒤통수(머리 길이 확인용)부터 발끝. 가로 2:1, 패널 2개.
- 세트 컷(B)은 네이티브 9:16. 거실 v14 마스터(`SET_LIVINGROOM/LIVINGROOM_master_v14.png`)를 얼굴과 함께 첨부한다.
- 금지어: film grain, skin pores, vignette, heavy color grading. 처음부터 깨끗하고 선명하게.
- 실제 배우를 닮게 쓰지 않는다.

## 공통 스타일 블록 (모든 프롬프트 끝)
```
STYLE: clean sharp high-resolution photo, same warm off-white plaster wall and soft window light from the left as the attached face photo, pale oak floor, neutral-warm color grade, modern Korean drama look, no film grain, no skin pores emphasis, no vignette, no text, no labels, no watermark, no extra limbs.
```

## A 시트 공통 틀 (2:1, 패널 2개)
```
Wardrobe continuity sheet, horizontal 2:1, exactly two equal panels side by side with a thin white gutter. Same person and identical outfit in both panels.
LEFT PANEL: full body FRONT view framed from the collarbone down to the feet, head and face cropped out of frame, standing straight, arms relaxed, a little floor space under the shoes.
RIGHT PANEL: full body BACK view framed from the top of the head down to the feet, showing the back of the hair and the outfit, same scale as the left panel.
```
아래 각 캐릭터의 `IDENTITY`와 `OUTFIT`을 이 틀의 뒤에 붙이고 스타일 블록으로 닫는다.

---

## 1. 리아 (Ria Villanueva) · 27 · 필리핀 엄마 + 미국 아빠 · 3층 앞방
확정 얼굴: `BEA_MASTER_FACE.png`
```
IDENTITY: a 27-year-old woman of Filipino and American mixed heritage, warm golden-tan skin, long dark-espresso hair past the collarbone with soft curtain bangs and a loose S-wave, small gold hoop earrings, a thin gold chain with a small round gold pendant. Height about 171 cm, tall and slim with long legs and a soft natural figure, relaxed open posture.
OUTFIT (v04, 2026-11-04 사용자 "옷이 너무 촌스러운데" → B안 확정): a crisp white cotton poplin button-up shirt with the sleeves cuffed twice to the forearm and the top button open, front-tucked loosely into high-waisted dark-indigo straight-leg jeans, a slim tan leather belt with a small gold buckle, tan leather penny loafers worn with no visible socks, a small structured tan leather shoulder bag. ※ 얼굴 마스터의 아이보리 가디건과 다르므로 세트 컷에는 얼굴 + BODY_BEA_v04 두 장을 함께 첨부. (v03 가디건은 _old, v04A 블랙니트+카멜은 _old_alt 두 번째 의상 후보)
```
B 세트 컷 포즈: 아일랜드 끝에 기대서 3-in-1 커피믹스 봉지를 들고 폰을 보며 웃는다. 소품: 3-in-1 커피믹스, 폰.

## 2. 준호 (김준호) · 29 · 한국 · 세입자 아님(2층 창고방에 짐)
확정 얼굴: `JUNHO_face_C.png`
```
IDENTITY: a 29-year-old Korean man, fair warm skin, soft jet-black two-block hair with a natural wave swept to one side, thin round gold wire-frame glasses with clear lenses always worn. Height about 184 cm, tall lean build, long legs, straight shoulders, polite slightly stiff posture.
OUTFIT: navy cotton button-up overshirt worn open over a plain white crew-neck T-shirt, straight-leg charcoal-gray slacks, black leather derby shoes, a company ID badge on a navy lanyard around his neck, a slim steel watch on the left wrist.
```
B 세트 컷 포즈: 현관 매트에 서서 구두를 벗다 말고 거실을 보며 어색하게 손을 든다(사원증 목걸이 보이게). 소품: 사원증, 구두.

## 3. 순덕 할머니 (박순덕) · 71 · 한국 · 옆집 건물주
확정 얼굴: `BOKRYE_face.png`
```
IDENTITY: a 71-year-old Korean grandmother, sun-weathered warm skin, short tight gray curly perm, deep laugh lines, wide open-mouth smile. Height about 155 cm, short sturdy build, slightly hunched shoulders, strong forearms, hands-on-hips posture.
OUTFIT (v05 확정, 2026-11-04 사용자 "화려한 색으로, 남색이 너무 많다" → "초록색으로". `BODY_BOKRYE_v05.png`. v04 네이비·v05A 보라는 _old): a VIVID EMERALD-GREEN cotton French chore jacket with three patch pockets and the sleeves pushed up, worn open over a plain white crew-neck T-shirt; straight-leg cream wide trousers cropped at the ankle; clean white leather sneakers; a bunch of apartment keys on a brass ring clipped to the jacket pocket; half-rim reading glasses on a beaded chain around her neck; a small black nylon crossbody wallet bag; a thin gold band ring. ※ 얼굴 사진의 누빔조끼·꽃무늬 블라우스와 다르므로 세트 컷에는 얼굴 + BODY_BOKRYE_v05 두 장을 함께 첨부. (v03 몸뻬 버전은 _old)
```
B 세트 컷 포즈: 현관문을 반쯤 열고 들어오며 스테인리스 반찬통 2개를 양손에 들고 있다. 소품: 반찬통.

## 4. 미유 (Miyu Tanaka) · 24 · 일본 오사카 · 3층 뒷방
(v03 무릎 스커트+스니커즈는 폐기. 사용자 지시 11-04: 패션과니까 옷을 더 스타일 있게.)
확정 얼굴: `MIYU_face.png`
```
IDENTITY: a 24-year-old Japanese woman, pale cool-toned skin, dark-brown chin-length bob with straight wispy bangs, small silver hoop earrings, small closed-lip smile. Height about 153 cm, petite and small-framed, narrow shoulders, slightly shy posture with hands clasped in front.
OUTFIT (v07 확정, 2026-11-04 사용자 "빨간 자켓" → "블랙으로". `BODY_MIYU_v07.png`. v05 네이비·v06 빨강은 _old): an oversized BLACK velour track jacket with a high standing collar, two white stripes down each sleeve, white corded frog-knot button closures down the front, ribbed black hem and cuffs, worn open over a fitted white ribbed tank top; white tiered ruffle bloomer shorts with a lace hem, mid-thigh; sheer white ankle socks; white chunky-sole sneakers; a small red knit ribbon tied on the left wrist; small silver hoop earrings. Playful Osaka street style, no logos. ※ 얼굴 사진의 스트라이프 셔츠와 상의가 다르므로 세트 컷에는 얼굴 + BODY_MIYU_v07 두 장을 함께 첨부한다. (v04 맥시스커트는 _old로 보관)
```
B 세트 컷 포즈: 창가 벤치에 앉아 응원봉을 무릎에 놓고 폰으로 티켓팅 중, 입을 꾹 다문 집중 표정. 소품: 응원봉, 포토카드 홀더.

## 5. 수만 (Suman Thapa) · 31 · 네팔 포카라 · 2층 앞방
확정 얼굴: `SUMAN_face.png`
```
IDENTITY: a 31-year-old Nepali man, deep warm brown skin, thick black curly hair, short neatly trimmed black beard and mustache, wide bright smile. Height about 172 cm, stocky solid build, broad shoulders, thick forearms, grounded relaxed stance.
OUTFIT (2026-11-06 개정, 사용자 A안): white double-breasted chef's jacket with cloth buttons and the sleeves rolled to the elbow, a plain BLACK full bib apron with a neck strap over it, NO towel, charcoal-gray work trousers, black kitchen clogs.
(옛 v03: 네이비 반앞치마 + 어깨 수건 → 1화 프레임이 전부 bib 앞치마로 나와 검정 bib로 확정. 바디 시트 BODY_SUMAN_v04. v03 파일은 BODY_SUMAN_v03_old_halfapron.png로 이름 변경, 보드·생성기에서 제외.)
```
B 세트 컷 포즈: 아일랜드 뒤에서 유리 피클병(아차르) 뚜껑을 열며 거실 쪽에 들어 보인다. 소품: 유리 피클병, 앞치마.

## 6. 하오 (왕하오 王浩) · 25 · 중국 칭다오 · 2층 뒷방
확정 얼굴: `DOYUN_face.png` (2026-11-04 재캐스팅 D안. 옛 얼굴 `DOYUN_face_v01_old_junholike.png`는 준호와 닮아 폐기. 파일 키 DOYUN 유지)
```
IDENTITY: a 25-year-old Chinese man, healthy warm tan skin, soft square jaw, large bright single-lid eyes, thick straight dark eyebrows, short neat black buzz-fade on the sides with a slightly longer textured top, open friendly grin with a dimple on the left cheek. Height about 172 cm, sturdy athletic build with broad solid shoulders, relaxed posture.
OUTFIT: heather-gray pullover hoodie with drawstrings over a white T-shirt, black over-ear headphones around the neck with the cable hanging, matching heather-gray sweatpants, black slides with white socks.
```
몸통 시트 확정: `BODY_DOYUN_v04.png` (v03은 _old)
B 세트 컷 포즈: 계단 아래쪽 2~3칸에 앉아 삼각대 위 폰을 거실로 향하게 조정하고 있다. 소품: 삼각대, 화이트보드 마커.

## 7. 하영 · 17 · 한국 · 순덕 할머니 손녀, 자주 오는 손님
확정 얼굴: `SONNYEO_face.png`
```
IDENTITY: a 17-year-old Korean high-school girl, light warm skin, dark-brown hair in a high ponytail tied with a cream fabric scrunchie, loose wispy strands around the face, big open-mouth laugh. Height about 155 cm, petite and slim, bouncy energetic posture.
OUTFIT: navy school blazer with thin white piping, white collared shirt, navy-and-burgundy striped ribbon bow tie, navy-and-gray plaid pleated school skirt to the knee, white socks, white sneakers, a beige canvas crossbody bag with a pink heart charm, a gold star charm and a clear acrylic K-pop photocard keyring clipped to the strap.
```
B 세트 컷 포즈: 소파 등받이 뒤에 서서 몸을 앞으로 숙이고 폰 화면을 누군가에게 들이민다(계단 쪽을 힐끗). 소품: 포토카드 키링.

## 8. 시우 · 22 · 한국 · 2층 거주 대학생
확정 얼굴: `DAEHAK_face.png`
```
IDENTITY: a 22-year-old Korean university student, light warm skin, neat dark-brown medium-length hair parted slightly off-center and swept to the sides, soft gentle smile. Height about 178 cm, slim athletic build, straight relaxed posture.
OUTFIT: heather-gray crew-neck sweatshirt over a white T-shirt, light-wash straight-leg jeans, white sneakers, a beige canvas backpack with a black buckle worn on both shoulders.
```
B 세트 컷 포즈: 계단을 내려오다 멈춰 난간에 한 손을 얹고 거실을 내려다본다(하단 2~3칸, 전신). 소품: 백팩.

---

## B 세트 컷 공통 틀 (9:16)
얼굴 + 거실 v14 마스터를 첨부하고 쓴다. `[IDENTITY]`, `[OUTFIT]`, `[POSE]`에 위 캐릭터 블록을 넣는다.
```
Use the first attached photo as the exact identity and wardrobe reference, and the second attached photo as the exact set reference. Same person, same hair, same outfit; same room, same furniture, same colors, same light oak herringbone floor.
Vertical 9:16 photo, full body from the chin down to the feet, head and face cropped out of the top of the frame (reference sheet, not a portrait), eye-level camera, slight wide-angle, in the "Yeonnam 3-Story House – 1F Common Living Room".
[IDENTITY]
[OUTFIT]
POSE: [POSE]
Soft even studio lighting matching the set photo, no sunbeams, window glass a plain soft neutral.
STYLE: clean sharp high-resolution photo, modern Korean sitcom look, neutral-warm color grade, no film grain, no skin pores emphasis, no vignette, no text, no watermark, no extra limbs.
```

## 저장 규칙
- A 시트: `BODY_<NAME>_v03.png` (예: `BODY_BEA_v03.png`, `BODY_SONNYEO_v03.png`)
- B 세트 컷: `SET_<NAME>_<pose>_v01.png` (예: `SET_JUNHO_entrance_v01.png`)
- 결과가 얼굴 사진과 상의·머리가 다르면 그 채팅은 버리고 새 채팅에서 다시. 결과를 다시 넣어 고치지 않는다.

## 세트 컷 주의 (2026-11-04)
- **세트 컷(B)은 레퍼런스라 얼굴을 뺀다** (사용자 2026-11-04 "세트컷에서도 얼굴 잘라야"). 프롬프트에 `framed from the chin down, head and face cropped out of the top of the frame` 추가. 얼굴이 들어가는 건 Kling 시작 프레임(에피소드 F컷)뿐이고, 그건 만들 때마다 마스터 얼굴과 대조. 기존 리아·준호 세트 컷은 턱 아래로 잘라 저장, 원본은 `_old_withface`.
- 거실 v14 마스터에는 **현관이 안 보인다**(현관 벽에서 찍은 앵글). 현관 컷을 요청하면 모델이 문·후크·에코백·신발장을 지어낸다. 사용자는 신발장을 일부러 없앴으므로 현관은 **빈 벽 + 문 + 바닥 매트 하나**로 고정. 프롬프트에 `no coat hooks, no shoe rack, no shelves, no bags on the wall, plain wall beside the door` 명시.
- 소품은 캐릭터가 손에 든 것만. 바닥에 다른 신발 두지 않기.
