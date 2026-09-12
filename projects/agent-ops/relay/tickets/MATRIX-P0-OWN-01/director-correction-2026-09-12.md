---
title: AWS 8GB 셧다운과 삭제 금지 구분 정정
status: director-correction / supersedes-shutdown-wording-only
date: 2026-09-12
thread: MATRIX-P0-OWN-01
---

# 이사님 정정 — AWS 8GB는 셧다운 대상이다

## 바로잡은 결론

이전 작업지시와 전체 공지에서 `AWS 중지·종료`를 한꺼번에 금지한 표현은 잘못이다.

- **해야 할 일:** 홈 이관과 필수 검증을 마친 뒤 AWS 8GB 앱 서버의 서비스·timer를
  `stop + disable`하고, 재기동 방지 관찰 뒤 EC2 인스턴스를 `stop`한다.
- **계속 켜둘 것:** 사용자 진입점인 `43.201.34.144` 소형 AWS Edge와 Tailscale 전달 경로.
- **하지 말 것:** AWS 8GB EC2 `terminate`, EBS volume 삭제, snapshot 삭제, DB·queue·파일·원천
  자산 삭제. 삭제는 셧다운과 다른 비가역 작업이며 이사님의 별도 명시 승인이 필요하다.

즉 목표 상태는 `AWS 8GB = stopped, recoverable`, `43 Edge = running`, `Home = serving`이다.

## 셧다운 실행 경계

셧다운은 취소된 것이 아니라 아래 영수증을 한 번에 확인한 직후 실행할 P0 작업이다.

1. 대상 instance/host가 8GB 앱 서버이며 `43.201.34.144` Edge가 아님을 식별한다.
2. 공개 root, sites, nexus, H8와 필요한 API가 Edge에서 홈으로 실제 응답한다.
3. AWS 8GB에만 남은 DB·queue·파일·bot·cron·timer가 0건이거나 승인된 예외로 기록된다.
4. 홈 복구 시험과 외부 backup, 중복 scheduler 방지, rollback 경로가 확인된다.
5. 정확한 unit 목록을 `stop + disable`하고 관찰한 뒤 인스턴스를 `stop`한다.

게이트 미통과는 삭제 허가가 아니며, 셧다운 목표 자체를 취소하는 것도 아니다. 누락 항목을 blocker로
보여 주고 끝나는 즉시 셧다운 단계로 이어 간다.

## `child mail`의 쉬운 이름

`child mail`은 사람에게 보내는 이메일이나 새 서비스가 아니다. 매니저가 큰 지시를 봇별로 쪼갤 때
만드는 **개별 Git 작업지시서**다. 담당 봇 한 명, 읽을 commit, 바꿀 범위, 금지 동작, 테스트와 완료조건을
고정해 여러 봇이 같은 파일을 동시에 건드리지 않게 한다.

앞으로 사용자 화면과 공지에는 `child mail` 대신 `개별 작업지시`라고 표시한다. 내부 JSON의
`parent_mail_id` 같은 필드명만 통신 규격 호환을 위해 유지한다.

## 이전 기록 처리

- `work-order-v2.json` attempt 1의 `aws_stop_disable_or_terminate` 금지는 이 문서로 정정한다.
- 기존 68/68 책임 분류는 유지하되, AWS 셧다운 준비·실행 항목은 삭제 금지와 분리한다.
- attempt 1의 공지는 취소 공지로 덮어쓰지 않고, 같은 idempotency key의 attempt 2가 정정본임을 알린다.
- 셧다운 실행은 AWS 제어 capability와 정확한 대상 검증을 가진 단일 actor에게 별도 배정한다.

