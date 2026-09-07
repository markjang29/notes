---
ticket: RELAY-62
stage: relay:1-확보
title: 43.201.34.144 Edge 진입점·홈서버 연계·관제 check-in·폴링 감사
date: 2026-09-07
requester: director
owner: aws-audit
status: captured
---

# RELAY-62 req

## 원문 요지

이사님 지시:

- 모든 접속은 이제 `43.201.34.144`에서 Tailscale로 홈서버에 연계된다.
- 모든 신규 개발은 해당 서버를 진입점으로, 1차적으로 홈의 사이트와 연결 가능하도록 개발한다.
- 2차 원사이트 통합 본(Spring + React)까지 고려한다.
- 관제/사칙 정책센터 주소를 확인 후 각 봇은 자신의 정보를 업데이트한다.
- 자신 앞으로의 메시지와 이사님 공통지시사항을 업데이트한다.
- 폴링 관련 스케줄링은 전부 리스트업하고, 부하 및 LMM 토큰 낭비 여부를 확인한다.

## 범위

- Notes 정책 정본 갱신.
- 8018 정책센터/관제 화면에 투영 가능한 정책 인덱스 갱신.
- `aws-audit` 자기 check-in 갱신.
- Cokacdir schedule, schedule history, cron, systemd timer, 주요 watchdog/polling 프로세스 점검.

## 금지

- 비밀값, 토큰, 세션 ID, raw chat ID를 Git/보고에 기록하지 않는다.
- 폴링 스케줄을 임의 삭제하지 않는다.
- 홈서버 실제 cutover 완료를 증명 없이 주장하지 않는다.
- Jira 상태 전이와 완료 검증은 증거 없이 주장하지 않는다.
