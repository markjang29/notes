---
title: 초안 vs 기존 정본 감사 — 신규 생성 대신 기존 정본 채택 제안
date: 2026-09-12
status: 제안 (브랜치 전용, main merge 대기)
author: devpass-code (초안), 이사님 검토
tags:
  - agent-ops
  - audit
  - policy
  - adoption
---

# 초안 vs 기존 정본 감사

ELI5: 새 규칙책을 만들려고 보니 **책장에 이미 다 꽂혀 있었습니다.** 문제는 책이 없어서가 아니라,
봇들이 그 책을 안 펴본다는 것이었습니다. 그래서 새 책 4권은 넣지 말고, **이미 있는 책을 강제로 펴게
하는 장치**만 붙이자는 제안입니다.

## 1. 결론

- 이사님 지시로 만든 기본 지시 초안 4종(L0 공통 / 역할 카드 템플릿 / 01→04 핸드오프 / 온보딩 구조)은
  **기존 정본과 대부분 중복**이다. 그대로 신규 문서로 추가하지 않는다.
- 진짜 격차는 "문서 부재"가 아니라 **배포·강제·검증(adoption)** 이다.
- 이 문서는 그 격차만 남기고, 소유자·기존 산출물을 지정하는 채택 계획이다.

## 2. 중복 감사 (초안 → 기존 정본)

| 초안 (이번 작업) | 기존 정본 | 판정 |
|---|---|---|
| `L0-agent-common.md` | `L0-agent-boot.md`(정체·역할경계·읽기순서), `agent-rules.md`(공용 규칙·NEVER), `projects/agent-ops/cokacdir-boot-v2.md`(actor·mail·secrecy) | **중복** — 신규 금지. 기존 3문서가 상위 호환 |
| `role-card-template.md` | `projects/agent-ops/roles/*.md` (예: `aws-audit-policy-steward.md`, `heav_firebat_zcode_bot.md`) | **부분 중복** — 카드 양식은 기존 문서 톤으로 통일 |
| `handoff-contract-01-04.md` | `gwanje-hub-rest-queue-v1.md`(`/api/hub/*` REST 큐, 타입·상태머신·멱등키·DLQ), `mail-v2.schema.json`, `task-contract-v1.md`(7필드), `hub-payload-schema-v1.md` | **중복·하위 호환** — 신규 스키마 금지. 기존 허브 계약 사용 |
| `onboarding-structure.md` | `projects/agent-ops/README.md`, `new-bot-onboarding.md`, `org-charter-v1.md`, `policy-index-v1.json`, `roster.json`/`actors.json` | **중복** — 신규 금지 |
| ELI5 형식 추가(`🧒 ELI5:`) | `eli5-glossary.md` — ELI5가 **이미 기본값**, 규칙=`첫 줄 결론 → 비유 먼저·실명 괄호 → 숫자 3개 이하 → 한 보고 한 주제` | **중복** — 신규 형식 금지. 기존 규칙 준수 |

## 3. 이미 있는데 안 쓰이는 것 (정본 목록)

- 정체 확인: `L0-agent-boot.md` §1, `actors.json`(v10), `cokacdir-boot-v2.md` §Boot, `new-bot-onboarding.md` §0
- 봇 간 통신: `관제 허브 v1` `/api/hub/*` — task만 wake, notice는 문맥 주입, ACK/DLQ/멱등키 구현·실측 완료
- 작업 지시 표준: `task-contract-v1.md` 7필드 ("이 7칸 없으면 배정 금지")
- 판본 도장: `policy-index-v1.json` + `POLICY_SHA`(Notes HEAD)
- 정책 사서(상담사 역할): `roles/aws-audit-policy-steward.md` — **이미 존재**
- ELI5: `eli5-glossary.md` (기본값 선언 완료)
- 완료 검증: `principles/audit-watchdog-foundation.md`, `principles/gwanje-ack-protocol.md`, `git-first-project-truth.md`

## 4. 진짜 격차 (초안이 지적한, 아직 장치 없는 것)

| 격차 | 근거 | 제안(신규 문서 아님) |
|---|---|---|
| **G1 부팅 주입 강제 없음** | 봇이 L0를 "읽어야" 하나 안 읽어도 통과. `COKACDIR recovery gate`는 일부 엔진에만 존재 | 기존 `cokacdir-boot-v2` 템플릿을 전 엔진 SessionStart 훅으로 승격. 미주입 시 프롬프트 차단(기존 gate 재사용) |
| **G2 보고 판본 검사 없음** | POLICY_SHA를 "적으라"만 하고, 안 적거나 stale이어도 통과 | 허브/ACK 파서가 `POLICY_SHA` 누락·불일치를 자동 반려(기존 `gwanje-ack-protocol`에 검사만 추가) |
| **G3 역할 카드 미비** | `roles/`에 01~04·매니저·허브 카드 없음(핸드오버 문서 위주) | 기존 `roles/*.md` 양식으로 6장 작성. `actors.json`이 사실 원천 |
| **G4 봇 기계 .md 직접 편집** | 환경마다 사본 편집→드리프트 | 기계에서는 canon **읽기 전용**. 수정은 허브 task로 정책 사서(aws-audit)에 제안, Notes commit만 정본 |
| **G5 정본 commit 보고 규율** | 이사님이 "항상 규칙 정본 마지막 commit 답장" 지시했으나 미정착 | G2와 동일 장치로 흡수 |

## 5. 채택 계획 (신규 문서 0, 기존 자산만)

1. **aws-audit(정책 사서)** — G1~G3 소유. 기존 `cokacdir-boot-v2`·`gwanje-ack-protocol`·`roles/`를 고쳐서
   장치화. 신규 파일 생성 금지, 기존 파일 수정만.
2. **codex_dev_1(허브 오너)** — G2를 `/api/hub` ACK 검사에 추가(정책 신규 아님).
3. **매니저** — G4를 전 봇 공지 + `shared-git-access.md`에 "기계 사본 편집 금지" 한 줄 추가.
4. **이사님** — 아래 정정 문장 3건만 전달. 이후 반복 설명 불필요.

## 6. 이번 작업의 산출물 처리

- `agent_ops/`의 초안 4종은 **merge하지 않는다.** 필요한 미세 델타만 기존 파일에 흡수:
  - 역할 카드: 기존 `roles/*.md` 양식 확인 후 6장 작성
  - 핸드오프: 기존 허브 계약 사용, 01→04 아티팩트 "이름"만 `hub payload`로 매핑
  - ELI5: `eli5-glossary.md` 규칙 준수(신규 형식 금지)
- 이 문서는 감사 기록으로만 보존한다.

## ELI5 (요약)

책은 이미 다 있습니다. 새 책을 쓰지 말고, **안 펴보면 다음 일을 못 하게 잠그는** 것만 하면 됩니다.
그 잠금은 감사봇(사서)과 허브(접수창구)가 이미 있는 도구로 붙일 수 있습니다.
