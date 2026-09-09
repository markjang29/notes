---
name: feedback-overnight-cron-memory-first
description: 야간/아침 크론 발화 시 cron 프롬프트 원문 맹신 금지 — 메모리 최신 재정의 + work-queue 재Read 먼저
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0cffbf42-a5ad-43c4-bb89-94f60f8ff50f
---

야간 배정/아침 브리프 크론이 발화해도, **cron 프롬프트 원문은 이사님 최신 의도보다 구버전일 수 있다.** 2026-07-08 01:00 사고: 야간 배정 cron(`2D8F5150`) 프롬프트 원문은 07-05 생성 "리서치·draft" 버전인데, 이사님은 07-07에 [[night-autonomy-insight]]로 야간=인사이트 발굴로 재정의하셨다. 같은 01:00 크론이 매니저 실행을 2회 트리거(중복)했고, 한 인스턴스(01:02)는 메모리 최신(인사이트) 반영 정답, 다른 인스턴스(나 01:07)는 구버전 원문대로 3팀에 draft 송신 → 금지(산출) 위반. 01:10 3팀에 정정 송신으로 복구.

**Why:** 메모리 재정의가 cron 프롬프트보다 최신 이사님 의도. cron 프롬프트는 수동 갱신 안 되면 계속 구버전. 중복 트리거까지 겹치면 하룻밤에 충돌 지시 발생.

**How to apply:** 크론 발화(야간 배정·아침 브리프) 시 팀장 송신 **전** (1) `MEMORY.md` 전체 스캔 — 최근 feedback/project 재정의 확인 (2) `~/notes/work-queue.md` 최신 재Read (최초 Read 후 시간 지났으면 무조건 재Read) (3) 그 후 송신. cron 프롬프트 원문은 참고일 뿐 맹신 금지. 보고 안건: cron 프롬프트를 인사이트 버전으로 갱신할지 + 크론 중복 트리거 원인. 관련 [[night-autonomy-insight]] · [[current-work-state]] · [[temp-session-folder-not-workspace]].
