# [impact] RELAY-61 — 관제 한판

## 영향 repo

- `matrix-home`: `/governance`, `/api/governance`, `/api/governance/checkin` 추가.
- `notes`: 관제 ACK 사칙, 관제 한판 설계, 정책 인덱스 갱신.
- `meeting-room`: 이번 커밋에서는 직접 수정하지 않고 codex_dev_1 리뷰 요청만 보낸다.

## 위험과 완화

- 화면 수정이 Git 정본처럼 오해될 위험 → check-in은 runtime 상태라고 표시.
- 봇별 상태 업데이트 위조 위험 → v0는 이사님 토큰 또는 해당 봇 토큰 비교로 제한.
- 토큰 노출 위험 → 헤더 인증만 사용하고 값은 응답·로그·Git에 저장하지 않음.
- ACK 도배/폴링 토큰 낭비 → 사칙에 "루틴 폴링 LMM 보고 금지" 명시.

## 판정

조건부 가능. 8018 v0 구현 후 8023 자동 ACK 파서와 메시지 타입 분리는 codex_dev_1 설계 리뷰를 거쳐
별도 구현한다.

