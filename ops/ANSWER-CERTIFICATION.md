---
title: 질문–AI 답변 근거 인증제
date: 2026-08-02
status: accepted
version: v1
authority: director
decision_ref: decisions/2026-08-02-ai-answer-certification.md
integration_status: pending-main
---

# 질문–AI 답변 근거 인증제

## 한 줄 원칙

**Director가 질문하면 AI는 결론만 말하지 않고, 중요한 주장마다 무엇을 어디까지 확인했는지를 함께 표시한다. 인증은 AI가 자기 답을 참이라고 선언하는 도장이 아니라 근거·시점·검증자를 묶은 증명서다.**

이 규칙은 Codex, ZCode, Claude 같은 제품명이나 세션 이름과 무관하다. 답변자는 현재 운영체계가 확인한 식별자만 사용한다.

- Agent Mail 경로는 같은 Notes commit의 `projects/agent-ops/actors.json`에서 `actor_id`를 확인한다.
- v2 작업 계약 경로는 같은 Notes commit의 `ops/registry.json`과 대상 프로젝트 `WORK.md`에서 `executor_ref`를 확인한다.
- `ops/registry.json`이 `shadow-only`인 동안에는 명시적으로 검증된 v2 작업 계약이 없는 실행자를 그 파일만 보고 인증자로 삼지 않는다.
- 한 인증 기록 안에서 두 등록 체계의 식별자를 섞지 않고 `identity_registry_ref`를 함께 적는다.

## 서로 섞지 않는 네 가지

다음 네 축은 독립적으로 기록한다.

1. **사실 검증:** 답변의 중요한 사실이 어느 수준까지 확인됐는가.
2. **최신성:** 언제 어떤 범위에서 확인했고 다시 확인해야 하는가.
3. **Director 판단:** 취향·방향·우선순위처럼 AI가 대신 확정할 수 없는가.
4. **실행 권한:** 질문이 아니라 별도 작업 계약이 수정·commit·push·배포를 허용했는가.

Director의 동의가 사실을 자동으로 참으로 만들지 않는다. 반대로 AI가 사실을 검증했어도 Director의 취향·결정이나 실행 권한을 대신하지 않는다. **질문은 실행 허가가 아니며 답변 인증도 실행 허가가 아니다.**

## 인증 등급

| 등급 | 이름 | 의미 |
|---|---|---|
| `C0` | 미검증 | 기억, 추정, 전달받은 보고 또는 아직 직접 확인하지 않은 주장 |
| `C1` | 근거확인 | 답변자가 고정된 원문, 원격 Git SHA, 공식 자료 또는 실제 파일을 직접 확인 |
| `C2` | 재현확인 | 답변자가 고정 입력으로 검사·테스트·실행을 재현하고 결과를 확인 |
| `C3` | 독립인증 | 답변자와 다른 등록 실행자가 같은 질문, 답변 digest와 근거를 다시 검증 |
| `MIXED` | 혼합 | 중요한 주장들의 등급이 서로 달라 주장별 표시가 필요한 답변 |

- `의견`, `제안`, `모름`은 사실 인증 등급이 아니다. 각각 그대로 표시한다.
- 추론은 근거보다 높은 등급을 받을 수 없다.
- 같은 논리 `actor_id` 또는 `executor_ref`의 다른 세션과 그 답변자가 만든 임시 하위 에이전트는 `C3` 검수자로 인정하지 않는다.
- 결론을 떠받치는 `fact`와 `inference`를 중요한 주장으로 센다. 모두 같은 등급일 때만 그 등급을 전체 판정으로 쓰고, 서로 다르면 `MIXED`와 최저 중요 주장 등급을 함께 표시한다.
- 테스트 통과는 그 테스트가 측정한 사실만 인증한다. 의미·품질·재미·취향까지 인증하지 않는다.
- `C3`는 독립성만 추가하는 이름이 아니다. 정적 사실은 두 실행자가 같은 불변 원문을 직접 확인하고, 동작·런타임 주장은 답변자와 해당 capability를 가진 검수자가 고정 입력이나 보호된 영수증으로 재현해야 한다. 검수자가 답변문만 다시 읽는 것은 `C3`가 아니다.

## 필요한 최소 등급

| 답변 종류 | 최소 표시 |
|---|---|
| 아이디어·추천·감상 | `의견` 또는 `제안`; 사용한 사실은 별도 등급 표시 |
| 파일 존재, 스키마 내용, Git 상태 | `C1` |
| 코드 동작, 파서 결과, 결정적 컴파일 | `C2` |
| 완료, 보안 봉쇄, 자산 승격, 릴리스, 배포, 8011·8012 실제 사용 | 런타임 또는 결정적 재현을 포함한 `C3` |
| 제품 재미, 표현, 체감 합격, 우선순위 | `Director 판단 필요` |

필요 등급을 얻지 못했어도 답변을 숨기지 않는다. 확보한 실제 등급으로 답하고 미확인 항목과 다음 검증 행동을 적는다.

## 질문에서 답변까지

```text
Director 질문
  → 질문인지 실행 요청인지 구분
  → 중요한 주장과 필요한 등급 결정
  → 고정된 근거 확인
  → 답변과 주장별 인증 표시
  → 필요할 때 다른 등록 실행자가 독립 검증
  → Director 판단은 별도 결정으로 기록
  → 실행은 별도 작업 계약으로만 시작
```

- 같은 대화 안의 가벼운 질문은 `qa_id`를 생략할 수 있다.
- 다른 실행자에게 넘기거나 Git에 보존할 답변은 안정적인 `qa_id`, `question_digest`, `answer_digest`를 사용한다.
- `C3` 요청은 검수자가 실제 답변을 읽을 수 있도록 불변 `answer_ref`를 함께 고정한다. digest만 전달하는 요청은 인증할 수 없다.
- 답변 문구가 바뀌면 `answer_digest`도 바뀌므로 이전 인증을 재사용할 수 없다.
- 중요한 답변만 Git에 보존한다. 일상 대화와 단순 확인을 모두 파일로 만들지 않는다.
- 프로젝트 방향·설계·승격·완료 판단의 근거가 되는 답변은 해당 프로젝트 Git에 둔다. 여러 프로젝트에 걸친 운영 질문은 Notes Git에 둔다.

digest를 다른 환경에서 재현할 때는 질문 또는 답변 본문만 대상으로 삼는다. 인증 표 자체는
`answer_digest`에서 제외한다. Unicode는 NFC, 줄바꿈은 LF로 정규화하고 각 줄의 끝 공백과
본문 앞뒤 빈 줄을 제거한 뒤 BOM 없는 UTF-8 bytes의 SHA-256을 계산한다. 질문에 비밀이나
capability URL이 들어 있으면 원문을 hash하지 말고 민감 부분을 `[REDACTED]`로 바꾼 안전한
질문 본문을 먼저 만든 뒤 그 본문을 hash한다.

## 최신성 규칙

- `현재`, `최신`, `지금 작동한다`는 주장에는 `checked_at`과 `as_of`가 없으면 `C1` 이상을 붙이지 않는다.
- Git 근거는 원격에 존재하는 40자리 commit과 저장소 상대경로로 고정한다.
- 서비스 상태는 Git만으로 인증하지 않는다. 시각이 있는 런타임 영수증이 필요하다.
- 변동 정보는 `valid_until` 또는 `check_on_use=true`를 표시한다.
- 근거 commit, 배포, 파일 또는 답변 내용이 바뀌면 이전 인증은 `expired` 또는 `superseded`다.

## 사용자에게 보이는 기본 형식

일반 답변은 짧게 표시한다.

```text
[답변 인증: C1 근거확인 | 기준: <짧은 근거> | 미확인: <없음 또는 항목>]

<쉬운 말로 답변>
```

혼합 답변, 완료·보안·배포·승격 판단 또는 다른 실행자에게 넘길 답변은 전체 형식을 사용한다.

```text
[AI 답변 인증]
qa_id: <ID>
identity_registry_ref: <Notes 40자리 commit과 registry 상대경로>
답변자: <해당 registry의 actor_id 또는 executor_ref>
독립 검수자: <C3일 때 답변자와 다른 등록 ID, 아니면 없음>
question_digest: sha256:<64 hex>
answer_ref: <불변 Git 또는 receipt ref>
answer_digest: sha256:<64 hex>
전체 판정: C0 | C1 | C2 | C3 | MIXED
최저 중요 주장: C0 | C1 | C2 | C3 | 해당 없음
확인 시각: <ISO 8601과 시간대>
유효 범위: <repo/commit/runtime/source scope>
근거: <안전한 ref 목록>
추론·제안: <없음 또는 명시>
미확인: <없음 또는 명시>
Director 판단: 해당 없음 | 필요 | 확정
실행 권한: 없음 — 별도 작업 계약 필요

[답변]
<결론을 먼저 쉬운 말로 작성>

[주장별 인증]
- claim-1 | fact | C2 | deterministic_reproduction | <근거> | <한계>
- claim-2 | inference | C1 | source_inspection | <근거> | <한계>
```

Git·Agent Mail에 넣는 근거 ref는 다음 안전 형식만 사용한다.

```text
git:<repo_id>@<40자리 commit>:<repo 상대경로>#sha256:<64 hex>
receipt:<안전한 receipt id>#sha256:<64 hex>
source:<안전한 source id>#sha256:<64 hex>
```

raw URL, URL query·fragment, 로컬 절대경로와 `..` 경로는 ref에 넣지 않는다. 공개 웹 자료는
사용자 답변에서 안전한 공개 링크로 보여 줄 수 있지만, 영속 인증 기록에는 별도 `source_id`와
내용 digest를 사용한다. 이 v1은 공용 보고 규칙이며 보안 validator라고 주장하지 않는다.
기계 강제 스키마와 반례 테스트는 별도 구현 작업에서 함께 도입하기 전까지 정본으로 간주하지 않는다.

## 독립 인증 요청 형식

```text
[ANSWER CERTIFICATION REQUEST]
qa_id: <ID>
question_digest: sha256:<64 hex>
answer_digest: sha256:<64 hex>
answerer_identity: <registry에 등록된 actor_id 또는 executor_ref>
identity_registry_ref: <Notes full commit과 registry 상대경로>
answer_ref: <불변 Git 또는 receipt ref>
requested_level: C3
claims: <검증할 중요한 주장 ID>
evidence_refs: <비밀 없는 exact refs>
forbidden: 답변 수정, 범위 확대, 실행, commit, push, deploy

같은 질문·답변 digest와 근거를 독립적으로 확인하라.
통과하면 주장별 등급과 한계를 제출하고, 실패하면 과장된 주장과 실제 가능한 등급을 제출하라.
```

## 금지

- 출처 하나를 읽고 답변 전체를 `C2` 또는 `C3`로 표시하지 않는다.
- 작성자와 같은 논리 actor가 `C3`를 발행하지 않는다.
- C3 검수자는 필요한 capability와 불변 `answer_ref` 없이 인증하지 않는다.
- 작업자 보고, Telegram의 “완료”, 대시보드 표시만으로 인증하지 않는다.
- 오래된 확인을 현재 사실처럼 표현하지 않는다.
- 사용자 “좋아”, “맞아”를 commit·push·배포 허가로 확대하지 않는다.
- capability URL, 비밀번호, cookie, token, session ID, private body 또는 로컬 절대경로를 근거에 넣지 않는다.
- 인증된 답변을 수정한 뒤 기존 digest와 인증을 유지하지 않는다.
- 인증서를 만들기 위해 모든 잡담과 사적 질문을 Git에 저장하지 않는다.

## 기존 상태 체계와의 관계

- `결정 필요`, `직접 테스트 필요`, `반영 완료`, `막힘`은 프로젝트 보고 상태다. 인증 등급이 아니다.
- Agent Mail의 `question`, `submitted`, `verified`, `closed`는 작업 event 상태다. 인증 등급이 아니다.
- `user_approval`은 행동 승인이다. 답변의 사실성 인증이 아니다.
- 기존 작업·메일·검수 생명주기는 유지하고, 중요한 답변이 필요할 때만 `qa_id`와 인증 ref를 연결한다.
- Agent Mail v2는 새 필드를 임의로 추가하지 않는다. event의 `binding_refs`에 `qa:<qa_id>`와 인증 기록 ref를, `evidence_refs`에 위 안전 형식의 근거 ref를 넣는다. Git 인증 기록이 없으면 `receipt_ref`를 사용한다.
