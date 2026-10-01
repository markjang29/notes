# 결정 안건 N5 — 전송계 3중 정리 (Taiga GOV#27) — 이사님 판정용

작성: 매니저 2026-10-01. 근거: 진단 문서 N5, 2026-10-01 실측. **이 문서는 판정 자료이며 아무것도 바꾸지 않았다.**

## 현재 상태 (실측)
- 8023 회의방: 가동 중(systemd 단일 감독, INFRA#11 이후). 8023을 쓰는 곳: taiga-bridge의 agenda.py·dispatcher.py, gmlnx 폴러 2개. 최근 548건 중 매니저 112, 이사님 105, gmwin claude 48, firebat claude 35, firebat zcode 29.
- 8024 comm(NATS 원장): 봇 사서함·ACK·원장. 17개 봇 통신 테스트가 이 경로로 접수됨.
- 8026: 문서상 hub-spring(Spring)이 주(主)이나 실제 점유는 Python nai-queue(nai-queue-8026.service). 2026-10-01 재확인(ps 직접 조회, pgrep 자기 자신 제외): hub-spring 프로세스는 **없다**(java 프로세스는 8024 app.jar 하나뿐). 빌드(target/hub-spring-1.0.0.jar, 9월 11일)와 java 실행 파일은 남아 있다. cron 2줄(5분 감시·@reboot)이 기동을 시도하는 구조지만 8026 포트를 nai-queue가 먼저 잡고 있어 뜨지 못하는 것으로 추정한다(실패 로그는 확인하지 못함: /tmp/hub-spring.log는 9월 11일 이후 갱신 없음). 한 가지 위험: nai-queue가 내려가면 cron이 hub-spring을 8026에 올릴 수 있다. cron 2줄 삭제(안 A 3번)는 이 위험을 없앤다.
- 이 때문에 dispatcher가 회의방에 "이사님" 명의로 발령하는 문제(G5)도 8023 의존에서 나온다.

## 선택지
- 안 A (권고): 8024로 단일화. 단계 — ①dispatcher·agenda를 8024 type=task 발송으로 교체(G5와 함께) ②gmlnx 폴러 2개에 8024 폴링 추가(INFRA#15) ③8023은 읽기 전용으로 강등 후 폐지 일정 확정. hub-spring은 폐기하고 8026은 nai-queue로 문서 정정, cron 2줄 삭제.
- 안 B: 3중 유지. 비용: 증적이 3곳으로 갈라져 감사가 어렵고, 같은 문제(토큰 경로 등)를 3번 고쳐야 함.
- 안 C: hub-spring 복구해 8026을 주 hub로. 비용: Spring 운영 부담이 늘고 이미 8024 원장을 채택한 결정과 충돌.

## 이사님이 정해 주실 것
1. 안 A/B/C 중 선택
2. 안 A면 8023 폐지 시점
3. hub-spring cron 2줄 삭제 승인

## 되돌리기
- 어느 안이든 단계마다 롤백 가능(설정 원복). 8023 폐지만 비가역에 가까우므로 마지막 단계로 둔다.
