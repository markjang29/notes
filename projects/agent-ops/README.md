---
title: Agent Mail 운영 정본
status: rollout
updated: 2026-07-14
---

# Agent Mail 운영 정본

이 디렉터리는 프로젝트별 지식을 한곳에 복사하지 않는다. 대신 모든 에이전트가 공통으로
사용할 논리 정체성, 메일형 작업지시 계약, 세션 복구 순서와 rollout 상태만 관리한다.

## 권위 분리

- 조직·논리 actor·persona: `actors.json`
- 작업지시와 회신 형식: `mail-v1.schema.json`
- AWS Cokacdir 세션 부팅 규칙: `cokacdir-boot-v1.md`
- 실행 중 상태: AWS mailbox API(구축 전에는 approval-board request ID)
- 프로젝트 전문 규칙과 산출물: 각 프로젝트 Git
- 사용자 알림·승인·장애 우회: Telegram
- 쿠키·token·Cokacdir key·session ID·lease 원문: Git과 메일 본문 금지

Telegram 메시지는 알림과 대화 수단이지 완료 정본이 아니다. 작업 완료는 mail event,
검증 근거, 필요 시 Git commit을 controller가 확인한 뒤 `verified`와 `closed`로 닫는다.

## 확인된 실제 구성

AWS Cokacdir에는 manager, scenario, RPG, trader, audit 다섯 Telegram agent가 있다. 다섯
bot identity와 long-polling service, restart session 복원은 2026-07-14 실측으로 확인했다.
다만 고정 `instructions`는 모두 비어 있어 표시명·workspace·과거 session에 역할이 분산돼
있다.

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

Windows Codex 새 task는 `windows-codex`로 복구하고 총괄 controller 역할을 갖는다. ZCode는
desktop session 기억을 신뢰하지 않는다. controller가 매 packet에 `windows-zcode` persona와
불변 작업지시를 넣고 bounded bridge receipt로 회수한다.

## 통신 계층

- REST: 등록, inbox, 원자적 claim, heartbeat, event, receipt, controller ACK
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
| R3 시작규칙 | Cokacdir instruction/hook와 로컬 skill에 registry boot 적용 | done |
| R4 mailbox | transaction claim/event/receipt/restore API | pending |
| R5 왕복 | 각 actor에 1개 no-op mail을 보내 closed까지 검증 | pending |

ACK가 끝나기 전 `actors.json`의 `ack_status=pending` actor는 관측된 후보이지 통일 완료로
보지 않는다.
