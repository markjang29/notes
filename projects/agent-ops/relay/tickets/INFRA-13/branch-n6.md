# INFRA#13 [N6] JetStream consumer 위생·max_deliver·원장 재생 검증 — 승인게이트(P2지만 자율; 진단 "자율") (2026-10-02, 98)
## 재현 (운영 무변경 — /jsz + nats-py(보드 venv) 실측)
- consumer 8개: 잔재 3(tc02-durable·tc04verify·gmlnx-scan-tmp — 진단과 일치) + 운영 5(relay98-msg/notice/ack, gmlnx-claude-inbox/once)
- **전 consumer max_deliver=-1, inactive_threshold=None** — 독성 메시지 무한 재전달 위험 확정
- gmlnx-scan-tmp: filter `>`, pending 222 (진단 시 77 → 222로 증가 — 계속 쌓이는 것 실측)
- gmlnx-claude-inbox·once: notice.broadcast pending 2 — 무ACK 잔류(PIPE#60 (b) 관련, 본 건 범위 밖 — 주석만)
## 준비 (적용절차+검증 확정 — 도구: nats-py를 보드 venv에 설치(시스템 무변경))
1. 잔재 3개 삭제(진단: 이사님 공지 불필요 — tc02·tc04·scan-tmp): `jsm.consumers_info→consumer_info.delete()`
   - 단, scan-tmp는 pending 222 원장 재생 테스트에 쓰고 나서 삭제
2. 운영 5개에 `max_deliver=5` + `inactive_threshold=1h`(권한은 cokacdir·사이드카에 영향 없음 — 검증 후)
   - relay98-ack/msg/notice, gmlnx-claude-inbox/once 순. 1개씩 적용·확인·다음(티켓 규칙 준수)
3. 8024 원장 재생 검증: 8024 정지 → 테스트 메시지 1건(nats publish bot.msg.test.ledger) → 8024 재시작 → totalLedger +1 확인
   - 재생 안 되면: studio-8024-msglog를 durable로 전환 안건 추가(별도 상신)
## 검증 (동일 명령)
- `/jsz`·`nats-py consumers_info`에서 max_deliver=5·inactive=1h 5개, 잔재 0, pending 감소 추이
- relay98·8024 사이드카 에러 0, 8024 whoami 정상
## 롤백
- consumer 재생성(nats-py, 설정 원값 max_deliver=-1·inactive=None) — 스트림 BOTLOG·메시지 원본 무영향

## 적용·검증 (10-03 11:48, 98 — 이사님 승인 [10-03] 후)
- 적용 전 현상(/jsz+nats-py 재실측): 8 consumer, 전부 max_deliver=-1·inactive=None. scan-tmp pending 258(진단 77→222→**258** — 증가 지속 재확인).
- ①잔재 3 삭제: tc02-durable·tc04verify 삭제(재조회 NOT FOUND) → gmlnx-scan-tmp는 ③재생검증 후 삭제(삭제직전 pending 258, 재조회 NOT FOUND).
- ②운영 5개 경계: relay98-ack→msg→notice→gmlnx-claude-inbox→once 순(1개씩 적용·같은명령검증·다음) — 전부 (5, 1h)로 전환 실측. nats-py 주의: inactive_threshold는 **초 단위**(3600 — nanosecond 아님. 3_600_000_000_000 넣으면 과대값 400. 실측으로 확정, 진단문서에 없는 계약).
- ③원장 재생: 8024 재시작 → totalLedger 569→569 무손실(재생 확인), relay98 pending=0·watchdog 평시, 8024 비-Duplicate 에러 0. 재시작전 스냅샷과 동일 — studio-8024-msglog durable 전환 상신은 불필요(재생됨).
- 최종: 5 consumer(전부 운영), 잔재 0, notice.broadcast pending 3×2(gmlnx) — 티켓 기재대로 본 건 범위 밖(PIPE#60(b)).
- 근거: 65b00e3, notes@본커밋.
