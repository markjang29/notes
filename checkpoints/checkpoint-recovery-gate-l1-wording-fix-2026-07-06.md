# recovery-gate L1 문구 명확화 — 2026-07-06

## 문제

시나리오 팀장이 recovery bootstrap의 아래 문구를 보고:

> 의무(L1): 아래 두 파일로 사칙(원칙) 상속·인증. 읽기 전 결정/발판 금지.

"아래 두 파일이 무엇인지 모르겠다"고 응답했다.

실제 bootstrap에는 곧이어 `BEGIN MEMORY.md`, `BEGIN current-work-state.md`가 나오므로 팀장이 읽고 판단했어야 하지만, 문구가 불필요하게 애매한 것도 사실이다.

## 조치

`/home/ubuntu/.claude/hooks/cokacdir-recovery-gate.sh` 문구를 다음처럼 수정했다.

- L1 대상 파일을 명시: `MEMORY.md + current-work-state.md`
- 정체확인 경로를 명시: `~/notes/onboarding.md` + `~/.cokacdir/bot_settings.json`

## 기대 효과

- 팀장이 "아래 두 파일이 뭔지 모른다"는 핑계를 줄임
- key/역할 불명확 시 확인 경로를 즉시 알 수 있음
- 사칙 인증 전 결정/발판 금지 규칙을 더 명확히 함

## 감사 판정

- 시나리오 팀장 답변: 주의~경고
- 시스템 문구: 개선 필요
- 조치: 운영 훅 문구 수정 완료

