---
name: memory-tick-impl
description: memory-tick 자동 메모리 시스템 구현 상태 (스킬/throttle/Stop hook + autoMemoryDirectory 보류)
metadata: 
  node_type: memory
  type: project
  originSessionId: a4db5139-18ce-4481-b67b-54f5b4d79eed
---

2026-06-26 memory-tick 자동 메모리 시스템 **부분 구현** (Codex 검증 2회 수용, GO).

- ✅ 스킬 `~/.claude/skills/memory-tick/` (SKILL.md + stop-hook-throttle.sh). Stop hook을 `~/.claude/settings.json`에 등록(matcher 제거 — Stop은 matcher 무시). throttle=5분 간격, 실패해도 `exit 0`.
- ⏸ **`autoMemoryDirectory`(Obsidian `~/notes/memory` 일원화)는 보류** — Codex 검증 결과 키 작동 미검증 + 기존 메모리(`~/.claude/projects/.../memory/`) 충돌 리스크로 안전상 보류. 빌트인 자율 메모리는 기존 경로에서 작동 유지.
- 비표준 `~/.claude/settings.local.json`(홈)은 제거 — 사용자 범위는 `~/.claude/settings.json`이 표준.
- **실제 Stop 발화 검증은 다음 세션 stop 이벤트에서** 필요 (이 세션에선 설정·스크립트 정합성만 검증).

관련 [[ai-dev-principles-system]].
