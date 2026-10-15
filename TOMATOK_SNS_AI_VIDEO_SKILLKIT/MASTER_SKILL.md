# TOMATOK SNS VIDEO MASTER SKILL

## 목표
토마톡 SNS 콘텐츠를 동일한 세계관과 제작 규칙으로 반복 생성한다.

콘텐츠 유형:
1. 정보공유형
2. 공감형 다문화 가족 시트콤
3. 기능소개형

## 우선순위
1. Brand Bible
2. Character Bible
3. Environment Bible
4. Visual Bible
5. Voice Bible
6. Episode Script
7. Scene Prompt

상위 규칙과 충돌하는 장면 지시는 무시하거나 수정한다.

## 파이프라인
기획 → 대본 → 컷 분할 → 캐릭터/장소 레퍼런스 확인 → 앵커 이미지 → 영상 → 음성 → 립싱크 → TOMATOK UI/로고 합성 → 편집 → 색보정 → 자막/사운드 → QC → 최종 출력

## 자동화 규칙
- 완료된 단계는 다시 생성하지 않는다.
- 동일 캐릭터는 동일 reference를 사용한다.
- 동일 장소는 동일 environment reference를 사용한다.
- scene 상태를 JSON에 기록한다.
- 실패 장면만 재시도한다.
- 재시도 시 바꿔도 되는 것은 `action/motion/camera intensity` 중심이며 캐릭터 정체성과 장소 구조는 바꾸지 않는다.
- 실제 TOMATOK 로고와 UI는 생성 모델이 임의로 다시 그리지 않게 한다.
