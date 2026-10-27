---
title: "주제 허브 — 통신 (topics 1호, LLM Wiki 허브 시범)"
date: 2026-10-26
status: active
tags:
  - topics
  - communication
  - hub
authority: 이사님 10-26 승인 "고고" (LLM Wiki 적용 ④ 허브 시범)
maintainer: aws-audit (lint 시 참조 무결성 점검)
---

# 주제 허브 — 통신

> "주제로 훑는 입구". 사칙·프로토콜·구현·원장이 사방에 흩어져 있어
> 통신 주제 하나로 모은 허브 페이지다. 정본은 각 링크 파일 — 이 페이지는 색인.

## 사칙·프로토콜 (정본)

- `principles/95-comms-autonomy-rules-v1.md` — 95_ 사칙: 선문의(95-1)·시도기록(95-2)·
  속도 자율(95-3)·담당주소(95-4)·쉬운 보고(95-5). 1차 수신자 = 98(통신담당).
- `principles/telegram-comm-protocol-v1.md` — 통신표준 v1 (comm 전환, 09-21).
- `principles/entrypoint-comms-progress-rules-v1.md` — 진입점·폴링·진행보고 (8023 시대 —
  **comm 전환 미반영, lint L2 지적**).
- `principles/gwanje-ack-protocol.md` — ACK = 이해의 서명.
- `L0-agent-common.md` §6 — 부팅 시 comm 미수신 확인·즉시 ACK·실명 발신·토큰은 경로만.

## 구현·도구

- `projects/agent-ops/comm/comm_client.py` — comm 클라이언트 원본(각 봇 복사 사용).
- 구(舊) 8023 허브 — 신규 발행 금지(09-21 공지), 기존 큐 소진까지만 예외.

## 원장 (상태는 각 원장이 정본)

- `projects/agent-ops/rules-acks/rules-acks-v1.ndjson` — 사칙 ACK 원장
  (2026-10-26 lint: 전 행 재확인 필요).
- `projects/agent-ops/report-addresses.json` — 담당 주소 원장 (95-4-a).
- `projects/agent-ops/policy-index-v1.json` — 사칙·정책 인덱스.

## 열람 화면

- http://43.201.34.144:8024/rules — 사칙 원장·ACK 현황 (정본 투영)
- http://43.201.34.144:8024/comm — 통신 이력

## 감사 기록

- `projects/agent-ops/audits/notes-lint-2026-10.md` — lint 1차(본 주제 L1·L2 지적 포함).
- `projects/agent-ops/research/llm-wiki-karpathy-2026-10.md` — 허브 도입 배경.

## 유지 규칙

- 통신 관련 정본이 새로 생기거나 바뀌면 커밋하는 봇이 이 페이지 항목도 함께 갱신
  (ingest 절차 제안 참조 — research 문서 채택 4항).
- 링크 대상은 항상 repo 상대경로. 이 페이지는 색인일 뿐 내용 중복 금지.
