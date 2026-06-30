# =============================================================================
# setup-windows.ps1 — Native Windows의 Claude Code를 Linux 서버 설정과 동기화.
# 사전 조건:
#   1) Git for Windows (bash.exe 동봉), Node.js 18.18+
#   2) GitHub 인증 — `gh auth login` 권장 (private repo clone용).
#   3) ANTHROPIC_AUTH_TOKEN 값 준비 (별도 안전한 수단으로 전달).
#   4) jq — `winget install jqlang.jq` 또는 `scoop install jq` (token-report 훅용).
# 실행(관리자 아님 권장):  powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1
# 재실행 안전.
# =============================================================================
$ErrorActionPreference = "Stop"

$HomeDir       = $env:USERPROFILE
$ClaudeDir     = Join-Path $HomeDir ".claude"
$NotesDir      = Join-Path $HomeDir "notes"
$ProjectsDir   = Join-Path $HomeDir "projects"
$SkillsSrcDir  = Join-Path $NotesDir "setup\windows\skills"
$HomeFwd       = $HomeDir.Replace("\", "/")   # hooks 경로는 슬래시 표기(Git Bash 호환)

function Clone-Or-Pull($Url, $Dir, $Name) {
  if (Test-Path (Join-Path $Dir ".git")) {
    Write-Host ">>  pull  $Name"
    git -C $Dir pull --ff-only
  } else {
    Write-Host ">>  clone $Name"
    git clone $Url $Dir
  }
}

Write-Host ">> [0/9] 디렉토리 준비"
New-Item -ItemType Directory -Force -Path $ClaudeDir, $ProjectsDir, (Join-Path $ClaudeDir "skills\memory-tick") | Out-Null

Write-Host ">> [1/9] git author"
git config --global user.name "markjang29"
git config --global user.email "markjang29@users.noreply.github.com"
git config --global init.defaultBranch main

Write-Host ">> [2/9] notes repo (스크립트·skills 번들의 원본)"
Clone-Or-Pull "https://github.com/markjang29/notes.git" $NotesDir "notes"
# clone 직후 경로 갱신
$SkillsSrcDir = Join-Path $NotesDir "setup\windows\skills"

Write-Host ">> [3/9] project repos"
Clone-Or-Pull "https://github.com/markjang29/autotrader.git" (Join-Path $ProjectsDir "autotrader") "autotrader"
Clone-Or-Pull "https://github.com/markjang29/rpg_game.git"   (Join-Path $ProjectsDir "rpg_game")   "rpg_game"

Write-Host ">> [4/9] .claude\CLAUDE.md <- agent-rules.md 미러 (경로 치환)"
$rules = Get-Content (Join-Path $NotesDir "agent-rules.md") -Raw
$rules = $rules.Replace("/home/ubuntu", $HomeFwd)
$rules = $rules.Replace("/akl0hdys", "<linux-서버전용:/akl0hdys>")
Set-Content -Path (Join-Path $ClaudeDir "CLAUDE.md") -Value $rules -Encoding UTF8

Write-Host ">> [5/9] skills 3종 복제"
Copy-Item (Join-Path $SkillsSrcDir "memory-tick\SKILL.md")              (Join-Path $ClaudeDir "skills\memory-tick\SKILL.md") -Force
Copy-Item (Join-Path $SkillsSrcDir "memory-tick\stop-hook-throttle.sh") (Join-Path $ClaudeDir "skills\memory-tick\stop-hook-throttle.sh") -Force
Copy-Item (Join-Path $SkillsSrcDir "token-report.sh")                  (Join-Path $ClaudeDir "skills\token-report.sh") -Force

Write-Host ">> [6/9] bash.exe / jq 확인"
$candidates = @(
  "C:\Program Files\Git\bin\bash.exe",
  "C:\Program Files\Git\usr\bin\bash.exe",
  "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
)
$bash = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $bash) { Write-Warning "bash.exe 못 찾음 — Git for Windows 설치 필요. 훅이 작동 안 함." }
else { Write-Host "   bash: $bash" }
if (-not (Get-Command jq -ErrorAction SilentlyContinue)) {
  Write-Warning "jq 없음 — 'winget install jqlang.jq' 권장. token-report 훅은 jq 있어야 동작."
}

Write-Host ">> [7/9] .claude\settings.json (토큰 제외 — 토큰은 process env로 주입)"
$bashFwd = $bash.Replace("\", "/")
$hook1 = "`"$bashFwd`" `"$HomeFwd/.claude/skills/memory-tick/stop-hook-throttle.sh`""
$hook2 = "`"$bashFwd`" `"$HomeFwd/.claude/skills/token-report.sh`""
$settings = [ordered]@{
  env = [ordered]@{
    ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic"
    API_TIMEOUT_MS = "3000000"
    ANTHROPIC_DEFAULT_HAIKU_MODEL = "glm-4.7"
    ANTHROPIC_DEFAULT_SONNET_MODEL = "glm-5.1"
    ANTHROPIC_DEFAULT_OPUS_MODEL = "glm-5.2"
  }
  enabledPlugins = [ordered]@{ "codex@openai-codex" = $true }
  extraKnownMarketplaces = [ordered]@{
    "openai-codex" = [ordered]@{ source = [ordered]@{ source = "github"; repo = "openai/codex-plugin-cc" } }
  }
  theme = "dark"
  hooks = [ordered]@{
    Stop = @(@{ hooks = @(
      @{ type = "command"; command = $hook1 },
      @{ type = "command"; command = $hook2 }
    ) })
  }
}
$settings | ConvertTo-Json -Depth 20 | Set-Content -Path (Join-Path $ClaudeDir "settings.json") -Encoding UTF8

Write-Host ">> [8/9] 토큰 — Windows 사용자 환경변수(차선)로 세팅 안함. 수동 입력 안내만."
Write-Host "   권장: Windows Credential Manager / SecretStorage 보관 → 실행 직전 process env 주입."
Write-Host "   차선(편의):  setx ANTHROPIC_AUTH_TOKEN \"<토큰>\"  (레지스트리 평문 주의)"
Write-Host "   최선: 터미널에서 매번  `$env:ANTHROPIC_AUTH_TOKEN=\"<토큰>\"; claude"

Write-Host ">> [9/9] 완료 — 남은 수동 단계는 아래 출력 참고"
Write-Host ""
Write-Host "============ Native Windows 동기화 완료 ============"
Write-Host "남은 수동 단계:"
Write-Host "  1) jq 설치:  winget install jqlang.jq   (안 했으면)"
Write-Host "  2) 토큰 주입 후 claude 실행 (위 [8/9] 안내)"
Write-Host "  3) Claude 안에서 plugin 재설치:"
Write-Host "       /plugin marketplace add openai/codex-plugin-cc"
Write-Host "       /plugin install codex@openai-codex"
Write-Host "       /reload-plugins"
Write-Host "       /codex:setup"
Write-Host "       /config theme dark"
Write-Host "  4) 첫 세션에 온보딩 프롬프트(ONBOARDING-PROMPT.md)로 사칙 상속·인증."
Write-Host ""
Write-Host "복제하지 않은 것(서버 전용/로컬 상태 — 의도적):"
Write-Host "  ~/.claude.json, plugins/installed_plugins.json, plugins/cache,"
Write-Host "  daemon/*, sessions/, shell-snapshots/, cokacdir, cron, Telegram 그룹 협업."
Write-Host ""
Write-Host "⚠ 함정: token-report.sh 폴백 경로(`$HOME/.claude/projects)는"
Write-Host "   Git Bash 홈과 Native Claude transcript 위치가 달라 깨질 수 있음."
Write-Host "   Stop 훅이 stdin으로 transcript_path를 주면 정상 동작하니, 폴백 의존 금지."
