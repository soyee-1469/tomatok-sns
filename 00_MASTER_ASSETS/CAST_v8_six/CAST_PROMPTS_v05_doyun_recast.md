# 도윤 재캐스팅 프롬프트 v05 (2026-11-04)

이유: 확정 얼굴 `DOYUN_face.png`가 준호(`JUNHO_face_C.png`)와 얼굴형·눈매·코·머리색까지 같음(안경만 다름). 사용자: "준호랑 도윤이랑 너무 닮았는데 다르게 뽑아볼까?" → 도윤을 다시 뽑는다. 준호는 주연이라 고정.
사용자 질문 "중국사람할까?" → 중국인 버전(A)과 한국인 유지 버전(B)을 각 1장씩 뽑아 비교.

## 준호와 갈라야 하는 지점 (둘 다 공통)
| 준호 | 도윤(새) |
|---|---|
| 갸름한 V라인, 광대 없음 | **둥근 얼굴, 볼살 약간, 턱 짧음** |
| 쌍꺼풀 있는 또렷한 눈 | **무쌍 가는 눈, 웃으면 사라짐** |
| 오똑한 코 | **낮고 둥근 코끝** |
| 가르마 투블럭, 검정 | **짧게 친 머리 또는 애쉬브라운 펌**, 앞머리 내림 |
| 금테 둥근 안경 | 안경 없음, **헤드폰 목에** |
| 177, 마른 체형 | **172, 약간 통통/어깨 둥근 체형** |
| 호감형 따뜻한 미소 | **삐딱한 반쪽 웃음**, 한쪽 입꼬리만 |

## A. 중국인 버전 (제안 이름: 왕하오 王浩 · 25 · 칭다오)
첨부: `BEA_MASTER_FACE.png` (스타일 레퍼런스로만). ChatGPT 새 채팅.
```
Generate ONE image of ONE person only. Use the attached photo ONLY as a style and lighting reference (same warm off-white plaster wall, same soft window light from the left, same 4:5 chest-up framing, same clean photo look). The person is completely different from the photo.

IDENTITY: a 25-year-old Chinese man from Qingdao, light warm skin, ROUND soft face with slightly full cheeks and a short chin, narrow single-lid (monolid) eyes that nearly close when he grins, thick straight black eyebrows, a low rounded nose tip, slightly full lips. Hair: short cropped ash-brown hair with a soft textured fringe falling onto the forehead. Build: about 172 cm, slightly stocky with rounded shoulders. Black over-ear headphones resting around his neck.
EXPRESSION: lopsided half-grin, only the left corner of the mouth lifted, eyes narrowed and amused, like he just thought of a joke he will not share.
OUTFIT: heather-gray pullover hoodie with drawstrings over a white T-shirt.
He must look likeable and warm, not sloppy. He must NOT look like a K-drama lead: no sharp V-line jaw, no double eyelids, no tall nose bridge, no glasses.

STYLE: clean sharp high-resolution photo, vertical 4:5 portrait, chest-up, head and shoulders centered, looking straight into the camera at eye level, neutral-warm color grade, modern Korean sitcom look, no film grain, no skin pores emphasis, no vignette, no text, no labels, no watermark. Do not resemble any real actor or celebrity.
```
저장: `DOYUN_recast_CN_v01.png`

## B. 한국인 유지 버전 (이도윤)
같은 프롬프트에서 IDENTITY 첫 줄만 교체:
```
IDENTITY: a 25-year-old Korean man, light warm skin, ROUND soft face with slightly full cheeks and a short chin, narrow single-lid (monolid) eyes that nearly close when he grins, thick straight black eyebrows, a low rounded nose tip, slightly full lips. Hair: short cropped black hair with a soft textured fringe falling onto the forehead. Build: about 172 cm, slightly stocky with rounded shoulders. Black over-ear headphones resting around his neck.
```
저장: `DOYUN_recast_KR_v01.png`

## 확정 후 할 일
1. 확정본을 `DOYUN_face.png`로 교체(옛 파일은 `DOYUN_face_v01_old_junholike.png`).
2. `BODY_DOYUN_v03.png`는 얼굴 없는 시트라 체형(통통)만 다르면 재생성. 머리 뒷모습이 바뀌므로 재생성 권장.
3. 무표정 `DOYUN_face_neutral.png` 생성 (v04_neutral_face.md의 IDENTITY를 새 얼굴로 교체).
4. CAST_BIBLE·WORLD_PLAN의 도윤 이름/국적 갱신, 보드 재발행.

## v02 (2026-11-04) — 사용자: "얼굴이 비호감인데"
v01(CN/KR)은 눈을 너무 가늘게, 볼을 너무 통통하게 잡아 비호감. v02는 호감 요소를 넣고 준호와는 피부톤·눈·턱·보조개로 가른다. 국적은 중립(동아시아), 이름은 확정 후.

공통 (첨부 BEA_MASTER_FACE.png 스타일 레퍼런스):
```
Generate ONE image of ONE person only. Use the attached photo ONLY as a style and lighting reference (same warm off-white plaster wall, same soft window light from the left, same 4:5 chest-up framing, same clean photo look). The person is completely different from the photo.

IDENTITY: a 25-year-old East Asian man, healthy warm tan skin (noticeably warmer and darker than a typical fair K-drama lead), a soft square jaw with a gently rounded chin, large bright single-lid (monolid) eyes that are wide open and friendly, straight thick dark eyebrows, a medium straight nose, and a deep dimple on his left cheek when he smiles. Clean clear skin, no stubble. [HAIR]. Build: about 172 cm, sturdy athletic shoulders, relaxed posture. Black over-ear headphones resting around his neck.
EXPRESSION: open friendly grin showing upper teeth, eyes bright and wide (not squinting), head tilted very slightly, dimple visible — the kind of face people instantly like.
OUTFIT: heather-gray pullover hoodie with drawstrings over a white T-shirt.
He must look handsome in a boyish, approachable way. He must NOT look like the attached photo's style of lead: no double eyelids, no narrow V-line jaw, no glasses, no puffy cheeks, no squinting.

STYLE: clean sharp high-resolution photo, vertical 4:5 portrait, chest-up, head and shoulders centered, looking straight into the camera at eye level, neutral-warm color grade, modern Korean sitcom look, no film grain, no skin pores emphasis, no vignette, no text, no labels, no watermark. Do not resemble any real actor or celebrity.
```
- C: [HAIR] = `Hair: short black hair with a soft natural curl perm, textured and slightly tousled, fringe pushed up off the forehead showing the brows` → `DOYUN_recast_C_v02.png`
- D: [HAIR] = `Hair: short neat black buzz-fade on the sides with a slightly longer textured top, forehead fully visible` → `DOYUN_recast_D_v02.png`


## 확정 (2026-11-04 사용자 "d 중국")
- D안(페이드컷) + 중국인. 이름 **왕하오 王浩**, 25, 칭다오. 표시명 "하오". 파일 키 DOYUN 유지.
- 교체 완료: `DOYUN_face.png`(=D v02), `BODY_DOYUN_v04.png`, `DOYUN_face_neutral.png`. 옛 파일은 `_old`.
