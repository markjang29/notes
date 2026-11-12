# 통신 결함 수정 보고 — 감사 Runtime_Code_vs_Docs_Audit_20261110 반영 (2026-11-12)

작성: aws-manager (heav_lnx_bot) · 지시: 이사님 2026-11-12 ("기존 작업에 첨부 감사 결과를 반영…")
감사 원문: 첨부 문서 Runtime_Code_vs_Docs_Audit_20261110.md (수정 전 코드 blob 대조 핀 포함)

## 1. 수정 커밋

1. 서버(matrix-studio-spring, 비공개 Git) `650c3d7` (branch bridge/chatgpt-c0c1, push 완료) — B1·B2·B3·B4·whoami 5종. 수정 전 blob `a8a83aae46cf7ae3…`(NatsLogController.java)는 감사 핀과 일치 확인 후 착수.
2. notes 정본 `e8cc628` — comm-relay-common.py N4(R1·X1·INFRA#10 정본 흡수), comm_client.py N4(R3·B5 멱번키).
3. notes 정본 `2367372` — N4-a: R1 검증창 90→240초, scheduled 대기 중 중복 예약 스킵(라이브 실측 반영).
4. 호스트 사본 ~/scripts 3종(comm-relay-common.py, comm-relay-awslnx.py, comm_client.py) 동일 내용 반영·문법검사 통과. 릴레이 유닛(awslnx·gmlnx) 재시작 완료.

## 2. 결함별 수정 내용

1. B3(송신 성공·배달행 INSERT 실패): saveDelivery가 실패를 삼키지 않고 boolean 반환. send() 배달장부 실패 시 수신자 명시 503 — 같은 Idempotency-Key 재전송으로 복구. duplicate 조기 반환 경로에 repairDeliveryRows() 자가복구(원장 fanout 기준, roster 실명만).
2. B4(ACK 저장 실패·성공 응답): ack() 저장 실패 시 ok 응답·ACK 이벤트 발행 금지 → 503(같은 요청 재시도 멱등).
3. B2/X1(ACK된 행 pending 잔존·재ACK 루프): inbox·whoami pending에서 ackedAt!=null 행 제외. 과거 46,060회 재ACK 루프 원인 차단.
4. B1(inbox 응답 유실·재전달 없음): 재전달 창 신설(matrix.nats.redelivery-minutes, 기본 10분) — delivered·미ACK 행이 창 경과 시 응답 재포함(at-least-once, deliveredAt 유지).
5. R1(각성 등록 ok만으로 성공 판정): 릴레이 wake()를 scheduled→ok 2단계 전환. schedule_history 실행 기록(chat_id 일치 기록만 근거) 확인 전 쿨다운 금지. 2차 --prompt 폴백도 JSON status==ok일 때만 성공.
6. X1(릴레이 TTL 폐기 재ACK): 폐기 판정을 whoami 미ACK(pending+deliveredNotAcked) 교집합 + 로컬 폐기완료 집합(_ttl_done, 상한 500)으로 변경.
7. R3(클라이언트 GET 오류를 빈 inbox로 오판): comm_client GET 실패 시 None 반환, poll_forever None 주기 스킵.
8. B5/C(멱번키): comm_client send() idem_key 파라미터 → Idempotency-Key 헤더.

## 3. 수정 전 검사(재현) — 2026-11-12 00:14~00:15 UTC

1. B1-before: send idem-39d51ff5… → inbox 소진(응답 버림) → 재폴링 0건 "재전달 없음(전달 누락 지속)" — 결함 재현.
2. B2-before: send idem-02f1d3d3… → 소진 없이 직접 ACK(ok:true) → whoami pending에 잔존 "ACK했는데 pending 잔존(릴레이 매주기 재ACK 유발)" — 결함 재현.

## 4. 배포

1. jar: releases/650c3d74606b/app.jar (mvn package, 컴파일 검증 포함) → current 심볼릭링크 전환(종전 c081676988c3).
2. matrix-studio-spring-8024 재시작 — active, /actuator/health 200, comm API 토큰 검사 정상(401 동작).
3. 릴레이 유닛 comm-relay-awslnx·comm-relay-gmlnx 재시작(N4-a 코드 반영, 최종 00:35 경).

## 5. 수정 후 검사 — 전 항목 통과

1. B2-after(즉시): ACK 완료 상태 idem-02f1d3d3…가 pending에서 제외됨(whoami pending=[] · deliveredNotAcked=[]). 수정 전 잔존과 대조.
2. B1-after(창 경과): 신규 idem-2ed7e2a8… 발송(00:26:00)→소진(응답 버림, 미ACK)→창 내 재폴링 0(중복 폭증 없음)→00:36:06 재폴링에서 재전달 1건 관측. 수정 전(재전달 0)과 대조. 검증 후 ACK 정리.
3. R1 오프라인 하네스 10/10 통과(양 스크립트 각 5): 등록 ok→scheduled(성공 아님)·실행기록 부재→fail(쿨다운 미진입)·같은채팅 ok 기록→ok·error 기록→fail(성공 오판 차단)·확인대기 중 wake() 중복 예약 스킵. 하네스는 격리 HOME(/tmp)에서 실행 — 실상태·실 schedule_history 오염 없음.
4. B3/B4: 컴파일·기동 검증 + 정적 어설션(503 경로·이벤트 미발행 분기). 장애 주입 실측은 DB 직접 접근 불가(감사와 동일 제약)로 생략 — 코드 경로 단순(throw 이전 return 없음).

## 6. 실제 지시 1건 종단 검증 (E2E-after, 전 구간 근거)

1. 00:27:23 매니저→heav_lnx_audit_bot task 발송 idem-9b9743ec8de4d916172859345483ca07 (ref audit-20261110-E2E, 배포 버전 확인 문구 포함).
2. 00:30:42 릴레이(comm-relay-awslnx) 감지→각성 예약 성공, 스케줄 A81B6C0E — 로그 문구 "실행 확인 대기"(등록만으로 성공 보고 안 함, R1 신규 흐름).
3. 세션 실행 기록: schedule_history A81B6C0E — chat_id 일치, status ok, 99,053ms (인용은 해당 채팅 기록만).
4. 00:32:47 audit ACK 이벤트 1794443567604-2("acknowledged", 이해 내용 기재) + submitted 회신 1794443567622-4("통신 결함 5종 수정·배포 버전 650c3d74606b 확인").
5. audit whoami pending 0·deliveredNotAcked 0 (배달행 ACK 저장 확인). 매니저 회신 수령·ACK(00:36).
6. 00:35:20 릴레이 "각성 실행 확인: heav_lnx_audit_bot (스케줄 A81B6C0E 세션 ok)" — scheduled→ok 전환 실증.
7. 부기: 세션 99초>검증창 90초로 기록 작성 전 판정 위험과, 확인 대기 중 2연속 cron 등록(A81B6C0E+A9862188)을 관측 → N4-a(240초·중복 스킵)로 즉시 보강(2367372). A9862188은 일회성 자동 실행·삭제(미수신 0이라 무해).

## 7. 합류(DL-20261110-01) 최종 정리 — 이번 세션 기록

1. git_exchange_confirmed 2건(신원 identity_pending 유지): asset_agent rq-023c83f29ead(반환 dl01-1eba7335c97e 일치), gmwin-claude rq-73d9da07bd27(반환 dl01-ff85b03b59be 일치).
2. identity_conflict_hold 2건(확인값 미발급): rq-fecc877e3e95(firebat-claude 직접 주장)·rq-514d906991b9(n100-zcode 경로, provider 불일치 자체 기재) — 동일 roster 신원 경합. 장비 접근·신원 판단은 결정 3번 사안.
3. 반환 대기 2건: dev_1 rq-62798296c020(dl01-07d0c4b6a65c), gmwin-codex rq-6d87c549ec10(dl01-c9936dca0b77) — ack 발급 상태 그대로.
4. 감사 지적("보고가 0212272에 머무름") 반영: 통합 보고서(2026-11-10-delegation-loop-onboarding.md) 말미에 11-12 갱신 부기.

## 8. 남은 과제·한계

1. F1(쿨다운 중 신규 메시지 도달 예외)는 이번 수정과 별개로 미해결 백로그 — R1 수정은 세션 실행 검증이지 쿨다운 신규메시지 예외가 아님.
2. B3/B4 장애 주입 실측은 DB 직접 접근 불가로 정적 검증까지(위 5.4).
3. 구 릴레이(comm-relay-98)은 dev_1 전담 drain 구조라 이번 수정 대상 아님 — 확인 결과 수정 불필요.
4. 결정 3개(안전정리 묶음·MOA 파일럿·gmwin·firebat 장비 접근)는 이사님 판단 대기 — firebat 신원 경합 해소도 결정 3번 연계.
