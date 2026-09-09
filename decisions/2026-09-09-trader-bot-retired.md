---
title: 결정 — heav_lnx_trader_bot 퇴사·삭제
date: 2026-09-09
status: decided
authority: director
tags: [org, retirement, trader]
---

# heav_lnx_trader_bot 퇴사·삭제 (이사님 09-09 결정)

## 결정
- `@heav_lnx_trader_bot` (actors: aws-trader, trader 팀장)은 **오늘부로 퇴사·삭제**된다.

## 실행 상태 (실측)
- cokacdir 봇 설정: trader 항목 부재 확인 — 봇 삭제는 이사님 측에서 완료.
- actors.json: v9→v10, `aws-trader` 액터 제거 (매니저 작업분 포함, 본 커밋으로 확정).
- 관제 한판 row: 제거 대기 — codex_dev_1 (관제 오너).
- meeting-room BOTS 등록: 제거 대기 — codex_dev_1.

## 보존 (삭제하지 않음)
- `~/projects/autotrader` repo — 보존 (Git-first; 담당 공석, 인수자는 이사님 결정 대기).
- autotrader venv로 구동 중인 서비스 2개(포트 8003·8021) — 봇 페르소나와 별개 인프라라
  임의 종료 금지. 처분(유지·이관·종료)은 매니저 실측 후 이사님 승인으로 결정.

## 후속
- 전 봇: 신규 task를 trader로 라우팅 금지 (허브 notice 방송됨).
- work-queue: trader 관련 항목 정리 — 매니저.
