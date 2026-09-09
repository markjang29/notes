---
name: checkpoint-529-recovery-0703
description: 2026-07-03 529 레이트 리밋 발생 시 체크포인트
metadata: 
  node_type: memory
  type: project
  incident_date: 2026-07-03
  incident_type: 529-rate-limit
  originSessionId: 191fd855-42e2-43bf-838c-72845770b877
---

# 529 레이트 리밋 체크포인트

**발생 시점:** 2026-07-03 (컨텍스트 윈도우 포화 추정)

**증상:**
- 529 에러 반복 ("또 529야....")
- 컨텍스트 윈도우 최대치 도달
- 회피(요약/분할) 메커니즘 실패

**현재 work-queue 상태:**
- autotrader: 백테스트 웹 REST API 구현 완료, Oracle DB 연동 완료, 대시보드 기동 OK (AWS 보안그룹만 오픈 대기)
- RPG: Godot 엔진 확정, Reasoning-Parry 데모 완료, APK export 성공, 시나리오 팀장 핸드오프 완료
- scenario: 제조공장 은폐팩 방향 확정 BUT 07-01 이후 팀장 비활성 (0건 산출, coverup-B01 미생성) ★이슈

**인프라:**
- Oracle DB Free 23ai: 1521 LISTEN (설치됨, docker 권한 분리)
- 매니저 cron 3종 정상 가동 (01:00 야간 배정 / 07:00 아침 브리프 / 08:00 시나리오 리포트)
- 포트 정책 확정 (8000-8099 API / 1521 Oracle / 80·443 nginx)

**복구 절차:**
1. 세션 /clear → 컨텍스트 해제
2. work-queue.md 우선 읽기 (L2 규칙)
3. 팀장 상태 점검 (특히 scenario 팀장)
4. 이슈 해결 (보안그룹 오픈 / scenario 팀장 재배정)

**다음 액션:** /clear 실행 → 매니저 복구
