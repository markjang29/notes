# Spring 완전 이식 + 파일 DB화 계획 v1 (2026-09-17, 개발팀장 Zcode)

> 이사님 정정(09-17): 지향점은 **파이썬 소멸 — 스프링부트에서 로직까지 직접 돌리는 완전 마이그레이션 + 파일 데이터 DB화**.
> 프록시 흡수(껍데기만 스프링)는 중간 안전 단계일 뿐 목적지 아님.

## 4단계 게이트 (사이트별)
1. **화면 흡수**(프록시) — 안전 병행 운행 확보 (BD 완료)
2. **자체 데이터 DB화** — 사이트 소유 파일(jsonl/json) → JPA 엔티티 + 초기 마이그레이터
3. **로직 이식** — 파이썬 계산로직 Java 재작성, 실측 동치 검증(응답 대조)
4. **파이썬 종료** — 원본 서비스 중지·포트 폐쇄 (이사님 전환 게이트 승인 후)

## 1호 케이스: BD 봇 대시보드(8025)
- 자체 데이터: profiles.jsonl(20)·notices·dismissed·model-change-log → H2(JPA): BotProfile, Notice, DismissedNotice, ModelChangeLog
- 외부 집계(roster·승인보드·회의방·게이트웨이·봇설정): Spring 서비스가 원장 파일/HTTP 직독 — 각 원장은 해당 시스템 이식 때 DB화
- 로직: /api/{profiles,kanban,tokens,models,model,decisions,roadmap,skills,notices,notices/active,gateway} 11 엔드포인트 Java 재작성
- 동치 검증: 파이썬 응답 vs 스프링 응답 JSON 대조 자동화 → 통과 시 8025 중지 티켓(이사님승인)

## 사이트별 분류 (완전이식 기준, 순서 제안)
| 사이트 | 난이도 | 비고 |
|---|---|---|
| BD 봇 대시보드(8025) | 하 | 1호 케이스 — 진행 중 |
| ENGINE(8010)·SETTINGS(8006) | 하~중 | 조회형 |
| APPROVAL(8005) | 중 | decisions/requests json → DB, 브릿지 연동 재조정 |
| ARCADE(8004) | 중 | releases/approvals ndjson → DB |
| HOME(8018)·MEETING(8023) | 상 | 허브 — 최후 |
| WORKBENCH(8015)·IMAGE_STUDIO(8016) | 상 | mongo 의존 → 유지 또는 H2 전환 판정 |
| CANDIDATE(8008)·RPG(8009)·RISU_LAB(8003)·MV(8020) | 중 | release 사본 운행 → repo 정본화 병행 |

## DB 전략
- 기존 H2 체인 DB 확장(사이트별 테이블 prefix) — 인프라 단순 유지
- 파일 원본은 이식 검증 후 아카이브(gdive 3차), 즉시 삭제 안 함

## 게이트 준수
각 사이트·각 단계 Taiga 티켓(SITE 프로젝트) — 3→4단계 전환은 승인보드 판정 필수.
