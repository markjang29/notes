---
title: 야간 아이디어 후보 운영 v1
status: rollout
updated: 2026-07-15
authority: projects/agent-ops/overnight-ideation-v1.md
---

# 야간 아이디어 후보 운영 v1

## 목적과 경계

야간 작업의 목적은 시나리오, RPG, 거래 프로젝트에서 다음 검토 가치가 있는 아이디어를
발견해 아침 후보함에 쌓는 것이다. 야간 작업은 제품 구현, 저장소 변경, 전략 채택 또는
자산 승격이 아니다.

이 정책은 2026-07-15 사용자의 직접 지시에 따라 scenario를 후보 전용 야간 아이디에이션에
포함한다. 이는 과거 scenario 저장소 동결이나 일반 자율 개발을 해제하지 않는다. 후보는
mailbox에만 기록하며 project Git에는 쓰지 않는다. 기존 usable 검증 부산물의 후보 등록은
별도 source인 `usable_byproduct`로 계속 유지한다.

## 기본 일정

- 생성 시작 기본값: 매일 01:00 KST
- 아침 브리프 기본값: 매일 07:00 KST
- 대상: `aws-scenario`, `aws-rpg`, `aws-trader`
- 한도: actor별 최대 2건, 전체 최대 6건
- 한 actor에는 동시에 열린 야간 mail을 하나만 둔다.
- 각 실행은 `overnight-ideas:<KST-date>:<actor-id>` idempotency key를 사용한다.

시각과 한도는 mailbox의 검토된 schedule 설정으로 바꿀 수 있다. 과거 cron ID를 그대로
재활성화하지 않는다. 먼저 실제 runtime schedule과 마지막 실행을 읽고 중복이 없음을 확인한
뒤 새 schedule을 적용한다. R4 mailbox와 schedule 실행기가 준비되기 전에는 이 문서만으로
자동 실행이 시작됐다고 보고하지 않는다.

## 작업 발행

`aws-manager`가 actor별로 하나의 Agent Mail v2 work order를 발행한다.

- `request_origin`: `scheduled`
- `intent`: `ideate`
- `result_disposition`: `candidate_only`
- `controller_actor`: `windows-codex`
- `approval_policy`: `controller_review`
- `write_scope`: 빈 배열
- `forbidden`: 대상 actor의 상시 금지와 `auto_implement`, `auto_promote`, `repo_write`,
  `external_side_effect`를 모두 포함

대상 actor는 자기 identity, 필수 참조, source commit과 범위를 확인한 뒤 ACK한다. 결과는
`idea-candidate-v1.schema.json`에 맞는 후보와 mailbox receipt로 제출한다. Windows Codex가
오프라인이어도 actor는 `submitted`까지 진행할 수 있으나 스스로 `verified`나 `closed`를
기록할 수 없다.

사용자가 Telegram으로 직접 맡긴 일이 있으면 그 mail을 우선한다. 야간 mail은 중복 실행하지
않고 명시적으로 대기 또는 보류 상태를 남긴다. 기존 작업을 몰래 취소하지 않는다.

## 사용할 수 있는 근거

- 대상 프로젝트 Git의 검토된 commit과 규칙
- registry의 `required_refs`
- 이미 검토된 catalog, 결정, deliverable과 provenance
- 이전에 승인된 후보와 폐기된 후보의 제목·dedupe 근거

Scenario는 새 후보를 만들 때 (1) 아직 후보화되지 않은 usable 부산물, (2) 이사님이 사용을
승인한 reviewed 자산, (3) 특정 자산 이름을 쓰지 않는 추상 메커니즘 순서로 선택한다. 이사님이
알거나 승인하지 않은 특정 캐릭터·자산을 임의로 골라 창작 후보를 만들지 않는다.

새 Arca 수집, live login, QR 복구, 다운로드 또는 승인되지 않은 원문 접근은 야간 아이디어
작업에 포함하지 않는다. 그런 근거가 필요하면 현재 mail은 `question` 또는 `blocked`로 남기고
별도의 Arca collection work order를 요청한다.

## 후보 품질 기준

각 후보는 다음을 짧고 구체적으로 포함한다.

1. 제목과 한 문단 pitch
2. 사용자가 체감할 한 줄 hook
3. 재현 가능한 provenance ref
4. 기존 아이디어와 다른 점
5. 주요 위험과 반례
6. 구현이 아닌 다음 검증 실험

`aws-manager`는 exact duplicate를 `duplicate_of`로 연결하고 아침 브리프를 프로젝트별로
묶는다. manager는 아이디어의 승인·폐기 또는 구현을 결정할 수 없다. 근거가 부족한 새
아이디어도 숨기지 말고 부족한 점을 표시한다.

## 아침 결정

아침 브리프에는 아직 결정되지 않은 후보만 싣고 후보 ID, 생산 actor, 제목, hook, provenance,
위험과 추천 이유를 보여준다. 사용자는 Telegram에서 다음 중 하나를 결정한다.

- 승인: `candidate_approved` event로 후보 backlog에 보관
- 보류: `candidate_held` event와 보류 이유 기록
- 폐기: `candidate_discarded` event를 남기되 감사 이력은 삭제하지 않음

결정은 `director`만 append-only candidate event로 기록한다. immutable proposal의
`status=pending_morning_review`와 `decision_*=null`은 수정하지 않으며 현재 상태는 마지막으로
검증된 candidate event에서만 계산한다. 모든 candidate와 decision event의
`implementation_authorized`는 항상 `false`다. `candidate_approved`도 구현 허가가 아니며,
실행하려면 `intent=execute`인 별도 work order, 정확한 범위, commit, 완료조건과 controller
검수가 필요하다.

## 실패와 복구

- restart 후 같은 idempotency key의 새 작업을 만들지 않고 마지막 durable event 다음부터 재개한다.
- timeout이면 재실행 전에 마지막 event와 candidate receipt를 확인한다.
- actor별 사용 시간과 실제 제공되는 token usage를 기록하되 추정 quota는 보고하지 않는다.
- 연속 실패 한도에 도달하면 schedule을 새로 복제하지 말고 중지 상태와 재개 조건을 보고한다.
- secret, cookie, token, session 식별자, lease 값, 서명 URL과 개인 원문은 mail, candidate,
  Telegram 요약과 Git에 기록하지 않는다.

## 전환 완료조건

1. AWS에서 과거 schedule과 현재 실행 상태를 read-only로 점검한다.
2. Agent Mail v2, intake, candidate validator가 통과한다.
3. actor별 candidate-only no-op mail을 `submitted`까지 왕복한다.
4. 후보 1건 완료조건의 mail에는 candidate receipt가 정확히 1개만 결속됨을 검증한다.
5. 후보 하나에 승인·보류·폐기 결정을 각각 시험하고 구현 mail이 자동 생성되지 않음을 확인한다.
6. Cokacdir 재시작 후 중복 candidate와 중복 schedule run이 없음을 확인한다.
7. 검증이 끝난 뒤에만 runtime schedule을 enabled로 표시한다.
