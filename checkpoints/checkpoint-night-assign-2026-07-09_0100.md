# Checkpoint — 야간 자율 배정 (2026-07-09 01:00 KST)

- **cron:** `2D8F5150` (야간 자율 배정, `0 1 * * *`, 매니저 본업)
- **매니저:** `@heav_lnx_bot` (key `f5c0501a3a7999ad`), 정체 인증 완료
- **이사님 지시 요지:** 3팀장에게 야간 작업 지시. 사칙 준수. 야간 = 리서치·draft·설계 프레임워크만(WIP 팀당 2건 한도). 전략 채택·commit/push·외부송신·실거래 금지(아침 승인 필수). 07:00 아침 브리프 취합. show-don't-tell(체감 우선). KST.

## ★ 이사님 07-09 재정의 (07-08 대비 변화)

- 07-08: 야간 자율 = 인사이트 발굴(산출 금지)
- 07-09: 야간 자율 = **리서치·draft·설계 프레임워크**(산출 허용, 팀당 2건 한도)
- 범위 확장. show-don't-tell은 v2 방향과 일관.
- 메모리 `night-autonomy-insight.md`(07-07 인사이트 발굴)와 충돌 → **07:00 브리프에서 이사님 확인 후 메모리 정정** (임의 수정 보류)

## 3팀 배정 내역

### RPG (`@heav_lnx_rpg_bot`) — 2건(한도 내)
1. 첫 보스 1턴 체감 인스턴스 구체화 — `rpg_game/ideation/DRAFT-first-boss-one-turn-instance.md` → 한 장면 대본
2. 패막 손맛 "속이는 자" 패턴 장면 — `rpg_game/ideation/WIP-second-battle-scene-reasoning-parry.md`
- 금지: 시그니처 변경·Godot commit·새 모듈 구현

### autotrader (`@heav_lnx_trader_bot`) — WIP 3→2 좁힘
1. 전략 인스턴스 거래 딥다이브 — `autotrader/research/WIP-strategy-instance-trade-v1-draft.md` (2008/2020/2022 중 1~2장면)
2. 비중 슬라이드 MDD vs 수익 체감 — `autotrader/research/WIP-weight-slide-results-v1-draft.md`
- 제외: 재진입(WIP-reentry) — 2건 한도
- 금지: 실거래·거래소API·전략 채택·commit. yfinance 백테스트 범위만

### scenario (`@heav_lnx_scenario_bot`) — 2건(한도 내, 사칙 준수)
1. 자산 공장 1사이클 체감 draft — `scenario/drafts/d1-scene-minami-rio.md`
2. 자산→제품 이식 캐릭터 회전 1예 — `scenario/drafts/d2-rpg-advisor-han-jiwon.md`
- 금지: 구현/디벨롭(컨펌 전)·전략 채택·commit. PROVENANCE 의무, .extract/ 실제 내용 사용

## 전달 수단

- 지시문 파일 3개: 각 팀 repo에 `OVERNIGHT_2026-07-09.md` 작성 (commit 안 함)
  - `/home/ubuntu/projects/rpg_game/ideation/OVERNIGHT_2026-07-09.md`
  - `/home/ubuntu/projects/autotrader/research/OVERNIGHT_2026-07-09.md`
  - `/home/ubuntu/projects/scenario/OVERNIGHT_2026-07-09.md`
- `--message` 송신 3건(모두 status: ok):
  - RPG: `msg_20260709_010622_0cad9ecc`
  - trader: `msg_20260709_010627_4081e532`
  - scenario: `msg_20260709_010631_702d21a1`
- `~/notes/work-queue.md` "야간 자율 배정" 섹션 07-09 재정의로 갱신 (commit 안 함 — notes는 감사봇 정합성 후, 또는 이사님 지시 시)

## 금지사항(공통, 아침 승인 필수)

전략 채택 · commit/push · 외부 송신 · 실거래 · 이사님 직접 보고(07:00 매니저 취합). 시나리오팀 추가: 컨펌 전 디벨롭/구현 금지.

## 다음

- 07:00 아침 브리프(cron `88C5A226`)에서 3팀 결과 취합 → 이사님 보고.
- 컨펌 안건(07:00): ① 야간 결과 push 여부 ② 메모리 night-autonomy-insight 정정 ③ autotrader 재진입 WIP 다음 야간 편성 여부.
- 팀장 진행 보고 도착 시 매니저가 기록. 팀장 실행 장애 시 07:00 전 매니저가 보완 배정.
