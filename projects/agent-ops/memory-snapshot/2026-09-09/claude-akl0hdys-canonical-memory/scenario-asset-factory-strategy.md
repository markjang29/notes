---
name: scenario-asset-factory-strategy
description: scenario-generator 상위 정체성 = 제품용 자산 공장. 이사님 07-07 확정. 4대 축, 자산 뱅크 최우선.
metadata:
  type: project
---

이사님 2026-07-07 확정: scenario-generator는 단순 창작기가 아니라 **"우리가 만드는 제품(RPG·대화서비스 등)이 활용할 수 있는 창작 자산을 쉽게 뽑고 축적"** 하는 **제품용 자산 공장**.

**4대 축:**
1. **인증 자산 뱅크** ★ (최우선) — 실험 결과 중 이사님 피드백 ★4+ 통과 → "인증 자산" 승격 → 제품이 검색·소비. "쌓아간다"의 본체.
2. **제품 포맷 익스포트** — 인증 자산 → RPG(Godot .tres/대사 JSON/퀘스트), 대화서비스(RISU 호환 카드) 변환 (1:N).
3. **의뢰 인터페이스** — 제품팀이 "이런 자산 필요" 의뢰 → 맞춤 생산 (사칙 2번).
4. **자산 종류 확장** — character/story 외 → 세계관 바이블·퀘스트 라인·대화 트리·이벤트.

**첫 사례(draft):** `drafts/d2-rpg-advisor-han-jiwon.md` — RISU 한지원 → RPG 참모 이식 = 자산→제품 이식 패턴 원형.

**Why:** 이사님이 "대화도 좋지만 제품이 쓸 자산이 우선"이라 명시. 한 번 창작한 자산 재사용 → 신제품 창작 비용↓ (자산 자본화).

**How to apply:**
- 시나리오팀 작업은 전부 "제품이 소비할 자산" 관점. 소모성 창작이 아니라 축적.
- ADR: `~/projects/scenario/decisions/2026-07-07-scenario-asset-factory.md`
- DESIGN.md 상단에 상위 정체성 명시됨.
- 관련 [[feedback-risu-asset-real-content]] (실내용 사용 = 근본 정책), [[current-work-state]]
