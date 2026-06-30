# 온보딩 프롬프트 — Windows Claude 첫 세션에 그대로 복붙

> 셋업 스크립트(setup-wsl.sh / setup-windows.ps1) 실행이 끝난 뒤,
> Windows의 Claude Code **첫 세션**에 아래 프롬프트를 그대로 준다.
> Linux 서버의 onboarding.md 인증 절차를 Windows 경로로 옮긴 것.
> 사칙(원칙)은 git(notes repo)에 있으므로, 이 프롬프트 한 방으로
> Linux의 Claude와 같은 사칙 체계를 스스로 상속·검증한다.

---

```
온보딩한다. 코드/기획 작업 전에 아래를 순서대로 수행하고 인증하라.

1. 사칙 원본 읽기 (경로는 내 환경 기준 — WSL이면 ~/notes, Native면 %USERPROFILE%\notes):
   - notes/agent-rules.md            (어떻게 — 실행 절차·검증 루프·메모리·pull→push)
   - notes/principles/ai-dev-신념.md  (왜 — 판단 기준 · 부채 3종 · 의도 보존)
   - notes/personas/markjang29.md     (판단 대리 기준 · 완성 판정 · 정지 프로토콜)
   - notes/decisions/README.md + notes/decisions/ADR-template.md  (결정=ADR 의무)
   - notes/principles/context-budget.md  (토큰/컨텍스트 예산)
   - (프로젝트 작업 시) notes/project-rules/README.md 및 해당 repo 내 CLAUDE.md

2. 경로 인식: 이 문서의 /home/ubuntu/... 와 /akl0hdys 는 Linux 서버 기준이다.
   /akl0hdys 는 서버 전용 cokacdir workspace 포인터 — Windows엔 대응 경로 없음.
   내 작업 디렉토리는 notes 와 projects(autotrader / rpg_game) 의 Windows/WSL 경로다.

3. 읽은 직후, 아래 형식으로 온보딩 인증(자기선언):
   "원칙 체계 읽음 — [위 각 문서의 핵심을 1줄씩 인용]. 환경=Windows(WSL|Native)."
   핵심 인용이 없는 "읽었음"은 거부다 — 실제 읽었는지 인용으로 검증.

4. 인증 전에는 결정(ADR) · 코드 발판 · commit/push 금지.
   "스택 미확정 발판 금지" — 결정(ADR) 없이 코드 발판 안 친다.

5. 협업 규칙(Linux 봇과 동일): 작업 전 git pull, 작업 후 즉시 add/commit/push.
   결정·진행은 notes 에 기록(ADR은 decisions/, 진행은 work-queue). 충돌 시 사칙이 상위.
```

## 주의
- `/start <작업디렉토리>` 로 workspace를 먼저 여는 것은 Linux cokacdir 환경의 절차.
  Native Windows Claude는 터미널 직접 입력이므로, 작업 디렉토리에서 바로 `claude` 실행.
- 인증이 끝나면 Linux 서버 Claude와 **동일한 사칙** 으로 판단한다.
  이후 사칙 변경은 notes repo 의 pull/push 로 양쪽이 자동 동기화.
