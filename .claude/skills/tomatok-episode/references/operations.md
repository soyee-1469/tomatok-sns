# 현행 운영 명령어

저장소 루트에서 실행. 아래는 문법 예시이며 이번 문서 수정은 생성·최종본 교체 승인이 아니다. 대괄호 대신 실제 파일·확정 값을 넣는다. CLI가 PATH에 없으면 `/Users/ymy/project/ai-creative-studio/node_modules/.bin/higgsfield`를 사용한다. 버전별 플래그는 `--help`로 확인한다.

## 계정·비용 (생성하지 않음)

```sh
higgsfield account status --json
higgsfield account transactions --size 100 --json
higgsfield generate cost nano_banana_pro --prompt "[확정 프롬프트]" --aspect_ratio 9:16 --resolution 2k --image-references "[참조.png]" --json
higgsfield generate cost kling3_0 --prompt "[확정 프롬프트]" --duration 3 --aspect_ratio 9:16 --mode std --sound on --start-image "[시작.png]" --json
```

3초는 조회 예시다. 실제 길이와 모든 참조·설정을 포함해 견적을 조회하고 승인 범위를 확인한다. 거래 내역의 후속 페이지는 응답의 커서를 사용한다.

## 승인 후 1회 생성·전사

```sh
python3 01_EPISODES/EP01R/tools/hf_gen.py "[새 출력 기본경로]" nano_banana_pro --prompt "[확정 프롬프트]" --aspect_ratio 9:16 --resolution 2k --image-references "[참조.png]"
python3 01_EPISODES/EP01R/tools/hf_gen.py "[새 출력 기본경로]" kling3_0 --prompt "[확정 프롬프트]" --duration 3 --aspect_ratio 9:16 --mode std --sound on --start-image "[시작.png]"
python3 01_EPISODES/EP01/tools/transcribe.py "[결과.mp4]"
```

`hf_gen.py`는 출력 디렉터리를 만들지 않으므로 먼저 준비한다. 기존 출력과 겹치지 않는 이름을 사용한다. start_image 외 추가 설정은 실제 CLI 지원을 확인한다. 기본 대사 컷에 end_image를 추가하지 않는다. 전사 일치는 음성·연기 승인과 다르다.

## 보드·아웃트로·마무리

```sh
python3 tools/build_series_board.py
python3 tools/serve_series_board.py
python3 00_MASTER_ASSETS/08_OUTRO/render_outro.py
python3 01_EPISODES/EP01R/tools/finish.py "edit/[실제 조립 스크립트].py" "[새 태그]" --bgm-vol 0.08
```

finish.py는 EP01R 폴더로 이동한 뒤 조립한다. 입력 경로는 해당 회차 기준으로 확인한다. `--no-bgm`, `--no-template` 지원. 아웃트로와 finish는 로컬 산출물을 쓰므로 같은 이름의 승인본을 덮어쓰지 않도록 출력 경로를 먼저 확인한다. EP01·EP02 사본은 각 회차 파일을 사용한다.

## 승인된 최종본 교체

```sh
python3 01_EPISODES/EP01R/tools/finish.py "edit/[실제 조립 스크립트].py" "[새 태그]" --final --final-name "EP01R_[확정 제목]_FINAL.mp4"
```

`99_FINAL`은 에피소드당 한 파일. 현재 최종본과 같은 확정 파일명으로 교체하며 작업 버전은 edit/export에 보존한다. 최종본 이름 변경은 이전 파일과 README 참조 처리를 먼저 검토한다. `--final`은 실제 덮어쓰기를 수행하므로 최종 교체 승인 범위 안에서만 실행한다. `--open`은 GUI 실행이 필요한 경우에만 사용한다.

EP01R/tools/finish.py는 `--final`에 `--final-name`이 없으면 렌더 시작 전에 종료한다. EP01(구 캐스트)과 EP01R은 별도 작품이므로 구 EP01 최종 파일명을 EP01R 기본값으로 사용하지 않는다. 새 제목의 중복 생성 여부는 실행 전 최종본 목록과 대조한다.
