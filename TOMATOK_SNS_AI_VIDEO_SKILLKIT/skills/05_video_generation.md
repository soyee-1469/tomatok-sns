# SKILL 05 — VIDEO GENERATION

## 목표
앵커 이미지의 디자인을 유지하면서 필요한 움직임만 생성한다.

## 입력
- anchor image
- character references
- environment reference
- action prompt
- camera motion prompt

## 기본값
- 9:16
- 3~5초
- natural speed

## AI가 유지해야 하는 것
- face identity
- hairstyle
- wardrobe
- body proportions
- environment geometry
- lighting direction

## AI가 생성해야 하는 것
- eye movement
- micro-expression
- hand gesture
- body movement
- subtle camera breathing

## 재시도 조건
- face morph
- extra fingers
- broken phone
- set geometry change
- unnatural motion

재시도 시 캐릭터/장소 프롬프트는 고정하고 motion 강도만 조절한다.
