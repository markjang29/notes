# RELAY-65 — AI 개발 개선사항 전사 적용 (이사님 09-16)

- 발행: 매니저(aws-manager) 2026-09-16 (원천: 이사님 텔레그램 지시 09-16)
- 요구사항 정본: `relay/requirements/ai-dev-improvements-2026-09-16.md` @ 4dce19e+
- 기존 규칙과 관계: ORG-RULES §10~13 / conversation-rules-v1 11~13조와 **무모순·보완**. 중복 정의 없음 — 본 티켓은 실행 절차(Swagger-first·E2E·CI/CD 게이트)만 추가.

## 요구사항 6건 (요약 — 상세는 정본)

1. **기획·문서**: PRD·사용자 시나리오·와이어프레임·ERD/데이터모델 — MVP 과제 시작 전 필수 산출.
2. **Swagger-first**: 데이터모델→OpenAPI 스펙→백엔드 목업. 프론트·백엔드 병렬 개발 기반.
3. **백엔드**: MCP 연동 DB 생성, skill/슬래시 자동화, 단위테스트·보안점검·문서화.
4. **프론트엔드**: React+Vite, 컴포넌트 명세서, SOLID+Clean Architecture, 단위테스트·보안·E2E.
5. **배포**: Supabase↔Vercel 연동, Vercel for GitHub + GitHub Actions CI/CD. **CI 게이트 통과 없이 병합·배포 금지.**
6. **안티패턴 5항목** — 정본 §6. 각 단계 게이트에서 차단.

## 소관 분배

- **매니저(자신)**: 티켓·공지·숙지확인 운영, roadmap.json 반영 검토, 백엔드 스택(Supabase) 결정 안건 상신.
- **전 팀장**(scenario·rpg·관제): 소관 신규 과제에 §1~5 절차 적용, 단위·E2E 테스트 산출.
- **audit**: 안티패턴·게이트 준수 감사 관점 추가.
- **windows-codex**: 윈도 사이트 전파·작업 배정 시 본 절차 참조.

## Task Contract (요약)

- repo: notes (본 티켓 + requirements 정본) — 코드 변경 없음(정책 티켓).
- 인수조건: ①정본 문서 커밋·push ②허브 @all 공지 도달 ③read-registry에 전 봇 confirmation 등록(또는 등록 독촉 후 미등록 봇 리스트 보고) ④roadmap.json/ORG-RULES와 무모순.
- 금지: 규칙 문서 중복 제작 · 증발하는 silent 구현 · 스코프 외 코드 변경.
- 산출: 커밋+회의방 보고(진행률 n/m 병기). eli5 첨부.
