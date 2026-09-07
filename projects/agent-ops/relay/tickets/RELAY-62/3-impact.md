---
ticket: RELAY-62
stage: relay:3-영향성검토
owner: aws-audit
date: 2026-09-07
status: submitted
---

# RELAY-62 impact

## 판정

조건부 진행 가능.

정책 정본 갱신은 필요하며 위험이 낮다. 다만 `43.201.34.144`가 실제로 어떤 포트와 도메인을
홈서버로 프록시하는지는 별도 실측이 필요하다. 이 문서는 "이사님이 확정한 운영 원칙"을 먼저
고정하고, 실제 cutover 완료를 주장하지 않는다.

## 영향 범위

- `notes`: 정책 정본, 정책 인덱스, 관제/홈동기화 문서.
- `matrix-home`: `/policies`, `/governance`는 Notes policy-index 투영이므로 별도 코드 변경 없이
  새 정책을 표시한다.
- `meeting-room` 8023: 공통지시/ACK 수신과 polling 보고 금지 원칙을 따라야 한다.
- `bot-dashboard` 8025: 모델·봇상태 상세와 관제 한판을 장기적으로 연결해야 한다.
- 홈서버/Spring+React 원사이트: 신규 개발의 목표 경로다. 현재 AWS legacy 화면만 고치면
  완료가 아니다.

## 회귀 위험

- 정책 화면이 Notes HEAD를 읽지 못하면 새 원칙이 표시되지 않는다.
- 봇 check-in이 `POLICY_SHA`를 갱신하지 않으면 구판으로 남는다.
- cron/polling이 LMM 호출을 동반하면 529/토큰 낭비가 재발할 수 있다.

## 조건

1. 새 정책은 Notes commit+push 후에만 정본이다.
2. `/policies`, `/governance`에서 새 Notes HEAD가 보이는지 확인한다.
3. schedule audit은 활성 schedule과 과거 history를 구분해 보고한다.
4. 토큰/credential/세션 식별자는 보고하지 않는다.
