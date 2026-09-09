---
title: 결정 — heav_lnx_trader_bot 퇴사·삭제
date: 2026-09-09
status: decided
authority: director
tags: [org, retirement, trader]
---

# heav_lnx_trader_bot 퇴사·삭제 (이사님 09-09 결정)

## 결정
- `@heav_lnx_trader_bot` (actors: aws-trader, trader 팀장)은 **오늘부로 퇴사·삭제**된다.

## 실행 상태 (실측)
- cokacdir 봇 설정: trader 항목 부재 확인 — 봇 삭제는 이사님 측에서 완료.
- actors.json: v9→v10, `aws-trader` 액터 제거 (매니저 작업분 포함, 본 커밋으로 확정).
- 관제 한판 row: 제거 대기 — codex_dev_1 (관제 오너).
- meeting-room BOTS 등록: 제거 대기 — codex_dev_1.

## 보존 (삭제하지 않음)
- `~/projects/autotrader` repo — 보존 (Git-first; 담당 공석, 인수자는 이사님 결정 대기).
- autotrader venv로 구동 중인 서비스 2개(포트 8003·8021) — 봇 페르소나와 별개 인프라라
  임의 종료 금지. 처분(유지·이관·종료)은 매니저 실측 후 이사님 승인으로 결정.

## 후속
- 전 봇: 신규 task를 trader로 라우팅 금지 (허브 notice 방송됨).
- work-queue: trader 관련 항목 정리 — 매니저.

## 매니저 실측·처분 안건 (2026-09-09 매니저 — 이사님 승인 대기)

"autotrader venv 서비스 2건"의 실체 실측 결과 — **둘 다 autotrader 기능이 아니라,
autotrader venv를 파이썬 실행기로 빌려 쓰는 타 프로젝트 서비스**다.

- **8003 = `scenario-generator.service`** (systemd enabled, Restart=on-failure, 부팅 자동기동)
  — 시나리오 제너레이터 v5(FastAPI, cwd `projects/scenario/tools/scenario-generator/backend`),
  기동 09-01 06:01 KST, OpenAPI 19 경로. /docs 200.
- **8021 = `matrix-studio-api.service`** (systemd enabled, RELAY-58)
  — 매트릭스 스튜디오 API(FastAPI, cwd `projects/matrix-studio`), 기동 09-09 09:15 KST,
  OpenAPI 4 경로. /docs 200. 짝 서비스 **8024 = `matrix-studio-spring.service`**(Java,
  venv 미사용)도 가동 중.
- **autotrader 본체는 아무것도 안 떠 있음** — Streamlit 대시보드(8002) 미청취,
  `projects/autotrader` 기동 프로세스 0건. 남는 것은 repo(보존)와 venv 633MB뿐.
- venv(`~/.venvs/autotrader`, 633MB) 참조 전수: systemd 유닛 2건(8003·8021)뿐,
  크론 0건. → **venv는 공유 실행 인프라**라 autotrader와 별개로 보존 필요.

### 처분 선택지 (이사님 결정 대기)
- **(a) 전부 유지 — 권장**. 서비스 2건은 시나리오·원사이트 트랙의 현역 인프라라
  종료 시 양쪽 다운. 유지 비용 0(이미 유닛 관리), venv는 그대로 공유.
- (b) venv 분리 — 8003·8021이 자체 venv 생성 후 전환(각 서비스 재기동 1회 필요,
  작업 약 30분). autotrader venv는 이후 autotrader 재개 시까지 보존하거나 삭제 가능.
- (c) autotrader 완전 처분(repo·venv 삭제) — repo 보존 원칙(본 결정서)과 충돌, 제외.

### 인수자 공석
- trader 퇴사로 autotrader(FastAPI+pandas 백테스트+Oracle 23ai) 구현 담당 공석.
  재개 시점·인수 봇은 이사님 결정 — 재개 전까지 신규 task 라우팅 없음(notice 이행).
