# INFRA#10 [N2] 8024 REST 봇 토큰 강제+쿼리스트링 제거 — 승인게이트 (2026-10-02, 98)

## 재현 (운영 무변경)
- 무토큰 200: `curl -s -o /dev/null -w '%{http_code}' 'http://127.0.0.1:8024/api/nats/whoami?bot=heav_lnx_codex_dev_1_bot'` → 200
- 타봇 사서함 열람 200: `.../api/nats/inbox?bot=heav_lnx_bot` → 200 (공용토큰 1개라 누구나 열람)
- 근거: 진단문서 §4 N2 — 8024가 신원 확인 없이 봇 상태 노출, 토큰이 쿼리스트링/본문으로 서버로그에 남음

## 준비 (8024 브랜치 n2-token-bearer @ 8024 repo — 컴파일 통과, 배포 승인 후 적용)
- NatsLogController.java:
  - `matrix.nats.comm-tokens-file`(JSON {봇명:토큰}, 600) 신설 — 파일 설정 시 소유자 검사
  - Authorization: Bearer 헤더 우선, 쿼리·본문 token은 하위호환 수용(제거 2단계 별도 상신)
  - 미제시 401 / 소유자 불일치 403 / 파일 미판독 시 1단계(공용 토큰) 폴백 — 가용성 우선
  - roster 60초 캐시와 동일 규약(읽기전용·값 노출 없음)
- 컴파일: mvn -DskipTests compile → BUILD SUCCESS(JDK17)

## 승인 후 적용 절차 (요약 — 상세는 8024 배포 절차 준용)
1. 토큰표 신설: 봇명→토큰 JSON(600) + MATRIX_NATS_COMM_TOKENS_FILE env에 경로
2. 8024 재배포(브랜치 n2-token-bearer → 빌드 → 서비스 재시작)
3. 각 봇 클라이언트(comm_client.py 등)에 토큰표 참조 전달 — 점진 전환(1단계 공용 토큰도 병행 수용)

## 롤백
- MATRIX_NATS_COMM_TOKENS_FILE 미설정(또는 제거)→ 재시작: 1단계 공용 토큰 동작으로 완전 복귀

## 적용·검증 (10-03 11:29, 98 — 이사님 승인 [10-03] 후)
- 선행: 전봇 공지 1건 8024 notice.broadcast(fanout 18, id 1791026670905-182) — 토큰 값 미기입, 경로·취득방법만.
- 토큰표: `~/.config/matrix-studio-spring/comm-tokens.json`(600, 12봇 — 로컬 보유분. 로컬 외 봇 6: gmwin_devpass·aws512·firebat_zcode·firebat_claude·firebat_codex·gmwin_zcode·gmwin_codex·gmwin_claude 중 미등록분 403 — 회신에 잔여 명시) + env `MATRIX_NATS_COMM_TOKENS_FILE` 경로만.
- 배포: 8024@n2-token-bearer(2e19147) 빌드 BUILD SUCCESS → releases/2e1914751341 → current 심링크 교체 → 재시작 active.
- 클라이언트 5종 표 참조 패치+재기동: comm-relay-98·comm-relay-awslnx·comm-relay-common(gmlnx relay)·room-poller-gmlnx-zcode·comm-poller-gmlnx(기존 표참조). 토큰값은 어디에도 기입하지 않고 표(600)에서 읽음. 미판독시 무토큰 폴백.
- 검증(같은 명령 재실측): 무토큰 whoami 200→**401** · 자기토큰 200 · 타봇토큰 403 · Bearer헤더 200 · inbox 200 · send→ack 200(6/6). relay98 기동완료 pending=0, relayawslnx 각성 정상(audit·scenario 2건 성공 11:28) — 단 표 미등록 원격봇(gmwin_devpass 등) whoami 401로 감시보류(본봇 토큰 등록 시 자동해소 — 표에 봇명:토큰 추가만).
- 근거: 8024@2e19147, 본티켓, 롤백 1줄(env 경로 제거→재시작).
