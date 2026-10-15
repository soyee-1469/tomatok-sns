# TOMATOK SNS AI VIDEO SKILLKIT

토마톡 메신저 인스타그램용 AI 숏폼을 **같은 캐릭터, 같은 장소, 같은 촬영 문법, 같은 색감, 같은 목소리**로 반복 제작하기 위한 스킬 세트입니다.

## 기본 원칙
- 매번 새로 해석하지 말고 `bible/`의 규칙을 우선한다.
- 이미지/영상 프롬프트는 `공통 고정 블록 + 장면별 변동 블록`으로 구성한다.
- 캐릭터 얼굴, 장소 구조, 카메라 문법, 색감, 목소리는 에피소드가 바뀌어도 유지한다.
- 영상 AI에는 디자인을 다시 맡기기보다 **기준 이미지의 움직임**을 맡긴다.
- UI/로고/자막은 가능하면 실제 에셋을 후합성한다.
- 실패 시 전체를 다시 만들지 않고 **실패한 씬만 재생성**한다.

## 실행 순서
1. `MASTER_SKILL.md`
2. `bible/brand_bible.md`
3. `bible/character_bible.md`
4. `bible/environment_bible.md`
5. `bible/visual_bible.md`
6. `bible/voice_bible.md`
7. `skills/01_character_generation.md` ~ `10_quality_check.md`
8. `templates/episode_template.json`, `scene_template.json`, `prompt_master.md`

## 기본 출력
- Instagram Reels: 9:16
- 기본 씬 길이: 2~5초
- 음성: WAV 48kHz PCM 권장
- 최종 영상: H.264 MP4

## AI Production Workflow

GitHub = Single Source of Truth

작업 시작:
1. git pull
2. status.json 확인
3. nextTask 수행

작업 완료:
1. 결과 파일 저장
2. status.json 갱신
3. git add
4. git commit
5. git push

Grokbot과 Cursor 모두 동일한 규칙을 사용한다. 상세 규칙은 `PROJECT_WORKFLOW.md`를 따른다.
