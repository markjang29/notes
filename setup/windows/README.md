# Windows 동기화 셋업

Linux 서버(Ubuntu 24.04, cokacdir/Telegram)의 Claude Code 설정을
Windows 머신에 그대로 옮기는 스크립트 모음. **Codex 1회 검증 수용본.**

## 한 줄 요약
`git clone notes` → 환경에 맞는 스크립트 1회 실행 → Claude 안에서 plugin 재설치 →
첫 세션에 온보딩 프롬프트로 사칙 상속. 끝.

## 사칙 동기화 원리 (이게 핵심)
사칙(원칙 체계)은 **이미 이 notes repo에 체계화**되어 있다.
`agent-rules.md` 헤더가 "모든 머신(Linux/Windows) 공유, 각 머신이
`~/.claude/CLAUDE.md`로 미러링, 경로는 자기 환경으로 치환"이라고 명시.
그래서 Windows Claude도 notes clone → CLAUDE.md 미러 → 경로 치환만 하면
Linux Claude와 **동일한 사칙** 을 갖는다. 이후 사칙 변경은 pull/push로 양쪽 자동 동기화.

## 사전 준비 (양쪽 공통)
1. **GitHub 인증** — private repo clone 위해 `gh auth login` (권장) 또는 SSH key.
2. **ANTHROPIC_AUTH_TOKEN** — 별도 안전한 수단으로 전달받을 것. ⚠ 절대 git/스크립트/settings 템플릿에 기록 금지.
3. Claude Code 본체 설치.

## WSL 안에서 Claude Code를 쓸 때
```bash
git clone https://github.com/markjang29/notes.git ~/notes
bash ~/notes/setup/windows/setup-wsl.sh
# → 토큰 입력 후: source ~/.config/claude-code/env && claude
```
의존: `jq` (스크립트가 `apt-get install` 시도). bash/jq 그대로라 가장 안정적.

## Native Windows(PowerShell)에서 쓸 때
```powershell
git clone https://github.com/markjang29/notes.git "$env:USERPROFILE\notes"
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\notes\setup\windows\setup-windows.ps1"
# → 토큰 주입 후 claude 실행
```
의존: **Git for Windows**(`bash.exe` 동봉, 훅 실행용), **Node.js 18.18+**, **jq**(`winget install jqlang.jq`).

## Claude 안에서 plugin 재설치 (수동 복사보다 안전 — 경로 깨짐 방지)
스크립트 실행 후 Claude Code 첫 세션에서:
```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
/config theme dark
```

## 사칙 상속 (첫 세션)
[`ONBOARDING-PROMPT.md`](ONBOARDING-PROMPT.md) 를 첫 세션에 그대로 복붙.
핵심 문서를 1줄씩 인용해 읽었음을 인증 → 그래야 결정/발판/commit 권한 획득.

## 복제하는 것 / 하지 않는 것

**복제:** `CLAUDE.md`(agent-rules 미러), `settings.json`(토큰 제외 구조), skills 3종,
git author, notes·projects repos, plugin(명령 재설치).

**복제 금지 (서버 전용/로컬 상태 — 의도적):**
- `~/.claude.json` (startup count·플래그·로컬 상태만)
- `plugins/installed_plugins.json`, `plugins/cache`, `plugins/data` (절대경로 묻음 → 재설치)
- `daemon/*`, `daemon/control.key`, `sessions/`, `session-env/`, `shell-snapshots/`
- `projects/`(transcript), `history.jsonl`, `file-history`, `jobs`, `tasks`, `backups`, `.last-*`, `.memory-tick-last`
- cokacdir, cron 스케줄, Telegram 그룹 매니저/팀장 협업 (Windows Claude는 터미널 직접 입력)

## 검증이 밝힌 함정 (Codex 리뷰)
1. **Native 훅**: `bash /home/...` 안 됨 → Git Bash 절대경로로. `token-report.sh` 폴백(`${HOME}/.claude/projects`)은 Git Bash 홈과 Native transcript 위치가 달라 깨질 수 있으니 stdin의 `transcript_path`에 의존.
2. **`/akl0hdys`**: 서버 cokacdir workspace 포인터 → 복제 말고 "서버 전용" 마커로 치환.
3. **`autoMemoryDirectory`**: agent-rules.md엔 Obsidian 일원화로 적혀있으나 실제 설정엔 없고 memory-tick/SKILL.md도 "보류/미검증". → 동기화 안 함(의도적).
4. **세 번째 환경**: Native Claude가 hook에서 WSL/Git Bash 부르는 혼합 — transcript path·HOME·jq 위치가 꼬여 가장 취약. WSL 또는 Native 중 하나로 통일 권장.
5. **토큰**: settings.json 평문 금지. WSL=`~/.config/claude-code/env`(600)에서 source, Native=Credential Manager/SecretStorage → 실행 직전 process env 주입.

## 파일 구성
- `setup-wsl.sh` — WSL(Ubuntu)용 bash
- `setup-windows.ps1` — Native Windows용 PowerShell
- `ONBOARDING-PROMPT.md` — Windows Claude 첫 세션 프롬프트
- `skills/` — memory-tick(SKILL.md + stop-hook-throttle.sh), token-report.sh (번들)
- `README.md` — 이 파일
