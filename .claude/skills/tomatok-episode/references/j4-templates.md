# 현행 J4 기반 스틸·영상 템플릿

과거 철칙 17의 유효한 틀을 유지한 수정본이다. 원문 재현이 아니라 현행 제작 출발점이며, 각 대괄호를 확정 콘티·연기 지시로 채운다. J4 구도 자체를 재현할 때만 85mm tight close-up, 렌즈 바로 아래 시선과 폰 불빛을 사용한다. 다른 컷에는 그 컷의 샷·시선·광원을 사용한다. 성공한 컷의 변경은 별도 버전에서 한 요소씩 비교한다.

## J4 원문 예시 — 같은 클로즈업을 재현할 때

아래 세 줄은 과거 철칙 17에 보존된 J4 스틸 템플릿 원문이다. 비교·재현용으로 함께 둔다. 일반형 템플릿과 구분하며, 다른 샷에 85mm·폰 불빛·렌즈 옆 시선을 강제하지 않는다. 실제 촬영 높이는 콘티 기준으로 정리한다(원문에는 eye level과 slightly below eye level이 함께 있음).

```text
Photo-real still for a Korean sitcom, 9:16 vertical, evening living room (warm lamps, string lights, arched window dark navy), fixed tripod camera at eye level, natural skin, no beauty filter, no text, no watermark. Keep the exact face, hair, glasses and clothes of the people in the reference images and the exact room from the references.
Tight close-up (85mm): the face of [인물 설명] fills the frame from the top of the head to the collar, slightly below eye level, soft phone-screen glow from below, looking down just past the lens, mouth slightly open, [감정 두 단어], background sofa and window very blurred.
KEEP this exact staging, camera distance, furniture placement and room; change only what follows. Situation: [상황]. Emotion: [감정]. Action: [동작]. The first reference images are the exact faces to keep; identity must match them exactly. Candid mid-action, like a frame grabbed from video.
```

## 스틸 — Nano Banana Pro

```text
Photo-real still for a Korean sitcom, 9:16 vertical, natural skin, no beauty filter, no text, no watermark.
Keep the face, hair, glasses and clothes of [character] from the identity references. Use the storyboard for composition and blocking only, and the set reference for visible room details.
[Shot size and lens cue], [crop boundaries], [camera angle]. [Visible light sources], [gaze target and direction], [starting expression and observable action]. [Background focus appropriate to this shot]. Candid mid-action, like a frame grabbed from video.
Situation: [cause of the reaction]. Emotion: [start emotion]. Action: [starting pose].
```

같은 구도에서 일부만 수정할 때만 아래를 덧붙인다. 새 구도를 만들 때는 사용하지 않는다:

```text
KEEP this exact staging, camera distance and visible room; change only [the requested element].
```

## Kling — 일반 고정 대사 샷

```text
SCENE CONTEXT
[Only what is actually visible in the start still, plus the camera axis]. [Off-frame element] is off-frame to the [left|right] and stays off-frame. Exactly as in the start image: [character, pose and visible prop state]. [He|She] is the only person visible in this shot.

CAMERA
One continuous shot. Locked tripod camera, no cuts, no zoom, no pan, no reframing, no horizontal flip. Preserve the starting camera composition while allowing natural character movement. Modern Korean sitcom look, natural warm colors.

ACTION
0.0–0.3s: [one short beat: gaze or breath; no speech yet].
[Speech start]–[speech end]s: [character] says the line with [emotion and purpose], [one observable small action].
[Speech end]–[clip end]s: [listening or reaction].

PERFORMANCE
[Start emotion → trigger → end emotion]. [Specific natural expression]. Avoid [only the unwanted exaggerated action for this cut].

AUDIO
[Approved quiet scene ambience]. No music or notification effects.

IDENTITY AND CONTINUITY
Preserve the same face, hair, glasses, clothes and visible scene throughout. [Held prop] stays [where it is in the start image] for the whole clip. The background stays empty of people for the entire clip: no one walks past, no one appears at the edge of the frame. Nothing new appears in the frame: no lamp, no cushion, no new object. Absolutely no other person enters or is visible at any point. No subtitles, no on-screen text, no watermark.

DIALOGUE
[Character], [language and approved accent], [baseline voice quality].
Delivery: [pace, emphasis, pause, and rising/falling/level ending for THIS line].
Exact spoken words: “[approved dialogue]”. No additional speech. Natural visible lip-sync. Every syllable must be finished by [clip end − 0.6]s.
```

길이는 실제 발화·쉼·반응을 반영한다. 카메라 고정을 얼굴·몸 정지나 동일 끝 이미지 잠금으로 대체하지 않는다. 과거 설정 std/720p/cfg 0.5/enhance off/sound on은 지원과 비용 확인 후 적용한다. 대사 톤 수정 때 공통 연기 제한을 추가하지 않는다. 이동 컷은 이 템플릿을 그대로 쓰지 말고 도착 위치와 시작·끝 이미지를 별도 설계한다.


## 2026-11-16 검증된 수정 (컷 1·8·11·12·14, 사용자 채택본 기준) — 모든 세션 공통

1. **SCENE CONTEXT에는 시작 스틸에 실제로 보이는 것만.** 보이지 않는 인물·광원·소품을 서술하면 모델이 만들어 넣는다. 컷 14 "친구가 아일랜드에 서 있다" → 배경에 사람이 걸어 들어옴(take05). 컷 11 "warm pendant light from above" → 전구가 생김(take03). 방향만 필요하면 `off-frame to the right and stays off-frame`.
2. **3초 컷의 발화 전 비트는 한 단계·0.3초.** 두 단계(0.0–0.4 / 0.4–0.8)로 쓰면 발화가 2.2초까지 밀려 잘린다(컷 12 take03). 끝낼 시각을 명시: `The whole line must finish by 2.4s`.
3. **대사 길이로 컷 길이를 정한다.** 17음절 + 중간 쉼 = 5초(컷 8). 3초에 밀어 넣지 않는다. 비용 3s 6cr / 4s 8cr / 5s 10cr (std).
4. **준호 PERFORMANCE 금지어 추가:** sulky, childish, 특정 단어 강세, brow furrowed → 짜증으로 들린다(컷 8 take06). 반대로 half-smile·amused → 너무 신남(take07). 실망은 `quiet, soft, low, resigned, deflated, a worried man keeping his voice level`로.
5. **들뜬 당황(컷 14 채택본):** `flustered in a happy way, a nervous little smile, eyes bright and darting, excited and a little scared at the same time` — 심각·공포 어휘 금지.
6. **손에 든 폰·소품은 CONTINUITY에 높이 고정 문장.** 없으면 후반에 프레임 아래로 내려간다.
7. **배경 결함은 정지 패치로 고치지 않는다.** 원본 배경이 3초에 8px 흘러서 패치가 어색(컷 14 take05_clean 불채택). 재생성.
8. **와이드+아주 느린 푸시인은 통과**(컷 1 take01). `very slow, smooth, barely noticeable push-in … ending only slightly tighter`.
9. **네팔어 중얼거림은 Kling이 발음함**(컷 11 take04 채택). DIALOGUE에 데바나가리 + 로마자 병기, `only Nepali, not Korean, not Hindi`.
10. **같은 계정에서 세션 두 개가 동시에 생성하지 않는다.** 생성 전 `higgsfield generate list --json`으로 진행 중 작업을 확인하고, 다른 세션이 돌고 있으면 멈추고 사용자에게 알린다. `tools/series_board_reviews.json`·애니매틱 JSON은 한 세션만 쓴다.
11. **한 글자·숫자 답("2")은 유료 생성 전에 뜻을 확인한다.** 오독으로 6cr 낭비(컷 14 take04).
12. **SCENE CONTEXT에 대사의 뜻을 영어 문장으로 쓰지 않는다.** "he has just read that her family is sending questions for him to check first"처럼 쓰면 모델이 한국어 대사 대신 **그 영어 문장을 말한다**(컷 30 take03). 상황은 짧은 구절로만, 말은 DIALOGUE에만.
13. **20음절 넘는 대사는 6초 + 보통 속도.** "slowly / counting it out" 지시와 말줄임표는 발화를 늦추고 줄인다(컷 30 take02: 5초에 절반만).
14. **2막 미디엄 3/4 스틸(OTS·단독 모두)에서 Kling 3.0 대사가 깨진다.** 11-16 7테이크 전부 축약·다른 문장·영어·글자 생성(컷 23·24·30). 같은 날 J4식 타이트 CU는 11/11 성공. 대사 컷 시작 스틸은 **얼굴이 프레임을 채우는 타이트 CU**(머리~옷깃, 렌즈 옆 시선)로. 미디엄은 무대사·반응 컷에만.
