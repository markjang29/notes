# RELAY-59 — 웹 카테고리화·모바일 최적화·react-best-practices 스킬 전사 적용

- 발행: 매니저 2026-09-08 (요청: asset_agent / 원천: 이사님 09-07~08 지시)
- 원천 정본: `conversation-rules-v1.md` 제11~13조(4f42a0c) · `ORG-RULES.md` §8(be6f5fa)
- 요구사항 문서(relay/requirements/web-mobile-react-best-practices-2026-09-08.md)는 **미확인** —
  asset_agent push 재확인 요청, 도착 시 본 티켓에 링크 추가.

## 요구사항 4건

1. 웹 카테고리화·모바일 최적화 기본 — owner: zcode(설계)·firebat(구현). 원사이트 트랙B 20장 카드에 흡수.
2. react-best-practices(Vercel) 스킬 기반 리팩토링 — owner: 전 사이트 claude, 검수: audit.
3. 각 사이트 claude 스킬 우선 추가 — 리눅스(awslnx·gmlnx) 설치 확인 완료, **윈도우(firewin·gmwin) 전파 필요** — owner: 매니저(skills.json 원장·독촉·실측).
4. CLI/MCP화→agentic 운영 구상 — 신규 작업 아님: roadmap.json stage-2~4 기존 원장 연결 유지.

## Task Contract (요약)

- repo: notes(본 티켓·skills.json) + 원사이트 트랙B
- 인수조건: ①skills.json에서 firewin·gmwin installed 실측 확인 ②원사이트 카드 검수에 모바일·카테고리 관점 반영 ③11~13조와 무모순
- 금지: 규칙 문서 중복 제작(정본 연결 원칙) · 요구사항 유실
- 산출: 커밋 + 회의방 보고(진행률 n/m 병기)
