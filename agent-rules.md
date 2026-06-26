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
- 복구入口: memory (`@/home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory/MEMORY.md`) + `@/home/ubuntu/notes` + `/akl0hdys`

## AGENT RULES
- 충분한 정보가 있으면 행동. 진짜 모호할 때만 물어본다 (Telegram은 비대화형).
- 코드는 주변 스타일에 맞춘다. 커밋 메시지는 변경을 명확히 (한국어 OK).
- 새 코드 프로젝트는 스택(언어/엔진) 확인 후 발판.

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
