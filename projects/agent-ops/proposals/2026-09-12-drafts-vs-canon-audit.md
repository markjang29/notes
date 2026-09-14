---
title: L0/역할카드 반영분 Post-merge 리뷰 — 채택 배선 누락과 중복 규약
date: 2026-09-12
status: 리뷰 제안 (브랜치 전용, main merge 대기)
reviewer: devpass-code (초안), 이사님 승인 필요
tags:
  - agent-ops
  - review
  - policy
---

# L0/역할카드 반영분 Post-merge 리뷰

ELI5: 매니저가 새 안내문을 아주 잘 썼습니다. 그런데 **게시판에 붙이질 않았습니다.**
그래서 새로 온 봇은 그 안내문이 있는 줄도 모릅니다. 잘 쓴 문서가 안 읽히는 게 이 조직의 반복 병입니다.

## 0. 무슨 일이 있었나

- 이 리뷰 작성 중 `origin/main`이 `638ba66` → **`6f5a0a6`** 로 전진했다.
- 커밋: `agent-ops: L0-agent-common + 역할카드 제도 반영 …` (author markjang29, 2026-09-12 14:58 UTC)
- 신규 11개: `L0-agent-common.md`, `role-card-template.md`, `handoff-contract-01-04.md`,
  `onboarding-structure.md`, `roles/{aws-arcade,aws-asset-agent,aws-codex-dev,aws-novel-col,n100-zcode,windows-zcode}.md`,
  `policy-reread-pending.md` 갱신.
- **`policy-index-v1.json`과 `L0-agent-boot.md`는 변경되지 않았다.**

## 1. 항목별 판정

| 산출물 | 판정 | 사유 |
|---|---|---|
| `roles/*.md` 6카드 + `role-card-template.md` | **채택 권장** | actor_id가 `actors.json` v10과 일치. 기존 `roles/` 양식과 정합 |
| `onboarding-structure.md` | **채택 권장(경량)** | 기존 `new-bot-onboarding.md`의 지도 역할. 단 §3 "새 문서는 지도에 한 줄 추가" 규칙을 스스로 지켰어야 함 |
| `L0-agent-common.md` | **정합화 필요** | 부팅 문서가 `L0-agent-boot.md`·`cokacdir-boot-v2.md`에 이어 3개가 됨. `[CERT]` 신설이 기존 `[ACK]`와 중복 |
| `handoff-contract-01-04.md` | **이름 충돌** | 01~04가 **파이프라인 단계**를 뜻하는데, 실제 내용은 **세션 인수인계 4필드**로 작성됨 |
| `policy-reread-pending.md` | 정상 | 파일럿 6기 CERT 대기 기록 추가 |

## 2. 핵심 결함 (중요도 순)

### F1. 배선 누락 — 새 L0가 아무 데도 연결되지 않음 (치명)
- `L0-agent-boot.md` §3 읽기 순서에 `L0-agent-common.md` 없음.
- `policy-index-v1.json` docs[]에 신규 문서 미등록 → 홈 `/policies` 미표시.
- 결과: 신규 봇은 `L0-agent-boot.md`만 읽고 `[CERT]` 규약을 모른다. **이번 반영의 목적 자체가 무력화.**

### F2. 진입 규약 2개 병존 — `[CERT]` vs `[ACK]`
- 기존: `cokacdir-boot-v2.md` → `[ACK {{ACTOR_ID}} <registry-revision>]`,
  `principles/gwanje-ack-protocol.md`의 ACK 최소필드.
- 신규: `L0-agent-common.md` → `[CERT <actor_id> <notes-head-7자리>]`.
- 둘은 사실상 같은 것. **전 봇이 어느 쪽을 쓸지 모르면 검사 자동화가 불가능.** 하나로 통일 필요.

### F3. handoff 이름/의미 불일치
- 파일명 `handoff-contract-01-04` = 파이프라인 01→04 단계 계약으로 읽힌다.
- 실제 내용 = 근거·미완료·블로커·다음 (세션 인수인계 4필드).
- 실제 파이프라인 전달은 이미 `관제 허브`(`/api/hub/*` task/progress/submitted)가 담당.
- → 이름을 `session-handoff-4field.md`로 바꾸거나 기존 `decisions/2026-08-16-matrix-successor-handoff.md`에 흡수.

### F4. 승인 게이트 없이 main 직행
- `policy-index-v1.json` change_policy: `required_review: director decision or delegated controller review`,
  forbidden: `silent_policy_change`.
- 이번 커밋은 리뷰/승인 기록 없이 main에 반영됨. (담당 봇이 이사님 지시로 했다면 사후 승인 필요)

## 3. 권고 조치 (신규 대문서 없이, 기존 파일 수정만)

1. **F1 배선** (최우선): `L0-agent-boot.md` 읽기 순서에 `L0-agent-common.md` 추가,
   `policy-index-v1.json` docs[]에 신규 4문서 + 역할 카드 6종 등록. → 홈 `/policies`에 뜨게.
2. **F2 통일**: 진입 1줄을 기존 `[ACK <actor_id> <registry-revision>]`로 통일하고
   `[CERT]`는 폐기(또는 ACK의 별칭으로만 명시). 검사기(허브/감사)가 한 형식만 파싱.
3. **F3 개명**: `handoff-contract-01-04.md` → `session-handoff-4field.md` (파이프라인 오해 제거).
4. **F4 게이트**: main 직접 push는 director review 기록 필수. 감사봇이 정책 인덱스 정합성을
   주기 검사(이미 `roles/aws-audit-policy-steward.md` 임무 2·4·5).

## 4. 이 리뷰의 위치

- 이 파일은 **merge용이 아니라 참고 리뷰**다. F1~F4를 기존 파일 수정으로 반영한 뒤 닫는다.
- 소유: F1·F2 → 감사봇(정책 사서) / F3 → 매니저 / F4 → 감사봇+매니저.
- 검증: `policy-index-v1.json`에 신규 문서 존재 + `/policies` 200 표시 + 신규 봇 `[ACK]` 형식 단일화.

## ELI5 (요약)

좋은 안내문을 써 놓고 **안내판에 안 붙였습니다.** 다음 사람은 못 봅니다.
안내판(`policy-index`)에 붙이고, 인사말을 한 가지로 통일하면 끝입니다.
