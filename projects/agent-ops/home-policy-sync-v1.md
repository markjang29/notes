---
title: 홈/홈서버 정책 투영 동기화 v1
date: 2026-09-07
status: active
tags:
  - agent-ops
  - home
  - policy
  - sync
---

# 홈/홈서버 정책 투영 동기화 v1

## 한 줄 결론

현재 8018 홈과 이관될 홈서버는 모두 Notes Git의 `policy-index-v1.json`을 읽고, 같은 Notes HEAD를
`POLICY_SHA`로 표시해야 한다.

ELI5: 가게를 옮겨도 메뉴판 원본은 같은 책이다. 손님용 메뉴판은 복사본이고, 원본 책이 바뀌어야
진짜 메뉴가 바뀐다.

## 구성

- 정본 저장소: `notes`
- 정책 인덱스: `projects/agent-ops/policy-index-v1.json`
- 투영 구현: `matrix-home` `/policies`, `/api/policies`
- 변경요청: `/api/policies/change-request`
  - 접수 상태는 `draft_site_intake_not_policy`
  - Notes commit+push 전까지 정책 정본이 아니다.

## 환경 변수

- `MATRIX_POLICY_NOTES_ROOT`: 홈 서비스가 읽을 Notes checkout 위치.
- `MATRIX_POLICY_CHANGE_QUEUE`: 사이트 변경요청 초안을 append할 runtime queue.
- `MATRIX_POLICY_CHANGE_TOKEN_FILE`: 변경요청 접수에 사용할 승인 토큰 파일.

환경 변수를 지정하지 않으면 서비스 사용자의 홈 디렉터리 기준 기본값을 쓴다. 운영 문서에는 토큰값과
개인 경로를 기록하지 않는다.

## 동기화 판정

1. `notes`가 최신 main을 가리킨다.
2. `matrix-home`이 `/policies`와 `/api/policies`를 제공한다.
3. `/api/policies`의 `notes_commit`이 운영자가 확인한 Notes HEAD와 같다.
4. `/api/policies`의 `policy_sha`가 각 봇 보고의 `POLICY_SHA`와 같다.
5. 정책 변경요청은 초안 queue에만 남고, 확정 정책처럼 표시되지 않는다.

## 이관 시 주의

- AWS 8GB를 내리기 전, 홈서버 8018에서도 같은 `policy_sha`를 표시해야 한다.
- 홈서버에 직접 반영할 수 없는 actor는 Git commit+push와 적용 요청문을 남기고, 홈서버 권한을 가진
  zcode/manager가 pull·restart·실측을 수행한다.
- 한쪽 홈만 수정한 상태로 완료 보고하지 않는다.

