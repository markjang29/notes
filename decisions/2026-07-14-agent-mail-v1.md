---
title: ADR — Agent Mail v1과 단일 actor registry
date: 2026-07-14
status: rollout
tags: [agents, mailbox, telegram, cokacdir, codex, zcode]
---

# ADR — Agent Mail v1과 단일 actor registry

## 결정

다섯 프로젝트 Git의 전문 지식은 합치지 않는다. 대신 `notes/projects/agent-ops/actors.json`을
논리 정체성·persona·권한 경계의 단일 reviewed seed로 두고, AWS runtime mailbox가 열린 작업과
event를 보존한다. 모든 지시는 Agent Mail work order, 모든 회신은 event로 교환한다.

Telegram/Cokacdir는 사람 대화와 wake/relay, Git은 reviewed 명세와 산출물, REST mailbox는
claim·heartbeat·상태·receipt를 담당한다. Kafka는 현재 규모에서 채택하지 않는다.

## 이유

- 현재 AWS bot 다섯 개는 session을 복원하지만 고정 instructions가 비어 있다.
- identity가 Notes 문서, 각 repo, `bot_settings`, session memory와 runtime JSON에 중복돼 있다.
- approval-board의 `accepted`는 claim일 뿐 agent ACK가 아니다.
- RPG/trader/audit/ZCode의 target과 실제 실행 route가 일치하지 않는다.
- Windows Codex와 ZCode에는 공통 논리 actor가 없었다.

## 새 로컬 persona

- `windows-codex` / **관제 CODEX**: 작업 분해, 배정, 사용자 대화, controller 검수와 통합.
- `windows-zcode` / **검증원 Z**: bounded frozen-input 분석과 exact-file 제안만 수행.

표시명은 사용자가 언제든 바꿀 수 있지만 actor ID와 권한 경계 변경은 별도 registry version으로
기록한다.

## 완료조건

1. AWS 5개와 Windows Codex/ZCode가 독립 `IDENTITY_PROBE`에 ACK한다.
2. 각 Cokacdir 시작 경로와 로컬 skill이 registry version을 읽는다.
3. transaction claim과 immutable event/receipt를 가진 mailbox가 동작한다.
4. 각 actor에 no-op mail 한 건을 보내 `closed`까지 왕복 검증한다.

그 전에는 문서 작성 완료를 조직 통일 완료라고 보고하지 않는다.
