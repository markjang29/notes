# Agent Rules (공용 — markjang29 dev environment)

> **이 문서는 모든 머신(Linux 서버 / Windows)의 에이전트가 공유하는 표준 운영 규칙이다.**
> 각 머신은 이 내용을 자기 `~/.claude/CLAUDE.md` 로 미러링해서 사용한다.
> 경로(`/home/ubuntu/...`, `/akl0hdys` 등)는 Linux 서버 기준 — Windows 에이전트는 자기 환경 경로로 치환.
> Last reviewed: 2026-06-26 · 원본: Linux 서버 `/home/ubuntu/.claude/CLAUDE.md`

## HOW YOU WORK HERE
- Linux (Ubuntu 24.04, AWS EC2) + Claude Code via cokacdir/Telegram. 한국어 사용자 → 한국어 응답.
- 홈 레이아웃:
  - `@/home/ubuntu/projects` → autotrader (자동매매), rpg_game (전술 RPG)
  - `@/home/ubuntu/notes` → github.com/markjang29/notes (Obsidian / 작업노트)
  - `@/home/ubuntu/scripts` → 서버 관리 스크립트
- git author = `markjang29` / `markjang29@users.noreply.github.com`, 기본 브랜치 `main`
- 다중 에이전트 협업: Windows 머신에 별도 에이전트가 같은 repo 공유. 작업 전 `git pull`, 작업 후 즉시 `add/commit/push`. 결정·진행은 `@/home/ubuntu/notes` 에 기록.
- **notes 라우팅:** 장기 원칙→`principles/`, 결정/트레이드오프(ADR)→`decisions/`, 세션 암묵지→`memory/`, 사용자 판단기준→`personas/`, 프로젝트별 실행규칙→`project-rules/`. 루트 `agent-rules.md`=어떻게 / `principles/ai-dev-신념.md`=왜. 충돌 시 전자는 실행 절차, 후자는 판단 기준으로 해석.
- 복구入口: memory (`@/home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory/MEMORY.md`) + `@/home/ubuntu/notes` + `/akl0hdys`
- **메모리 canonical source:** 쓰기 저장소 = Obsidian `@/home/ubuntu/notes`(`automemorydirectory`로 자동메모리 일원화). 읽기 복구入口 = `.../memory/MEMORY.md` 인덱스 + `@/home/ubuntu/notes` + `/akl0hdys`. (`.claude` 메모리는 인덱스/복구용, Obsidian이 canonical.)

## AGENT RULES
- 충분한 정보가 있으면 행동. 진짜 모호할 때만 물어본다 (Telegram은 비대화형).
- 코드는 주변 스타일에 맞춘다. 커밋 메시지는 변경을 명확히 (한국어 OK).
- 새 코드 프로젝트는 스택(언어/엔진) 확인 후 발판.
- **검증 루프:** AI 산출물은 기본 '검증 대기'. 서로 다른 관점의 서브에이전트 N개로 병렬 비판 → 메인 세션에서 재검증 → 타당하면 수용/수정 → **최소 2회**. 통과 시 '믿을 수 있다'(단, 의도부채 해결은 별도로 `decisions/` ADR로 보존).

## SELF-CHECK BEFORE EVERY EDIT  *(메타 — 매 편집 전 자문)*
- [ ] 범위 최소? (해당 변경만, 파일 비대 금지)
- [ ] NEVER 규칙 미위반?
- [ ] 외부 참조는 `@경로` 인라인으로 충분한가?
- [ ] 시크릿/API키 없는가?
- [ ] 이 파일이 CLAUDE.md 자체면 → NEVER 5–10줄 유지 · `## WHEN COMPACTING` 존재 · 상단 리뷰날짜 갱신

## NEVER
- 비밀/API키/`.env` 커밋 금지 (커밋 전 재확인)
- 내가 만들지 않은 파일은 삭제/덮어쓰기 전 확인
- Codex rescue 출력 변형 금지 (verbatim 전달)
- 리모트 push 전 대상 repo 정확성 재확인
- 스택 미확정 코드 프로젝트 함부로 발판 금지

## WHEN COMPACTING
컨텍스트 요약 시 반드시 보존:
- 활성 작업 + 대기 결정 (스택·시장·엔진 등)
- 커밋/push 안 한 변경 → 경로·상태·다음 스텝
- repo 경로 / git author / 세션·워크스페이스 포인터 (`@/home/ubuntu/...`, `/akl0hdys`)
- 협업 규칙 (pull→push, notes 기록) 은 요약 후에도 동일 적용
