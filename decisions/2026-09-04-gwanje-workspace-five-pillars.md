# ADR — 관제 디벨롭 A안 채택, 범위는 관리 5축으로 한정

- 날짜: 2026-09-04
- 상태: **accepted** (이사님 09-04 승인: "A 안 승인인데… 주요의사결정, 로드맵, 담당업무, 개발시 참고 스킬, 사용 lmm 모델설정 관리 위주로 가자")
- 근거 조사: `projects/agent-ops/gwanje-slacklike-upgrade-research.md` (9ca4d02)

## 맥락

Slack류 디벨롭 조사 결과 A안(자체 발전)이 추천됐고 이사님이 승인. 단, 소통은 이미 텔레그램+현 회의방(8023)으로
충분하므로, 채팅 UX 개편(채널·스레드·리액션 등)은 보류하고 **관제 = 조직 관리 표면**에 집중하기로 범위를
한정했다.

## 결정

- **A안 채택** — 관제(대시보드 8025 중심)를 다음 5축으로 디벨롭한다:
  1. **주요의사결정** — ~/notes/decisions/ ADR + work-queue 대기결정 + requirements-log.jsonl(이사님 발언 원문)
  2. **로드맵** — notes projects/agent-ops/roadmap.json (신설, 단일 원장)
  3. **담당업무** — 기존 지라칸반에 담당자별 뷰 추가
  4. **개발 참고 스킬** — notes projects/agent-ops/skills.json (신설, 스킬×사이트 설치 실측 원장)
  5. **LLM 모델설정 관리** — 기존 모델표/변경 API 강화 + 변경 이력(model-change-log.jsonl)
- **보류**: 채널·스레드 등 회의방(8023) 채팅 UX 개편(조사 문서 Phase 1~3). 필요 시 별도 결정으로 재개.
- 불변 원칙: 토큰 0(파일 직독)·CDN 0·변경 API는 이사님 ACCESS_TOKEN 전용·모바일 최적화.

## 결과

- 구현은 zcode 배정, 데이터 원장 초안(roadmap.json·skills.json)은 매니저가 작성·유지보수.
- 로드맵 1단계(사이트 정합성)의 관제 워크스트림으로 편입 — 2~4단계(CLI·MCP·agentic) 경로는 유지.
