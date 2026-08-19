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

## 규칙

- 아티팩트는 전부 이 디렉토리(`relay/tickets/<RELAY-키>/`)에 Git 커밋한다. Jira에는 링크만 건다(2GB 저장 제한).
- Jira 티켓 키(`RELAY-n`)가 모든 아티팩트 파일명과 커밋 메시지에 들어간다.
- 단계 이동은 라벨 갱신 + 해당 단계 산출물 커밋이 둘 다 있어야 성립한다.
- 4단계 설계검토는 기존 approval-board 카드 흐름과 같은 자리다. 봇 지시는 director 사전 승인 후 발송.
- 커스텀 필드 옵션 API가 free plan에서 불가하여 단계 표현은 라벨로 한다 (유료 전환 시 필드 이관 가능).

## 실행 스택 가시성 (LangSmith, 도입 예정)

모든 trace 메타데이터에 `{jira_ticket, relay_stage, bot_id}` 3필드를 강제한다.
계측 지점은 모델 추상화 레이어 1곳 — 각 봇 개별 계측 없이 전체 커버.
