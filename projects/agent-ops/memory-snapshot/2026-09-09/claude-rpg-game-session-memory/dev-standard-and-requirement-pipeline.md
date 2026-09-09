---
name: dev-standard-and-requirement-pipeline
description: "이사님 09-08 지시 — UI 카테고리화·모바일 최적화 기본, Vercel react-best-practices 스킬 기반 리팩토링(사이트별 Claude 설치), 이사님 발언=JIRA 요구사항→검증→구현, 조직 방향 CLI/MCP화→agentic"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2f7dfab6-fab6-4ae5-8b5c-129799683889
  modified: 2026-09-07T15:29:56.247Z
---

이사님 2026-09-08 지시 (repo `PROJECT-RULES.md` §9~§11 반영):

1. **개발 표준**: 페이지·메뉴·선택 항목은 최대한 **카테고리화**, **모바일 최적화가 기본**(폰 확인 전제, 데스크톱 전용 금지).
2. **웹 스킬**: 추후 Vercel 계열 **react-best-practices** 스킬 기반으로 모바일 최적화·리팩토링 검토. 스킬은 사이트(윈도우/리눅스 PC)별 Claude에 먼저 설치 — 리눅스(awslnx)는 `~/.claude/skills/react-best-practices` 설치 완료(Vercel Engineering v1.0.0), 설치 원장 notes `projects/agent-ops/skills.json`(매니저), firewin·gmwin 보고 대기.
3. **요구사항 파이프라인**: 이사님 발언 = 요구사항 원천 → 티켓화(JIRA) → 검증(수용기준) → 구현 → 보고. Jira 장애 중 interim = notes `relay/tickets/`, 티켓 없는 착수 무효, 복구 시 소급 등록.
4. **조직 방향**: 각자 사이트 정합성 구축 → 반복 업무 CLI/MCP화 → agentic 운용(허브 큐·이벤트형). rpg는 워크벤치 배치·게임 배포·갤러리 검수부터 서브커맨드·MCP 후보화.

**Why:** 화면이 분류 체계 없이 늘어나면 모바일에서 무너지고, 말로만 끝난 요구는 검증·구현 없이 유실된다. 조직 확장은 도구화(agentic)가 전제.
**How to apply:** UI 작업 전 카테고리·모바일 기준 점검, 리팩토링 시 react-best-practices 스킬 호출, 이사님 새 지시는 티켓화 여부를 스스로 판단해 놓치지 않기. 관련 [[edge-entrypoint-comms-progress-rules]] · [[nai-asset-workflow]].
