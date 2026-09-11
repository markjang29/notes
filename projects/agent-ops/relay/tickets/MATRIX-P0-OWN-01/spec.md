---
title: MATRIX-P0-OWN-01 route·site 책임 배정과 전환 통제
status: ready-for-dispatch
issued: 2026-09-12
accountable_actor: aws-manager
controller_actor: windows-codex
---

# MATRIX-P0-OWN-01

## 결론

`aws-manager` 한 명이 조정 책임을 맡아, 이미 실측·검사된 경로와 사이트 전환 목록에 등록 actor를
배정하고 각 actor의 ACK와 Git 근거를 모은다. 전체 봇 공지는 작업 배정이 아니라 이 정본의 위치를
알리는 wake-up이며, 실제 구현은 별도 Agent Mail을 받은 actor만 시작한다.

## 고정 입력

- 제품 repo: `markjang29/matrix-home`
- full commit: `15ce46e9516b015f63955bcd536d5cc257bc186e`
- 전환 명세: `docs/migration/legacy-route-site-disposition-v1.json`
- 우선순위: `docs/architecture/priority-backlog-v1.json`의 `P0-OWN-01`
- 검사: Flask route 36/36, catalog site 27/27, internal component 5/5; 전체 unittest 16/16 통과
- 상태 의미: 분류와 누락 검사가 완료됐을 뿐, Spring 전환이나 AWS 종료가 완료된 것은 아니다.

## 매니저가 할 일

1. 전환 명세의 route 36개, site 27개, internal component 5개를 빠짐없이 읽는다.
2. `actors.json`의 현재 capability와 repo 권한을 대조해 각 항목에 책임 actor를 정확히 한 명만 둔다.
3. `matrix-home` 쓰기 권한이 registry에 없는 actor에게 구현을 배정하지 말고
   `capability_not_registered`로 막은 뒤 필요한 최소 권한 변경안을 별도 제시한다.
4. `needs_adr`인 8002, 8011, 8013, 8020, 8765, 8766은 결정을 추측하지 말고 이사님 선택 안건으로
   짧게 묶는다.
5. 실행 가능한 항목은 repo, full input commit, exact read/write scope, 금지 동작, 완료조건,
   idempotency key가 있는 child Agent Mail v2로 한 actor에게만 배정한다.
6. ACK는 완료로 세지 않으며, `submitted` 결과를 controller가 검증하기 전에는 완료 표시하지 않는다.

## 산출물 범위

이 티켓 아래에만 다음을 추가한다.

- `owner-allocation-v1.json`: 68/68 항목의 단일 owner 또는 명시적 blocker
- `status.md`: ACK, 진행, submitted, verified 수와 마지막 Git 근거
- `mail/`: 실행 가능한 항목에 대한 child Agent Mail v2

제품 코드는 각 child mail이 지정한 `matrix-home` 범위에서만 변경한다. 매니저는 조정자이며 제품 기능을
몰래 대신 구현하지 않는다.

## 금지

- 신규 공개 웹이나 포트 생성
- AWS 서비스, 인스턴스, bot, cron, timer 중지·비활성화·종료
- DB·queue·파일·snapshot 삭제 또는 원천 자산 이동
- token, chat ID, key file, session, 내부 절대경로를 Git이나 메시지에 기록
- 다른 저장소의 구현을 `matrix-home` 완료로 계산
- ACK 또는 요청 접수를 완료로 보고

## 완료조건

- 68/68 항목이 정확히 한 등록·capable actor 또는 하나의 검증 가능한 blocker를 가진다.
- 중복 writer와 미등록 권한이 0건이며, 필요한 권한 변경은 실행하지 않고 결정안으로 분리된다.
- 여섯 ADR 후보가 각각 유지·통합·종료 선택지와 영향으로 정리된다.
- child mail마다 actor ACK가 있고, ACK가 없는 항목은 시작하지 않는다.
- 결과 commit이 원격 Git에 push되고 `submitted`로 보고된다.
- controller가 근거를 대조해 `verified`하기 전 티켓을 닫지 않는다.

## 봇 공지 원칙

Git push 뒤 전체 공지는 한 문장으로만 보내며, 수신 봇은 자신에게 별도 child mail이 오기 전에는 구현,
배포, 종료를 시작하지 않는다.

