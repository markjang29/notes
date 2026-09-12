---
title: L0 Agent Common
date: 2026-09-12
status: v1
tags:
  - boot
  - agent
  - common
  - role-card
  - pilot-6
---

# L0 Agent Common

모든 actor(봇)가 공통으로 지키는 L0 사칙. `L0-agent-boot.md`(본점 절차)와 병행 읽기.
이 문서는 이사님 2026-09-12 지시로 신설한 **파일럿 6기 역할 카드 제도**의 공통 상위 규정이다.

## 1. 정체와 경계 (L0)

- actor는 `actors.json` 한 곳에서만 정의된다. 이름·provider·workspace·session은 actor를 재정의하지 않는다.
- 부팅마다 레지스트리 명령을 실행해(워킹트리 변경 없이) 자기 actor 항목의
  transport·role·persona·required_refs·capabilities·forbidden을 확인한다.
- 미확인 상태(정체·scope·완료조건 불명)면 결정·commit·발언을 하지 않는다.

## 2. 판본 선언 — [CERT]

- 모든 actor는 작업·보고·회신의 첫 줄에 자기가 읽은 정본 판본을 아래 형식으로 선언한다.

```text
[CERT <actor_id> <notes-head-7자리>]
```

- `정본=<commit>`: 자기가 읽고 판단한 Notes origin/main HEAD 짧은 해시. 예: `정본=638ba66`.
- 부팅 시 `actors.json`의 registry revision(HEAD 해시)과 `[CERT]`의 해시가 같아야 한다.
- 다른 판본을 근거로 한 주장은 그 판본을 명시하지 않으면 증거가 아니다.

## 3. 정책 재독 대장 — policy-reread-pending.md

- 판본이 일치하지 않거나 CERT 응답이 없는 actor는 **`policy-reread-pending.md`** 에 기록한다.
- 기록 형식: 한 줄 1건 — 날짜, actor_id, 대상 문서(또는 판본 불일치), 사유. 재독 확인 후 체크.
- 이 문서의 레코드는 자기 갱신 금지 — 각 actor는 **남의** 미완료 항목만 기록하고, 자기 항목은
  재독 완료 후 `[x]` 체크만 한다.
- 담당: 매니저(`aws-manager`)가 정기 대조. 기록은 근거(실측·커밋 해시)와 함께.

## 4. 역할 카드 제도 (파일럿 6기)

- 각 actor의 상세 경계는 `projects/agent-ops/roles/<actor_id>.md` 역할 카드로 정본화한다.
- 카드는 `role-card-template.md` 양식을 따르며, `actors.json` 필드와 충돌하면 레지스트리가 이긴다.
- **파일럿 6기** (2026-09-12 이사님 지시, actors.json v10 기준):
  `windows-zcode` · `aws-asset-agent` · `aws-arcade` · `aws-novel-col` · `aws-codex-dev` · `n100-zcode`
- 6기 완료 기준: 전원이 `[CERT]` 답장을 남기고, 각자 인용한 `정본=<commit>`이 일치하는 것.
  불일치·무응답 봇은 `policy-reread-pending.md`에 자동 기록한다.

## 5. 인수인계와 온보딩

- 인수인계 계약: `projects/agent-ops/handoff-contract-01-04.md` (4필드 — 근거·미완료·블로커·다음).
- 온보딩 구조·순서: `projects/agent-ops/onboarding-structure.md`.
- 신규 봇 합류 실무는 기존 `projects/agent-ops/new-bot-onboarding.md`를 그대로 따른다.

## 6. 금지 (전 actor 공통)

- 비밀키·쿠키·토큰·세션/채팅 ID·lease 값·사설 raw 소스·기계 로컬 절대경로를
  프롬프트·답장·Git·intake·mail·candidate·event에 넣지 않는다.
- capabilities·routes·results·commits·tests·ACKs·completion을 지어내지 않는다.
- 자기 산출물을 자기 혼자 verified/closed 처리하지 않는다(verified·closed는 authorized controller만).
