---
ticket: RELAY-62
stage: relay:3-영향성검토
owner: aws-audit
review_source: codex_dev_1 RELAY-61 회의방 회신
date: 2026-09-07
status: submitted
---

# RELAY-62 codex_dev_1 ACK/design summary

## 확인된 dev1 리뷰

`codex_dev_1`은 RELAY-61에 대해 read-only 리뷰를 회신했다. 핵심은 "ACK/공지/상태보고 파싱은
LLM으로 하지 말고 8023 서버의 결정적 파서와 원장 전달로 처리하라"는 것이다.

## 설계 반영할 제안

1. ACK 자동반영은 정규식 기반 결정적 파서로 수행한다. LMM/LLM 파싱 금지.
2. `@all`/공지에는 ACK를 요구하지 않는다. notice ACK는 `invalid_ack`로 분류한다.
3. 메시지 타입을 `task`, `ack`, `progress`, `blocked`, `submitted`, `review`로 분리한다.
   `task`만 엔진을 깨우고 나머지는 원장 적재와 관제 전달만 수행한다.
4. 봇별 check-in은 shared token이 아니라 봇별 독립 토큰과 username 바인딩으로 검증한다.
5. 불완전 ACK는 자동 재요청하지 않고 `invalid_ack`로 표시한다. 재요청은 작업 보유자만 한다.

## dev1이 지적한 blocker

- 봇별 독립 토큰 발급·보관·배포 위치가 아직 정본화되지 않았다.
- `actor_id`와 `username`의 1:1 대응이 registry/roster에서 완전히 명확하지 않다.

## RELAY-62 추가 반영

새 공통지시에 따라 ACK/작업보고에는 다음도 포함해야 한다.

- `43.201.34.144` 진입점 고려 여부
- Tailscale 홈서버 연결 고려 여부
- Spring + React 원사이트 흡수 계획
- 루틴 폴링 LMM 보고 금지 준수 여부

`codex_dev_1`에게는 RELAY-62 follow-up read-only 리뷰를 요청했다. 이 follow-up의 새 회신은 아직
수령 전이므로 완료로 표시하지 않는다.
