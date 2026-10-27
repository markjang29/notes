---
title: "notes 정본 lint 1차 보고 (LLM Wiki 건강검진 시범)"
date: 2026-10-26
auditor: aws-audit
base: notes HEAD 016f4cb
status: reported
tags:
  - audit
  - lint
  - llm-wiki
authority: 이사님 10-26 승인 "고고" (LLM Wiki 적용 ①②)
---

# notes 정본 lint 1차 보고 — 2026-10-26

> Karpathy LLM Wiki 패턴의 Lint 운영 첫 실행(월 1회 목표). 방법: 읽기 전용 스캔
> (인덱스↔파일 대조, ACK 원장 sha256 재계산, 참조 빈도 grep). 정본 수정 없음.

## 요약

구조 정합성(인덱스↔파일)은 양호. 운영 준수(ACK 원장)가 전면 지연 — **전 행 재확인 필요**.
정본 2건에 comm 전환(09-21) 이전 문구 잔존.

## L1 (높음) ACK 원장 — 14행 전부 sha 불일치(재확인 필요)

- 대상 5룰(95-comms-first, 95-speed-autonomy, 95-org-speed, 95-report-addr,
  95-plain-report)의 최신 행 14개 전부 `recorded_doc_sha` ≠ 현재 정본 sha256.
  원인: 95_ 정본 v3 이후 추가 변경(95-4-b 등 09-20~21) 이후 재확인 없음.
- 제출 봇 3개(aws-audit, aws-manager, gmwin-claude)뿐 — roster active 18 중
  **15봇 미제출**. 95-plain-report는 aws-manager 행 부재.
- **권고**: 현재 전 행이 이미 stale라 갱신 비용이 최소인 지금이 정정 적기.
  L2의 95_ 정본 갱신(98 지정 반영)과 함께 **1사이클 전 봇 재ACK** 배치 권장.

## L2 (중간) 정본 간 정합성 — comm 전환(09-21) 미반영 2건

1. `principles/95-comms-autonomy-rules-v1.md` 상호참조에 "통신담당 미지정 — 매니저
   배정 대기" 잔존. 실제: 09-21 전봇 공지로 95-1 1차 수신자 = 98(통신담당) 확정.
2. `principles/entrypoint-comms-progress-rules-v1.md` — NATS/comm 미언급, 8023 중심
   서술. 실제: 8023 신규 발행 금지·comm(NATS) 전환 공지 시행 중.
- **권고**: 두 정본 갱신(이사님/매니저 승인 후). 갱신 시 해당 룰 sha 변화→재ACK 유발은
  설계된 동작(동기화 계약).

## L3 (낮음) policy-index 미등록 — 실질 후보 5건

`ai-dev-신념.md`, `context-budget.md`, `scenario-resources.md`,
`scenario-team-purpose.md`, `references.md` (모두 principles/).
- README.md(안내문)·tmp-wait.md(임시)는 등록 대상 아님으로 판단.
- **권고**: 각 소유자가 인덱스 등록 또는 폐기 결정. scenario 2건은 L4와 중복 지적.

## L4 (낮음) 고아 문서(다른 문서에서 참조 0) — 2건

`scenario-resources.md`, `tmp-wait.md` — 자기 언급만 존재.
- **권고**: 참조 추가 또는 보관 디렉터리 이동/삭제. topics 허브 확산으로 자연 해소 기대.

## 통과 항목

- A1 인덱스→파일: 22건 전부 실존(죽은 ref 없음).
- 인덱스 판본 2026-09-21.1, roster 22봇(active 18) 실측 정상.

## 재현

HEAD에서: policy-index-v1.json의 ref 파일 존재 검사 · rules-acks-v1.ndjson 최신행의
recorded_doc_sha와 정본 sha256 대조 · `git ls-files '*.md' '*.json'` 전문에서
파일명 언급 빈도 집계. 스크립트 부록 없음(감사 세션 내 python 표준 라이브러리 실행).

## 상호 참조

- 원흐름: `projects/agent-ops/research/llm-wiki-karpathy-2026-10.md`
- 다음 lint: 2026-11 말 예정(월 1회) — topics 허브 참조 무결성 포함 확장.
