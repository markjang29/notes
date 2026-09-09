---
name: handoff-intake-not-enough
description: "핸드오프를 '인수 문서'로만 격리하고 본 산출물에 안 녹이면 컨셉 정합성 붕괴. 매니저가 본 산출물 반영까지 검증해야."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2d60fee3-a246-447a-86a2-4f09c441171e
---

2026-07-04 이사님 지적으로 발견된 협업 패턴 위반. RPG 팀장이 07-03에 시나리오 팀장에 RPG 시그니처(Reasoning-Parry·Walk-to-Play·4인 파티 보스전·원기옥 정당성) 핸드오프 2종을 전달했으나, 시나리오 팀장은 `rpg-signature-connection.md`(277줄)에 **"인수 문서"로만 복사 보관**하고 본 산출물(`manufacturing-coverup-B01/scene-01,02`)에는 **RPG 시그니처 키워드 0건** — 커밋 메시지는 "RPG 시그니처 인수"라 했지만 실제론 구 배정(manufacturing-coverup, 매니저 07-02 배정)을 디벨롭. 이사님이 **manufacturing-coverup-B01 폐기 + RPG 시그니처 기반 전환(A안)** 확정 (`rpg_game/ideation/DECISION-2026-07-04-manufacturing-deprecate.md`).

**Why:** 핸드오프를 "받았다"고 문서화만 하고 본 작업에 반영 안 하면, 새 시그니처가 무시되고 구 배정이 잔존해 컨셉 정합성이 무너진다. 이사님 눈에는 "자기 마음대로 다른 시나리오 디벨롭"으로 보임 — 협업 신뢰 붕괴.

**How to apply:** 팀장에 핸드오프 전달 시, (1) "인수 문서" 작성만으로 끝내지 말고 본 산출물(scene·코드 등)에 시그니처가 실제로 녹았는지 매니저가 검증. (2) 구 배정이 시그니처 확정 이전 기준이면 신규 핸드오프가 우선, 구 배정은 자동 철회 — 팀장이 임의로 구 배정을 고수하지 못하게. (3) 커밋 메시지("인수")와 실제 산출물 불일치를 grep/검증으로 잡을 것. 관련 [[subagent-no-commit-contract]].
