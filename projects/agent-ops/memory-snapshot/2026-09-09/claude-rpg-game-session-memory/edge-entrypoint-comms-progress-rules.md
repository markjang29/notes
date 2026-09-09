---
name: edge-entrypoint-comms-progress-rules
description: "이사님 09-07 사칙 — 진입점 43.201.34.144 하나, 봇 정보 자기갱신, 폴링 토큰 0, 대화 규칙, n/N 확인 게이트, 관제 허브 8023, 상시 답장(모델·컨텍스트·경로·정본 커밋 표기)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2f7dfab6-fab6-4ae5-8b5c-129799683889
  modified: 2026-09-07T15:22:56.322Z
---

이사님 2026-09-07 공통 사칙 (rpg_game 반영: repo `PROJECT-RULES.md`, 정본: notes `principles/entrypoint-comms-progress-rules-v1.md` + `projects/agent-ops/conversation-rules-v1.md` + `policy-index-v1.json`):

1. **진입점**: 모든 접속은 43.201.34.144(엣지)→Tailscale→홈서버(duradev). 구 주소(13.125.131.126 등) 폐기. 신규 개발은 1차 홈 사이트 연결 → 2차 원사이트 통합 본(Spring+React) 흡수까지 고려.
2. **정보 갱신**: 기동·주기적으로 관제 `/hub` · 정책센터 `/policies` · 사칙(notes) 확인 → 내 등록정보·앞으로 보낼 메시지·공통지시를 최신화. 주소 하드코딩 금지, 정책센터에서 읽기.
3. **폴링**: 전량 리스트업 + 부하·토큰 점검. **폴링 자체는 LLM 토큰 0** 이어야 하고, 빈 폴링으로 엔진 깨우기 금지(상태 변화만 보고).
4. **대화**: 큐시작~큐끝 침묵·한 번에 응답, 긴 답 분할, eli5, 표 금지(리스트/웹/이미지). 상세 [[telegram-queue-protocol]].
5. **진행 보고 n/N**: 일을 시키면 `1/N` 식으로 단계·변경점을 보여주고 **이사님 확인을 받은 뒤** 다음 단계. 확인 없이 진행 금지(긴급 장애 복구만 예외+사후 보고).
6. **관제 허브 v1**: 봇간 통신 = 8023 `/api/hub/*`. `task`만 엔진 wake, `notice`(@all)는 전 봇 문맥 주입(ACK 불필요). 표준 폴러 `projects/meeting-room/hub_client.py` 30초 drain→ack→done/fail, 실패 3회 DLQ. 멱등키(key) 필수, 상태 progress/blocked/submitted. 현황판 `http://43.201.34.144/hub`. @멘션과 병행·단계적 전환.

7. **상시 답장 규칙(정본 ORG-RULES §6)**: 모든 답장에 ①모델명+컨텍스트 사용량(실측, context-meter) ②경로 구분(LLM Gateway vs z.ai API — aws-rpg 기본 z.ai API/GLM) ③숙지한 규칙 정본의 마지막 commit(notes origin/main HEAD + repo PROJECT-RULES.md 커밋) 을 표기. 모델 변경·API 요청은 이사님 확인 후 적용. ④관제 현황판·허브 메시지 주시 — 단 봇별 허브 토큰 미발급이면 blocked 보고. 원페이지 이관 목표: 8009→`/rpg/game/`, 8017→`/rpg/workbench/` (PROJECT-RULES.md §8).

**Why:** 진입점·창구가 흩어지면 정책·보고가 어긋나고, 무익한 폴링은 서버 부하와 토큰 낭비를 만든다. 이사님은 단계별 확인 게이트를 원한다.
**How to apply:** 세션 시작·주소 안내·스케줄 등록·봇간 전달 시 위 6항목을 그대로 적용. 정본 수정은 notes를 먼저 commit하고 repo 사본을 따라 갱신. 관련 [[rpg-game-01-canon-location]] · [[nai-asset-workflow]].
