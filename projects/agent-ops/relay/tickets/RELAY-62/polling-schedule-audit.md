---
ticket: RELAY-62
stage: relay:3-영향성검토
owner: aws-audit
date: 2026-09-07
status: submitted
---

# RELAY-62 polling/schedule audit

## 한 줄 결론

현재 이 대화 기준 Cokacdir 활성 schedule은 없다. 다만 OS cron/timer에는 매분·30분 주기의 폴링성
작업이 남아 있어, LMM 토큰 낭비보다는 "빈 폴링의 운영 부하"와 "요청 발생 시 LMM 호출 경계"를
계속 감시해야 한다.

ELI5: 지금 알바생에게 예약된 심부름은 없지만, 가게 안에는 1분마다 우편함을 열어보는 직원과
30분마다 창고를 도는 직원이 있다. 우편이 없으면 돈이 안 들지만, 너무 자주 문을 여닫는지는 봐야 한다.

## 확인 범위

- Cokacdir schedule list: 현재 이 대화 소유 schedule 없음.
- Cokacdir schedule history: 이 대화 소유 기록만 필터링.
- OS cron: 운영자 crontab.
- systemd timer: 시스템/user timer.
- 주요 실행 중 프로세스: polling/watchdog/scheduler 성격만 확인.
- 주요 스크립트: LMM 호출 여부, 빈 폴링 시 종료 여부, 중첩 방지 여부.

## Cokacdir schedule

- 현재 활성 schedule: 0개.
- 이 대화의 schedule history: 92개 고유 schedule 기록.
- 그중 poll/loop/status 성격으로 분류된 기록: 30개.
- 중요한 과거 반복 루프:
  - 소설/자산 대량 세션 루프: 88회 실행, 2026-09-02 종료 기록.
  - 소설 수집 운용 콘솔 반영 루프: 10회 실행, 2026-09-02 종료 기록.
  - 소모 스위치 루프: 32회 실행, 2026-09-03 종료 기록.
  - matrix_asset_agent 안전 카드 루프: 286회 실행, 2026-09-03 마지막 기록.

판정: 현재 활성은 아니므로 즉시 LMM 토큰을 쓰는 Cokacdir schedule은 확인되지 않았다. 다만 과거에는
짧은 주기의 장시간 루프가 많았으므로, 재등록 시 반드시 "빈 폴링 LMM 금지"와 "상태 변화만 보고"를
조건으로 걸어야 한다.

## OS cron / timer 판정

### 낮은 LMM 토큰 위험

- request router poll: 매분 실행. 코드상 새 requested 요청이 없으면 즉시 종료한다. 새 요청이 있을 때만
  Cokacdir one-shot으로 매니저 라우터를 깨운다.
- 529 watchdog: 1초 간격으로 로컬 프록시 로그를 tail한다. 새 LMM 작업을 시작하지 않고, 최종 529 실패가
  있을 때만 Telegram alert를 보낸다.
- chat log backup: 매시간 백업. LMM 호출 없음.
- session reaper: 30분마다 고아 세션 정리. LMM 호출 없음.
- room log autocommit: 매시간 회의방 로그 자동 커밋. LMM 호출 없음.
- scenario dashboard ledger sync: systemd timer 60초 주기. Git fetch/show 중심. LMM 호출 없음.

### 운영 부하/정책 점검 필요

- request router poll은 원칙에 맞게 빈 폴링 LMM 0 구조지만, 요청 발생 시 one-shot LMM을 만든다.
  다음 개선은 요청 digest/idempotency를 관제 화면에 남겨 중복 LMM 깨우기를 더 쉽게 감사하는 것이다.
- scenario dashboard ledger sync는 LMM 토큰은 쓰지 않지만 60초마다 Git fetch를 수행한다. 상태 변화가
  낮다면 5분 이상 또는 digest 기반으로 줄이는 방안을 검토할 만하다.
- S0 worker는 30분마다 자산 번들 처리와 원격 복사를 수행한다. LMM은 쓰지 않지만 대용량 I/O와 외부 저장소
  부하가 있을 수 있으므로 backlog가 없을 때 빠르게 종료하는지 계속 확인해야 한다.
- workbench backup은 LMM은 쓰지 않지만 외부 release 조회/download 경로가 있어, 장기적으로는 버전 pin과
  digest 검증이 필요하다.

## 실행 중 프로세스 관찰

- Cokacdir Telegram long-polling 서비스가 실행 중이다. 사용자/봇 요청을 받기 위한 필수 프로세스이며,
  요청이 없으면 LMM 작업을 새로 만들지는 않는다.
- 529 watchdog이 실행 중이다. 529 감지/알림 목적이며 LMM 호출은 하지 않는다.
- 여러 웹 서비스와 대시보드 프로세스가 실행 중이다. 이 감사에서는 CPU 과부하 증거를 확인하지 못했다.

보안 주의: 일부 장기 실행 프로세스의 credential 전달 방식은 별도 hardening 대상으로 보인다. 이 문서는
토큰값을 기록하지 않는다.

## 43.201.34.144 진입점 확인

- `http://43.201.34.144/`: 200 OK, MATRIX 홈 응답 확인.
- `http://43.201.34.144/policies`: 404.
- `http://43.201.34.144/governance`: 404.
- `http://43.201.34.144:8018/policies`: 404.
- `http://43.201.34.144:8018/governance`: 404.

판정: 새 진입점 자체는 살아 있지만, 정책센터와 관제 한판으로의 프록시/라우팅은 아직 미완이다.
현 시점에서 "43.201.34.144에서 정책센터/관제 접근 완료"라고 보고하면 안 된다.

## 현재 접근 가능한 정책/관제

- 기존 legacy 8018 정책센터와 관제 한판은 새 Notes HEAD를 정상 표시한다.
- 새 `edge-home-entrypoint` 정책 문서가 정책 API에 포함된다.
- `aws-audit` 자기 row는 새 POLICY_SHA로 갱신되었다.

## 권고

1. `43.201.34.144`의 `/policies`, `/governance`를 홈서버 또는 기존 정책/관제 서비스로 프록시한다.
2. request router poll은 현 구조를 유지하되, 요청이 있을 때만 LMM으로 전달된다는 감사 이벤트를 남긴다.
3. 60초 Git fetch timer는 5분 이상 또는 digest/mtime 기반으로 낮추는 개선안을 만든다.
4. 30분 이하 반복 작업은 신규 등록 시 "빈 결과 보고 금지, 상태 변화만 보고" 조건을 필수화한다.
5. 장기 실행 프로세스의 credential 노출 가능성은 별도 보안 hardening 티켓으로 분리한다.
