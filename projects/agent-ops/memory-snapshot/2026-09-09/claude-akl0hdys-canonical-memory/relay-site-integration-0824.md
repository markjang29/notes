---
name: relay-site-integration-0824
description: "사이트 통합 7단계 파이프라인 확립(이사님 08-24) — 매트릭스 정의 방향 결정, zcode SE, 매니저 조직화 담당"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0728c879-f832-4afc-a181-fe5f4a03f347
  modified: 2026-08-24T10:21:07.934Z
---

2026-08-24 이사님 지시로 사이트 통합 확립. **핵심 결정사항:**

- **7단계 파이프라인**: 1 리수세팅(8013 pocketrisu) → 2 검증 → 3 승인(8005 승인보드) → 4 매트릭스화 → 5 재테스트(8004 아케이드) → 6 이미지(8016) → 7 코어 디벨롭(CLI·AGENT·하네스) → 수익화(RPG 8009·신규소설 novel_col)
- **역할 분담**: SE 설계 정본 = zcode(RELAY-49), 매니저 = 조직화·게이트 운영·보고. 통합 홈 허브 = 8018(RELAY-50, zcode)
- **매트릭스 정의 방향(이사님 승인)**: 4단계 "매트릭스화"=자산 캡슐화 / 7단계 "매트릭스 코어"=CLI 클로드코드류 하네스. 노드 9종(Triage·HierarchicalPlanner·Verifier·Reflection·Debate·MemoryBank·ToolLearningSystem·ContextManager·IterationGuard)은 **스위치형**(direct/simple=단일경로, complex만 전체 가동). 뼈대=matrix_codex(CLI 본체·command bus) 재사용
- **공통 가이드 정본**: notes-registry `relay/site-integration-guide-2026-08-24.md` (a386af2). 결정 원문: `relay/tickets/RELAY-49/req.md` (a294bc0)
- **매니저→zcode 직통 없음**: zcode는 별도 하네스(telegram_zcode_bridge, getUpdates 폴링)라 외부 주입 불가 — 이사님 채팅 붙여넣기로만 전달
- **15개 사이트 전부 relay 등록 상태**, 신규 기동 시 RELAY_TICKET 필수(RELAY-15, 무단운행→승인보드 카드)
- RELAY-42(music_video 일상): 6-코드리뷰 중, 이사님 실사용 피드백→99c8796 보완 반영 완료

관련 [[current-work-state]]
