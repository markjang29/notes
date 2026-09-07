# [spec] RELAY-61 — 관제 한판

## 인수조건

1. 8018 홈과 사이트맵에서 `/governance`에 접근 가능하다.
2. `/api/governance`가 현재 `POLICY_SHA`, active bot 목록, 모델, 역할, 진행, 블로커, 봇별 사칙
   이해 버전을 반환한다.
3. 봇 check-in API는 무토큰 401을 반환한다.
4. 이사님 토큰은 전체 수정, 자기 봇 토큰은 자기 row만 수정하도록 설계한다.
5. ACK 규칙은 `principles/gwanje-ack-protocol.md`에 사칙으로 남긴다.
6. codex_dev_1 협업 요청은 `gwanje-governance-board-v1.md`와 회의방 메시지로 남긴다.

## 비목표

- 사이트 화면만으로 정책·역할·완료를 확정하지 않는다.
- 루틴 폴링을 LMM에 보내지 않는다.
- 비밀 토큰·채팅 ID·세션 ID를 화면/API/Git에 노출하지 않는다.

