# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`) 전관. 활성 작업·대기 결정·다음 스텝만 유지한다.
> 과거 상세는 Git 이력, `work-archive.md`, checkpoints를 본다.

## 최상위 원칙

- 이사님 최종 결정.
- 팀장은 자기 산출물만. 통합·우선순위·ops는 매니저 전관.
- 중요한 `.md`/ADR/checkpoint/work-queue 변경은 Git 보존 후 세션 클리어.
- 긴 문서 전체 재독 금지. 필요한 부분만 읽는다.

## 야간 자율 배정 (2026-07-09 01:00 KST — 리서치·draft·설계 프레임워크)

★ 이사님 07-09 재정의: 야간 자율 = **리서치·draft·설계 프레임워크** (WIP 팀당 2건 한도). 07-08 "인사이트 발굴(산출 금지)"에서 범위 확장 — 이제 산출(draft/프레임워크) 허용. **show-don't-tell(체감 우선)**: 추상 설계 말고 한 장면/한 거래/한 사이클의 체감 인스턴스로. 기존 WIP를 한 단계 구체화.

금지(아침 승인 필수): 전략 채택 · commit/push · 외부 송신 · 실거래. 시나리오팀은 추가로 컨펌 전 디벨롭/구현 금지(사칙).

- **RPG** (`@heav_lnx_rpg_bot`, 2건 — 한도 내): ① 첫 보스 1턴 체감 인스턴스 구체화(`ideation/DRAFT-first-boss-one-turn-instance.md` → 한 장면 대본 수준) ② 패막 손맛 장면(`ideation/WIP-second-battle-scene-reasoning-parry.md` "속이는 자" 패턴 변화 묘사). 금지: Godot 코드 commit·새 모듈 구현·시그니처 변경.
- **autotrader** (`@heav_lnx_trader_bot`, WIP 3→2로 좁힘): ① 전략 인스턴스 거래(`research/WIP-strategy-instance-trade-v1-draft.md` → 2008/2020/2022 중 1~2장면 구체 숫자 딥다이브) ② 비중 슬라이드(`research/WIP-weight-slide-results-v1-draft.md` → MDD 방어 vs 수익 트레이드오프 체감 시각화). 재진입(WIP-reentry)은 이번 제외. 금지: 실거래·거래소 API·전략 채택·commit. yfinance 백테스트 범위 내만.
- **scenario** (`@heav_lnx_scenario_bot`, 2건 — 한도 내, 사칙 준수): ① 자산 공장 1사이클 체감 draft(`drafts/d1-scene-minami-rio.md` → RISU 자산→장면 end-to-end 한 사이클) ② 자산→제품 이식 패턴(`drafts/d2-rpg-advisor-han-jiwon.md` → 캐릭터 회전 1예 확장). 금지: 구현/디벨롭(컨펌 전)·전략 채택·commit. PROVENANCE 블록 의무.

지시문 파일: 각 팀 repo에 `OVERNIGHT_2026-07-09.md`. 팀장에게 `--message` 송신. 산출은 각 팀 지정 경로에 남기고 이사님께 직접 보고 금지 — 07:00 아침 브리프에서 매니저 취합. 야간 결과 push는 이사님 확인 후(★ 07-08 지시).

## 활성 작업

### 1. 시나리오팀 — RISU 기반 창작 체계

- 사칙: `principles/scenario-team-purpose.md`
- 존재 이유: RISU 자산 기반 창작 스튜디오. 창작은 자유, 디벨롭은 이사님 컨펌 후.
- 현재 쟁점:
  - scenario-generator v5 재설계 흐름 확인
  - RisuAI 실제 데이터 구조 이해 부족 보완
  - 컨펌 없는 구현/디벨롭 방지
- 다음:
  - 시나리오팀 자기 정체 재인증
  - `scenario-team-purpose.md` 기준 작업 재정렬
  - 큰 소스 읽기는 요약/파일분리

### 2. RPG — Reasoning-Parry / Godot

- 엔진: Godot 확정.
- 시그니처: 참모 추론 × 지휘관 결정 × 패막 손맛.
- 다음:
  - 시나리오팀 산출이 RPG 요구와 맞는지 클라이언트 관점 검토.

### 3. autotrader — 백테스트/대시보드

- 스택: FastAPI + 기존 pandas 백테스트 + Oracle 23ai.
- 대시보드: Streamlit 8002 + 80.
- 포트 정정:
  - 8003 = 시나리오팀 scenario-generator backend
  - autotrader REST API는 미기동/포트 미확정
- 다음:
  - autotrader REST API 포트/소유 재정리 필요 시 ADR 갱신.

### 4. 매니저/감사/복구

- 감사봇: Codex 감사 봇 1개. Claude 매니저/팀장 감시.
- 일일 감사: `B7C51FA3` 매일 09:10 (`10 9 * * *`).
- ctx-evac:
  - Stop 훅 JSON 오탐 수정 완료
  - 실제 `API Error: context window limit`는 별도 장애로 취급
- recovery-gate:
  - L1 문구 명확화 완료
  - L0 도입 후 L0 + current-work-state 주입으로 단순화 예정

## 대기 결정

1. 대청소 후 recovery gate L0 적용 범위 확정.
2. recovery-gate `DISABLE` 제거 여부.
3. `.reviews/session-reaper.log` 커밋/무시 정책.
4. scenario-generator 방향 컨펌 여부.

## 세션 클리어 전 체크

```bash
git -C ~/notes status --short
git -C ~/projects/scenario status --short
git -C ~/projects/rpg_game status --short
git -C ~/projects/autotrader status --short
```

필요 시:

```bash
python3 ~/scripts/export-chat-backup.py --latest --out /tmp/chat-backup.md
```
