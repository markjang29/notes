# INFRA#15 [A2] zcode 폴러 8023만 감시 → 8024 사서함 폴링 추가 (2026-10-01, 98)

## 재현 (조치 전)
- `room-poller-gmlnx-zcode.py`는 ROOM=:8023 멘션만 감시(제안서 A2 그대로), 8024 미수신
- heav_gmlnx_zcode_bot 사서함: pending 1(T-1001) + deliveredNotAcked 2(09-30~10-01 잔여)
- 사이드카 comm-relay-gmlnx(watch)는 heav_gmlnx_zcode_bot을 "키 파일 미발견 — 각성 불가"(roster wake:false, 이 노드에 봇키 없음 — 09-28 설계) → 수령 주체가 폴러뿐인 상태

## 조치 (scripts/room-poller-gmlnx-zcode.py — gmlnx 노드, 폴러가 zcode 본체)
1. 8024 수신채널 추가: NATS_BASE·POLL_8024_INTERVAL=30·nats8024_json()·comm_8024()
2. 메인 2.5초 루프에 30초 주기 훅(8023 폴링은 그대로 — 기존 기능 무변경)
3. 수령→zcode 엔진 실행→7필드 준용 ACK(봤음 단독 금지)→8024로 task 회신
4. 보강 2건(시험 중 발견): ①pending+deliveredNotAcked 합집합 소화 ②pending→delivered 전환 동시성으로 같은 id 중복처리 방지(seen)
- systemd(gmlnx-zcode-poller)는 EnvironmentFile=bridge.env 주입 — 시험시 겪은 ZAI 키 블로커는 시험셸 한정, 운영 无영향

## 검증 (같은 명령)
- `whoami?bot=heav_gmlnx_zcode_bot` → pending 0 / deliveredNotAcked 0 (조치 전 1+2 → 0+0, 티켓 기준 "pending 0" 초과달성)
- 30초 폴링 로그: `8024_TASK id=… → 8024_REPLIED` — 엔진이 실제로 답변(원장에 98→아니고 zcode→매니저 회신 기록, 13:09:42 "미처리 지시 없음")
- 8023 폴링(POLL_INTERVAL=2.5) 병행 정상 — 기존 기능 회귀 없음(POLLER START 로그, 8023 처리 로그 유지)

## 비고
- deliveredNotAcked의 /ack은 수동 재시도시 성공(폴러 1회차 404는 pending→delivered 전환 직후 타이밍) — 2회차 seen+합집합으로 자체 해소
