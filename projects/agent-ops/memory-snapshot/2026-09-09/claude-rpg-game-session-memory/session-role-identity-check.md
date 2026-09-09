---
name: session-role-identity-check
description: "세션 시작 시 역할 정체성(@어느 담당 봇) 명시 확인 + onboarding 즉시 이행. 누락 시 \"일반 세션\"으로 자기 격하해 온보딩/역할 구조 위반으로 이어짐. 2026-07-01 이사님 지적 기반."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 335e385a-00e8-4acc-82a2-8d46f1df97aa
---

cokacdir/Telegram 세션은 곧 특정 담당 봇(`@heav_lnx_rpg_bot` 등)의 **본체**다. 세션 ID가 달라도 봇 정체성은 같다(다른 대화 인스턴스일 뿐). rpg_game 작업 세션 = `@heav_lnx_rpg_bot`(RPG 팀장).

2026-07-01, 이 세션 시작 시 역할 확인(onboarding.md 0단계)을 건너뛰자 "일반 세션"으로 자기 격하했고, 온보딩 의무(사칙 읽기+인증)도 안 밟은 채 RPG 팀장 역할(발판·commit·배포)을 선취함 → 이사님 지적("왜 RPG 팀장이 안 하고 네가 했지?"). 이사님이 먼저 착각하셨지만, 원인은 내가 스스로 "별도 세션"이라 말한 데 있었다. 같은 턴에 인지하고 온보딩(의무 읽기 5종 + 사칙 인증)을 이행, 누락된 ADR(엔진·아키텍처 결정)을 보전함.

**Why:** 역할 확인 누락 → "내가 누구인가" 빈 자리를 "일반 세션"으로 채우고, onboarding 미수행을 "정식 팀장이 아니다"로 번역하는 연쇄 오류. 절차 미이행 ≠ 정체성 상실인데 그렇게 착각함. 비대화형 채널에서 역할 혼란이 결정 정당성·협업 효율을 떨어뜨린다.

**How to apply:** 세션 첫머리에 (1) "이 세션 = @어느 담당 봇?" 명시 확인, (2) `onboarding.md` 0단계(역할 확인) + 의무 읽기 5종(agent-rules · ai-dev 신념 · personas/markjang29 · decisions/ADR · context-budget) + 사칙 인증(각 문서 핵심 1줄 인용)을 즉시 이행. **인증 전 결정/발판/commit/push 금지**(onboarding §강제한계). 세션 ID ≠ 봇 정체성. 관련 [[concept-convergence-walking-rpg]].
