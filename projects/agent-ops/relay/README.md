---
title: Relay 파이프라인 v1 (Jira 연동)
status: active
updated: 2026-08-19
owner: director 결정 / zcode 구축
---

# Relay v1 — 요구사항 → 구현 게이트

Jira 프로젝트 `RELAY` (heavenlyiris-matrix.atlassian.net, free plan)와 연동된
6단계 게이트 파이프라인이다. 각 단계를 통과해야 다음 단계로 이동한다.

## 단계와 산출물

| 단계 | 라벨 | 산출 아티팩트 | 템플릿 | 승인자 |
|---|---|---|---|---|
| 1 확보 | `relay:1-확보` | req (원문·출처·날짜) | `templates/1-req.md` | director |
| 2 정제 | `relay:2-정제` | spec (측정 가능 조건) | `templates/2-spec.md` | aws-manager |
| 3 영향성검토 | `relay:3-영향성검토` | impact (영향 repo·봇·서비스) | `templates/3-impact.md` | aws-audit |
| 4 설계검토 | `relay:4-설계검토` | design (구조·근거) | `templates/4-design.md` | director |
| 5 구현 | `relay:5-구현` | 커밋(티켓키 포함) + 테스트 | `templates/5-impl.md` | 자동 검증 |
| 6 코드리뷰 | `relay:6-코드리뷰` | review (승인/반려+사유) | `templates/6-review.md` | 해당 팀장 |

## 저장소 지도 — "Git에 넣는다"의 구체적 의미 (2026-08-20 확정)

| 무엇을 | 어디에 | 비고 |
|---|---|---|
| 요구사항·단계·상태 | **Jira RELAY** | 아티팩트 파일은 안 올림(링크만) |
| Relay 규칙·공지문·조직 정본(actors.json)·티켓 아티팩트(`relay/tickets/<키>/`) | **notes-registry** (github: markjang29/notes) | 조직 운영의 정본. 로컬 `/home/ubuntu/deploy/notes-registry` |
| 자산 ADR·매니페스트·소스유닛·검증 로그·자산 도구(워크벤치 등)·태그 사전 | **matrix_asset_agent** (github: markjang29/matrix_asset_agent) | **작업 사본은 `/home/ubuntu/projects/matrix_asset_agent` 하나만** — `/home/ubuntu/matrix_asset_agent`는 같은 원격의 읽기 참조용. 이중 커밋 금지 |
| 시나리오 산출물·소설 자산화 | **scenario** (github: markjang29/scenario) | |
| 승인보드 코드·decisions.json | **approval-board** (로컬 `/home/ubuntu/projects/approval-board`, 원격 없음) | 서버 장애 시 코드 유실 위험 — 원격 달아둘 것(향후 과제) |
| RPG·autotrader 도메인 | **rpg_game / autotrader** (github: markjang29/*) | |
| 대용량 원본·이미지 | **구글 드라이브** (COLD CAS / VISUAL-REF, ADR-0006) | Git 아님. Git엔 SHA stub만 |
| 실행 트레이스 | **LangSmith** (relay-observability) | Git 아님 |

규칙: 커밋 메시지에 RELAY 티켓 키 포함. 어느 repo인지 애매하면 notes-registry의 relay/tickets/에 넣고 티켓 코멘트로 연결 — 나중에 정본 repo로 이동(이동 이력 커밋).

## 규칙


- **아이디어 → Jira 선행 원칙 (이사님 2026-08-20 결정)**: 이사님이 아이디어·요구를 주면
  어떤 봇이든 개발 착수 전에 반드시 먼저 RELAY 요구사항 티켓(라벨 `relay:1-확보` +
  `요구사항-*`, 원문을 요약 없이 기입)을 만들고, 그 티켓 키를 받아야 코드를 고치기
  시작할 수 있다. 티켓 없는 착수는 무효이며 즉시 중단하고 티켓부터 만든다.
- 아티팩트는 전부 이 디렉토리(`relay/tickets/<RELAY-키>/`)에 Git 커밋한다. Jira에는 링크만 건다(2GB 저장 제한).
- Jira 티켓 키(`RELAY-n`)가 모든 아티팩트 파일명과 커밋 메시지에 들어간다.
- 단계 이동은 라벨 갱신 + 해당 단계 산출물 커밋이 둘 다 있어야 성립한다.
- **단위 테스트 게이팅 (이사님 2026-08-23 지시)**: 5-구현 산출물에는 순수 로직 단위 테스트가
  필수이고 repo 게이트(check.sh·pre-push 등)의 최상위 단계로 편입되어야 한다. 단위 테스트
  없는 구현은 6-코드리뷰에서 반려 사유가 된다.
- 4단계 설계검토는 기존 approval-board 카드 흐름과 같은 자리다. 봇 지시는 director 사전 승인 후 발송.
- 커스텀 필드 옵션 API가 free plan에서 불가하여 단계 표현은 라벨로 한다 (유료 전환 시 필드 이관 가능).

## 실행 스택 가시성 (LangSmith, 도입 예정)

모든 trace 메타데이터에 `{jira_ticket, relay_stage, bot_id}` 3필드를 강제한다.
계측 지점은 모델 추상화 레이어 1곳 — 각 봇 개별 계측 없이 전체 커버.
