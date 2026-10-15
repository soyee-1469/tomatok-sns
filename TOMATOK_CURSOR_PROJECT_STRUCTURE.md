# TOMATOK COMMUNITY SITCOM — 프로젝트 구조 및 Cursor 작업 지시서

## 목적
TOMATOK 생활형 PPL 시트콤을 반복 제작하기 위한 프로젝트 구조를 만든다.

핵심 관리 단위는 다음 3단계다.

**MASTER ASSETS → EPISODE → CUT**

- `MASTER ASSETS`: 여러 에피소드에서 반복 사용하는 공통 자산
- `EPISODE`: 한 편의 기획/대본/콘티/제작물
- `CUT`: 실제 이미지/영상 생성의 최소 단위

## 1. 최상위 폴더 구조

```text
TOMATOK_CONTENT/
├── 00_MASTER_ASSETS/
├── 01_EPISODES/
├── 02_CONTENT_PLANNING/
├── 03_PUBLISHING/
└── 99_ARCHIVE/
```

## 2. 공통 MASTER ASSETS

```text
00_MASTER_ASSETS/
├── 01_CHARACTERS/
│   ├── FEMALE_LEAD_01/
│   │   ├── FACE_FRONT.png
│   │   ├── FACE_45_LEFT.png
│   │   ├── FACE_45_RIGHT.png
│   │   ├── FACE_SIDE.png
│   │   ├── UPPER_BODY.png
│   │   ├── FULL_BODY.png
│   │   ├── EXP_NEUTRAL.png
│   │   ├── EXP_SMILE.png
│   │   ├── EXP_CONFUSED.png
│   │   ├── EXP_SURPRISED.png
│   │   └── character_bible.md
│   ├── MALE_LEAD_01/
│   │   └── 동일 구조
│   ├── UNIVERSITY_FRIEND_01/
│   └── KPOP_FAN_01/
├── 02_LOCATIONS/
│   ├── CAFE_A/
│   │   ├── MASTER_WIDE.png
│   │   ├── ANGLE_FRONT.png
│   │   ├── ANGLE_LEFT_45.png
│   │   ├── ANGLE_RIGHT_45.png
│   │   ├── TABLE_TWO_SHOT.png
│   │   └── location_bible.md
│   ├── HOME_A/
│   ├── CAMPUS_CAFE_A/
│   ├── UNIVERSITY_CLASSROOM_A/
│   └── FAN_CAFE_A/
├── 03_PROPS/
│   ├── PHONE_MALE/
│   ├── PHONE_FEMALE/
│   ├── WEDDING_ITEMS/
│   └── DAILY_PROPS/
├── 04_UI/
│   ├── TOMATOK_FAMILY_ROOM_KR/
│   ├── TOMATOK_FAMILY_ROOM_VN/
│   ├── TOMATOK_TRANSLATION/
│   ├── TOMATOK_GROUP_CHAT/
│   ├── TOMATOK_PHOTO_SHARE/
│   └── UI_RULE.md
└── 05_STYLE/
    ├── visual_bible.md
    ├── camera_rule.md
    ├── lighting_rule.md
    ├── color_rule.md
    ├── sitcom_performance_rule.md
    └── ppl_rule.md
```

## 3. 에피소드 폴더 구조

```text
01_EPISODES/
EP001_FAMILY_GROUP_CHAT/
├── 00_BRIEF/
│   └── EP001_brief.md
├── 01_SCRIPT/
│   ├── EP001_script_v01.md
│   ├── EP001_script_v02.md
│   └── EP001_script_final.md
├── 02_STORYBOARD/
│   ├── EP001_storyboard_v01.md
│   ├── EP001_storyboard_final.md
│   └── storyboard_images/
├── 03_SHOTLIST/
│   └── EP001_shotlist.md
├── 04_IMAGES/
│   ├── drafts/
│   ├── approved/
│   └── rejected/
├── 05_UI_ASSETS/
├── 06_AUDIO/
│   ├── dialogue/
│   ├── sfx/
│   └── bgm/
├── 07_VIDEO/
│   ├── generations/
│   └── approved/
├── 08_EDIT/
└── 09_FINAL/
    ├── instagram/
    ├── youtube/
    └── archive/
```

## 4. 캐릭터 바이블 템플릿

```md
# CHARACTER BIBLE

CHARACTER_ID: FEMALE_LEAD_01

## 기본 정보
- 국적: 베트남
- 연령대 인상:
- 한국어 수준: 일상 대화 가능하지만 아직 서툼
- 성격: 차분함, 현실적, 은근히 장난기 있음
- 역할: 한국 남성과 결혼을 준비 중인 여성

## 외형 고정
- 얼굴형:
- 눈:
- 코:
- 입:
- 눈썹:
- 피부톤:
- 헤어 길이:
- 헤어 컬러:
- 체형:
- 키 비율:

## 기본 의상
- 상의:
- 하의:
- 신발:
- 액세서리:

## 기본 표정
- Neutral
- Smile
- Confused
- Surprised
- Slightly embarrassed

## 말투
- 한국어 문장은 짧게
- 어려운 단어는 잘 사용하지 않음
- 과장된 외국인 말투 금지
- 자연스러운 생활 회화

## 절대 변경 금지
- 얼굴 비율
- 눈 간격
- 코 모양
- 헤어 길이
- 전체 체형
- 나이 인상
```

## 5. 장소 바이블 템플릿

```md
# LOCATION BIBLE

LOCATION_ID: CAFE_A

## 용도
커플 에피소드의 반복 등장 카페.

## 공간 고정
- 2인용 테이블 위치
- 창문 위치
- 출입구 위치
- 벽 재질
- 조명 위치
- 의자 형태
- 테이블 재질
- 배경 소품

## 색감
- warm cream
- beige
- light wood
- muted neutral

## 조명
- 부드러운 낮 자연광
- 따뜻한 실내 조명
- 얼굴이 선명하게 보이도록
- 과도한 역광 금지

## 카메라 기준
- MASTER: eye-level 35mm
- DIALOGUE: 50mm medium
- REACTION: 70–85mm
- PHONE INSERT: 50–70mm

## 생성해야 할 기준 이미지
- MASTER_WIDE
- ANGLE_FRONT
- ANGLE_LEFT_45
- ANGLE_RIGHT_45
- TABLE_TWO_SHOT
```

## 6. EP001 BRIEF 템플릿

```md
# EP001 BRIEF

EPISODE_ID: EP001
TITLE: 결혼 전에 가족 단톡방 초대하기

## 한 줄 요약
결혼 전에 서로 가족들과 가까워지기 위해 가족 단톡방에 초대하지만,
남자는 여자친구 가족방의 엄청난 인원수와 쏟아지는 인사에 압도당한다.

## 등장인물
- FEMALE_LEAD_01
- MALE_LEAD_01

## 장소
- CAFE_A

## 러닝타임
20–25초

## 핵심 웃음 포인트
1. 남자 가족방은 6명
2. 여자 가족방은 약 38명
3. 새 이모가 계속 들어옴
4. 마지막 “몇 번째 이모야?”

## TOMATOK PPL
- 남주 화면: 베트남어 원문 + 한국어 번역
- 여주 화면: 한국 가족의 한국어 메시지 + 베트남어 번역
- 기능 설명 자막 없음
- UI는 1~3초 정도 자연스럽게 노출

## 브랜드 원칙
토마톡이 문제를 해결하는 광고 구조가 아니라,
등장인물이 원래부터 사용하는 메신저처럼 보이게 한다.
```

## 7. EP001 SCRIPT 템플릿

```md
# EP001 SCRIPT

## CUT 01
여주: “결혼 전에 우리 가족들이랑 좀 친해지면 좋겠다.”
남주: “좋지. 서로 가족방에 초대할까?”
여주: “좋아.”

## CUT 02
남주: “우리 집은 엄마, 아빠, 동생… 나까지 여섯 명.”
여주: “귀엽네.”
남주: “귀여워?”
여주: “응. 작아서.”

## CUT 03
여주: “자, 이제 우리 가족방.”
남주: “…잠깐.”
여주: “왜?”
남주: “이게 가족방이야?”
여주: “응.”

## CUT 04
남주: “몇 명인데?”
여주: “지금 38명.”
남주: “…지금?”

## CUT 05
남주: “메시지가 다 베트남어야…”
여주: “한국어로 같이 뜨잖아.”
남주: “인사하는 데 하루 걸리겠는데?”

## CUT 06
띵— 새 참여자 알림

남주: “또 들어왔는데?”
여주: “우리 이모.”
남주: “…몇 번째 이모야?”

END
```

## 8. STORYBOARD 템플릿

```md
# EP001 STORYBOARD

## CUT 01
CHARACTERS:
- FEMALE_LEAD_01
- MALE_LEAD_01

LOCATION:
- CAFE_A

SHOT:
- MASTER TWO SHOT
- eye-level
- 35mm

ACTION:
카페에서 결혼 준비 이야기를 하던 중
여주가 서로 가족방에 초대하자고 제안한다.

DIALOGUE:
여주: “결혼 전에 우리 가족들이랑 좀 친해지면 좋겠다.”
남주: “좋지. 서로 가족방에 초대할까?”

EMOTION:
편안함 / 자연스러운 연인 관계

ESTIMATED_DURATION:
3.5 sec

LIPSYNC:
YES

REQUIRED_ASSETS:
- FEMALE_LEAD_01
- MALE_LEAD_01
- CAFE_A
```

## 9. SHOTLIST 템플릿

```md
# EP001 SHOTLIST

| CUT ID | Shot | Character | Location | UI | Status |
|---|---|---|---|---|---|
| EP001_CUT01 | MASTER TWO SHOT | F/M | CAFE_A | - | TODO |
| EP001_CUT02 | MALE MEDIUM | M | CAFE_A | KR FAMILY ROOM | TODO |
| EP001_CUT03 | TWO SHOT | F/M | CAFE_A | - | TODO |
| EP001_CUT04 | MALE REACTION | M | CAFE_A | VN FAMILY ROOM | TODO |
| EP001_CUT05 | PHONE INSERT | M | CAFE_A | VN→KR TRANSLATION | TODO |
| EP001_CUT06 | PHONE INSERT | F | CAFE_A | KR→VN TRANSLATION | TODO |
| EP001_CUT07 | TWO SHOT END | F/M | CAFE_A | JOIN ALERT | TODO |
```

상태값:

```text
TODO
GENERATING
REVIEW
APPROVED
REJECTED
FINAL
```

## 10. 파일명 규칙

### 이미지
```text
EP001_CUT01_MASTER_CAFE.png
EP001_CUT02_MALE_FAMILY_CHAT.png
EP001_CUT03_FEMALE_INVITE.png
EP001_CUT04_MALE_REACTION_38.png
EP001_CUT05_PHONE_VIET_KOR.png
EP001_CUT06_PHONE_KOR_VIET.png
EP001_CUT07_END_AUNT.png
```

### 영상
```text
EP001_CUT01_VIDEO_v01.mp4
EP001_CUT01_VIDEO_v02.mp4
EP001_CUT01_VIDEO_FINAL.mp4
```

### 음성
```text
EP001_CUT01_FEMALE_001.wav
EP001_CUT01_MALE_001.wav
```

### 최종
```text
EP001_INSTAGRAM_REELS_FINAL.mp4
EP001_YOUTUBE_SHORTS_FINAL.mp4
```

## 11. 공통 자산과 에피소드 자산 구분

### 공통 MASTER에 보관
- 얼굴
- 헤어
- 체형
- 캐릭터 기본 의상
- 반복 장소
- 반복 소품
- 휴대폰 디자인
- TOMATOK UI 스타일
- 카메라 규칙
- 조명 규칙
- 색감 규칙
- 연기 톤

### EPISODE에 보관
- 해당 편 대사
- 해당 편 콘티
- 해당 편 컷리스트
- 해당 편 전용 소품
- 생성 이미지
- 음성
- 영상
- 편집본
- 최종본

## 12. 버전 관리

```text
EP001_script_v01.md
EP001_script_v02.md
EP001_script_final.md

EP001_storyboard_v01.md
EP001_storyboard_v02.md
EP001_storyboard_final.md
```

최종 승인된 파일만 `final` 사용.

## 13. 제작 상태 관리

```text
IDEA
SCRIPTING
SCRIPT_APPROVED
STORYBOARDING
STORYBOARD_APPROVED
IMAGE_GENERATION
IMAGE_APPROVED
AUDIO_COMPLETE
VIDEO_GENERATION
EDITING
FINAL
PUBLISHED
HOLD
```

## 14. Cursor 실행 요청

Cursor는 다음 작업을 수행한다.

1. 위 폴더 구조를 실제 프로젝트에 생성한다.
2. 각 폴더에 README 또는 필요한 md 템플릿을 생성한다.
3. `EP001_FAMILY_GROUP_CHAT` 폴더를 먼저 생성한다.
4. 위 EP001 BRIEF / SCRIPT / STORYBOARD / SHOTLIST 내용을 각각 파일로 저장한다.
5. 모든 파일명은 위 naming rule을 따른다.
6. 공통 자산은 EP 폴더에 복제하지 말고 `00_MASTER_ASSETS`를 참조한다.
7. 생성물 상태를 SHOTLIST에서 계속 업데이트할 수 있게 한다.
8. 추후 EP002부터는 EP001 구조를 복제해서 사용한다.

## 15. 핵심 원칙

```text
MASTER ASSETS
    ↓
EPISODE
    ↓
CUT
    ↓
IMAGE / AUDIO / VIDEO
    ↓
FINAL
```

캐릭터와 장소를 매 에피소드마다 새로 만들지 않는다.

**공통 캐릭터 + 공통 장소 + 에피소드별 대본/콘티** 구조를 유지한다.

이 구조를 기준으로 이후 AI 이미지 생성, 영상 생성, 음성, UI 합성, 편집 자동화를 연결한다.
