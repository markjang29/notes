---
title: Scenario 자율 운영 계약
status: active
authorized_at: 2026-07-16
controller: windows-codex
---

# Scenario 자율 운영 계약

## 목적

사용자가 대화 창에 새 지시를 쓰지 않아도, 이미 승인된 제품 방향 안의 안전한 작업은 작은
단위로 계속 진행한다. 메인 대화는 director 대화, 우선순위, 분해·배정, 관제, controller 검수와
close만 담당한다. 구현·수집 작업은 별도 task 또는 예약 worker가 수행한다.

자율 운영은 토큰을 소진하기 위한 장치가 아니다. Git에 등록된 가치 있는 작업을 우선순위대로
진행하고, 더 할 안전한 일이 없거나 결정 gate에 닿으면 no-op/blocked receipt를 남긴다.

## 권한 경계

### 사용자 없이 진행할 수 있는 `safe_auto`

- 읽기 전용 inventory, dedupe, provenance, schedule/receipt health audit
- 승인된 의미를 바꾸지 않는 결함 수정과 회귀 테스트
- deterministic fixture, schema validator, 계측, 실패 fingerprint
- portability/bootstrap, skill mirror, 문서와 코드의 정본 링크 동기화
- 이미 승인된 테스트의 재실행과 동일 입력의 idempotent retry
- exact Git 근거가 있는 KPI 상태 갱신
- 전용 branch/worktree에서의 작은 구현, 검증, commit, push

`windows-codex`는 worker 결과를 독립 검수한 뒤 통합한다. worker의 완료 메시지만으로 main,
reviewed, usable, deployed 상태를 주장하지 않는다.

### 사용자 판단이 필요한 `decision_gate`

- 제품 최상위 목적이나 우선순위 변경
- candidate의 accept/hold/discard 또는 core/implemented 승격
- 새로운 비용·외부 전송·권한 확대
- 비가역 삭제, 데이터 의미 변경, production 배포
- 로그인·비밀·계정 소유자 행동
- 서로 다른 두 유효한 제품 방향 중 하나를 선택해야 하는 경우

기술 결함, 실패 테스트, 버전 불일치, 비활성 schedule, exact pin 갱신, 읽기 전용 진단은
원칙적으로 사용자 판단 사유가 아니다. 승인된 범위 안에서 진단·수정·재검증을 계속한다.

## 실행 구조

30분 이상 걸릴 것으로 보이거나 독립 commit·문서·분석 보고서가 생기는 작업은 사용자에게
보이는 별도 Codex task로 만든다. 짧은 읽기 전용 검사와 결정적 검증만 bounded subagent 또는
ZCode에 맡길 수 있으며, 이 경우에도 메인 화면에 `owner`, `state`, `deadline`,
`last_evidence`, `next_action`을 투영한다. 내부 실행 여부와 관계없이 메인 task의
`windows-codex`가 controller 책임을 유지한다.

| lane | 실행자/토큰 풀 | 주기 | 역할 |
|---|---|---|---|
| `factory-steward` | Windows Codex 경량 worker | 매시간 | Git 작업 보드에서 `safe_auto` 1개 선택, 최대 12분/도구 8회, WIP 1 |
| `morning-idea-audit` | Windows Codex audit | 매일 07:10 KST | AWS 야간 후보·receipt·중복·소유권 관제 |
| `overnight-ideas` | AWS Claude client + Z.AI pool | 01:00~07:00 KST | scenario/RPG 후보 생성과 manager 브리프; 후보만, 구현 금지. trader는 director hold |
| `arca-daily` | Windows collection controller | 매일 승인 시각 | fresh login preflight와 lifecycle gate 뒤 단건 완결 |

로컬 예약 작업은 PC가 켜져 있고 Codex desktop이 실행 중일 때만 동작한다. 항상 켜진 실행이
필요한 역할은 AWS actor에 남기되, Git 정본과 agent-mail receipt를 통해 검증한다.

## 시간축과 상위 목표

모든 작업은 `지금 문제`만 보지 않고 아래 시간 지평 중 하나에 연결한다. 하위 작업이 상위 목표를
지연시키면 기술적으로 흥미로워도 중단·우회·재배정한다.

| 목표 ID | 시간 지평 | 마감 | 검증할 결과 |
|---|---|---|---|
| `H-TODAY-20260716` | 오늘 | 2026-07-16 18:00 KST | Arca 1건 terminal, ZCode bounded packet ACK·RESULT·검수 1건, 자동 연속 controller 최소 구현·receipt |
| `H-7D-20260723` | 7일 | 2026-07-23 18:00 KST | 재부팅·로그인 해제·quota 분리 복구, warm-path 3건 계측, 신규/레거시 균형 기준 확정 |
| `H-30D-20260815` | 30일 | 2026-08-15 18:00 KST | Git 정본 기반 관리 화면, RISU-like continuity C1 benchmark, Matrix 멀티버스 최소 vertical slice |
| `H-90D-20261014` | 90일 | 2026-10-14 18:00 KST | 반복 가능한 세계·캐릭터·페르소나·서사 공장과 RPG Studio형 소비 흐름의 end-to-end 검증 |

날짜는 희망 표시가 아니라 검증 deadline이다. 매일 실제 처리량과 blocker를 반영해 예상 완료일을
다시 계산하고, 늦어질 때는 `원래 마감 / 현재 예상 / 지연 원인 / 회복 행동`을 함께 기록한다.

모든 실행 카드와 receipt에는 아래 기계 판독 필드를 둔다. 시각은 중복 문자열을 만들지 않고
`+09:00` offset이 포함된 ISO 8601 한 값으로 저장하며, 경과시간은 정수 초로만 누적한다.

- `created_at`, `started_at`, `last_evidence_at`
- `next_checkpoint_at`, `soft_deadline_at`, `hard_deadline_at`
- `finished_at` 또는 `blocked_at`
- `active_elapsed_seconds`, `waiting_elapsed_seconds`, `estimated_finish_at`
- `horizon_ids`: 연결된 오늘·7일·30일·90일 목표 ID 배열

아직 발생하지 않은 시각은 `null`이고, `estimated_finish_at`은 근거가 생기기 전에는 추정하지 않고
`null`로 둔다. 재시작 뒤 경과시간은 wall clock 차감이 아니라 마지막 durable event까지 누적된
값에서 이어 간다. ACK는 완료 증거가 아니라 SLA 시작점이다. 담당 actor의 `acknowledged` 뒤
실행 시작 시각부터 10분 안에 first evidence가 없으면 deadline miss를 기록하고, 20분까지 새
durable evidence가 없으면 카드 상태를 임의로 바꾸지 않은 채 `health=stalled`를 파생 판정한다.
30분까지 회복되지 않으면 controller가 기존 writer를 fence하고 checkpoint부터 `auto_reroute`한다.

## 관제자 운영 루프

`windows-codex`의 첫 번째 책임은 개별 기술 문제를 오래 붙잡는 것이 아니라 전체 목표를 계속
움직이는 것이다. 메인 대화는 director 대화·우선순위·분해·배정·모니터·controller 검수·close를
다루는 관제 전용 창구로 유지한다. 30분 이상 또는 독립 산출물이 있는 구현·수집은 사용자에게
보이는 별도 Codex task에 맡긴다.

1. 매일 08:30 KST 또는 당일 첫 활성 시점에 전일 terminal 결과, hold, 실제 인증·quota 상태,
   오늘의 결과 목표 최대 3개, 담당자, 완료조건, 예상 완료시각, 다음 checkpoint를 먼저 발표한다.
2. 전체 WIP는 최대 3개, repo별 의미 변경 writer는 1개다. 새 질문은 큐에 보존하되 현재 WIP를
   몰래 교체하지 않는다.
3. ACK/실행 시작은 SLA 시작점이다. 10분 안에 첫 증거를 만들고, 시작점부터 20분까지 새
   durable evidence가 없으면 `stalled`, 30분까지 회복되지 않으면 `auto_reroute`한다. 같은
   실패를 두 번 반복하지 않는다.
4. 작업 중에는 10분 checkpoint 또는 terminal 직후에 `현재 시각 / 경과 / 새 증거 / 다음 행동 /
   예상 완료 / 사용자 행동 필요 여부`를 짧게 보고한다.
5. 사용자의 결정이 필요한 카드만 멈춘다. 로그인·비밀·새 비용·권한 확대·비가역 변경·제품
   방향 선택 외의 기술 문제는 안전 범위에서 자동 복구하거나 다른 독립 카드로 넘어간다.
6. `done`은 worker의 말이 아니라 commit/path, test, runtime receipt, controller 검수로만 닫는다.
   `claimed`, Telegram 전달, 승인보드 accepted는 완료 증거가 아니다.
7. 새 세션이나 재부팅 뒤에는 Git 작업 보드, actor registry, open mail의 마지막 durable event를
   먼저 읽고 이어서 실행한다. 대화 기억만으로 상태나 담당을 재구성하지 않는다.
8. 모든 별도 task와 bounded worker packet에는 논리 repo, full input commit, exact read/write
   scope, done criteria, approval policy, stable idempotency key와 attempt를 둔다.

### 자동 controller 상태 전이

```text
idle -> selecting -> claimed -> acknowledged -> in_progress -> submitted
  ^                                                               |
  +--- closed <- verified <- controller_review <-------------------+
```

- `claimed`: router/controller가 실행권을 잡은 상태일 뿐 worker 수신 확인이 아니다. 담당 actor가
  정체·범위·금지·완료조건을 확인해 `acknowledged`한 뒤에만 `in_progress`로 간다.
- `controller_review`: 내부 관제 단계이며 mail event 이름이 아니다. controller만 검수 뒤
  `verified`, `closed`를 순서대로 기록한다.
- `verified/closed`: runtime lease를 반납하고 바로 다음 eligible 카드를 고른다.
- `submitted`: worker terminal일 뿐 카드 완료가 아니다. controller 검수 전에는 `done`으로 넘기지 않는다.
- `technical_failure`: 실패 fingerprint와 attempt를 기록한다. 같은 fingerprint가 두 번이면 그 카드만
  보류하고 다음 독립 safe 카드를 고른다.
- `decision_required`: exact 질문 하나를 남기고 멈춘다.
- `quota_exhausted`: 실제 429/usage-limit가 난 pool만 막고 다른 pool의 eligible 카드는 계속한다.
  모든 eligible 카드가 같은 막힌 pool을 요구할 때만 전체 실행을 멈춘다.
- `capacity/session/route/thread/quota failure`: checkpoint의 input commit/ref, last evidence,
  idempotency, attempt, writer lease/fence와 next action을 보존한다. 이전 writer를 종료하거나
  fence한 뒤 capability-compatible route에서 재개하며, 같은 작업을 새 key로 중복 실행하지 않는다.
- `global_blocker`: actor registry·queue Git commit·event chain·controller lease의 무결성을 확인할 수
  없을 때 fail closed한다. 단일 카드의 테스트 실패나 도구 오류는 global blocker가 아니다.

예약 중복은 Task Scheduler `IgnoreNew`와 runtime controller lease로 막고, repo별 의미 변경 writer는
1개만 허용한다. Arca 수집은 이 로컬 lease로 대체하지 않고 기존 AWS device lease와 lifecycle gate를
추가로 통과한다. 과거 대화의 승인 질문이나 승인보드 `accepted`는 재개 근거가 아니다. 결정 대기는
현재 queue commit, 카드 ID, attempt, input commit이 모두 일치할 때만 유효하며 하나라도 달라지면
`stale`로 무시한다. 자동 worker는 `approval=never`로 실행하고, 권한·sandbox 실패는 사용자 승인
질문이 아니라 `technical_failure`로 분류한다.

### 상태·quota 사실성 규칙

- 로그인, lease, 서비스, quota 판정에는 15분 TTL을 적용한다. 그보다 오래된 값은 `unknown`이며
  실행 직전 해당 경로만 다시 확인한다.
- AWS Claude client가 쓰는 Z.AI pool, Windows Codex pool, 로컬 ZCode pool은 별개다. 한 pool의
  429로 다른 pool을 중지하지 않는다.
- provider가 남은 비율·reset 시각을 주지 않으면 추정하지 않는다. live probe는 그 호출의 성공과
  실제 사용량만 증명한다.
- Codex는 설계·통합·controller review, 로컬 ZCode는 frozen deterministic 분석, AWS scenario/RPG는
  장기 아이디어·프로젝트별 독립 업무에 우선 배정한다. trader는 director가 해제할 때까지 배정하지 않는다.
- Git이 정본이며 Notion·웹·Telegram은 그 정본의 읽기·결정·알림 화면이다. 화면에만 존재하는
  결정이나 완료 상태는 인정하지 않는다.

## factory-steward 한 회 실행 계약

1. `notes/projects/scenario/tasks/README.md`와 대상 프로젝트의 `AGENTS.md`/`HARD_RULES.md`를
   정확한 Git commit에서 읽는다.
2. active lease나 다른 worker의 동일 WIP가 있으면 중복 실행하지 않는다.
3. `safe_auto` 후보 중 완료조건이 명확한 가장 앞 카드 하나만 고른다.
4. 전체 대화 이력을 fork하지 않는다. 작업 ID, exact refs, 완료조건, 금지사항만 담은 frozen
   packet을 사용한다.
5. 10분에 checkpoint를 만들고 12분 또는 도구 8회 중 먼저 도달하면 멈춘다.
6. 수정했다면 전용 branch/worktree에서 관련 test, `git diff --check`, secret/path 검사를
   통과한 뒤 commit한다. 실패하면 변경을 성공으로 표시하지 않는다.
7. runtime receipt에는 시작/종료, 작업 ID, commit, tests, elapsed, token telemetry가 실제로
   제공된 경우에만 기록한다. 개인 quota 잔여량은 추정하지 않는다.
8. 사용자 판단이 필요하면 정확한 질문 하나와 안전하게 계속할 수 있는 다음 카드 후보를
   남긴다. 다른 safe task가 있으면 전체 worker를 멈추지 않는다.

## 초기 safe-auto 후보

1. `ZC-02b` 입력 절대경로 오탐 최소 fixture
2. `AUTO-01` Arca sync 비활성·예약 CLI 모델/버전 실패 복구
3. `ZC-02c` bridge 단계·heartbeat 표시
4. `OPS-01` stage event 계약
5. `PY-01` import·entrypoint·dependency inventory
6. `MX-04` 시간·자산 사용 ledger
7. `NOTE-03` 현재 handoff 자동 갱신 후보
8. `NOTE-05` 주간 완료/소요시간 review

위 순서는 제품 우선순위 변경이 아니라 안전한 기술 backlog의 기본 순서다. 선행조건이나
working tree 충돌이 있으면 이유를 receipt에 남기고 다음 eligible 카드로 이동한다.

## 2026-07-15 5시간 감사 기준선

- 감사 구간 전체가 정지는 아니었고 약 3시간의 추적 활동이 있었다.
- 최장 무활동 구간은 약 1시간 52분이었다.
- 그 구간에는 추적된 새 Codex 모델/도구 이벤트와 token-count 증가가 없었다.
- 사용자 결정을 기다렸다는 근거는 없었고, 당시 기술 backlog는 자율 진행 가능했다.
- 메인 trace의 대규모 token counter는 대부분 cached input이며 결제·주간 quota 사용량과
  동일하지 않다. full-history fork의 counter는 중복되므로 서로 합산하지 않는다.

이 기준선의 운영 판정은 `자율운영 미달`이다. 다음 감사부터는 productive run 수, no-op,
decision-blocked, duplicate-avoided, wall time, exact commit/test receipt를 구분해 측정한다.

## 관련 정본

- `projects/scenario/tasks/README.md`
- `projects/agent-ops/README.md`
- `principles/git-first-project-truth.md`
- Scenario repo `docs/matrix-risu-long-term-kpi.md`
- Scenario repo `.agents/skills/agent-mail/SKILL.md`
- Scenario repo `.agents/skills/matrix-factory/SKILL.md`
