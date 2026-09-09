---
name: clear-recovery-map
description: /clear 가 지우는 것(in-session 대화) vs 남기는 것(디스크/git/akl0hdys 메모리/공유로그) 및 복구 루트
metadata:
  type: reference
---

2026-06-26 세션에서 사용자와 검증한 `/clear` 영속성 맵. **다음 /clear 후에도 아래 디스크/외부 자산은 그대로.**

**남음 (세션 외부)**
- `~/notes` (work-queue.md, onboarding.md, org-structure.md, decisions/, principles/ …) — 디스크 + git push. 세션과 무관.
- akl0hdys 복구 메모리 (이 디렉토리 전체, MEMORY.md 포함) — 고정 절대경로.
- cokacdir 그룹 공유 로그 + 스케줄 history — 세션 외부 보관.
- 프로젝트 repo 의 산출물 (rpg_game/autotrader `IDEATION.md` 등) — 디스크.
- cokacdir 시스템 프롬프트 — 매 세션 자동 주입 → 조직 구도(매니저+팀장2) 새 세션도 처음부터 앎.
- 팀장 봇들은 별도 세션 → 매니저 /clear 에 영향 없음. workspace 바인딩도 cokacdir이 기억.

**지워짐** — 오직 "이 스레드의 in-session 대화 기억" 한 가지.

**복구 루트 (3층)**
1. 시스템 프롬프트 자동 주입 → 조직·역할 자동 복원.
2. **복구入口 = 이 디렉토리의 [[current-work-state]] → `~/notes/work-queue.md` 우선 읽기.**
3. 팀장 workspace 바인딩은 cokacdir이 자동 복원.

**강제 게이트(2026-06-26 추가, ADR `decisions/2026-06-26-recovery-gate-hook.md`):** `~/.claude/settings.json` hooks가 매니저 봇(cwd `~/.cokacdir/workspace/*`) 새 세션마다 이 디렉토리의 `MEMORY.md`+`current-work-state.md`+`~/notes/work-queue.md`를 SessionStart로 **자동 주입**, 주입 전엔 UserPromptSubmit가 프롬프트 차단(fail-closed). 스크립트 `~/.claude/hooks/cokacdir-recovery-gate.sh`. 탈출구: `~/.claude/recovery-gate/DISABLE` 파일 또는 `disableAllHooks:true`. 팀장 봇은 cwd 가드로 no-op.

검증: 이 세션은 workspace `ltgqjhx1` 이지만 복구入口는 `akl0hdys` 경로(전 세션 workspace) — 즉 workspace ID 가 바뀌어도 akl0hdys 메모리가 안정 회복 닻. 관련 [[current-work-state]] · [[projects-and-collaboration]] · [[workspace-layout]].
