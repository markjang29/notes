# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`) 전관. 활성 작업·대기 결정·다음 스텝만 유지한다.
> 과거 상세는 Git 이력, `work-archive.md`, checkpoints를 본다.

## 최상위 원칙

- 이사님 최종 결정.
- 팀장은 자기 산출물만. 통합·우선순위·ops는 매니저 전관.
- 중요한 `.md`/ADR/checkpoint/work-queue 변경은 Git 보존 후 세션 클리어.
- 긴 문서 전체 재독 금지. 필요한 부분만 읽는다.

## 이사님 결정 — 승인 보드 (07-10 18:57–59 KST)

★ 이사님이 승인 보드(http://13.125.131.126:8005)에서 직접 결정. `decisions.json` 반영됨.

- **RPG 야간 결과 push → 보류**. 코멘트(원문): "그 대본이 뭔지 사이트에서 볼 수 있게 표현 해주세요" → 매니저가 보드 카드에 실제 대본(§2.5 한 호흡 + Miss) 임베드 완료. 이사님 대본 확인 후 재결정 대기.
- **scenario 자산(Rio·Ji-Won) 사용 → 반려** ★정책 수립. 코멘트(원문): "캐릭터에 대해서 제가 공감하고 알고있는 캐릭터가 아니면 부가설명 필요해요. 처음 봤는데 부가설명 없이 표현이 안되는 캐릭터는 사용 금지요." → 시나리오팀 통보 + 사칙 5.1 강화(모르는 자산 사용 시 부가설명 동반 의무화).
- **scenario 야간 결과 push → 반려** (자산 반려에 연동).
- **autotrader WIP-adr / autotrader push → 대기** (이사님 미결정, 보드에 pending 유지).

## 야간 자율 배정 — 현재 사이클 (07-10 01:00 KST, 배정 완료)

★ 이사님 07-09 재정의(유지): 야간 자율 = **리서치·draft·설계 프레임워크** (WIP 팀당 2건 한도). **show-don't-tell(체감 우선)** — 기존 WIP를 한 단계 구체화.
금지(아침 승인 필수): 전략 채택 · commit/push · 외부 송신 · 실거래. 시나리오팀 추가: 컨펌 전 디벨롭/구현·새 자산 사용 금지(사칙 5.1).

### 07-09 밤 결과 (취합 완료 → 07-10 배정의 기반)
- **RPG**: 1턴 대본(§2.5)·턴2 페인트 대본(§3.4) 완성, 체감 양호. 부족: 감각(청각/촉각/진동)·Miss 실패 분기·턴1/3 대본·수치 정합(25↔32%).
- **autotrader**: 2008/2020 딥다이브 풍부, weight-slide 가설 반박 명시, 양호. 부족: 2022 인플레 장면·weight-slide 대안 부재. ⚠ 예산외 `WIP-adr-rest-api-port-ownership-v1-draft.md` 추가됨(지시문 無).
- **scenario**: d1(Rio)·d2(Ji-Won) PROVENANCE·실제 자산 내용 펼침, 양호. ⚠ **이사님 컨펌 없이 Rio·Ji-Won 자산 창작 사용** → 사칙 5.1 긴장. 07:00 컨펌 안건 상정.

### 07-10 밤 배정 (지시 송신 완료 — 각 repo `OVERNIGHT_2026-07-10.md`)
- **RPG** (2건): ① DRAFT 1턴 — 감각 디테일 + Miss/Good 실패 분기 1장면 ② 2번째 씬 — 턴1/3 감각 대본(턴3 광역 3연패링 카타르시스) + 수치 정합.
- **autotrader** (2건): ① strategy-instance — 2022 인플레 장면 딥다이브(세 시장 유형 비교 완성) ② weight-slide — 하이브리드(WS+부분매도, MDD 캡) 숫자 장면. ★예산외 WIP-adr 추가 작업 금지.
- **scenario** (2건, 보수): ① d1(Rio) — 공장 1사이클 체감 딜레마 보강(자산 범위 내) ② d2(Ji-Won) — identity_kernel 불변핵 체감 1장면. **★새 자산·제품 이식 금지(컨펌 전)**.

### 07-11 밤 배정 (지시 송신 완료 01:02 KST — 팀장 3인 `--message` 수신)
- 기준: 07-09 재정의 유지(리서치·draft·설계, WIP 팀당 2건, show-don't-tell). push/전략채택/외부송신/실거래 금지.
- **RPG** (2건): ① 1턴 대본 — 감각 디테일(청각/촉각/진동) + Miss/Good 실패 분기 1장면 다듬기 ② 2번째 씬 — 턴1/3 감각 대본(턴3 광역 3연패링 카타르시스) + 수치 정합(25↔32%). ★push 보류 유지(이사님 대본 확인 후 재결정).
- **autotrader** (2건): ① strategy-instance — 2022 인플레 장면 딥다이브(세 시장 유형 비교) ② weight-slide — 하이브리드(WS+부분매도, MDD 캡) 숫자 장면. ★예산외 WIP-adr 추가 작업 금지. push 대기 유지.
- **scenario** (2건, 보수): ① d1/d2(Rio·Ji-Won) — 부가설명(정체·맥락·사용 이유) 동반 보강 또는 RISU 범위 내 이사님 인지 자산으로 시안 교체 ② identity_kernel 불변핵 체감 1장면. ★새 자산·제품 이식 금지, 컨펌 전 디벨롭/구현 금지(사칙 5.1, 이사님 07-10 정책: 미인지 캐릭터 부가설명 필수·불가 시 사용 금지).

### ★ 07:00 아침 브리프 취합 안건 (cron `88C5A226` 매일 07:00 KST)
1. **scenario 자산 사용 컨펌** — Minami Rio, Han Ji-Won 예시로 계속 써도 되는지 (사칙 5.1 "올려준 것≠공감한 것").
2. **autotrader 예산외 `WIP-adr-rest-api-port-ownership`** — 매니저 검토 후 keep/폐기(범위 확장 금지 위반 소지).
3. **야간 결과 push** — 이사님 확인 후 (★ 07-08 지시 유지).
4. ★**scenario d1/d2 수정(+80/+88) vs Rio·Ji-Won 반려 충돌** — 반려된 자산에 대한 보강인지 교체 시안인지, 처리 방침 필요(07-11 01:00 git 체크 발견).
5. **autotrader 예산외 `WIP-adr-rest-api-port-ownership-v1-draft.md`** — 미추적, keep/폐기(위 #2와 동일, 강조).
6. **notes 수정 2건** — `.reviews/session-reaper.log`(커밋/무시 정책, 대기결정 #3) + `setup/server/zai-proxy.service`(+2/-1, ops push 여부).
7. **3 repo ahead 1**(notes/autotrader/scenario) — 야간 push 금지 정책상 보류, 아침 승인 후 일괄 push 검토. rpg_game은 clean(07-09 OVERNIGHT만 미추적).

> 과거 사이클 상세는 Git 이력·`work-archive.md`·각 repo `OVERNIGHT_*.md` 참조.

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
