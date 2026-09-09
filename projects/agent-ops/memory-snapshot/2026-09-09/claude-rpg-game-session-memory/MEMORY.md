# MEMORY.md — rpg_game 프로젝트 메모리 인덱스

## 상위 원칙 (최우선)
- [★ 인스턴스 전 이사님 컨펌](instance-requires-director-confirm.md) — 방법론 단계에 이사님이 모르는 구체 인스턴스(캐릭터/설정/자산)를 아는 것처럼 전제하지 말 것. 3조: R1 층위분리·R2 전제금지·R3 공감선행 (2026-07-07 이사님 지적). repo: `ideation/PRINCIPLE-instance-requires-director-confirm.md`
- [★ 정책·대화 최신 위주 유지](keep-policy-and-conversation-latest.md) — 정책 문서와 대화·산출물을 항상 최신 결정 기준으로 다듬기. 구버전(06 초안·폐기 컨셉·manufacturing) 섞이면 최신이 우선. 8004 웹이 한참 전 의사결정처럼 보였던 사례 기반 (2026-07-07 이사님 지시).
- [★ rpg_game 정본은 projects/rpg-game-01/](rpg-game-01-canon-location.md) — 정본이 루트 아닌 projects/에 2026-07-17 이미 구축(a0c9bf4). 세션·논의 전 먼저 확인, 재논의 방지. 07-21~26 이사님+팀장 모르고 재논의→07-26 통합. 루트 ideation/은 legacy 판정.

- [🔒 시나리오 리뉴얼까지 수정금지](scenario-renewal-freeze-rpg.md) — 이사님 2026-07-11 지시. 시나리오 git 리뉴얼 완료 전 수정금지, 완료 후 리뉴얼 룰 따름. RPG 시나리오 의존 산출물(SCENARIO-REQUEST·DRAFT·WIP·세계관·한지원) 잠금. 순수 메커니즘(parry/duel/걷기/8004)은 예외 진행.
- [서브에이전트 커밋 금지 계약](subagent-no-commit-contract.md) — 서브에이전트 프롬프트에 항상 "커밋/push 금지, 파일 출력만" 명시 (2026-06-26 위반 사례 기반)
- [세션 역할 정체성 확인](session-role-identity-check.md) — 세션 시작 시 @어느 담당 봇인지 명시 확인 + onboarding(의무 읽기5종·사칙 인증) 즉시 이행. 누락 시 "일반 세션" 자기 격하 오류(2026-07-01 이사님 지적).
- [걷기×전술 RPG 컨셉 수렴](concept-convergence-walking-rpg.md) — 1안 확정(걷기+전술PvP/PvE+로맨스+진영분기) + 색 염색(마비노기풍) + 엔진 Godot 4.7·모듈식 프로토타입·첫 모듈(패링) 폰 검증. ★ 2026-07-03 핵심 원칙 전복: **Walk-to-Play**(걷기→전투 윈도우+심리전+패링). "걷기→전투력 0기여"는 폐기. 스토리(길 잇는/끊는 자)·스태미나 직결·색사진·CIPHER/LUMEN/RUMOR 후보 폐기.
- [전투 시그니처 Reasoning-Parry](reasoning-parry-signature.md) — 2026-07-02 확정. 참모(캐릭터 추론)×지휘관(플레이어 결정)×손(패막) 삼각 구도. "생각 천재·패션 잼병 AI". 오토배틀러화를 패막이 차단. ⚠ "걷기→전투력 0기여"는 09 Walk-to-Play로 전복 — 단 삼각 구도·걷기→사고 분리는 유효.
- [핸드오프는 인수 문서가 아니라 본 산출물 반영](handoff-intake-not-enough.md) — 시나리오 팀장이 RPG 핸드오프 '인수 문서'로만 격리, 본 산출물(manufacturing)엔 시그니처 0% 반영 (2026-07-04 이사님 지적→manufacturing 폐기 결정). 매니저는 본 산출물 반영까지 검증, 구 배정은 신규 핸드오프에 자동 철회.
- [시나리오팀 매트릭스 실상 + RPG 클라이언트 포지션](matrix-scenario-team-state.md) — 매트릭스=제품용 자산공장(v5 동작, FastAPI+Oracle+GLM). 4대 축(①자산뱅크★②익스포트③의뢰④확장). RPG는 클라이언트. ★ 2026-07-07 자산 고유번호 매핑 체계(CHR/MOD/PRM/META/SCN/DRF-NNNN) 도입 + 한지원 완전 폐기. 소통=역할 서술+고유번호 매핑.
- [참모 두뇌=악보 시스템](advisor-score-system.md) — 2026-07-09 GO. 참모 두뇌를 '악보'(텍스트 DSL)로, 유저가 자기 GPT/Gemini로 작곡·적용. 걷기 2축(윈도우+수련시간), 레이어 분리로 서버 LLM 비용0, AI는 초안만 짜줌. 코딩교육은 심화. repo `ideation/11-advisor-score-system.md`.
- [NAI 게임자산 워크플로우](nai-asset-workflow.md) — NAI Opus API 실측(v4.5-full v4_prompt 필수·무료조건) + RPG저장고 + RELAY-36 워크벤치 도구화 착수 (2026-08-22)
- [대전=서사 조정 토큰 대립](narrative-control-token.md) — 이사님 08-31 아이디어. 전투의 이유=이야기 조정권. RPG-1·RPG-8·패링 3각 연결. Jira 404 중 notes 보존
- [텔레그램 큐 규칙](telegram-queue-protocol.md) — "큐시작"~"큐끝" 침묵 후 한 번에 응답. 긴 답은 파일/분할+eli5 덧붙임, 표는 대체 표현 (2026-09-06)
- [★ 진입점·관제·진행보고 사칙](edge-entrypoint-comms-progress-rules.md) — 이사님 09-07: 진입점 43.201.34.144 단일(Tailscale→홈서버), 봇 정보 자기갱신, 폴링 토큰 0·빈폴링 금지, 관제 허브 8023 `/api/hub/*`, **n/N 단계별 이사님 확인 게이트**, **상시 답장(모델·컨텍스트·경로·정본커밋 표기)**. repo `PROJECT-RULES.md` + notes 정본 (2026-09-07)
- [개발 표준·요구사항 파이프라인](dev-standard-and-requirement-pipeline.md) — 이사님 09-08: UI 카테고리화·모바일 최적화 기본, Vercel react-best-practices 스킬 기반 리팩토링(사이트별 설치, awslnx 완료), 이사님 발언=JIRA 요구→검증→구현(Jira 장애 중 notes interim), 조직 방향 CLI/MCP화→agentic. repo `PROJECT-RULES.md` §9~§11
