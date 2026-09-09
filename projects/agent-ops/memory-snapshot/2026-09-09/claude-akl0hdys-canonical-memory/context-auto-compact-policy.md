---
name: context-auto-compact-policy
description: 전 봇 컨텍스트 자동 압축 기본 — 새 세션 권장 금지 (이사님 09-02 확정)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6f2d649c-3598-4170-88fd-57842b5cea87
  modified: 2026-09-02T01:32:24.614Z
---

이사님 2026-09-02 확정: **모든 봇은 컨텍스트 자동 압축으로 이어간다.** 컨텍스트 이유로
"새 세션 권장"을 보고하지 않는다.

**Why:** claude는 `~/.claude/settings.json` env(CLAUDE_CODE_AUTO_COMPACT_WINDOW=300000,
CONTEXT_LIMIT_TOKENS=1000000)이 전 기동에 상속되어 자동 압축이 이미 켜져 있고, zcode도
CLI 자체 압축이 있어 세션 수동 교체가 불필요하다는 것을 이사님이 확인 후 방침화.

**How to apply:** 컨텍스트 % 보고는 계속하되(요청 시) 새 세션 권장 문구 금지. 압축 직후
몇 턴은 요약 기반이므로 정밀 작업 전 디테일만 재확인. 관련 [[session-hygiene-per-task]]
(작업 단위 /clear 위생은 유지 — 이것은 맥락 관리 방침과 별개).
