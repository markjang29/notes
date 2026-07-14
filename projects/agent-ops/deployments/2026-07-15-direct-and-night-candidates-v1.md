---
title: Direct work and overnight candidates rollout
status: active-with-gates
date: 2026-07-15
authority: projects/agent-ops/deployments/2026-07-15-direct-and-night-candidates-v1.md
---

# Direct work and overnight candidates rollout

## 적용 결과

- Cokacdir boot v2를 AWS의 5 actor, 10 chat scope에 적용했다.
- service 재시작, settings mode 600, session binding 보존, Telegram identity 5/5와 instruction
  반영을 확인했다.
- 사용자가 manager 또는 lead Telegram에 직접 맡긴 일은 `director -> target` 독립 작업으로
  유지하며 manager와 Windows Codex가 소유권을 가져가지 않도록 정본·skill·boot에 반영했다.
- `scenario-176786718-idea-20260715`(한 끼의 약속)과
  `scenario-110558063-idea-20260715`(사라진 어제의 아이)를 approval-board의 pending 후보로
  복구했다. 둘 다 구현 권한은 없으며 후자는 RCC-110558063 REPO 인증 gate를 유지한다.

## schedule 장애와 교정

과거 manager 업무 schedule 세 개가 audit bot 소유였고, 별도 scenario 자율창작 schedule 하나도
낡은 규칙을 사용했다. 2026-07-15 01:00 실행은 audit identity가 권한 부족을 올바르게 감지해
`identity_error`로 중단됐다. 낡은 schedule 네 개는 제거했다.

초기 누락분 catch-up은 manager가 R4 부재를 보완하려다 저장소 전반 교차 탐색으로 범위를
넓혔다. controller는 488,834ms에 해당 child만 종료했고 transport는 exit 143/error를 기록했다.
이 실행은 후보 receipt가 없으므로 실패다. transport가 기록한 35개 model response의 합계는
input 285,060, cache-read 1,007,360, output 105,712 tokens였다. 요금이나 quota는 이 수치에서
추정하지 않는다.

실패 뒤 runtime은 다음처럼 교체했다.

- 01:00 `aws-scenario`: 후보 최대 1건
- 01:05 `aws-rpg`: 후보 최대 1건
- 01:10 `aws-trader`: 후보 최대 1건
- 07:00 `aws-manager`: 세 actor receipt와 pending 후보만 통합
- `aws-audit`: 야간·아침 schedule 없음

각 lead는 180초·read-only tool 4회·reviewed source 1개·800자 receipt, manager는
120초·read-only tool 4회로 제한한다. recursive 탐색, web, nested agent, repo write와 구현은
금지한다. R4 전에는 actor별 결과를 `[CANDIDATE PENDING <actor>]` 또는
`[NO CANDIDATE <actor>]` 임시 receipt로만 남긴다. runtime manifest는 Git 밖에서 mode 600으로
관리한다.

Windows Codex에는 매일 07:10 KST heartbeat 관제를 등록했다. 직전 run의 시작, actor identity
ACK, candidate 또는 no-candidate receipt, 종료 상태를 확인하고 이상과 승인 후보만 보고한다.

## 남은 gate

- R4 transactional mailbox는 아직 없다. 직접 Telegram 작업과 scheduled receipt는 durable
  mail/event가 아니라 임시 transport evidence다.
- R4.5 immutable candidate/run store가 아직 없어 approval-board는 임시 표시판이다.
- lead 3개와 morning curator의 첫 실제 bounded 왕복은 다음 schedule 실행 뒤 검증해야 한다.
- Cokacdir service가 bot token을 process argument로 넘겨 같은 OS 사용자의 process listing에
  노출될 수 있다. token을 Git에는 기록하지 않았지만, BotFather rotation과 process argument가
  아닌 restricted credential loading으로 이전해야 한다.
