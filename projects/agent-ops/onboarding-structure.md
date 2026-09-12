---
title: 온보딩 구조 (onboarding structure)
date: 2026-09-12
status: v1
tags:
  - onboarding
  - structure
  - agent-ops
---

# 온보딩 구조 — 문서 계층과 읽는 순서

> 모든 신규·기존 actor의 온보딩 자료가 어디에 무엇이 있는지 정의하는 지도 문서.
> 실제 합류 절차(폴러 연결·합류 시험)는 `new-bot-onboarding.md`가 담당하고, 이 문서는
> **무엇을 어디서 읽게 할지의 구조**를 규정한다.

## 0. 계층 — 온보딩 문서 3층

| 층 | 대상 | 문서 | 역할 |
|---|---|---|---|
| L0 공통 | 전 actor | `L0-agent-boot.md` · `L0-agent-common.md` | 부팅 절차·정체 확인·[CERT]·판본·공통 금지 |
| L1 조직 | 전 actor | `projects/agent-ops/README.md` · `actors.json` · `ORG-RULES.md` · `org-structure.md` | 메일 생명주기·권위·토폴로지·거점/배당 |
| L2 개별 | actor 단위 | `roles/<actor_id>.md` + 각 repo 사칭(AGENTS/HARD_RULES 등) | 그 actor의 경계·업무·보고·완료 판정 |

## 1. 읽는 순서 (신규 actor 표준)

1. 레지스트리 확인 — 부팅 명령 실행, 자기 actor 항목과 `정본=<commit>` 확정.
2. L0 공통 — `L0-agent-boot.md` → `L0-agent-common.md`. (L1/L2는 이후. 전문 재독 금지 원칙 유지)
3. L1 조직 — `projects/agent-ops/README.md`의 "메일 생명주기"·"Git-first 보고 불변 규칙".
4. L2 개별 — 자기 `roles/<actor_id>.md`. 없으면 `role-card-template.md`로 만들어 정본화.
5. 자기 repo 사칭 — required_refs가 가리키는 문서.
6. 실무 합류 — `new-bot-onboarding.md` (git 기초 → 관제 이용 → 폴러 합류 → 합류 시험).
7. 입장 보고 — `[ACK <actor_id> <registry-판본>]` 한 줄. 그 다음부터 결정·commit·발언 허용.

## 2. 인수인계 연결

- 기존 actor가 바뀌거나(퇴사·교체) 인계받을 때는 온보딩 순서에 더해
  `handoff-contract-01-04.md` 4필드(근거·미완료·블로커·다음)를 먼저 읽는다.
- 후계자 수려 사례: `decisions/2026-08-16-matrix-successor-handoff.md` —
  인계 문서 전독 → `[MATRIX-SUCCESSOR-CERT]` 출력 → 역할 경계 재검증 → 카드 실행.


## 3. 구조 규칙

1. 온보딩 내용은 층에 맞는 문서에만 둔다. L0에 특정 actor 사례를 적지 않고, L2에 공통 사칭을 복사하지 않는다.
2. 충돌 시 우선순위: actors.json > L0 > L1 > L2 > (그 외). 단 L0·L1·L2 모두 레지스트리에 종속.
3. 새 문서 추가 시 이 지도의 표에 한 줄 추가가 원칙 — 지도 없는 문서는 온보딩 자료가 아니다.
4. 판본 불일치·미독 actor는 `policy-reread-pending.md`에 기록하고 재독을 확인한다.
