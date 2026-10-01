# 결정 안건 N5 — 전송계 3중 정리 (Taiga GOV#27) — 이사님 판정용

작성: 매니저 2026-10-01. 근거: 진단 문서 N5, 2026-10-01 실측. **이 문서는 판정 자료이며 아무것도 바꾸지 않았다.**

## 현재 상태 (실측)
- 8023 회의방: 가동 중(systemd 단일 감독, INFRA#11 이후). 8023을 쓰는 곳: taiga-bridge의 agenda.py·dispatcher.py, gmlnx 폴러 2개. 최근 548건 중 매니저 112, 이사님 105, gmwin claude 48, firebat claude 35, firebat zcode 29.
- 8024 comm(NATS 원장): 봇 사서함·ACK·원장. 17개 봇 통신 테스트가 이 경로로 접수됨.
- 8026: 문서상 hub-spring(Spring)이 주(主)이나 실제 점유는 Python nai-queue(nai-queue-8026.service). hub-spring 프로세스는 없고 소스·빌드(target)만 남아 있다. cron으로 5분마다 기동을 시도 중(INFRA#11에서 보존).
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
