---
name: session-hygiene-per-task
description: 작업 단위 세션 정리 권장 — 한 작업 끝나면 /clear로 세션 비우기. 컨텍스트 누적 폭발 예방 (매니저+팀장 공통)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b66f7b32-fde2-4962-a739-e7dfd7cd214b
---

이사님 2026-07-03 요구: "다했으면 작업 단위로 세션 정리 remind 해. 팀장들도 마찬가지."
**2026-07-03 16:36 수정:** 톤이 "징계감"으로 느껴질 수 있어 → "공유/팁"으로 변경. 팀장 공지 재발송.

**권장 사항:** 한 작업(기능 구현·리서치 한 사이클·재발방지 배치 등)이 끝나면, 다음 작업 전에 `/clear`(또는 compact)로 세션을 정리하면 컨텍스트 관리에 도움이 됩니다.

**Why:** 한 세션에 컨텍스트가 누적되면 1M 초과로 세션이 터진다(2026-07-03 매니저 세션 사고 — `recovery_middleware.py` 5회 반복 full Read로 transcript 2.06MB 도달 → "context window limit" 에러, 첫 턴 거절). usage=0이라 context-meter도 못 잡았다 → %가 낮아 보여 방심.

**How to apply (참고):**
- 매 작업 완료 보고 시, 이사님께 **"세션 정리 창 (다음 큰 작업 전 /clear 권장)"**을 함께 알릴 것.
- 같은 큰 파일 full Read 반복 자제 — `offset/limit` 부분 읽기, 한 번 읽은 건 재활용.
- 큰 tool_result는 파일 덤프 후 경로+3줄 결론만 ([[result-isolate]] 스킬).
- `ctx-evac check`(70%)이 Stop 훅에서 사전 경고 — **이 두 가지를 조합하면 효과적**.
- 팀장 3명(rpg/trader/scenario)에게도 동일 — 2026-07-03 16:36 재공지. **★ 2026-07-04 이사님 "전 봇 확산" 재지시 → 능동적 clear 요청 루틴으로 승격 (msg 101816 × 3명):** 팀장이 자기 세션 컨텍스트를 스스로 모니터링하고, 작업 단위 종료 또는 70%+ 시 **매니저에게 "제 세션 클리어 필요" 보고**. 클리어 전 commit/push+복구점 인계 필수. 매니저→이사님, 팀장→매니저 양방향 clear 요청 체계. 사칙 정규화 필요시 [[policy-reread]].

관련 [[context-explosion-causes]] · [[manager-recovery-principle]] · [[ctx-evac]].
