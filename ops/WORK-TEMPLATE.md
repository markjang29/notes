---
title: 프로젝트 WORK.md 템플릿
date: 2026-07-27
status: shadow-only
authority: OPERATING.md
---

# 프로젝트 `WORK.md` 템플릿

`WORK.md`는 특정 봇의 영구 직책표가 아니라 Director가 한 작업에만 내리는 임시 발령장이다.
현재 v2는 `shadow-only`이므로 이 템플릿만으로 실제 권한이 생기지 않는다.

## Director가 먼저 볼 다섯 항목

```text
목표: objective
지금 볼 것: director_attention
하지 말 것: forbidden
끝났다고 판단할 기준: done_when
확인 방법: test_plan
```

한 프로젝트에는 진행 중인 주 작업 한 건과 선택적인 독립 실험 한 건만 둔다.
끝난 작업은 `state`를 `done` 또는 `cancelled`로 바꾸고, 역할 권한도 함께 끝낸다.

Director에게 제출하는 답변이 산출물인 작업은 `required_refs`에 `ops/ANSWER-CERTIFICATION.md`를,
`evidence_required`에 필요한 인증 등급과 근거를 적는다. 새 필드를 임의로 추가하지 않는다.

## 기계가 읽는 계약

실제 프로젝트의 `WORK.md`에는 아래처럼 `ops-work-v2` JSON 블록 하나를 둔다.
설명 문장은 블록 위에 자유롭게 쓸 수 있지만, 발령 내용은 블록 안의 값만 정본으로 본다.

```json
{
  "schema": "ops-work-v2",
  "version": 1,
  "assignments": [
    {
      "task_id": "project-task-01",
      "state": "assigned",
      "director_attention": "none",
      "role_id": "worker",
      "executor_ref": "windows-codex",
      "assigned_by": "director",
      "objective": "사용자 의도와 이번 목표를 쉬운 한 문장으로 적는다.",
      "project": "대상 프로젝트 이름",
      "repo_id": "대상 저장소 ID",
      "base_commit": "0000000000000000000000000000000000000000",
      "branch": "task/project-task-01",
      "allowed": [
        "analyze",
        "repo_read"
      ],
      "read_scope": [
        "AGENTS.md"
      ],
      "write_scope": [],
      "forbidden": [
        "repo_write",
        "main_merge",
        "deploy"
      ],
      "required_refs": [
        "AGENTS.md"
      ],
      "preconditions": [
        "기준 커밋과 현재 작업 상태를 확인했다."
      ],
      "done_when": [
        "조사 결과와 누락·충돌이 쉬운 말로 정리된다."
      ],
      "evidence_required": [
        "검사 결과"
      ],
      "test_plan": [
        "정본과 실제 상태를 다시 대조한다."
      ],
      "reviewer": "director",
      "expires_at": "task-end"
    }
  ]
}
```

`base_commit`은 실제 발령 시 검증한 전체 40자 커밋으로 바꾼다. 문자열 모양만 맞거나
로컬에 commit 객체가 있는 것만으로는 부족하며, canonical remote의 실제
default-branch tip과 정확히 일치해야 한다.
예시의 all-zero 커밋과 일반 `repo_id`는 의도적인 무효 placeholder이므로 그대로는 발령 검사를 통과하지 않는다.
`expires_at`의 `task-end`는 작업이 `done`·`cancelled`가 되거나 Director가 회수하는 즉시 만료된다는 뜻이다.
`executor_ref`에는 세션 ID, 키, Telegram chat ID 또는 접근 URL을 쓰지 않는다.
판정 순서는 고정한다. 파일 자체가 없으면 읽기 전용으로 끝낸다.
파일이 있으면 먼저 전체 문서의 형식·필수 필드와 `task_id` 유일성을 검사한다. 빠진 필드, 깨진 형식 또는 ID 중복이 있으면 `막힘`으로 끝낸다.
다른 실행자의 정상 종료·만료 기록은 문서 전체를 막지 않는다. 정상 문서에 현재 실행자와 일치하는 활성 계약이 없으면 읽기 전용으로 끝낸다.
현재 실행자와 일치하는 후보끼리 충돌하거나 그 활성 계약이 이미 만료됐을 때만 `막힘`으로 끝낸다.
현재 실행자의 계약이 `blocked`이면 이를 역할 없음으로 숨기지 않고 위 다섯 항목과 함께 `막힘`으로 보여준다.
`reviewer`는 `director` 또는 현재 작업자와 다른 등록 executor만 허용한다.
문서는 UTF-8 8MiB·JSON 깊이 64를 넘을 수 없고 duplicate key, 비정상 숫자와 알려진
credential 형식이 있으면 원문 값을 출력하지 않고 차단한다.
