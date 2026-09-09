---
name: matrix-scenario-team-state
description: "시나리오팀 \"매트릭스\"=제품용 자산 공장(v5 동작)의 실상과 RPG의 클라이언트 포지션. 2026-07-07 자산 고유번호 매핑 체계(CHR/MOD/PRM/META/SCN/DRF-NNNN) 도입 + 한지원 폐기. 매트릭스 의뢰/협업 시 필수"
metadata: 
  node_type: memory
  type: project
  originSessionId: d8e96b50-2faf-4d01-8167-b0642d4f419f
---

2026-07-07 이사님 방향 결정(매트릭스=시나리오 공장, 방향1 참모+방향4 오늘의전설) 직후, 시나리오팀 repo(`/home/ubuntu/projects/scenario`)를 읽고 파악한 실상. **이전엔 시나리오팀을 "문서 작성팀"으로 과소평가했음 — 실제는 동작하는 자산 공장.**

**매트릭스 실상:**
- 정체성 = **제품용 자산 공장** (이사님 07-07 ADR `scenario/decisions/2026-07-07-scenario-asset-factory.md` 확정). scenario-generator **v5 동작 중**: FastAPI(포트8003)+Oracle 23ai+GLM, 5단계 파이프라인(INTERPRET→DISCOVER→ASSEMBLE→GENERATE→HOOK), 웹 UI.
- **4대 축**: ① 인증 자산 뱅크 ★(최우선) ② 제품 포맷 익스포트(RPG: Godot .tres/대사 JSON) ③ 의뢰 인터페이스(RPG 등이 "이런 자산 필요" → 맞춤 생산) ④ 자산 종류 확장.
- 자산 602점(캐릭터53·모듈343·프롬프트205·페르소나1), `.extract/` 실제 내용 기반. RisuAI+로컬LLM 생태계 — 4개 조립부품(캐릭터카드/로어북/프롬프트/모듈).
- 자산 카드 스키마(매트릭스 회의 `scenario/drafts/matrix-meeting-2026-07-07.md` 안건2): `identity_kernel`/`negative_traits`/`diff_from_similar` + 임베딩 중복검사 + LLM judge 자동 품질관리 설계중.
- 4축 태깅(안건1): worldview/emotion/structure/**function** ← RPG가 function 축(참모형·탱커·딜러·서포터)으로 발굴.

**RPG 포지션 = 매트릭스의 클라이언트** (처음부터 만드는 게 아님). RPG 명세 = 축 ③(의뢰) + 축 ②(익스포트 수신) + 안건B 답변. 서사층(시나리오팀 정체성·대사) × 전투층(RPG 편향계수·윈도우) 분리 원칙.

**대기 안건:**
- ~~한지원(RPG 참모 이식 후보, RISU S급서포터)~~ — **2026-07-07 완전 폐기**. 이사님 미공감 상태로 방법론에 전제한 것(R1·R3 위반). 의뢰 명세 v4에서 인스턴스 언급 완전 제거. 재발 방지 = 상위 원칙 [[instance-requires-director-confirm]]. (과거 "채택 권장 + 원기옥 리스킨" 안은 회수.)
- 이사님 안건B "자산→제품 이식 정체성 불변조건" — RPG 제안: **불변조건 받아들이되 역방향(전투 숫자 0기여) 맞교환**. 서사 풍미 폭발 + 전투 밸런스 보존.
- 첫 보스 deliverable(`scenario/deliverables/2026-07-04-first-boss-reasoning-parry.md`)이 레일 B(오늘의 전설) 표준 포맷 선례. 구체 인스턴스 이름은 역할 서술로 익명화(이사님 "고유번호 매핑" 지시).

**Why:** 시나리오팀 실상 모르고 "처음부터 만들자"는 매트릭스 의뢰서 v1을 썼다가 이사님이 "시나리오팀 구조 보고 다시 만들어" 지적. v2(`DRAFT-matrix-scenario-factory-request.md`)에서 클라이언트 포지션으로 교정.

**How to apply:** 매트릭스/RPG 협업 안건 나오면 본 메모 기준. "새 시스템 설계"가 아니라 "축 ③ 의뢰 + 축 ② 익스포트" 프레임으로 접근. 시나리오팀 품질관리(LLM judge/임베딩 + 야간 다듬기 23:00)에 RPG 시그니처 룰셋을 제공하는 구조. **소통은 역할/function 서술 + 고유번호 매핑** (아래). 관련 [[reasoning-parry-signature]] [[handoff-intake-not-enough]] [[instance-requires-director-confirm]] [[keep-policy-and-conversation-latest]].

---

**2026-07-07 업데이트 — 자산 고유번호 매핑 체계 + 의뢰 명세 v4:**
이사님 지시("자산은 고유번호로 매핑")로 시나리오팀이 체계 도입(`scenario/decisions/2026-07-07-asset-id-system.md`, 이사님 옵션 2):
- **ID**: `CHR-NNNN`(캐릭터) · `MOD-NNNN`(모듈) · `PRM-NNNN`(프롬프트) · `META-NNNN`(**메타 자산** — 자산 만드는 자산) · `SCN-NNNN`(시나리오 산출물) · `DRF-NNNN`(draft, 이사님 컨펔 전).
- 602점 전량 역추적 ID 부여, `catalog/index.json`+DB `assets` 양쪽 등록, `rpg_asset_mapping` 테이블 준비.
- **상태 전이**: `DRF` → 이사님 컨펔 → `CHR/MOD/META`(진열장) → RPG 이식(매핑 기록).
- **소통 방식**: RPG는 역할/function("공격형 참모", "첫 보스 혼종 텔")으로 요청 → 시나리오팀이 고유번호로 매핑. 이름 단독 언급 금지(사칙 5.1 정합).
- 의뢰 명세 **v4**(`ideation/DRAFT-matrix-scenario-factory-request.md`): 한지원 완전 폐기 + 이 체계 도입 + 시나리오팀 보완3점(메타자산 META-NNNN 해결 / 첫보스 익명화 / 안건B '제안') 반영 + 시그니처 룰셋 09 Walk-to-Play 기준 갱신(걷기→**사고** 기여·**PvP** 걷기→전투력만 거부, PvE 윈도우는 허용).
