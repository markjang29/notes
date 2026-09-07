---
title: 관제 한판 v1 — 정책·봇·ACK·진행 통합
date: 2026-09-07
status: v0 implemented on 8018, codex_dev_1 review requested
tags:
  - agent-ops
  - gwanje
  - governance
  - policy-sha
---

# 관제 한판 v1 — 정책·봇·ACK·진행 통합

## 한 줄 결론

이사님이 한 화면에서 사칙 판본, 봇별 모델, 맡은 일, 진행상황, 어려움, 다음 행동, 사칙 이해 버전을
보게 한다.

2026-09-07 이후 관제 한판은 모든 신규 개발이 `43.201.34.144` 진입점, Tailscale 홈서버 연결,
Spring + React 원사이트 흡수 계획을 고려했는지도 확인하는 기준 화면이다.

ELI5: 가게 벽에 직원 근무표, 규칙책 판본, 오늘 할 일, 막힌 일을 한 장으로 붙여두는 것이다.

## v0 구현

- 구현 위치: `matrix-home` 8018
- 화면: `/governance`
- API:
  - `GET /api/governance`
  - `POST /api/governance/checkin`
- 입력 원장:
  - Notes `policy-index-v1.json`, `roster.json`, `actors.json`
  - bot-dashboard `profiles.jsonl`
  - Cokacdir bot settings의 모델 정보(토큰값은 미노출)
  - runtime `governance_checkins.json`

## 보이는 항목

- 현재 `POLICY_SHA`
- 정책 문서 수
- 전체 active bot 수
- 사칙 OK / 구판 / 미보고 수
- 봇별:
  - username, display, site
  - actor_id, ACK 상태
  - engine, model
  - 역할/맡은 일
  - 진행사항
  - 어려움/블로커
  - 다음 행동
  - 봇이 이해한 `POLICY_SHA`

## 수정 권한

- 이사님 토큰: 모든 봇 row 수정 가능.
- 자기 봇 토큰: 자기 username row만 수정 가능.
- 무토큰: 읽기만 가능, 수정 401.
- 사이트 check-in은 runtime 상태이며, 역할·정책·완료의 정본은 여전히 Git commit이다.

## codex_dev_1 협업 설계 요청

`@heav_lnx_codex_dev_1_bot`은 8023 소통/관제 앱 관점에서 다음을 검토한다.

1. 8023 회의방의 `ACK` 메시지를 `/api/governance/checkin`으로 자동 반영할 수 있는가?
2. `@all` 공지는 ACK 도배 없이 다음 봇 구동 시 문맥 주입만 유지하는가?
3. 루틴 폴링이 LMM 호출로 가지 않도록, 메시지 종류를 `notice`, `task`, `ack`, `progress`,
   `blocked`, `submitted`, `review`로 분리할 수 있는가?
4. 봇별 자기 row 업데이트 인증을 shared token이 아니라 bot-specific token으로 강제할 수 있는가?
5. ACK가 `POLICY_SHA`, 읽은 ref, scope, prohibitions, done criteria 없이 들어오면 `invalid_ack`로
   표시할 수 있는가?

## 다음 단계

1. codex_dev_1의 8023 관점 리뷰 수령.
2. 8023 메시지 타입/ACK 파서 설계 확정.
3. 8018 `/governance`와 8023 회의방을 runtime event로 연결.
4. 8025 대시보드가 같은 `/api/governance`를 읽거나 링크한다.
5. 홈서버 이관 후에도 `POLICY_SHA` 동기화 확인.
6. 봇별 check-in에 `43.201.34.144` 진입점/홈서버 연결 고려 여부와 공통지시 수신 상태를 표시한다.
