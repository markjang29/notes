---
title: 운영체계 v2 최소 부팅 규칙
date: 2026-07-27
status: shadow-only
authority: OPERATING.md
---

# 운영체계 v2 최소 부팅 규칙

이 파일은 세션이 길고 모순된 구형 온보딩 대신 읽을 짧은 기계·사람 공용 진입점이다.
현재는 무삭제 전환 시험용이며, 실제 포인터 전환 전까지 새 권한을 만들지 않는다.

## 시작 순서

1. `OPERATING.md`와 `ops/registry.json`을 읽는다.
2. 실제 transport와 비공개 runtime manifest로 자신의 `executor_ref`만 확인한다.
3. 대상 프로젝트의 `AGENTS.md`·프로젝트 규칙·`WORK.md`를 읽는다.
4. `WORK.md` 파일 자체가 없으면 역할이 없는 상태다. 오류가 아니라 읽기 전용 현황 확인으로 끝낸다.
5. 파일이 있으면 먼저 문서 형식과 모든 기록의 `registry.assignment_contract.required_fields` 22개, field rule, `task_id` 유일성을 검증한다. 형식 손상·필드 누락·ID 중복이 있으면 문서 전체가 불명확하므로 `막힘`으로 끝낸다. 다른 실행자의 정상 종료·만료 기록은 전역 오류로 취급하지 않는다.
6. 정상 문서에서 현재 `executor_ref`와 일치하는 계약 후보를 찾는다. 활성 후보가 없으면 역할이 없는 상태다. 읽기 전용 현황 확인으로 끝낸다.
7. 현재 실행자와 일치하는 후보끼리 충돌하거나 활성 후보가 이미 만료됐으면 `막힘`으로 끝낸다. 통과한 계약에만 `role.grants ∩ environment.supports ∩ WORK.allowed`를 적용하고 역할·환경·작업의 금지는 항상 우선한다. 기준 커밋, 읽기·쓰기 범위와 저장소 gate도 함께 대조한다.
8. 검증을 모두 통과한 경우에만 `executor_ref / role_id / task_id / objective / repo_id / base_commit / allowed / forbidden / done_when / test_plan / expires_at`을 짧게 확인하고 시작한다.
9. 기존 dirty 변경이 쓰기 범위와 겹치면 쓰기를 중단하고 `막힘`으로 보고한다. 읽기 전용 shadow probe는 dirty 상태를 보존한 채 수행할 수 있다.

## 고정 경계

- 봇 이름, Telegram 채팅방, 모델, 컴퓨터, 세션 기억과 과거 직책은 권한이 아니다.
- 역할은 현재 `WORK.md` 작업 계약에서만 생기고 작업 종료·만료·회수와 함께 끝난다.
- 한 작업의 작성자는 한 명이다. 독립 검수가 필요하면 별도 reviewer를 둔다.
- Telegram은 알림·질문·깨우기 수단이며 완료 정본이 아니다.
- 제품 지식과 완료 상태는 대상 프로젝트 Git, 공통 운영은 Notes Git이 정본이다.
- 키·쿠키·세션 ID·chat ID·절대경로·private runtime binding을 Git이나 작업 계약에 기록하지 않는다.
- 승인된 `gitignore` 원자료는 보호 영역에 두고 Git에는 해시·출처·manifest만 기록한다.

## 전환 시험

- `ops/registry.json`은 현재 `shadow-only`다.
- 구형 `actors.json`과 v2가 같은 실제 실행 경로를 가리키는지만 쓰기 없이 비교한다.
- AWS·Windows·ZCode 세 환경이 같은 결과를 내기 전에는 구형 레지스트리·스키마·부팅 문서를 삭제하지 않는다.
- v2 결과가 구형 지시와 충돌하면 새 작업을 시작하지 말고 차이를 보고한다.
- 서비스 중지·설정 저장·재시작·세션 초기화는 별도 전환 승인 전 금지한다.
