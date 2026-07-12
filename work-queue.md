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

## 야간 자율 배정 — 현재 사이클 (07-11 01:00 KST, 배정 완료)

★ 이사님 07-09 재정의(유지): 야간 자율 = **리서치·draft·설계 프레임워크** (WIP 팀당 2건 한도). **show-don't-tell(체감 우선)** — 기존 WIP를 한 단계 구체화.
금지(아침 승인 필수): 전략 채택 · commit/push · 외부 송신 · 실거래. 시나리오팀 추가: 컨펌 전 디벨롭/구현·새 자산 사용 금지(사칙 5.1).

### 07-10 밤 결과 (취합 완료 → 07-11 배정 기반)
- **RPG**: 1턴 감각(히트스톱·파열음·촉각)+Miss/Good 실패 재도전 루프 완성. 2번째 씬 턴1·3 대본+수치 정합, 세 턴 감정 곡선. 양호. 부족: 풀 1판 경험(오프닝~결말) 미완, 패링 손맛 인터페이스 미첨.
- **autotrader**: 2008/2020/2022 세 시나리오 실측 딥다이브 완성, WS-A +134%/MDD−21% 명확, 한계 솔직 인식. 양호. 부족: 통합 "나침반" 미정형, WS+재진입 완전형 미탐색.
- **scenario**: Rio DISCOVER→ASSEMBLE 딜레마(tampered 시줄)·Ji-Won identity_kernel 불변핵 3상황 체감. 양호(d1/d2 +80/+88 = 07-10 밤 산출, 반려 18:57 이전이라 유효). ⚠ **이사님 07-10 반려**(Rio·Ji-Won 자산 사용 금지·부가설명 없는 사용 금지) → 07-11 밤부터 사칙 5.1 강화 적용.

### 07-11 밤 배정 (각 repo `OVERNIGHT_2026-07-11.md` + 선행 `--message`)
⚠ **중복 트리거 사고**(07-08 유사): 선행 세션(01:02)이 `--message`로 07-10 복사형 배정 송신, 본 세션(01:00)이 07-10 밤 결과 반영 repo 파일 작성. **repo `OVERNIGHT_2026-07-11.md`(07-10 결과 반영)을 정본 제안** — `--message` 배정은 07-10 결과 미반영·scenario ② 중복. 07:00 이사님 결정.
- **RPG** (2건): ① DRAFT 1턴 — 패링 손맛 인터페이스(입력→히트스톱→감각) 한 호흡 ② 2번째 씬 — 보스전 풀 1판 플레이스루 대본(오프닝→3턴→결말).
- **autotrader** (2건): ① strategy-instance — 세 시나리오→"전략 선택 나침반"(의사결정 트리/매트릭스, 전략 채택 아님) ② weight-slide — WS/exit/하이브리드 3-way 비교(2020 코로나, 트레이드오프 숫자). ★예산외 WIP-adr 추가 작업 금지.
- **scenario** (2건, 보수·사칙 정위치): ① d1(Rio) — **이사님용 부가설명 블록**(PROVENANCE+캐릭터 배경, 장면 수정 없이 메타 보강만) ② d2(Ji-Won) — 부가설명 블록 + 가상제품 사칙 정위치("추상 예시, 컨펌 후 실제 적용" 명시). **★Rio·Ji-Won 디벨롭·창작 확장·새 자산 금지**.

### 07-12 밤 배정 (01:02 KST, `--message` 송신 완료 — 3팀장 수신)
★이사님 07-09 재정의 유지(리서치·draft·설계, WIP 2건, show-don't-tell). push/전략채택/외부송신/실거래 금지.
**★★07-11 밤 배정 과제 3팀 전체 미수행**(repo에 07-11 01:18 이후 산출 commit 없음 → 07:00 최우선 안건 #1). 07-11 밤 과제를 사실상 재배정.
- **RPG** (2건, 재전달): ① 1턴 패링 손맛 인터페이스(입력→히트스톱→감각) 한 호흡 draft ② 2번째 씬 풀 1판 플레이스루 대본(오프닝→3턴→결말).
- **autotrader** (2건, 재전달): ① strategy-instance 세 시나리오→'전략 선택 나침반'(의사결정 트리, 전략 채택 아님) ② weight-slide WS/exit/하이브리드 3-way 비교(2020 코로나 숫자). ★예산외 WIP-adr 작업 금지 유지.
- **scenario** (2건, 재전달·보수): ① d1(Rio) 부가설명 블록(PROVENANCE+배경, 장면 수정 없이 메타 보강) ② d2(Ji-Won) 부가설명 + 가상제품 사칙 정위치. ★새 자산·디벨롭 금지 유지. 배정 과제를 자율 ops보다 우선 요청(07-11 새벽 크롤링 ops 우선시한 정위치).

### ★ 07:00 아침 브리프 취합 안건 (cron `88C5A226` 매일 07:00 KST)
1. **★★ 07-11 밤 배정 과제 3팀 전체 미수행** — RPG/autotrader/scenario 모두 repo에 07-11 01:18 이후 산출 commit 없음. 팀장 세션 미실행 또는 commit 누락 의심. 원인 파악 + 07-12 밤 재배정 효력 확인. ★최우선.
2. **★ 07-11 밤 중복 트리거 사고 보고** — 두 매니저 세션 동시 배정(01:02 + 01:18). repo 파일 정본 처리. 재발 방지(cron 중복 감지 후보).
   - **★★ 07-12 밤 동일 재발** — 선행(01:02, commit `071d402` 정본) + 본 세션(01:04~05). 선행은 '07-11 미수행→재배정', 본 세션은 '다음 단계'로 방향 충돌. 본 세션이 선행에 양보: 3팀 정정 송신(01:08) + repo `OVERNIGHT_2026-07-12.md` 3개 보류(경고 라인 추가). ★재발 방지(cron 중복 감지 락) 긴급 — 2연속 밤 동일 패턴.
3. **07-10 밤 결과 push** — 이사님 확인 후 (★ 07-08 지시 유지). RPG 대본 사이트 표현(07-10 이사님 요청)은 매니저 보드 카드 처리(완료).
4. **autotrader 예산외 `WIP-adr-rest-api-port-ownership-v1-draft.md`** — 미추적, keep/폐기 결정(이사님 07-10 "대기"). 기존 안건 #3·#5 통합.
5. **scenario 부가설명 보강 결과** — 이사님 반려(07-10) 후 산출. ★07-11 밤 미수행 → 07-12 밤 산출로 이월. 부가설명으로 자산 사용 재개 가능한지 재컨펌.
6. **scenario 자율 ops 정위치** — 07-11 02:49-02:50 크롤링 파이프라인 commit 2건. 부가설명 배정 과제 대신 ops 우선시한 것인지 확인(사칙상 RISU 자산 수집 영역일 수 있으나 우선순위 점검).
7. **notes 수정 2건** — `.reviews/session-reaper.log`(+173, 커밋/무시 정책, 대기결정 #3) + `setup/server/zai-proxy.service`(+2/-1, ops push 여부). 07-11과 동일 미해결.
8. **Git push 대기 상태** — 07-12 01:00 실측: notes **ahead 0**(동기화됨), autotrader ahead 2, rpg_game ahead 1, scenario ahead 2. 미추적: autotrader 3건(OVERNIGHT-09/예산외 WIP-adr 2)/rpg ideation/OVERNIGHT-09/scenario OVERNIGHT-09. (07-11 09:10 감사 주석은 별도 보존.)

#### 09:10 감사 실측 주석 (2026-07-11 KST)

- `notes`: `origin/main` 대비 ahead 3, 로컬 수정 2건(`.reviews/session-reaper.log`, `setup/server/zai-proxy.service`).
- `autotrader`: ahead 2, 로컬 WIP/야간 draft 미반영 4건.
- `rpg_game`: ahead 1, 로컬 미추적 `ideation/OVERNIGHT_2026-07-09.md`.
- `scenario`: ahead 2, 로컬 draft 수정 2건 + 미추적 `OVERNIGHT_2026-07-09.md`.
- 해석: 07:00 안건의 repo 수/ ahead 수는 작성 시점 관측값으로 보존하고, 현재 기준 판단은 이 09:10 실측값을 우선한다.

#### 09:10 감사 실측 주석 (2026-07-12 KST)

- `notes`: `origin/main` 대비 ahead 2, 로컬 수정 2건(`.reviews/session-reaper.log`, `setup/server/zai-proxy.service`). `zai-proxy.service`는 실제 user service와 동일한 `STANDARD_FALLBACK_MAX_BYTES=614400` 보존 변경으로 확인. `.reviews/session-reaper.log`는 자동 로그라 커밋/무시 정책 결정 전 보류.
- `autotrader`: ahead 2, 로컬 변경/미추적 7건. 07-12 WIP 2건은 `commit 금지` 문구를 담은 야간 draft, `WIP-adr-rest-api-port-ownership`은 이사님 대기 안건, 나머지는 07-09/07-12 야간 산출 보존 후보.
- `rpg_game`: ahead 1, 로컬 미추적 6건. 07-12 정본 재배정 산출 2건(`DRAFT-parry...`, `WIP-second-battle-full-match-script`)과 취소된 01:05 보류 draft 2건이 섞여 있어 이사님 처분 전 push 금지.
- `scenario`: ahead 2, 로컬 draft 수정 2건 + 미추적 `OVERNIGHT_2026-07-09.md`, `OVERNIGHT_2026-07-12.md`. Rio/Ji-Won 부가설명·사칙 정위치 보강이나 07-10 반려 미해제 상태라 이사님 재컨펌 전 push 금지.
- 해석: 2연속 야간 중복 트리거로 선행 01:02 정본과 01:04~05 보류 산출이 혼재. 팀장 repo는 기계적 push 금지, 매니저가 정본/보류/폐기 분류 후 승인 보드 또는 이사님 확인 필요.

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
