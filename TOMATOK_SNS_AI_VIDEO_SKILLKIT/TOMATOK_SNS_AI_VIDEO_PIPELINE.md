# TOMATOK SNS AI 영상 제작 파이프라인

## 목적
토마톡 메신저 인스타그램용 SNS 콘텐츠를 반복 제작하기 위한 자동화 파이프라인.

콘텐츠는 크게 3가지 템플릿으로 운영한다.

1. 정보공유형 — 다문화 생활/가족 관련 정보
2. 공감형 — 다문화 가정에서 생길 수 있는 상황을 시트콤처럼 표현
3. 기능소개형 — 토마톡 메신저 기능을 실제 상황 안에서 보여주기

첫 번째 제작 대상은 **기능소개형**이며, 핵심 메시지는 다음과 같다.

> 다문화 가족 구성원이 하나의 메신저 안에서 각자 편한 언어로 대화하고, 사진을 공유하고, 실시간 번역을 통해 마치 서로 모국어로 대화하는 것처럼 소통할 수 있다.

---

# 1. 전체 제작 구조

```text
기획/대본
  ↓
캐릭터 확정
  ↓
캐릭터 시트 제작
  ↓
장면 분할
  ↓
장면용 앵커 이미지 생성
  ↓
Higgsfield / Kling 영상화
  ↓
음성 생성
  ↓
립싱크
  ↓
실제 TOMATOK UI 합성
  ↓
자막 / BGM / 효과음 / 편집
  ↓
검수
  ↓
Instagram Reels 최종 출력
```

---

# 2. 툴 역할 분담

## GPT / ImageGen
주 역할: **기획 + 캐릭터 디자인 + 이미지 제작**

- 에피소드 아이디어 생성
- 상황극 대본 생성
- 장면별 콘티 생성
- 캐릭터 얼굴 후보 생성
- 캐릭터 시트 생성
- 장면용 기준 이미지 생성
- 이미지 수정
- 프롬프트 작성

### 권장 사용
실사형 인물 중심 SNS 콘텐츠는 먼저 GPT/ImageGen에서 기준 인물을 확정한다.

---

## Cursor
주 역할: **자동 제작 파이프라인 관리**

- 폴더 및 파일 구조 관리
- 장면 JSON 읽기
- 이미지/영상 생성 순서 제어
- Higgsfield 호출
- 생성 결과 저장
- 실패 장면 재시도
- 진행 상태 기록
- 완료된 장면 건너뛰기
- 파일명 자동 관리

### 권장 사용
반복 제작이 시작되면 Cursor를 메인 제작 관리자 역할로 사용한다.

---

## Higgsfield
주 역할: **영상 생성 + 인물 움직임 + 립싱크**

- Image-to-Video
- 인물 제스처
- 카메라 움직임
- 표정 변화
- 말하는 장면
- 립싱크
- 필요시 Motion Control

### 권장 사용
실사형 다문화 가족 시트콤과 기능소개 영상의 메인 영상 엔진으로 사용한다.

---

## Kling
주 역할: **보조 영상 엔진**

- 캐릭터/이모티콘 애니메이션
- 스타일 일관성이 중요한 캐릭터 영상
- Higgsfield 결과가 만족스럽지 않은 컷 대체
- 특정 모션 테스트

### 권장 사용
실사 가족 콘텐츠의 기본값은 Higgsfield로 두고 Kling은 보조로 유지한다.

---

## Premiere / CapCut / After Effects / FFmpeg
주 역할: **최종 편집**

- 컷 연결
- 자막
- BGM
- 효과음
- 실제 토마톡 UI 합성
- 로고 합성
- 모션그래픽
- 엔드카드
- 최종 렌더링

---

# 3. 가장 중요한 원칙 — 캐릭터를 먼저 확정한다

시리즈형 SNS 콘텐츠는 장면 생성보다 먼저 **고정 등장인물**을 만든다.

예시:

- 외국인 아내
- 한국인 남편
- 시어머니 또는 친정어머니
- 아이

각 캐릭터는 처음 확정한 얼굴을 이후 모든 에피소드에서 계속 사용한다.

---

# 4. 캐릭터 생성 방식

## 실사형 인물
권장:

```text
GPT/ImageGen에서 기준 얼굴 생성
→ 캐릭터 시트 확정
→ 동일 이미지를 Higgsfield/Kling reference로 사용
```

실사형 콘텐츠는 이미지와 영상을 반드시 같은 플랫폼에서 만들 필요는 없다.

중요한 것은 **생성 플랫폼보다 동일한 레퍼런스 이미지를 계속 사용하는 것**이다.

---

## 캐릭터 / 이모티콘 / 3D 토이
권장:

```text
같은 생성 플랫폼에서 이미지 + 영상 생성
```

이 유형은 얼굴 정체성보다 재질, 비율, 스타일 일관성이 중요하기 때문에 같은 엔진에서 이어서 제작하는 것이 유리할 수 있다.

---

# 5. 캐릭터별 최소 이미지 세트

각 주인공별로 아래 이미지를 확보한다.

```text
01_front.png
02_three_quarter.png
03_side.png
04_upper_body.png
05_full_body.png
06_smile.png
07_neutral.png
08_confused.png
09_surprised.png
10_talking.png
```

권장 추가 항목:

- 자주 입는 기본 의상
- 집에서 입는 의상
- 외출복
- 회사/학교용 의상

---

# 6. Character Bible 작성

각 인물마다 고정 정보를 문서화한다.

예시:

```text
이름: Linh
역할: 베트남 출신 아내
나이대: 30대 초반
헤어: 어깨 아래 검은 생머리
얼굴: 둥근 얼굴, 부드러운 눈매
키/체형: 162cm, 보통 체형
기본 의상: 크림/베이지 계열
성격: 차분하고 현실적, 유머감각 있음
표정: 과장 금지
말투: 친근하고 자연스러움
목소리: 밝지만 너무 높지 않은 여성 음성
```

이 문서를 모든 이미지/영상 생성 프롬프트의 기준으로 사용한다.

---

# 7. 에피소드 기획

기본 쇼츠 구조:

```text
HOOK
→ 문제 상황
→ 오해 / 공감 포인트
→ TOMATOK 사용
→ 해결
→ 감정 또는 펀치라인
→ CTA
```

권장 길이:

```text
15초 ~ 30초
```

---

# 8. 기능소개형 기본 템플릿

첫 번째 기능소개 콘텐츠 예시:

## 핵심 메시지

```text
가족인데 언어가 달라도
하나의 단톡방에서 각자 편한 언어로 대화할 수 있다.
```

## 흐름

```text
0~3초    언어가 다른 가족 문제 제시
3~6초    각자 다른 언어를 사용하는 모습
6~8초    TOMATOK 등장
8~13초   실시간 번역 시연
13~17초  사진 공유
17~22초  각자 자기 언어로 이해하는 모습
22~27초  가족이 편안하게 소통
27~30초  TOMATOK 엔드카드
```

---

# 9. 대본 작성 규칙

립싱크와 쇼츠 편집을 고려해 대사는 짧게 작성한다.

권장:

```text
한 대사 = 2~4초
최대 5초 이내
```

좋은 예:

```text
"어머니가 뭐라고 하신 거지?"
"오늘 저녁 같이 먹자는 뜻이야?"
"아, 이제 알겠어."
```

피해야 할 예:

```text
한 사람이 10초 이상 길게 설명하는 문장
```

---

# 10. 장면 JSON 생성

각 에피소드는 장면별 JSON으로 관리한다.

예시:

```json
{
  "scene_id": "EP001_SC03",
  "characters": ["wife"],
  "location": "living_room",
  "action": "looking at smartphone and becoming mildly confused",
  "emotion": "mild confusion",
  "dialogue": "어머니가 뭐라고 하신 거지?",
  "duration": 3.5,
  "reference_character": "characters/wife/front.png",
  "image_status": "pending",
  "video_status": "pending",
  "audio_status": "pending",
  "lipsync_status": "pending",
  "ui_composite_status": "pending"
}
```

---

# 11. 장면용 이미지 생성

각 영상 컷은 먼저 **앵커 이미지**를 만든다.

## 이미지 단계에서 고정할 것

- 등장인물 얼굴
- 헤어
- 체형
- 의상
- 공간 분위기
- 조명
- 카메라 각도
- 토마톡 브랜드 톤

## 스마트폰 화면

가능하면 실제 UI를 이미지 생성 단계에서 만들지 않는다.

권장:

```text
blank / simple / clean phone screen
```

이후 실제 TOMATOK UI를 편집 단계에서 합성한다.

---

# 12. 장면 이미지 생성 권장 수

각 장면별 기본:

```text
Anchor Wide
Anchor Medium
Anchor Close
```

중요한 장면:

```text
3~5장 생성 후 가장 안정적인 이미지 선택
```

영상화를 위해 매번 모든 변형 이미지를 사용할 필요는 없다.

---

# 13. 영상 생성

기본 파이프라인:

```text
Anchor Image
→ Higgsfield Image-to-Video
→ 3~5초 영상
```

영상 생성에서 지시할 내용:

- 행동
- 시선
- 표정 변화
- 손 움직임
- 카메라 움직임
- 속도

영상 AI에게 얼굴 자체를 다시 디자인하게 하지 않는다.

---

# 14. Higgsfield / Kling 선택 기준

## Higgsfield 우선

- 실사 사람
- 다문화 가족 상황극
- 기능소개 영상
- 말하는 장면
- 자연스러운 사람 움직임
- 립싱크

## Kling 우선 또는 대체

- 이모티콘
- 3D 캐릭터
- 스타일화된 캐릭터
- 특정 모션 결과가 Higgsfield보다 나을 때

---

# 15. 영상 생성 실패 처리

다음 문제가 있으면 해당 컷만 재생성한다.

```text
얼굴 변화
손가락 오류
입 주변 깨짐
의상 변화
인물 추가 생성
배경 왜곡
카메라 과도한 움직임
```

자동화 시 권장:

```text
최대 재시도 2회
```

완료된 컷은 다시 생성하지 않는다.

---

# 16. 음성 생성

캐릭터마다 고정된 목소리를 사용한다.

예:

```text
wife_voice_01
husband_voice_01
grandmother_voice_01
child_voice_01
```

한 번 정한 목소리는 시리즈 전체에서 유지한다.

---

# 17. 립싱크

기본 방식:

```text
완성된 짧은 영상
+
캐릭터 대사 음성
→ Higgsfield Lipsync
```

권장:

- 정면 또는 3/4 얼굴
- 입이 잘 보이게
- 대사 2~4초
- 손/컵 등으로 입 가리지 않기
- 큰 카메라 움직임 피하기

립싱크는 영상 생성과 분리해 처리하는 것이 수정하기 쉽다.

---

# 18. TOMATOK UI 합성

토마톡의 핵심 기능을 보여주는 컷에서는 **실제 UI**를 사용한다.

예:

- 가족 단톡방
- 실시간 번역
- 번역 전/후 메시지
- 사진 전송
- 음성 메시지
- 각 언어별 표시

권장:

```text
AI 이미지 안에서 fake UI 생성 X
실제 화면 또는 Figma UI를 후합성 O
```

---

# 19. 브랜드 로고 처리

TOMATOK 로고는 AI가 새로 해석하지 않도록 실제 PNG를 사용한다.

권장 위치:

- 명찰
- 모자
- 행사 부스
- 태블릿 스탠드
- 안내판
- 엔드카드

주의:

- 모든 컷에 큰 로고 반복 금지
- 자연스러운 브랜드 노출
- 로고 형태/색상 변형 금지

---

# 20. 최종 편집

편집 단계에서 다음을 적용한다.

```text
컷 연결
대사 음성 싱크
립싱크 영상 배치
실제 UI 합성
자막
효과음
BGM
브랜드 컬러 포인트
CTA
```

---

# 21. Reels 권장 포맷

```text
Aspect Ratio: 9:16
Resolution: 1080 × 1920
Length: 15~30 sec
```

자막과 중요한 UI는 상하단 UI 영역을 피해 Safe Area 안에 배치한다.

---

# 22. 폴더 구조

```text
TOMATOK_SHORTS/
│
├── characters/
│   ├── wife/
│   ├── husband/
│   ├── grandmother/
│   └── child/
│
├── brand/
│   ├── tomatok_logo.png
│   ├── ui/
│   ├── fonts/
│   └── colors.md
│
├── bible/
│   ├── character_bible.md
│   ├── visual_bible.md
│   ├── voice_bible.md
│   └── generation_rules.md
│
├── templates/
│   ├── info_template.md
│   ├── empathy_sitcom_template.md
│   └── feature_template.md
│
├── episodes/
│   └── EP001_family_chat/
│       ├── script.md
│       ├── scenes.json
│       ├── images/
│       ├── raw_video/
│       ├── audio/
│       ├── lipsync/
│       ├── ui_composite/
│       └── final/
│
└── README.md
```

---

# 23. Cursor 자동화 기본 순서

```text
1. scenes.json 읽기
2. pending 장면 검색
3. 캐릭터 reference 확인
4. 앵커 이미지 확인
5. 없으면 이미지 생성
6. Higgsfield 영상 생성
7. 결과 저장
8. TTS 음성 생성
9. 대사가 있으면 립싱크 생성
10. status 업데이트
11. 다음 scene 실행
12. 전체 완료 후 편집 단계로 전달
```

---

# 24. Cursor 자동 실행 규칙 예시

```text
EP 폴더의 scenes.json을 읽는다.

각 scene에 대해:

- 완료된 작업은 건너뛴다.
- reference_character는 항상 지정된 파일을 사용한다.
- 캐릭터의 얼굴, 헤어, 나이, 체형을 변경하지 않는다.
- 기본 포맷은 9:16이다.
- 한 영상은 3~5초를 기본으로 한다.
- 영상 생성은 Higgsfield를 기본 엔진으로 사용한다.
- 실패 시 동일 scene만 최대 2회 재시도한다.
- 대사가 있으면 캐릭터별 고정 음성을 생성한다.
- 생성된 음성을 이용해 lipsync를 실행한다.
- 모든 결과물을 scene_id 기반 이름으로 저장한다.
- 각 단계 완료 후 scenes.json status를 업데이트한다.
```

---

# 25. 파일명 규칙

```text
EP001_SC01_anchor.png
EP001_SC01_video_v01.mp4
EP001_SC01_voice.wav
EP001_SC01_lipsync_v01.mp4
EP001_SC01_ui.mp4
EP001_SC01_final.mp4
```

캐릭터:

```text
CHAR_WIFE_front.png
CHAR_WIFE_threequarter.png
CHAR_WIFE_fullbody.png
```

---

# 26. 검수 체크리스트

## 캐릭터

- [ ] 같은 인물처럼 보이는가
- [ ] 헤어가 유지되는가
- [ ] 의상이 의도 없이 변하지 않았는가
- [ ] 나이대가 유지되는가

## 영상

- [ ] 얼굴 변형이 없는가
- [ ] 손가락 이상이 없는가
- [ ] 인물이 추가/복제되지 않았는가
- [ ] 카메라 무빙이 과하지 않은가

## 립싱크

- [ ] 입모양이 음성과 맞는가
- [ ] 치아/입 주변이 깨지지 않았는가
- [ ] 발화 시작과 종료가 자연스러운가

## TOMATOK

- [ ] 로고가 실제 로고와 동일한가
- [ ] 실제 UI를 사용했는가
- [ ] 번역 문장이 정확한가
- [ ] 기능 표현이 실제 서비스와 맞는가

## SNS

- [ ] 첫 2~3초에 Hook이 있는가
- [ ] 자막 가독성이 좋은가
- [ ] 9:16 Safe Area를 지켰는가
- [ ] 15~30초 내로 정리되었는가
- [ ] 마지막 CTA가 있는가

---

# 27. 운영 원칙

처음부터 모든 단계를 완전 자동화하지 않는다.

## 1단계

```text
캐릭터 확정
→ 이미지 생성
→ 영상 생성
→ 립싱크
```

여기까지 먼저 안정화한다.

## 2단계

```text
UI 자동 합성
→ 자막 자동 생성
→ 오디오 믹싱
→ 자동 렌더링
```

추가한다.

## 3단계

```text
에피소드 기획
→ 생성
→ 편집
→ 출력
```

전체 자동화를 진행한다.

---

# 28. 현재 프로젝트 권장 최종 조합

```text
GPT / ImageGen
    ↓
캐릭터 + 콘티 + 앵커 이미지
    ↓
Cursor
    ↓
Higgsfield
    ↓
영상 + 립싱크
    ↓
실제 TOMATOK UI 합성
    ↓
Premiere / CapCut / AE
    ↓
Instagram Reels
```

### 기본 원칙

- 실사 인물: GPT → Higgsfield
- 이모티콘/캐릭터: Kling 단일 파이프라인도 고려
- 동일 인물 유지: 같은 reference asset 반복 사용
- 실제 서비스 UI: 반드시 후합성
- 로고: 실제 PNG 사용
- 시리즈 제작: Character Bible + scenes.json 중심으로 관리

---

# NEXT STEP

다음 작업은 아래 순서로 진행한다.

```text
1. 고정 등장인물 구성 확정
2. 각 등장인물 Character Bible 작성
3. 얼굴 후보 이미지 생성
4. 최종 얼굴 선택
5. 캐릭터 시트 제작
6. EP001 기능소개 콘티 제작
7. Cursor 자동화 파일 세팅
8. Higgsfield 테스트 생성
```


---

# SkillKit 연동
이 파이프라인은 `TOMATOK_SNS_AI_VIDEO_SKILLKIT`의 다음 문서를 공통 규칙으로 사용한다.

- `MASTER_SKILL.md`
- `bible/brand_bible.md`
- `bible/character_bible.md`
- `bible/environment_bible.md`
- `bible/visual_bible.md`
- `bible/voice_bible.md`
- `skills/01_character_generation.md` ~ `10_quality_check.md`
- `templates/prompt_master.md`
- `templates/episode_template.json`
- `templates/scene_template.json`
