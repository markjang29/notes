---
name: context-explosion-causes
description: 1M 컨텍스트 폭발 원인(Codex 서브에이전트 반환 누적)과 예방 — 결과 파일 분리·루프 분산·Read 절제·측정
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4db5139-18ce-4481-b67b-54f5b4d79eed
---

cokacctl/텔레그램 자체는 컨텍스트를 안 먹는다(채널일 뿐). 폭발 원인은 구조적.

**왜 (2026-06-26 세션에서 100만+ 도달):**
1. Codex rescue 서브에이전트가 매번 큰 입력(맥락+요약)을 메인에서 끌어쓰고, 큰 출력(항목별 비판)을 원문 그대로 메인에 재적재. 검증 루프(v1→v2→v3)가 겹쳐 기하급수. ← 압도적 1위.
2. 큰 문서 전문을 매 라운드 Write → 메인에 잔류.
3. 같은/큰 파일을 여러 차례 full Read.
4. 1M 컨텍스트 창(glm-5.2[1m])이라 autoCompact가 늦게 터진다.

**How to apply (예방):**
- 서브에이전트 결과는 메인에 full로 올리지 말고 **파일로 덤프**(예: `~/notes/.reviews/codex-N.md`), 메인엔 결론 요약만. "원문 그대로"는 사용자 표시용.
- Codex 호출 시 맥락/이전 비교를 프롬프트에 넣지 말고 **파일 경로만**(Codex가 직접 읽음) → 메인 재적재 차단.
- 검증 2회 루프는 한 세션에 몰지 말고 산출물 단위로 세션 분리 / compact 사이에 1회씩.
- 같은/큰 파일 full 재독 금지, `offset/limit` 부분 읽기, 한 번 읽은 건 재활용.
- 매 턴 토큰 가시화: `token-report` Stop 훅(`~/.claude/skills/token-report.sh`). 임계 도달 시 조기 compact.
- **전체 예방 원칙(5개 + `.reviews/` 규칙)은 `~/notes/principles/context-budget.md`(v2, 커밋 `d48d7f4`)로 운영규칙화.** Codex 결과 분리는 이 원칙의 첫 실천으로 적용 중.

관련 [[ai-dev-principles-system]], [[memory-tick-impl]].
