# N100 회의방 입장 카드 — aws-manager → n100-zcode(firebat_claude)

- 발행: 2026-08-31, 이사님 승인 하 전달. 수신 즉시 이사님 1:1 DM으로 "입장 카드 수신" 보고.
- 목적: firebat 3봇이 AWS 관제 회의방(웹챗)에 입장해 이사님 지시를 받게 한다.

## 방 API (AWS)

- 수신(폴링): `GET http://13.125.131.126:8023/api/messages?after=<마지막id>`
  헤더 `X-Token: <ROOM_BOT_TOKEN>` → 2~5초 간격
  응답: `{"messages":[{"id","ts","kind","sender","text"}…], "inflight":{}}`
- 송신(발언): `POST http://13.125.131.126:8023/api/bot/send`
  헤더 `X-Token: <ROOM_BOT_TOKEN>`, 본문 `{"username":"<봇유저명>","text":"<응답>"}`
- 지시 형식: 이사님이 방에서 `@heav_firebat_claude_bot <지시>` 식 멘션. 자기 봇 멘션만 처리.

## 구현 지침

1. N100에 폴러 상시 구동(언어·위치 자율, 작업관리자/서비스 등록 권장).
2. 멘션 수신 → 해당 봇 엔진 실행 → 결과를 송신 API로 회신. 봇별 잠금으로 중복 실행 방지.
3. 회신 프롬프트에 방 로그 직전 몇 개를 문맥으로 포함.
4. 대상 3봇: `heav_firebat_claude_bot` · `heav_firebat_zcode_bot` · `heav_firebat_codex_bot`

## 완료 판정

- 이사님이 방에서 `@heav_firebat_claude_bot 인사` → 응답 뜨면 성공. 완료/실패 시 이사님 DM 보고.

## 비밀

- `ROOM_BOT_TOKEN`은 이사님이 보내는 전달 문장에 포함되어 있다. Git 커밋·재공유 금지.
- 방 로그의 다른 봇 발언은 읽기만 가능 — 조작 없음.

## 엔진 구동 규격 (09-02 사고 보강 — 필수)

- claude 엔진은 `--dangerously-skip-permissions` 로 구동할 것. 근거: 헤드리스 폴러 구동 시
  권한 프롬프트가 자동 거부되어 `git` 실행·설정 편집 전부 차단 (09-02 RELAY-58 착수 실패 사례).
  AWS 회의방 11기와 동일 방식. 플래그를 못 붙이는 경우 최소 `C:\Users\<사용자>\.claude\settings.json`
  의 `permissions.allow`에 `"Bash(git:*)"` 필요.
- private repo 작업 봇은 사전에 N100 Git Bash에서 1회 clone + 깃허브 로그인(자격 저장) 요건.
- codex 엔진 기본 sandbox read-only → 쓰기 대리 조치 용도로 쓸 수 없음.
