# PROJECT WORKFLOW

GitHub가 기준 저장소다. Grokbot과 Cursor는 같은 규칙으로 이어서 작업한다.

## 작업 시작

1. `git pull`
2. `PROJECT_WORKFLOW.md`를 읽는다.
3. 해당 콘텐츠의 `status.json`을 읽는다.
4. `nextTask`부터 작업한다.

## 작업 규칙

- 완료된 작업은 다시 생성하지 않는다.
- 기존 APPROVED 파일은 사용자 요청 없이는 수정하지 않는다.
- 파일을 생성하거나 수정한 뒤 `status.json`을 즉시 갱신한다.
- AI가 중단되어도 다른 AI가 `status.json`과 Git 기록만 보고 이어갈 수 있어야 한다.
- 이미지와 영상 원본의 파일명을 임의로 바꾸지 않는다.
- 기존 파일을 삭제하지 않는다.
- 불확실한 경우 덮어쓰지 말고 새 버전을 만든다.
- 이미지는 이 아이맥에만 둔다. GitHub에는 문서와 코드만 올린다.

## 상태값

아래 중 하나만 사용한다.

```text
IDEA
SCRIPT_DRAFT
DIALOGUE_REVIEW
SCRIPT_APPROVED
STORYBOARDING
STORYBOARD_APPROVED
IMAGE_GENERATION
IMAGE_APPROVED
AUDIO_COMPLETE
VIDEO_GENERATION
EDITING
REVIEW
SCHEDULED
FINAL
PUBLISHED
HOLD
```

## status.json 필수 항목

```text
id
type
title
status
lastCompleted
nextTask
publishDate
platforms
updatedBy
updatedAt
assets
```

`updatedAt`은 갱신 시각이다. `updatedBy`는 작업한 에이전트 이름이다.

## 에피소드 위치

제작 이어받기는 `01_EPISODES/EP01/`를 본다. `01_EPISODES/EP001_FAMILY_GROUP_CHAT/`은 이전 초안이며 삭제하거나 덮어쓰지 않는다.

## 커밋 메시지

```text
EP01: script approved
EP01: storyboard complete
EP01: ST01 generated
EP01: stills approved
EP01: video generated
EP01: final export
INFO001: draft created
FEATURE001: scheduled
```

## 작업 완료

1. 결과 파일을 저장한다.
2. `status.json`을 갱신한다.
3. `git add`
4. `git commit`
5. `git push`

## 미디어

2026-10-15 기준 저장소는 약 352KB이고 이미지·영상 바이너리가 없다. Git LFS는 필요하지 않다. 이미지 결과물은 `.gitignore`로 제외하고 아이맥에만 둔다. 대용량 영상 파일을 올리게 되면 삭제하지 말고 LFS 필요 여부만 먼저 보고한다.
