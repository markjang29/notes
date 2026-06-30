# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`)가 관리. 활성 작업 · 대기 결정 · 다음 스텝. **과거 상세는 `work-archive.md`**.
> 최근 갱신: 2026-07-01 — 복구번들 다이어트(work-archive 분리), cron 01:00(야간)/07:00(아침) KST.

## 활성 작업

### 🔥 autotrader — 라오어 하이브리드 전략 백테스트
- 스택 Python+pandas, 엔진 구축 완료(`autotrader/backtest/`). 첫 결과: 하이브리드 MDD -16% / 수익 +82%.
- 다음 실험: 비중 슬라이드 개량(exit_ratio {0,0.3,0.5,0.7,1.0}). 상세·이론은 `work-archive.md` + `.reviews/seminar-raoer-*`.
- **대기 ADR:** (a) 라오어 단독 / (b) 하이브리드★ / (c) 타 방향.
- v1(차익)과 공존 가능.

### ✅ RPG — 걷기×전술 컨셉 수렴(확정) → 체감 시나리오 진행
- 컨셉 1안 확정(걷기=입장재화·동기화 PvP·로맨스 A안·진영 분기·P2W 0). 상세 `ideation/06-concept-convergence.md`.
- 진행: 한 판 체감 시나리오(07) draft — **RPG 팀장 미완료, 촉구 중**.
- **대기 ADR:** 엔진(Godot 권장).

### 🆕 시나리오 팀 — 자생 세계관 시나리오 (06-30 신설)
- 팀장 `@heav_lnx_scenario_bot` → `~/projects/scenario`. 캐릭터 챗(character.ai류) 자생 세계관. **RPG 분리**.
- 이사님 07-01 00:15 push 완료(catalog/ + ecosystem/) → 팀장 초기 설계 draft 착수 지시.
- 설계 원칙(codex)·상세는 `work-archive.md`.

### 아이디에이션 v1 → v2 대기
- 피드백 "기술 분석 과다, 실체화 부족" → v2 = show-don't-tell(체감 시나리오·구체 숫자).

## 대기 결정 (ADR)
- RPG 엔진: Godot? — 컨셉 수렴 후.
- trader 스택: Python + NautilusTrader? — v2 후.
- 팀장 사칙 인증: 결정·commit 전 필수.

## 🔥 야간 자율 운영 (이사님 승인)
- **야간 자동** = 리서치·draft·숫자표·설계 프레임워크 (WIP 팀당 2건).
- **아침 승인 필수** = 전략 채택·엔진 확정·commit/push·ADR·외부 송신·실거래.
- **cron(cokacdir):** `01:00` 야간 배정 / `07:00` 아침 브리프 (KST). fallback: 팀장 비활성 시 매니저 직접.

## 다음 스텝
1. v2 아이디에이션(체감 우선).
2. 팀장 사칙 인증 완료 확정.
3. 쿼터/검색 장애 → `decisions/2026-06-26-quota-checkpoint-resume.md`.
