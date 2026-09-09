---
name: current-work-state
description: /clear 후 첫 복구 지점 — work-queue.md 우선 읽기. 매니저-팀장 조직·ideation v1→v2·대기 결정
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f2d649c-3598-4170-88fd-57842b5cea87
  modified: 2026-09-09T09:53:47.364Z
---

2026-06-26 기준 매니저(`@heav_lnx_bot`) 작업 상태. **/clear 후 첫 복구 = `~/notes/work-queue.md` 읽기.**

- **조직:** 매니저가 팀장 **2명** 제어 — `@heav_lnx_rpg_bot`→`/home/ubuntu/projects/rpg_game`, `@heav_lnx_scenario_bot`→`/home/ubuntu/projects/scenario`(2026-06-30 신설, 자생 세계관·RPG 분리). **trader 봇(`@heav_lnx_trader_bot`)은 2026-09-09 퇴사·삭제(이사님 지시) — autotrader repo는 보존, 담당 봇 공석.** 세부 `~/notes/org-structure.md`, `~/notes/onboarding.md`, `~/notes/decisions/2026-09-09-trader-bot-offboard.md`.
- **진행:** 아이디에이션 v1 양 팀 완료(각 repo 루트 `IDEATION.md` + 지원 문서). 사용자 1차 리뷰 받음.
- **v2 방향(사용자 피드백 ★):** "기술 분석 과다, 아이디어 실체화가 피부에 안 와닿음" → v2는 **체감적 인스턴스 우선(show, don't tell)**, 기술 분석 최소화. RPG=한 판 체험 시나리오·구체 장면, trader=구체 예시 거래·숫자.
- **대기 결정:** 엔진/스택 미확정(RPG Godot? / trader Python+NautilusTrader?). 컨셉 수렴 후 ADR.
- **쿼터/검색 장애 대응:** `~/notes/decisions/2026-06-26-quota-checkpoint-resume.md` (proposed). LM 호출 529/MCP-429 실패 시 체크포인트 기록 + `cokacdir --cron --session` 예약 재개. 검색 병렬도 권장 1~2회.
- **핸들 주의:** 팀장 실제 Telegram 핸들은 `_bot` 접미사 필수(`@heav_lnx_rpg_bot` 등). `--message` 대상은 `_bot` 붙일 것.
- **서버 timezone:** `Asia/Seoul`(KST, UTC+9). 2026-06-30 UTC→KST 변경(이사님 "여기 한국이야" 지적). cron·cokacdir·`--currenttime` 모두 KST 기준. cokacdir cron `0 23`/`0 7` = KST 23:00/07:00 그대로. reaper crontab(`*/30`)은 무관.
- **매니저 역할(이사님 06-30/07-01):** 작업 기획·배분 주도. **실행은 팀장(매니저 직접 작업 금지, 보고/조율만)**. 정시 **결과 보고**(할 일/지시 반복 금지 — 결과 중심). **ops(복구/스크립트/cron 등)는 매니저가 자율 처리 — 중간 과정 보고 말고, 이사님께는 결과·결정 안건·통찰(영감/후보방향)만.** 시간은 항상 **KST**. cron 사이클: 야간 자율 배정(현재 01:00, 이사님 조정 가능) / 07:00 아침 브리프.

세션 ID(재개용): `e935f596-4e0a-4a6b-8323-531195e7208f`. 후속 세션(workspace `ltgqjhx1`, 2026-06-26)이 [[clear-recovery-map]] 검증·추가. 관련 [[ai-dev-principles-system]] · [[context-explosion-causes]] · [[projects-and-collaboration]] · [[clear-recovery-map]].
