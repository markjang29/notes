---
title: ADR — 복구번들 L1/L2 계층화 + 한계값 단일화
date: 2026-07-01
status: accepted (이사님 승인 + 비관/낙관/codex 3중 리뷰 수렴)
project: 공통(서버 운영, recovery gate)
source: 야간/아침 cron 작업 미실행 원인 분석 → 복구번들 재설계
related:
  - decisions/2026-06-30-session-reaper.md
  - .reviews/recovery-redesign-pessimistic.md
  - .reviews/recovery-redesign-optimistic.md
  - .reviews/recovery-redesign-codex.md
tags:
  - adr
  - ops
  - recovery
  - cron
---

# ADR — 복구번들 L1/L2 계층화 + 한계값 단일화

## 상태
`accepted` — 2026-07-01 시행. gate.sh·health-check.sh 수정 + 백업 완료. 수동 검증 통과(.ok 생성 확인).

## 배경 — cron 작업이 안 돌던 원인
- 01:00 야간 cron, 07:00 아침 cron **둘 다 트리거는 됨** — 하지만 `recovery gate` hook에 막혀 실행 안 됨.
- 원인: 복구 번들(MEMORY.md + current-work-state.md + work-queue.md = 9298~10218B)이 커서, Claude Code가 SessionStart의 additionalContext를 preview로 대체 → SessionStart가 `.ok` 마커를 못 남김 → UserPromptSubmit 게이트가 매니저 프롬프트를 차단(fail-closed).
- 따라서 매니저가 팀장에게 작업 배정도, 아침 브리프도 못 함. **RPG 07 미완료의 진짜 원인 = 매니저 지시 자체 불가.**
- 핵심 인사이트(codex): 컨텍스트 **용량** 문제가 아니라 **fail-closed 구조** 문제. 번들이 크면 `.ok` 생성 조건이 묶여 전부 차단.

## 3중 리뷰 수렴점 (비관/낙관/codex)
- **비관(치명)**: "L2 = /clear 후 1회"인데 cron은 /clear가 아님 → 재설계안이 버그 재생산. 한계값 3곳 불일치(health 9000 / gate 20000). 계층화는 과잉 가능.
- **codex**: L1 bootstrap만 `.ok` 조건, work-queue는 L2 온디맨드. 한계 상향만은 응급처치. cron 전면 우회 말고 **L1 필수 + 실패 시 장애 보고**.
- **낙관**: L1 축소로 gate 통과 + git 단일진실원 + 팀장봇 재사용 패턴.

## 결정
1. **L1/L2 계층화** (`cokacdir-recovery-gate.sh`):
   - **L1(매 턴 자동 주입)** = MEMORY.md + current-work-state.md만. 약 3.4KB.
   - **L2(매니저 온디맨드 Read)** = work-queue.md. L1에 "**세션 시작 직후 읽을 것(/clear·cron·resume 무관)**" 의무 명시 → cron 매니저도 work-queue를 읽도록 보완 (비관 치명결함 해소).
   - `.ok` 생성 조건 = L1(MEMORY+state) 존재 + 크기 ≤ MAX_CONTEXT_BYTES(20000). work-queue 크기는 .ok와 무관.
2. **한계값 단일화**: `recovery-health-check.sh` MAX_BUNDLE 9000 → **20000** (gate 기본값과 일치).
3. **백업**: 수정 전 스크립트 `.bak-20260701` 보존.

## 검증
- 문법 검사(bash -n) OK.
- 수동 sessionstart: 주입 3443B, work-queue 제외 확인, L2 의무 포함, `.ok` 정상 생성.
- 다음 cron(01:00 KST) 실발화 시 최종 확인.

## 남은 과제 (fail-safe)
- gate 막힌 세션은 실행 자체 불가 → 매니저 장애 보고 불가. `recovery-health-check.sh`가 `.fail` 마커를 잡으면 이사님께 보고하는 라인 추가 예정(codex 권장).

## 정합성 메모 (토큰 vs 용량)
- 복구번들 2500~3000 토큰 = glm-5.2[1m] 1M의 **0.3%**. 다이어트/계층화의 목적은 **컨텍스트 용량 절약이 아니라 gate 작동 해제**. 컨텍스트 18~24%의 진짜 원인은 system prompt(CLAUDE.md/skills/cokacdir 참조) + 대화·tool 결과 누적. 본 ADR로 매 턴 주입은 10218B→3443B로 줄어들어 tool 결과 누적 억제에 기여.
