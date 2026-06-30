#!/usr/bin/env bash
# =============================================================================
# setup-wsl.sh — WSL(Ubuntu) 안의 Claude Code를 Linux 서버 설정과 동기화.
# 사전 조건:
#   1) GitHub 인증 — `gh auth login` 권장 (private repo clone용). 또는 SSH key.
#   2) ANTHROPIC_AUTH_TOKEN 값을 준비 (별도 안전한 수단으로 전달받을 것).
# 실행:  bash setup-wsl.sh
# 재실행 안전 (clone ↔ pull 자동 분기). 기존 파일은 덮어쓰지 않는 항목은 보존.
# =============================================================================
set -euo pipefail

NOTES_URL="https://github.com/markjang29/notes.git"
AUTOTRADER_URL="https://github.com/markjang29/autotrader.git"
RPG_URL="https://github.com/markjang29/rpg_game.git"

NOTES_DIR="${NOTES_DIR:-$HOME/notes}"
PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"
CLAUDE_DIR="$HOME/.claude"
SKILLS_SRC="$NOTES_DIR/setup/windows/skills"

echo ">> [0/8] 디렉토리 준비"
mkdir -p "$PROJECTS_DIR" "$CLAUDE_DIR/skills/memory-tick" "$(dirname "$NOTES_DIR")"

clone_or_pull () {
  local url="$1" dir="$2" name="$3"
  if [ -d "$dir/.git" ]; then
    echo ">>  pull  $name"
    git -C "$dir" pull --ff-only
  else
    echo ">>  clone $name"
    git clone "$url" "$dir"
  fi
}

echo ">> [1/8] git author"
git config --global user.name "markjang29"
git config --global user.email "markjang29@users.noreply.github.com"
git config --global init.defaultBranch main

echo ">> [2/8] notes repo (이 스크립트·skills 번들의 원본)"
clone_or_pull "$NOTES_URL" "$NOTES_DIR" "notes"

echo ">> [3/8] project repos"
clone_or_pull "$AUTOTRADER_URL" "$PROJECTS_DIR/autotrader" "autotrader"
clone_or_pull "$RPG_URL"        "$PROJECTS_DIR/rpg_game"   "rpg_game"

echo ">> [4/8] ~/.claude/CLAUDE.md ← agent-rules.md 미러 (경로 치환)"
# /home/ubuntu → WSL $HOME,  /akl0hdys → 서버 전용 마커 (Windows엔 대응 경로 없음)
sed -e "s#/home/ubuntu#$HOME#g" \
    -e "s#/akl0hdys#<linux-서버전용:/akl0hdys>#g" \
    "$NOTES_DIR/agent-rules.md" > "$CLAUDE_DIR/CLAUDE.md"

echo ">> [5/8] skills 3종 복제"
cp "$SKILLS_SRC/memory-tick/SKILL.md"             "$CLAUDE_DIR/skills/memory-tick/"
cp "$SKILLS_SRC/memory-tick/stop-hook-throttle.sh" "$CLAUDE_DIR/skills/memory-tick/"
cp "$SKILLS_SRC/token-report.sh"                   "$CLAUDE_DIR/skills/"
chmod +x "$CLAUDE_DIR/skills/memory-tick/stop-hook-throttle.sh" "$CLAUDE_DIR/skills/token-report.sh"

echo ">> [6/8] jq (token-report 훅 의존)"
if ! command -v jq >/dev/null 2>&1; then
  echo "   jq 없음 → sudo apt-get install -y jq 시도"
  sudo apt-get install -y jq || echo "   WARN: jq 설치 실패. token-report 훅은 jq 있을 때까지 스킵됨."
fi

echo ">> [7/8] ~/.claude/settings.json (토큰 제외 — 토큰은 별도 env 파일에서 주입)"
# hooks 경로는 절대경로로 박음(원본 서버 설정과 동일 패턴). heredoc 비인용 → $HOME 확장.
cat > "$CLAUDE_DIR/settings.json" <<JSON
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.1",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.2"
  },
  "enabledPlugins": {
    "codex@openai-codex": true
  },
  "extraKnownMarketplaces": {
    "openai-codex": {
      "source": { "source": "github", "repo": "openai/codex-plugin-cc" }
    }
  },
  "theme": "dark",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "bash $CLAUDE_DIR/skills/memory-tick/stop-hook-throttle.sh" },
          { "type": "command", "command": "bash $CLAUDE_DIR/skills/token-report.sh" }
        ]
      }
    ]
  }
}
JSON

echo ">> [8/8] 토큰 env 파일 (git 밖, chmod 600) — 토큰은 여기만"
ENV_FILE="$HOME/.config/claude-code/env"
mkdir -p "$(dirname "$ENV_FILE")"
if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<'EOF'
# ⚠ git에 올리지 마세요. claude 실행 전:  source ~/.config/claude-code/env && claude
export ANTHROPIC_AUTH_TOKEN="여기에_토큰_입력"
EOF
  chmod 600 "$ENV_FILE"
  echo "   생성됨: $ENV_FILE"
else
  echo "   이미 존재(보존): $ENV_FILE"
fi

cat <<DONE

============ WSL 동기화 완료 ============
남은 수동 단계:
  1) 토큰 입력:  \$EDITOR $ENV_FILE  → ANTHROPIC_AUTH_TOKEN 값 기입
  2) Claude 실행:  source $ENV_FILE && claude
  3) Claude 안에서 (plugin 재설치 — 수동 복사보다 안전):
        /plugin marketplace add openai/codex-plugin-cc
        /plugin install codex@openai-codex
        /reload-plugins
        /codex:setup
        /config theme dark
  4) 첫 세션에 온보딩 프롬프트(../ONBOARDING-PROMPT.md)로 사칙 상속·인증.

복제하지 않은 것(서버 전용/로컬 상태 — 의도적):
  ~/.claude.json, plugins/installed_plugins.json, plugins/cache,
  daemon/*, sessions/, session-env/, shell-snapshots/, projects/ transcripts,
  cokacdir, cron, Telegram 그룹 협업.
DONE
