# 준호 말투 규칙 (2026-11-05 사용자 지적: "남자가 너무 짜증나는 말투야") → 같은 날 추가: "점잖지 않고 개그감 있는 남자야", "거실에서 우왕좌왕 떨려서 핸드폰 들고 촐싹거리는 느낌"

> 2차 수정(2026-11-05): 아래의 '낮고 차분하고 점잖게'는 **폐기**. 준호는 점잖은 사람이 아니라 **개그감 있는 남자**다. 뺄 것은 짜증·비꼼·따지기뿐이고, 익살·큰 리액션·자기 비하 개그·코믹 타이밍은 살린다. 좌절도 자기 자신을 향한 농담으로 푼다.

## 개그감 규칙
- 리액션이 크고 빠르다: 눈썹, 입, 작은 소리(헉, 어?). 코믹 더블테이크, 가슴에 손, 천장 보기.
- 자기 비하 개그: 망하면 자기를 웃음거리로 만든다. 리아를 웃음거리로 만들지 않는다.
- 짜증과 개그의 차이: 짜증은 상대를 향하고, 개그는 자기와 상황을 향한다. 같은 대사도 '상대에게 따지기'가 아니라 '관객에게 하소연하기'로 친다.
- 1화 상태: 거실에서 우왕좌왕, 떨려서 폰을 두 손으로 쥐고 촐싹거림. 무릎 떨기, 자세 고쳐 앉기, 화면 봤다 뗐다, 바지에 손바닥 닦기. 모든 1화 준호 컷 ACTION에 자동 삽입(make_prompts_v06.py).
- 프롬프트 공통 문장(모든 준호 컷 자동 삽입): `He is a very kind, funny man who loves her deeply: a natural comedian, playful and a little goofy, with quick expressive reactions and good comic timing. He is never irritated with her; when things go wrong he turns it into a joke on himself. His only flaw is that he cannot throw anything away.`
- 허용 어휘: playful, goofy, comic timing, double take, mock-serious, mock-wounded, cheeky, self-deprecating, animated, jittery, fidgety. 금지어는 아래 그대로.

준호는 걱정쟁이지 짜증쟁이가 아니다. 겉은 멀쩡하고 예의 바른 29세 회사원. 웃음은 **차분한 사람이 당황하는 낙차**에서 나지, 짜증·투정·따지기에서 나지 않는다.

## 소리
- 낮고 차분하고 느리다. 목소리를 절대 높이지 않는다. 끝음은 거의 항상 내림.
- 당황해도 톤은 그대로, 말 사이 간격만 길어진다. 되묻는 말도 조용하게 묻는다 ("……그건 뭐야." 는 의심이 아니라 조용한 궁금증).
- 변명도 담담하게, 설명하듯. 리아에게 따지지 않는다. 맞받아칠 때도 혼잣말처럼 작게.
- 혼잣말 성분 50%. 상대에게 던지는 말도 반쯤 자기한테 하는 말처럼.

## 금지어 (프롬프트에 쓰지 않는다)
aggrieved, incredulous, interrogating, pressing, petty, defensive, snapping, irritated, whiny, exasperated, hitting back, counter-attack

## 허용 어휘 (프롬프트용)
calm, quiet, low, soft, polite, earnest, deadpan, resigned, gently puzzled, murmured, matter-of-fact, unhurried, a worried man keeping his voice level

## Kling 프롬프트 공통 문장
`The man speaks in natural native Korean, low, calm and quiet, polite and unhurried, never raising his voice, the sentence ending on a soft falling tone; even when flustered his volume stays the same and only the pauses get longer.`

## 적용
- `01_EPISODES/EP01R/tools/make_prompts_v06.py` VOICE["JUN"] + 준호 delivery 문구 전부 교체 (2026-11-05).
- 기존 클립 중 톤이 가장 거친 것부터 재생성: E1_16, E1_21, E1_23, E2_04, E2_11, E1_14 (각 6cr).

## 준호 캐릭터 한 줄 (2026-11-05 사용자 확정)
**리아를 너무 사랑하는 아주아주 착한 남자. 흠은 물건을 못 버리는 것.** 2화의 창고방 짐은 게으름이 아니라 이 흠이다: 옮기려면 버릴 걸 정해야 하고, 준호는 그걸 못 한다. "공사 끝나면"은 그 결정을 미루는 말이다.

## 준호의 현재 심리 상태 — 고정 설정 (2026-11-05 사용자 지시: "남자의 현재 심리상태를 결정해 놓자")
시즌 초반(EP01~EP03) 준호는 **리아에게 한 번도 짜증을 내지 않는다.** 짜증의 방향은 항상 자기 자신이나 상황이지, 리아가 아니다.
- 리아를 향한 기본 감정: 좋아 죽겠고, 조금 기가 눌려 있고, 리아의 장난은 "내가 운 좋게 얻은 것"으로 받아들인다. 놀림을 당해도 반격하지 않고 받아들인 뒤 조용히 수습한다.
- 리아 가족을 향한 기본 감정: 잘 보이고 싶은 공포. 22명 앞에서 평가받는 게 무섭지만 티를 안 내려고 한다. 그래서 더 조용해진다.
- 할머니(순덕)를 향한 기본 감정: 평생 안 녹던 얼굴이 리아에겐 녹는 걸 보는 손자의 체념 + 안도. 서운함은 농담 수준.
- 싸울 때(2화): 화가 난 게 아니라 **찔려서 피하는 것**. 리아 말이 맞다는 걸 안다. 빨리 말하기 작전은 공격이 아니라 당황한 사람의 도망이다. 끝에 "벽이 얇아"도 체념이지 비꼼이 아니다.
- 한 줄 요약: **예의 바른 걱정쟁이가 사랑하는 사람 앞에서 쩔쩔매는 것**이 준호 코미디의 전부다. 짜증, 투정, 비꼼, 따지기는 캐릭터 밖이다.

프롬프트 공통 문장(모든 준호 컷의 PERFORMANCE에 자동 삽입): `He is fond of her and never annoyed with her; any frustration is aimed at himself or the situation, and it shows as stillness and longer pauses, never as a sharper voice.`
