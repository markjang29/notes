---
title: Scenario 자율 운영 계약
status: active
authorized_at: 2026-07-16
controller: windows-codex
---

# Scenario 자율 운영 계약

## 목적

사용자가 대화 창에 새 지시를 쓰지 않아도, 이미 승인된 제품 방향 안의 안전한 작업은 작은
단위로 계속 진행한다. 메인 대화는 관제와 의사결정 창구로 남기고, 구현·검사 작업은 별도
task 또는 예약 worker가 수행한다.

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

| lane | 실행자/토큰 풀 | 주기 | 역할 |
|---|---|---|---|
| `factory-steward` | Windows Codex 경량 worker | 매시간 | Git 작업 보드에서 `safe_auto` 1개 선택, 최대 12분/도구 8회, WIP 1 |
| `morning-idea-audit` | Windows Codex audit | 매일 07:10 KST | AWS 야간 후보·receipt·중복·소유권 관제 |
| `overnight-ideas` | AWS Claude client + Z.AI pool | 01:00~07:00 KST | scenario/RPG/trader 후보 생성과 manager 브리프; 후보만, 구현 금지 |
| `arca-daily` | Windows collection controller | 매일 승인 시각 | fresh login preflight와 lifecycle gate 뒤 단건 완결 |

로컬 예약 작업은 PC가 켜져 있고 Codex desktop이 실행 중일 때만 동작한다. 항상 켜진 실행이
필요한 역할은 AWS actor에 남기되, Git 정본과 agent-mail receipt를 통해 검증한다.

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
2. `ZC-02c` bridge 단계·heartbeat 표시
3. `OPS-01` stage event 계약
4. `PY-01` import·entrypoint·dependency inventory
5. `MX-04` 시간·자산 사용 ledger
6. `NOTE-03` 현재 handoff 자동 갱신 후보
7. `NOTE-05` 주간 완료/소요시간 review

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
