---
title: Agent Mail 운영 정본
status: rollout
updated: 2026-07-16
---

# Agent Mail 운영 정본

## 공유 Git 권한

Windows Codex는 더 이상 독점 controller·검수자·merge 담당·종결자가 아니다. 등록된 모든
에이전트는 `shared-git-access.md`와 `actors.json`에 따라 모든 등록 저장소에서 직접 작업할
수 있다. controller 지정은 선택 사항이며 해당 작업에만 적용된다.

이 디렉터리는 프로젝트별 지식을 한곳에 복사하지 않는다. 대신 모든 에이전트가 공통으로
사용할 논리 정체성, 메일형 작업지시 계약, 세션 복구 순서와 rollout 상태만 관리한다.

## 권위 분리

- 조직·논리 actor·persona: `actors.json`
- 기존 작업지시와 회신 형식: `mail-v1.schema.json` (v1 기록과 rollout 호환용)
- 새 작업지시와 회신 형식: `mail-v2.schema.json`
- Telegram 직접 지시 intake: `telegram-intake-v1.schema.json`
- 아이디어 후보와 결정 event: `idea-candidate-v1.schema.json`
- 야간 후보 정책: `overnight-ideation-v1.md`
- 이전 Cokacdir 부팅 규칙: `cokacdir-boot-v1.md`
- 현재 배포된 직접 지시·후보 부팅 규칙: `cokacdir-boot-v2.md`
- 실행 중 상태: AWS mailbox API(구축 전에는 approval-board request ID)
- 프로젝트 전문 규칙과 산출물: 각 프로젝트 Git
- 사용자 알림·승인·장애 우회: Telegram
- 쿠키·token·Cokacdir key·session ID·lease 원문: Git과 메일 본문 금지

## Git-first 보고 불변 규칙

공통 사칙은 `notes:principles/git-first-project-truth.md`다. 프로젝트 아이디어·결정·우선순위·
검증 현황은 해당 프로젝트 Git 또는 Notes Git의 commit이 먼저다. Notion과 기타 dashboard는
이사님이 읽기 쉬운 투영일 뿐이며, full commit과 exact ref 없이 내용을 만들거나 상태를
승격할 수 없다. worker 제출, Telegram 대화, mail receipt는 Git 정본을 대체하지 않는다.

controller는 보고 전에 repo, full commit, exact refs, source status, push 여부를 확인한다.
Git에 없는 Notion 내용을 발견하면 투영을 제거·중단하고 해당 actor의 repo/reporting 권한을
fail-closed한다. 상세 절차는 `notes:project-rules/notion-reporting.md`를 따른다.

Telegram 메시지는 알림과 대화 수단이지 완료 정본이 아니다. 작업 완료는 mail event,
검증 근거, 필요 시 Git commit을 controller가 확인한 뒤 `verified`와 `closed`로 닫는다.

## 모델 경로와 사용량 정본

- `aws-manager`, `aws-scenario`, `aws-rpg`, `aws-trader`는 Claude client surface에서 실행하되
  실제 backend/한도는 Z.AI token pool을 사용한다.
- `aws-audit`는 Codex client와 Codex token pool을 사용한다.
- client 이름, 모델 backend, token pool은 서로 다른 축이다. Claude 화면에서 실행됐다는
  이유만으로 Anthropic token 사용량이라고 기록하지 않는다.
- 성능 보고는 actor, client surface, runtime이 노출한 backend/model, token pool,
  input/output/cache token, wall time, 완료 기준 통과 여부를 함께 기록한다. 서로 다른
  backend의 token 수를 품질이나 비용으로 직접 비교하지 않고, 남은 quota를 추정하지 않는다.
- token 값이나 credential 원문은 어떤 정본, 메일, Git, 로그에도 남기지 않는다.

## 확인된 실제 구성

AWS Cokacdir에는 manager, scenario, RPG, trader, audit 다섯 Telegram agent가 있다. 다섯
bot identity와 long-polling service, restart session 복원은 2026-07-14 실측으로 확인했다.
2026-07-15에는 v2 부팅 규칙을 5 actor의 10 chat scope에 적용하고 service, session binding,
Telegram identity와 instruction 반영을 재검증했다. Telegram 직접 지시의 durable intake와
후보 decision event 왕복은 R4/R4.5가 준비되기 전까지 임시 receipt 단계다.

같은 날 과거 야간·아침 schedule이 `aws-manager`가 아니라 `aws-audit`에 잘못 등록돼 identity
gate에서 중단된 사실을 확인했다. 낡은 schedule 네 개와 임시 manager 생성 schedule을 제거하고
bounded candidate run과 `aws-manager` 아침 통합 브리프로 교체했다. 2026-07-16 이사님 직접
지시로 `aws-trader`는 별도 재개 전까지 운영 동결했으며 schedule, 위임, 후보 생성과 브리프에서
제외한다. 현재 active lead는 `aws-scenario`, `aws-rpg` 두 개다. schedule 소유 actor도 실행
권한의 일부로 검증하며, 예약이 존재하거나 일회성 예약이 삭제됐다는 사실만으로 성공을 주장하지
않는다.

기존 approval-board는 manager/scenario만 실제 실행 분기가 있다. RPG·trader는 target으로
접수돼도 실행되지 않고, audit target은 없으며, Telegram agent가 없는 zcode target은 존재한다.
따라서 기존 API는 깨우기/상태 조회용으로만 사용하고 Agent Mail 계약을 그대로 운송하는
정본으로 간주하지 않는다.

사진에서 보인 `회의`는 channel, `BotFather`는 Telegram system, `노트북`은 Arca login
notification으로 분류한다. `모니터codex`는 별도 bot이 아니라 기존 manager/audit session일
가능성이 있어 독립 actor로 등록하지 않는다. `노트북_Zcode`는 `windows-zcode`의 표시 alias로만
두고 transport identity는 ACK 후 확정한다.

## 메일 생명주기

```text
queued -> claimed -> acknowledged -> in_progress -> submitted -> verified -> closed
                     |               |             |
                     +-> blocked     +-> failed    +-> cancelled
```

- `claimed`: router/adapter가 중복 실행권을 획득했다는 뜻이다. 담당자의 수신 확인이 아니다.
- `acknowledged`: `to_actor`가 자기 정체·범위·완료조건을 읽고 수행 가능하다고 회신했다.
- `submitted`: worker/팀장이 결과를 냈지만 controller 검증 전이다.
- `verified`, `closed`: controller만 기록한다.
- 모든 event는 work-order digest, attempt, idempotency key, 선택적 packet digest, 연속 sequence,
  직전 event ID를 묶는다. actor 권한이나 상태 전이가 맞지 않으면 새 세션에서도 복구 근거로 쓰지 않는다.

## 새 세션 복구 순서

1. runtime transport identity를 `actor_id`로 해석한다.
2. `actors.json`의 persona와 필수 규칙을 읽는다.
3. mailbox에서 자신이 담당한 열린 mail과 마지막 event를 읽는다.
4. `input_commit`, dependency, lease/expiry를 다시 검증한다.
5. 정체가 없거나 충돌하면 작업하지 않고 `identity_error`를 회신한다.
6. 이전 결과를 다시 실행하지 말고 마지막 검증된 event 다음부터 재개한다.

Windows Codex 새 task는 `windows-codex`로 복구하되 독점 controller 권한을 되살리지 않는다.
ZCode 역시 `windows-zcode`로 복구하며, 등록된 모든 저장소에서 직접 작업·commit·push할 수
있다. 세션 기억은 권한 근거가 아니며 현재 registry와 저장소 규칙을 다시 읽는다.

## Windows Codex 병렬 task 관제

메인 Codex task는 요청받았을 때 director와의 대화, 목표·우선순위 관리, 작업 분해·배정,
상태 관제를 맡을 수 있지만 다른 actor의 Git 작업·검수·종결을 독점하지 않는다. 30분 이상 걸릴 것으로 보이거나 독립
commit·문서·분석 보고서 등 별도 산출물이 있는 실행은 사용자에게 보이는 별도 Codex task로
만든다. 메인 task가 그 실행을 직접 오래 수행하거나 사용자에게 보이지 않는 worker로 대체하지
않는다.

짧은 읽기 전용 검사와 결정적 검증은 bounded subagent 또는 `windows-zcode`에 맡길 수 있다.
이 경우에도 메인 task 화면에는 최소한 `owner`, `state`, `deadline`, `last_evidence`,
`next_action`을 투영한다. 내부 worker의 세션·route 이름은 소유권이 아니며, 책임 actor와
controller는 계속 registry와 work order로 결정한다.

모든 별도 task와 내부 worker packet은 실행 전에 다음을 고정한다.

- 논리 `repo_id`와 full 40-character `input_commit`
- exact read/write scope와 금지 동작
- 관찰 가능한 `done_criteria`와 `approval_policy`
- stable `idempotency_key`, `attempt`, 선행 dependency와 필요 skill ref

ACK는 완료 증거가 아니라 SLA의 시작점이다. 담당 actor가 `acknowledged`하고 실행을 시작한
시각부터 10분 안에 first evidence를 남긴다. 20분까지 새 durable evidence가 없으면
`health=stalled`, 30분까지 회복되지 않으면 담당 coordinator가 `auto_reroute`할 수 있다.
`controller_review` 작업은 `submitted`에서 멈추고 지정 reviewer가 검수한다. 검수가 필요 없는
`approval_policy=none` 작업은 담당 actor가 동일 기준을 확인한 뒤 `verified`, `closed`를 기록한다.

capacity, session crash, route missing, thread slot, quota 오류는 사용자 의미 결정이 아니라
controller 복구 사건이다. checkpoint의 full input commit, exact refs, last durable evidence,
idempotency key, attempt, writer lease/fence와 `next_action`을 보존하고, 이전 writer를 종료하거나
fence한 뒤 capability-compatible route에서 재개한다. 가능한 route가 남아 있는 동안 director에게
같은 작업을 다시 설명하거나 새 idempotency key로 중복 실행을 만들지 않는다.

## Telegram 직접 작업

사용자는 manager 또는 project lead의 Telegram bot에 독립된 일을 직접 맡길 수 있다.
인증된 owner 메시지는 `director`가 보낸 것으로 해석하되 곧바로 자유 형식 실행으로 넘기지
않는다.

```text
owner message
  -> sanitized durable intake
  -> clarification or Agent Mail v2 work order
  -> target ACK -> work -> submitted
  -> configured review policy -> verified -> closed
```

- bot route는 정확히 한 `to_actor`를 결정한다.
- 불명확한 지시는 `needs_clarification`으로 보존하고 한 가지 질문 뒤 실행을 멈춘다.
- 정규화된 mail은 `from_actor=director`, `request_origin=director_telegram`을 사용한다. 별도
  검수가 필요하면 어떤 capable actor든 `controller_actor`가 될 수 있고, 필요 없으면 target
  자신을 지정하고 `approval_policy=none`을 사용한다.
- Windows Codex의 온라인 여부는 target의 직접 Git 작업 권한과 무관하다.
- manager가 일을 나누면 child mail은 `request_origin=delegated`와 `parent_mail_id`로 원 지시를
  연결한다.
- 직접 지시는 actor capability, repo 규칙, exact scope, commit, login·lease gate 또는 상시
  금지를 확대하지 않는다.
- R4가 없을 때 `[DIRECT PENDING <actor>]` 회신은 임시 증거일 뿐이다. 지정된 Git-capable actor가
  sanitized transport receipt digest를 idempotency key에 묶어 intake, mail, candidate를
  정확히 한 번 정본화한다. 대상 actor는 가짜 ID를 만들거나 스스로 backfill하지 않는다.

## 아이디어 후보 생명주기

야간 아이디에이션과 usable 검증 부산물은 구현물이 아니라 candidate로 저장한다.

```text
immutable proposal(status=pending_morning_review)
  -> candidate_created
     |-> candidate_approved
     |-> candidate_held
     +-> candidate_discarded
```

- proposal의 `status`와 `decision_*`를 수정하지 않는다. 현재 결정 상태는 검증된 append-only
  candidate event chain의 마지막 event에서만 계산한다.
- project lead는 `candidate_propose`, manager는 `candidate_curate` 범위에서만 작업한다.
- manager는 exact duplicate를 연결하고 아침 브리프를 만들지만 승인하거나 폐기하지 않는다.
- 후보 결정은 `director`만 기록한다.
- `candidate_approved`는 backlog 보관 승인이지 구현 허가가 아니다.
- candidate와 decision event의 `implementation_authorized`는 항상 `false`다.
- 구현은 `intent=execute`인 별도 work order와 controller 검수 없이는 시작할 수 없다.
- candidate-only mail은 project Git 쓰기, commit, push, 배포, 외부 송신, 실거래, 전략 채택,
  자산 승격과 자동 구현을 금지한다.
- R4 저장소는 후보 1건 완료조건인 mail에 candidate receipt가 정확히 1개만 연결되도록
  cardinality와 idempotency를 transaction으로 강제한다.

기본 야간 운영과 중복·재시작 규칙은 `overnight-ideation-v1.md`를 따른다. 과거 schedule을
그대로 재활성화하지 않으며 실제 runtime inventory와 no-op 왕복 뒤에만 enabled로 표시한다.

## 통신 계층

- REST: intake, 등록, inbox, 원자적 claim, heartbeat, event, candidate decision, receipt,
  controller ACK
- SSE 또는 long polling: 상태 변경 알림
- Telegram/Cokacdir: 사람 알림, 질문, 장애 시 relay
- Git: 검토된 명세·프로필·산출물

현재 규모에서는 Kafka를 사용하지 않는다. REST와 transaction 저장소로 부족하다는 실제
부하 근거가 생겼을 때만 SQS/queue를 추가한다.

## rollout gate

| 단계 | 완료조건 | 상태 |
|---|---|---|
| R0 인벤토리 | 실제 agent, service, route 검증 | done |
| R1 정본 | registry, schema, identity probe Git push | done |
| R2 자기확인 | AWS 5개 + Windows Codex/ZCode ACK | done |
| R3 시작규칙 | Cokacdir instruction/hook와 로컬 skill에 registry boot v1 적용 | done |
| R3.5 v2 정본 | direct intake, mail v2, candidate, 야간 정책 작성 | done |
| R3.6 v2 부팅 | Cokacdir boot v2 적용과 identity probe | done (direct durable intake는 R4에서 검증) |
| R4 mailbox | transaction claim/event/receipt/restore API | pending |
| R4.5 후보함 | immutable candidate decision과 schedule run 저장 | pending |
| R5 왕복 | 각 actor no-op과 야간 후보·아침 결정 왕복을 closed까지 검증 | pending |

ACK가 끝나기 전 `actors.json`의 `ack_status=pending` actor는 관측된 후보이지 통일 완료로
보지 않는다.
