---
name: scenario-renewal-freeze-rpg
description: "이사님 2026-07-11 지시 — 시나리오 git 리뉴얼 완료 전까지 수정금지, 완료 후 리뉴얼 룰 따름. RPG의 시나리오 의존 산출물 잠금"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f7dfab6-fab6-4ae5-8b5c-129799683889
---

이사님 2026-07-11 지시 (RPG 팀장에게 직접): **"시나리오 git 갈아엎는다. 리뉴얼 되기 전까지 수정 금지, 리뉴얼 된 룰 따를 것."**

**Why:** RPG는 시나리오 매트릭스(자산뱅크)의 클라이언트 — 세계관·캐릭터·고유번호 매핑(CHR/MOD/PRM/META/SCN/DRF)·의뢰 체계를 시나리오에서 공급받는다(관련 [[matrix-scenario-team-state]]). 시나리오 repo가 현재 리뉴얼 중(최근 커밋: "이사님 07-10 자산 반려 반영", "새 자산/제품이식 금지 사칙 5.1", d1/d2 draft 수정 미커밋). 기준 체계가 바뀌는 동안 RPG가 구 시나리오 룰 기반으로 산출물을 고치면 리뉴얼 후 재맞춤 비용·충돌이 발생.

**How to apply (RPG 팀장 범위):**
- **시나리오 repo(`/home/ubuntu/projects/scenario`) 직접 수정 금지** — 본래 시나리오 팀장 영역이나 이사님 명시적 금지로 재확인.
- **RPG 내 시나리오 의존/협업 산출물 — 리뉴얼 전 수정 보류:**
  - `ideation/SCENARIO-REQUEST-first-boss-reasoning-parry.md` (시나리오에 보낸 의뢰서)
  - `ideation/DRAFT-first-boss-one-turn-instance.md` (시나리오팀 메모·뼈대 전제 포함)
  - `ideation/WIP-party-boss-godot-impl-design.md`, `ideation/WIP-second-battle-scene-reasoning-parry.md` (to: 시나리오 팀장/매니저)
  - 세계관 관련(`03-themes.md`, `06-concept-convergence.md` 세계관 축) — 백지 상태 유지
  - 한지원(d2-rpg-advisor-han-jiwon) 참모 이식 — [[instance-requires-director-confirm]] 미공감 보류에 더해 리뉴얼까지 확정 잠금
- **예외(계속 진행 OK):** 순수 메커니즘 작업 — `demo/modules/parry`, `duel_advance`, 걷기→윈도우 환산, Reasoning-Parry 삼각 메커니즘, 8004 웹 content. 시나리오 자산과 무관.
- **만료조건:** 시나리오 리뉴얼 완료 + 새 룰 확정 시점. 그때 RPG 시나리오 의존 산출물을 새 룰로 재맞춤한다.

**전파:** 매니저에게도 공유 필요(우선순위/work-queue 반영). RPG 팀장은 매니저에게 보고 의무.
