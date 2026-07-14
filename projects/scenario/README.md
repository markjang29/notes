---
title: Scenario 프로젝트 운영 인덱스
status: active
last_reviewed: 2026-07-14
---

# Scenario 프로젝트 운영 인덱스

이 디렉터리는 사람이 보는 프로젝트 정본이다. 질문·결정·우선순위·현재 인수인계만
관리하고, 실행 숫자와 상태를 복사해 별도의 진실을 만들지 않는다.

## 바로 보기

- 사용자 질문 접수와 처리 상태: [inbox.md](inbox.md)
- 실행 로드맵·공수·담당·완료 조건: [roadmap.md](roadmap.md)
- 현재 단건 체크포인트: [handoffs/current.md](handoffs/current.md)

## 정보 소유권

| 정보 | 정본 |
|---|---|
| 불변 운영 규칙·RCC 인증 | `scenario/HARD_RULES.md` |
| Codex/Claude/ZCode 실행 계약 | `scenario/.agents/skills/` |
| 일일 신규/레거시 배분 | `scenario/catalog/operations/daily_ingestion_policy.json` |
| 현재 열린 게시글·terminal 상태 | `scenario/catalog/asset_lifecycle.ndjson` |
| 실패·실행 증거 | `scenario/catalog/reports/skill_runs/` |
| 코드·테스트·기술 명세 | `scenario` Git 저장소 |
| 질문·방향·비용·우선순위 | 이 디렉터리 |

`scenario`는 현재 Windows에서
`C:\Users\heave\projects\scenario-next-one` worktree를 사용한다. 다른 worktree 이름을
정본 이름처럼 문서에 고정하지 않는다.

## 코드 한눈에 보기

| 영역 | 현재 경로 | 역할 | 판단 |
|---|---|---|---|
| 단건 수집 계약 | `.agents/skills/arca-collection/` | 로그인부터 terminal까지 | 유지·효율화 |
| Matrix 공장 | `tools/matrix_factory/` | 세계·캐릭터·페르소나·서사 조립/재현 | 새 정본 |
| 수집기 | `tools/crawler/` | Arca 탐색·본문·링크 | 유지 |
| 파서 | `tools/risu_parser/` | 승인 포맷 파싱·검증 | 유지 |
| 정책 선택기 | `tools/ingestion_policy/` | 신규/레거시 균형 | 유지 |
| lifecycle | `tools/asset_lifecycle.py` | 한 건 잠금·판정·종결 | 트랜잭션 보강 |
| 로컬 자동화 | `tools/scenario_automation/` | 설정 sync·lease·스케줄 | Hub로 흡수 |
| 요청 bridge | `tools/request_bridge/` | AWS 요청 조회 | Hub 전환 후 호환층 |
| 구형 생성기 | `tools/scenario-generator/` | FastAPI/Oracle/랜덤 실험기 | Matrix 출력 어댑터로 축소 |
| Notes | `C:\Users\heave\notes\projects\scenario\` | 질문·결정·로드맵 | 사람 정본 |

현재 도구는 Python 중심 81개 파일, 약 17.6K줄이다. 전면 재작성보다 패키지·의존성·진입점
표준화가 비용과 위험이 낮다.

## 관리 규칙

1. 새 질문은 `inbox.md`에 한 줄로 접수한다.
2. 방향이 확정되면 `decisions/` ADR로 옮긴다.
3. 실행 항목은 `roadmap.md`에 담당·공수·완료조건을 둔다.
4. 현재 진행 중인 것은 `handoffs/current.md` 한 파일만 갱신한다.
5. 실행 상태는 machine truth를 링크하고 Notes에 복제하지 않는다.
6. 종료된 상세는 Git 이력 또는 `archive/`로 보낸다.

