# 2026-08-27 RELAY-15 오탐 사건 — Jira 토큰 401로 정상 포트 17건 허위 적발

## 요약
- 09:10 정기 포트 감사가 `ticket_invalid` 17건을 적발, 카드 `req-20260827091008-193936` 자동 발행.
- 실측 결과 **전부 오탐**. `~/.jira-token`이 401(자격증명 실패)이 되었고, 비공개 프로젝트의
  미인증 이슈 조회는 404 "Issue does not exist or you do not have permission"로 응답하므로
  `jira_ticket_exists()`가 존재하는 티켓 전부(14개)를 '없음' 판정.
- 토큰 파일 자체는 08-19 이후 불변(192B, 폐기는 Atlassian측). 08-26 09:10 감사까지 전 티켓 True.

## 조치
- `relay_port_audit.py`에 `jira_authenticated()`(GET /rest/api/3/myself) 사전검증 추가.
  인증 실패·도달불가면 `ticket_invalid` 판정 전체 보류, 보고서에 `jira_auth_ok` 기록.
  08-27 정기 실행부터 적용. 재실행으로 정정 카드가 추가 발행되는 것은 방지(기준 보고 왜곡 금지).

## 실위반(오탐 제외 후 잔존, 어제와 동일 계열)
- 8016: env RELAY-56 != 레지스트리 RELAY-35
- 8018: env RELAY-56 != 레지스트리 RELAY-50
- 포트 1건 env_missing(RELAY_TICKET 부재)
→ 서비스 재시작이 필요한 운영 조치라 이사님 승인 전 불개입. 토큰 갱신 전까진 Jira 검증 불가.

## 이사님 조치 필요
- **Jira API 토큰 재발급**(id.atlassian.com → Security → API tokens). 새 토큰을
  `~/.jira-token`에 반영하면 다음 감사부터 티켓 검증 재개.

## 파급
- Jira API를 쓰는 모든 경로(감사, 8018 /api/jira 프록시, RELAY 완료판정)가 같은 토큰 의존 —
  갱신 전까지 Jira 기반 완료 근거 불가(RELAY-54 분류와 동일 결론).
