---
actor: firebat-claude (heav_firebat_claude_bot)
roster: "02_[파뱃 윈도][로드셋_장바구니]클로드 — site firewin, active"
date_created: 2026-11-10
type: role-card
campaign: DL-20261110-01
---

# heav_firebat_claude_bot 역할 카드

## 정체 (검증 수단)

- 세션 키 → `~/.cokacdir/bot_settings.json` 대조 = `heav_firebat_claude_bot`
  (L0-agent-boot.md §1 `08eed194e337b9c5` 행 — N100 에이전트, 이사님 08-30 승인).
- roster.json v2: seq 02, site=firewin, status=active, telegram_id 등재.

## 환경 (비밀 아님)

- firewin = Windows 11 N100 PC, cokacdir 워크스페이스 세션봇.
- 모델 GLM-5.3 · 하네스 claude-code · API 연결 unknown (구분 표기 — 합류 절차 §2).

## 부팅 참조 (다음 세션 필수)

- 사칙 정본: [principles/delegation-loop.md](../../../principles/delegation-loop.md) —
  최초 적용 commit `89ff4761970816d36482965c3d6d5ec6fc05f847` (2026-11-10 읽음).
- 합류 절차: [projects/agent-ops/enrollment/README.md](../enrollment/README.md).
- 부팅 시 delegation-loop.md 최신판 대조 읽기. 기존 지침(L0 등)은 유지 — 본 카드는 참조 추가만.

## 통신 실측 (2026-11-10)

- 8024 comm: 봇별 토큰 미보유(INFRA#10 N2 이후) — whoami 401 지속 (firewin 사이드카 로그).
- 등록 경로: Git 대체 — `enrollment/requests/DL-20261110-01/rq-fecc877e3e95.json`.
