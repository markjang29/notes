---
title: Telegram 직접 작업과 야간 아이디어 후보 운영
date: 2026-07-15
status: decided
implementation_status: rollout
decided_by: 이사님
tags: [agent-mail, telegram, overnight, ideation, candidate]
---

# Telegram 직접 작업과 야간 아이디어 후보 운영

## 결정

이사님은 Telegram에서 `aws-manager` 또는 각 프로젝트 팀장에게 Windows Codex를 거치지
않고 독립된 일을 직접 맡길 수 있다. 이 지시도 구두 세션 기억으로만 처리하지 않고
Agent Mail의 durable intake와 work order로 보존한다.

대상 actor는 정체와 범위를 확인한 뒤 ACK하고, Windows Codex가 오프라인이어도 허가된
범위에서 `submitted`까지 진행할 수 있다. 관제 CODEX는 복귀 후 결과와 근거를 검수해
`verified`와 `closed`를 기록한다. 직접 지시라는 이유로 프로젝트 규칙, commit 고정,
로그인·lease gate, cross-repo 제한 또는 상시 금지를 건너뛰지 않는다.

## 직접 지시의 책임

- Telegram의 인증된 owner는 registry의 `director`다.
- 메시지를 받은 bot route가 하나의 `to_actor`를 결정한다.
- 불명확한 지시는 intake로 보존하고 한 가지 확인 질문을 한 뒤 멈춘다.
- 충분한 지시는 `from_actor=director`, `request_origin=director_telegram`,
  `controller_actor=windows-codex`인 v2 work order로 정규화한다.
- manager가 팀에 나눠 맡기면 child mail은 parent mail과 restrictions를 연결한다.
- project lead는 자기 repo와 capability 안에서만 수행하고 스스로 승인하거나 종결하지 않는다.

## 야간 작업의 재정의

야간 작업은 구현이나 자율 개발이 아니라 **좋은 아이디어를 아침 검토 후보로 쌓는 작업**으로
재정의한다. 대상에는 scenario, RPG, trader 팀을 포함한다. manager는 actor별 후보 전용
work order를 발행하고 아침에 하나의 짧은 브리프로 취합한다.

이 결정은 과거 scenario 저장소 동결이나 일반 야간 개발 중단을 해제하지 않는다. scenario는
검토된 자산을 read-only로 사용해 mailbox 후보만 제안할 수 있다. project Git 수정, 구현,
commit, push 또는 자산 승격은 허용하지 않는다. 과거 cron을 그대로 되살리지 않고 실제
runtime 상태와 중복 여부를 먼저 확인한 뒤 새 schedule로 전환한다.

기존 usable 검증에서 자연히 나온 스토리 부산물을 후보화하는 흐름도 유지한다. 야간 신규
아이디에이션과 usable 부산물은 source를 구분하되 같은 아침 후보함에서 검토할 수 있다.

## 아침 결정

이사님은 각 후보를 다음 중 하나로 결정한다.

- `candidate_approved`: 좋은 아이디어 후보로 보관
- `candidate_held`: 판단을 보류하고 이유와 함께 유지
- `candidate_discarded`: 폐기하되 감사 이력은 보존

immutable proposal은 항상 `status=pending_morning_review`, `decision_*=null`로 보존한다.
승인·보류·폐기는 proposal을 수정하지 않고 `director`의 append-only candidate event로만
기록하며, 현재 상태는 마지막으로 검증된 event에서 계산한다.

승인된 후보도 구현이 승인된 것은 아니다. 모든 candidate와 decision event는
`implementation_authorized=false`를 유지한다. 구현, 실험 코드 작성, 전략 채택 또는 제품
적용을 시작하려면 이사님 또는 관제 CODEX가 `intent=execute`인 별도 work order를 발행하고
정확한 범위와 완료조건을 다시 승인해야 한다.

## 역할

- `director`: 직접 mail 발행, 후보 승인·보류·폐기, 우선순위와 취소 결정
- `aws-manager`: schedule과 child mail 배정, exact duplicate 연결, 아침 브리프 취합
- project lead: 근거가 있는 후보 제안과 제출
- `windows-codex`: 구조·근거·중복 검수, 실행 mail 분리, 최종 work lifecycle 종결
- `aws-audit`: read-only 감사
- `windows-zcode`: 고정 입력의 schema·중복 검토만 수행하고 후보 상태나 Git을 변경하지 않음

## 적용 조건

정본 schema와 정책 작성은 결정 기록 단계다. 다음을 검증하기 전 runtime 자동화 완료로
보고하지 않는다.

1. 실제 AWS schedule과 이전 cron의 read-only inventory
2. mailbox의 intake, claim, immutable event, candidate decision 저장
3. manager와 각 project lead의 no-op 왕복
4. 재시작·retry 중 중복 작업과 중복 후보가 생성되지 않음
5. 후보 승인 뒤 실행 work order가 자동 생성되지 않음

세부 계약은 `projects/agent-ops/README.md`, `mail-v2.schema.json`,
`telegram-intake-v1.schema.json`, `idea-candidate-v1.schema.json`,
`overnight-ideation-v1.md`가 따른다.
