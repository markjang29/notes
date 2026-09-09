---
name: codex-communication-policy
description: codex 통신 정책 — 평소 매니저 직접, 이사님이 물어볼 때만 codex 통신, 매니저 세션 보호
metadata:
  type: feedback
---

이사님 2026-07-04 요구: "메니저 세션 크게 증가 안하는 방향으로, 내가 코덱스 의견 물어볼 때 통신은 하도록 해."

**정책:**
- **평소**: 매니저 직접 처리. codex 통신 X → 매니저 세션 보호.
- **이사님이 codex 의견 물어볼 때만**: `codex exec` 동기 직접 호출. 결과는 파일(`--write OUTFILE`)로 받고, 메인엔 **결론 요약만** 발췌.
- **companion `task --background` 사용 중지** — 회수 불안정(job registry 증발, 2026-07-04 2회 연속 확인). 근본 원인: `codex:codex-rescue` 에이전트 경로가 companion job 등록 누락 + 백그라운드 job 종료 시 로그까지 cleanup.

**Why:** 매니저 세션 컨텍스트 폭발(1M)이 최대 위험. codex 백그라운드 진단은 매니저 세션을 쓰면서 회수도 불안정 → 이중 손해. 동기 직접 호출 + 파일 회수가 안전.

**How to apply:**
- 이사님이 "codex 의견 들어볼까" 등 명시 시 → `codex exec --write ~/notes/.tool-results/codex-<TS>.md "프롬프트"`, 결과 파일에서 결론만 발췌 보고.
- 자발적 codex 사용 금지. 매니저 직접 처리가 기본.
- codex CLI 자체는 정상(gpt-5.5, 2026-07-04 ping 확인). 문제는 companion 백그라운드 관리 경로만.

관련 [[codex-sandbox-fix]] · [[context-explosion-causes]] · [[session-hygiene-per-task]] · [[glm-proxy-environment]].
