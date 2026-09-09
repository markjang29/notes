# ADR — trader 봇 퇴사·삭제

- 날짜: 2026-09-09
- 결정자: 이사님 (Telegram 지시 — "오늘부로 퇴사, 삭제")
- 상태: accepted

## 결정
`@heav_lnx_trader_bot`(trader 팀장, actor `aws-trader`)을 조직에서 제외한다.
autotrader 프로젝트와 repo(`~/projects/autotrader`)는 **보존**한다 — 퇴사한 것은 봇이지
프로젝트가 아니다. 재개 시 구현 담당 봇은 재배정한다(work-queue 대기결정 #2).

## 정리 내역 (매니저 집행, 09-09)
- `~/.cokacdir/bot_settings.json` — 봇 블록(`e802e57aacbe8f8b`) 제거. 백업 `bot_settings.json.bak-20260909-trader-offboard`. **다음 cokacdir.service 재시작 때 프로세스 미기동 반영**(단일 프로세스라 즉시 재시작은 전 봇 세션 사망 → 유보)
- `notes/projects/agent-ops/actors.json` — `aws-trader` 액터 제거(13→12)
- `notes/L0-agent-boot.md`, `notes/onboarding.md` — 키 매핑 라인 제거(주석으로 이력 연결)
- `notes/org-structure.md` — 조직도·프로토콜·체크리스트·/contextlevel 기록 5곳 갱신
- `notes/work-queue.md` — aws-trader 상태 갱신, autotrader 재개 안건에 담당 공석 표기
- `notes/healthcheck-deployment-checklist.md` — 4.3 절 비활성화
- `notes/policy-reread-pending.md` — 대상 소멸 처리
- `~/projects/meeting-room/server.py` — REMOTE trader 항목 제거(문법 검증 OK, 재시작 시 반영)
- memory `current-work-state.md` — 팀장 3명→2명

## 교훈/주의
- actors.json 정리 시 `json.dumps` 문자열 매칭으로 제거하면 `autotrader` 프로젝트를 참조하는
  무관 액터까지 일괄 삭제되는 과잉 제거가 일어난다(실제 13→6 사고 → git 복구 후
  `actor_id=='aws-trader'` 정밀 매칭으로 재수행). **레코드 삭제는 식별자 필드 정밀 매칭으로만.**

## 영향
- AWS 봇 10기 → 9기. 메시지 테스트 통과 기준 10/13 → 9/12.
- autotrader 관련 신규 지시는 매니저가 수령 후 담당 재배정 전까지 보류 큐.
