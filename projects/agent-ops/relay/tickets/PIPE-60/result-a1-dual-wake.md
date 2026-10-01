# PIPE#60 [N3] 잔여 — 부록 A1 각성 이중화 (2026-10-01, 98)

## 선행해소 확인 (N3 본문 — 04:25 매니저 세션 notes@e5b307e로 완료된 것)
- (a) 큐 적체 → 지수백오프(BACKOFF_MAX=8배) ✅  (b) 미ACK 공지 루프 → TTL 72h 폐기 ✅
- (c) 커버리지 firewin/gmwin → 배포절차 문서화+roster wake:false ✅  (d) 키없는봇 로그스팸 → nokey 1회화 ✅
- (e) 로그 리터럴 \n → 3abcbc2 수정 ✅
- 검증기준: 스킵 로그 일 50줄 미만(로그 상태변화시 1회화로 충족), 성공률 지표(주기종료 로그에 % 표시 — 실측: "각성성공률 -1% (0/0)" 출력 확인)

## 잔여 = 부록 A1 개정1 (각성 이중화) — 이번 커밋
- **문제(재현)**: wake()가 `cokacdir --cron --once` 1개 경로. 12:29 각성 "성공" 후에도 heav_lnx_bot 미수신 13건 적체(13:00 실측) — 1차 경로가 큐 적체·데몬 소화지연(결함1)에 묶이면 소화가 안 됨
- **조치** (notes@dec58db + df4ddf7, 3단 계약):
  1. 1차 실패 → 2차 `cokacdir --prompt --key-file` 직접 호출(큐 무관·동기실행, timeout 300s) — 실측: 5초내 응답
  2. 1·2차 모두 실패 → 3단 8024로 "[각성 경보]" 1회 발행(type=task, ref=wake-fail) — 사이드카 무음 원칙 유지(장애시만)
  3. 1차 예외(cokacdir 부재·timeout)시에도 2차 폴백(시험중 발견한 누수 제거)
- 적용처: 정본 comm/comm-relay-common.py + awslnx판 scripts/comm-relay-awslnx.py(95-5 사본 — 95-4-b 준용, 코드동기화 주석에 정본해시 명기) + gmlnx 사이드카 재기동

## 검증 (같은 명령)
- 단위시험(1차 강제실패): "각성 1차 예외 → 2차 폴백: 강제실패(시험)" → "각성 성공(2차 --prompt, 1차예외 폴백): heav_gmlnx_claude_bot" → wake()=True
- 실제 소화: heav_gmlnx_claude_bot 사서함 pending 1 → 0 / DNA 0 (2차 경로가 실제로 99를 깨움)
- 회귀: 3개 사이드카(awslnx·gmlnx·98) 모두 active, 98 사서함 0/0, 8023 폴링·TTL·적체방지 기존 기능 무변경

## 잔여 표기
- "awslnx 일부" — heav_lnx_bot 13건 적체는 결함1(데몬 토큰 미등록)이므로 INFRA#11·12와 별도 진행건. 이중화로 각성은 도달하나 소화는 데몬 등록 후 자동.
