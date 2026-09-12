---
title: 역할 카드 양식 (role card template)
date: 2026-09-12
status: v1
tags:
  - role-card
  - template
  - agent-ops
---

# 역할 카드 양식

> 각 actor의 역할 카드는 이 양식을 그대로 복사해 `roles/<actor_id>.md`로 만든다.
> 한 카드 = 한 actor. 두 명 이상의 actor를 한 카드에 합치지 않는다.
> 카드의 모든 필드는 `projects/agent-ops/actors.json`을 근거로 채운다. 레지스트리가 항상 이긴다.

```markdown
---
title: 역할 카드 — <actor_id>
date: <YYYY-MM-DD>
status: active
tags:
  - role-card
  - <actor_id>
actor_id: <actor_id>
registry_ref: projects/agent-ops/actors.json
---

# 역할 카드 — <display_name> (<actor_id>)

## 0. 판본 선언
- 이 카드가 참조한 레지스트리 판본: 정본=<commit> (actors.json version <N>)

## 1. 한 줄 결론
<persona를 한 줄로. 이어서 ELI5 한 문장.>

## 2. 정체와 연락
- kind: <human|agent> · location: <location> · providers: <providers>
- transport: <transport.kind — address>
- repo_ids: <repo_ids>

## 3. 역할과 권한
- role: <role>
- capabilities: <capabilities>
- 금지(forbidden): <forbidden> (actors.json)
- jira: <project / component / relay_stages>

## 4. 필수 규칙 (required_refs)
<각 required_refs 링크와, 카드 작성 시점의 그 문서 핵심 요지 1줄씩.>

## 5. 담당 업무
<3~7개, 동사로 시작. 추측이 아니라 등록된 capability 범위 안에서.>

## 6. 보고와 인수인계
- 보고: 무엇을 어디에(회의방/메일) 어떤 형식으로 남긴다 — [CERT <actor_id> <commit>] 선두 필수.
- 인수인계: projects/agent-ops/handoff-contract-01-04.md 4필드를 채워 남긴다.

## 7. 금지 (카드固有)
<레지스트리 forbidden 외에 이 카드가 문서로 굳힌 구체적 금지. 없으면 생략.>

## 8. 완료·검증
- 완료 판정은 controller만 내린다. 자기 산출물을 자기가 verified/closed하지 않는다.
- 완료기준 예: <이 actor의 대표 done_criteria 1~2개>
```

## 채우기 규칙

1. **모든 필드는 actors.json 값만** 복사한다. 해석·확장·추측 금지 — 근거가 없으면 빈 값으로 둔다.
2. 카드에 적을 capability 밖 업무가 있으면 먼저 레지스트리 갱신(이사님 승인)이 선행된다.
3. `[CERT]`·`정본=<commit>` 의미는 `L0-agent-common.md` §2를 따른다.
4. 카드 변경도 Git commit+push로 정본화한다. 채팅·메모리의 버전은 증거가 아니다.
