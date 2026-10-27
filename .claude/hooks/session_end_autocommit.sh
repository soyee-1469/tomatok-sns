#!/bin/bash
# 세션 종료 시 문서 파일만 자동 커밋 + 푸시.
# 이미지는 .gitignore로 제외되고, 영상/압축/PDF 같은 대용량 바이너리는 여기서 아예 add하지 않는다.
set -u
root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
cd "$root" || exit 0
# 1) 이미 추적 중인 파일의 수정/삭제는 모두 스테이징 (추적 파일은 전부 문서)
git add -u 2>/dev/null
# 2) 새 파일은 문서 확장자만 스테이징
git ls-files -z -o --exclude-standard \
  | grep -zE '\.(md|json|txt|html|css|js|csv|tsv|ya?ml)$|(^|/)\.gitignore$' \
  | xargs -0 git add -- 2>/dev/null
git update-index -q --refresh
if git diff --cached --quiet; then
  exit 0
fi
msg="auto: session end $(date '+%Y-%m-%d %H:%M')"
git commit -q -m "$msg" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" || exit 0
git push -q origin HEAD 2>/dev/null || true
exit 0
