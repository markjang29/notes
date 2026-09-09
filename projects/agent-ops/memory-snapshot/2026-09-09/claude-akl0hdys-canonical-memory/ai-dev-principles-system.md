---
name: ai-dev-principles-system
description: notes에 구축한 AI Native 개발 신념 원칙 체계 (디렉토리 구조·핵심 파일·남은 작업)
metadata: 
  node_type: memory
  type: project
  originSessionId: a4db5139-18ce-4481-b67b-54f5b4d79eed
---

2026-06-26 `~/notes`에 **AI Native 개발 신념 원칙 체계**를 구축했다 (commit `0d909fa`, push 완료).

- 디렉토리: `principles/ decisions/ memory/ personas/ project-rules/` (+ 루트 `agent-rules.md`).
- 핵심 `principles/ai-dev-신념.md` 7장 — 부채3종(기술/인지/의도) · 검증루프(인간 기준/AI 루프/시스템, 병렬 비판 2회) · 의도보존(ADR) · AI Native(Queryable/closed loop/self improving) · 암묵지캡처(memory-tick 강제) · 판단모델(페르소나=판단기준) · 문서관(문서=기저데이터 렌더링).
- 분업: `agent-rules.md`="어떻게", `principles/`="왜". 충돌 시 전자는 실행절차·후자는 판단기준.
- memory 상태모델: 자동저장=후보(candidate) → 사용자 승인/승격기준 → 지식(knowledge).
- 메모리 canonical: 쓰기=Obsidian `notes/`, 읽기 복구=`.../MEMORY.md` 인덱스.
- **제작 방식 자체가 신념의 실천**: Codex 비판 루프 2회 자동 수용 → 최종 GO.

**personas/markjang29.md v3 완료** (2026-06-26): 인터뷰 라운드1-2 + Codex 비판 2회 자동 수용 → "취향 나열"을 판정 기반(체크리스트·프로토콜·기본값)으로 전환. commit `1ec86e8` push. **남은 것(후속 인터뷰):** 기술/언어/엔진 선택 구체 기준(§8 임시값 다듬기) · 도구화 경계 심화(후회 사례) · 이어받기 완료 기준 심화 · 복구 vs 기록 보존. 관련 [[projects-and-collaboration]], [[context-explosion-causes]].
