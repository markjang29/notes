---
title: Relay 역할 배정표 (Jira component ↔ 봇)
status: active
updated: 2026-08-19
---

# 봇별 역할 부여

Jira `RELAY` 프로젝트 component(`bot:*`) 기준. 단계 소유권은 relay/README.md의 게이트 표 참조.

| 봇 (component) | Relay 소유 단계 | 핵심 책임 | 금지 |
|---|---|---|---|
| manager (@heav_lnx_bot) | 1-확보 전관, 전체 조율 | 요구사항 원문 확보, 티켓 발행, 단계 게이트 운영 | 직접 실행 |
| scenario (@heav_lnx_scenario_bot) | 2-정제, 4-설계검토(자기 도메인) | 시나리오 spec·설계 | 미검토 자산 승격 |
| rpg (@heav_lnx_rpg_bot) | 2-정제, 4-설계검토(Godot) | RPG 설계·구현 spec | — |
| trader (@heav_lnx_trader_bot) | (pause) 재개 시 2·4 | 거래 시스템 | 07-16 hold 준수 |
| audit (@heav_lnx_audit_bot) | 3-영향성검토 전관 | 독립 영향성 검토, read-only | 상태 변경·자기승인 |
| asset_agent (@heav_lnx_asset_agent_bot) | 5-구현 | 자산 파싱 파이프라인 | 자동 승격 |
| arcade (@heav_lnx_arcade_bot) | 5-구현 | Arcade(8004) 개발 | — |
| novel_col (@heav_lnx_novel_col_bot) | 5-구현 | 소설 수집 | — |
| codex_dev_1/2 (@heav_lnx_codex_dev_1/2_bot) | 6-코드리뷰 전관 | 리뷰 판정(승인/반려+사유) | 무사유 승인 |
| zcode (aws, 이 세션) | 5-구현(직접 실행) + 계측 | 매니저 금지 작업 실행, LangSmith 계측 | 사전승인 없는 봇 지시 |

## 공통 규칙
- 봇은 Jira API를 서비스 계정 토큰(/home/ubuntu/.jira-token)으로만 접근한다. 봇별 계정 없음.
- 티켓 배정은 component로 표현, 단계는 라벨(`relay:n-단계명`).
- 모든 실행 노드는 LangSmith trace에 `{jira_ticket, relay_stage, bot_id}`를 남긴다(계측 완료 후 적용).
