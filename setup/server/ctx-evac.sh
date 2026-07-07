#!/bin/bash
#
# ctx-evac.sh — 컨텍스트 방전 (요약 → 필수백업 → clear 권고)
# 사칙: 529(레이트리밋) 폴백은 있으나 1M(컨텍스트한계) 방전이 없어 신설.
#       2026-07-03 ADR. 기존 context-meter.sh(측정)·emergency-write.sh(atomic) 재사용.
#
# 트리거:
#   precompact  — settings.json PreCompact 훅 (자동 압축 직전)
#   check       — Stop 훅 사전방어선 (70% 초과 강제 방전)
#   manual      — 수동 호출 (위기 감지 시)
#   watch       — cron/reaper 임계 감시
#
# 임계 정책:
#   check   : > 70%  — 강제 방전(요약 + 필수 백업 + /clear 권고)
#   < 85%   : 정상. PreCompact/watch는 백업 생략(과다 백업 방지).
#   85~95%  : Phase1 — checkpoint 백업(요약)
#   ≥ 95%   : Phase2 — 필수 백업 + emergency + /clear 권고
#
# usage: ctx-evac.sh [precompact|check|manual|watch]
#

set -euo pipefail

MODE="${1:-manual}"
BOT="${HEAV_LNX_BOT_NAME:-manager}"
TS_FS=$(TZ='Asia/Seoul' date '+%Y-%m-%d %H:%M:%S KST')
TS_FILE=$(TZ='Asia/Seoul' date '+%Y-%m-%d_%H%M%S')
CKPT_DIR="$HOME/notes/checkpoints"
CKPT="$CKPT_DIR/checkpoint-${BOT}-${TS_FILE}.md"
TMP="$CKPT.tmp.$$"
HOOK_JSON=""

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ctx-evac] $*" >&2; }

mkdir -p "$CKPT_DIR"

if [ "$MODE" = "check" ]; then
  # Stop 훅 stdin JSON에는 transcript_path가 들어온다. 과거에는 이를 버려
  # context-meter/byte fallback이 엉뚱한 최근 파일을 볼 수 있었다.
  HOOK_JSON="$(timeout 0.2 cat 2>/dev/null || true)"
fi

detect_transcript() {
  if [ -n "$HOOK_JSON" ]; then
    local from_hook
    from_hook="$(python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("transcript_path",""))
except Exception:
    print("")' <<<"$HOOK_JSON" 2>/dev/null || true)"
    if [ -n "$from_hook" ] && [ -f "$from_hook" ]; then
      printf '%s\n' "$from_hook"
      return 0
    fi
  fi

  local tf="${CODEX_COMPANION_TRANSCRIPT_PATH:-}"
  if [ -n "$tf" ] && [ -f "$tf" ]; then
    printf '%s\n' "$tf"
    return 0
  fi

  local sid="${CLAUDE_CODE_SESSION_ID:-}"
  if [ -n "$sid" ]; then
    ls "$HOME"/.claude/projects/*/"$sid".jsonl 2>/dev/null | head -1
    return 0
  fi

  ls -t "$HOME"/.claude/projects/*/*.jsonl 2>/dev/null | head -1
}

estimate_pct_from_bytes() {
  local tf="$1"
  [ -n "$tf" ] && [ -f "$tf" ] || return 1
  python3 - "$tf" <<'PY'
import os, sys

size = os.path.getsize(sys.argv[1])
# GLM effective context가 1M이 아니라 128k~256k 근처에서 터지는 패턴.
# transcript 0.75MB 근처에서 RPG 세션이 실패했으므로 보수적으로 0.75MB=70%.
threshold = 0.75 * 1024 * 1024  # 0.75MB ~= 70% 임계
pct = size / threshold * 70 if threshold else 0
print(f"{pct:.1f}")
PY
}

is_trigger_error() {
  local text="${*,,}"
  [[ "$text" == *"429"* ]] ||
  [[ "$text" == *"529"* ]] ||
  [[ "$text" == *"quota"* ]] ||
  [[ "$text" == *"context window limit"* ]] ||
  [[ "$text" == *"context_length_exceeded"* ]]
}

# --- 1. 측정 (context-meter.sh 재사용) ---
TF="$(detect_transcript || true)"
METER=$(CODEX_COMPANION_TRANSCRIPT_PATH="${TF:-}" bash "$HOME/scripts/context-meter.sh" 2>/dev/null || echo "⚠ 측정불가")
# "한계 1,000,000 | 850,000 (85.0%)" 형태에서 % 추출
PCT=$(echo "$METER" | grep -oE '\([0-9.]+%\)' | grep -oE '[0-9.]+' | head -1 || echo "0")
PCT_INT="${PCT%.*}"
[ -z "$PCT_INT" ] && PCT_INT=0
FALLBACK_NOTE=""
if [ "${PCT_INT:-0}" -eq 0 ]; then
  BYTE_PCT="$(estimate_pct_from_bytes "$TF" 2>/dev/null || true)"
  if [ -n "$BYTE_PCT" ]; then
    PCT="$BYTE_PCT"
    PCT_INT="${PCT%.*}"
    FALLBACK_NOTE="usage=0/없음 폴백: transcript byte 크기 기준 추정(0.75MB≈70%). transcript=$TF"
    METER="$METER | $FALLBACK_NOTE"
  else
    FALLBACK_NOTE="usage=0/측정불가 및 transcript byte 추정 불가 — 보수적 경고 필요"
    METER="$METER | $FALLBACK_NOTE"
  fi
fi

TRIGGER_TEXT="${*:2} ${CLAUDE_ERROR:-} ${ERROR_MESSAGE:-}"

# --- 2. checkpoint 백업 (활성작업·git·세션포인터 자동 수집) ---
write_checkpoint() {
  local section
  section() {
    # $1=레포경로
    local d="$1"
    if [ -d "$d/.git" ]; then
      echo "status:"; git -C "$d" status -s 2>/dev/null | head -15
      echo "log:"; git -C "$d" log --oneline -3 2>/dev/null
    else
      echo "(디렉토리 없음)"
    fi
  }

  cat > "$TMP" <<EOF
# 컨텍스트 방전 체크포인트 — $BOT
- 시각: $TS_FS
- 모드: $MODE
- 측정: $METER
- 퍼센트: ${PCT}%

## 활성 작업 (work-queue.md 상단)
\`\`\`
$(head -45 "$HOME/notes/work-queue.md" 2>/dev/null || echo "(work-queue 없음)")
\`\`\`

## git 상태 — scenario
$(section "$HOME/projects/scenario")

## git 상태 — rpg_game
$(section "$HOME/projects/rpg_game")

## git 상태 — autotrader
$(section "$HOME/projects/autotrader")

## 세션·복구 포인터
- canonical memory: $HOME/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory
- 복구入口: akl0hdys memory MEMORY.md → work-queue.md
- CLAUDE_CODE_SESSION_ID: ${CLAUDE_CODE_SESSION_ID:-(n/a)}
- transcript 힌트: ${TF:-$HOME/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/*.jsonl}

## 복구 지침
1. /clear (또는 신규 세션). cron --session 으로 같은 세션 resume 금지(누적 폭발 원인).
2. 위 활성 작업·미커밋 변경부터 마무리.
3. memory + work-queue.md 기반 복구 (clear-recovery-map 참조).
4. 1M 폭발 재발 방지: work-queue/memory 통째 주입 억제, WebSearch dump 발췌만.
EOF
  mv "$TMP" "$CKPT"
  log "✅ checkpoint 작성: $CKPT"
}

# --- 3. 임계 분기 ---
if [ "$MODE" = "check" ] && { [ "$PCT_INT" -gt 70 ] 2>/dev/null || is_trigger_error "$TRIGGER_TEXT"; }; then
  write_checkpoint
  bash "$HOME/scripts/healthcheck/emergency-write.sh" \
       "context ${PCT}% (>70% check 임계 또는 트리거 에러)" "ctx-evac check 완료: $CKPT" 2>/dev/null || true
  cat <<EOF
🚨 컨텍스트 ${PCT}% — Stop 훅 check 임계(>70%) 또는 트리거 에러 감지. 강제 방전 완료.
체크포인트: $CKPT
emergency:   $HOME/notes/emergency-${BOT}.md
권고: 즉시 /clear 또는 신규 세션 전환. 큰 tool_result 원문은 파일분리.
EOF
  exit 0

elif [ "$MODE" = "check" ] && [ -n "$FALLBACK_NOTE" ] && [ "$PCT_INT" -eq 0 ] 2>/dev/null; then
  echo "⚠ ctx-evac check: $FALLBACK_NOTE"
  echo "권고: transcript 경로/usage 기록을 점검하고 큰 tool_result는 파일분리."
  exit 0

elif [ "$PCT_INT" -ge 95 ] 2>/dev/null; then
  # Phase 2: 필수 백업 + emergency + clear 권고
  write_checkpoint
  bash "$HOME/scripts/healthcheck/emergency-write.sh" \
       "context ${PCT}% (≥95% 임계)" "ctx-evac Phase2 완료: $CKPT" 2>/dev/null || true
  cat <<EOF
🚨 컨텍스트 ${PCT}% — 임계(≥95%) 도달. Phase2 백업 완료.
체크포인트: $CKPT
emergency:   $HOME/notes/emergency-${BOT}.md
권고: 즉시 /clear 또는 신규 세션 전환. (cron --session 누적 주의)
EOF
  exit 0

elif [ "$PCT_INT" -ge 85 ] 2>/dev/null; then
  # Phase 1: 요약 백업
  write_checkpoint
  echo "⚠ 컨텍스트 ${PCT}% — 요약 단계(85~95%). checkpoint: $CKPT"
  echo "권고: 여유 있을 때 /clear 후 체크포인트로 복구."
  exit 0

else
  # 정상 — watch/precompact는 생략, manual은 정보만
  if [ "$MODE" = "manual" ]; then
    echo "ctx-evac: ${PCT}% — 정상 범위(<85%). 백업 불필요."
    echo "측정: $METER"
  else
    log "정상(${PCT}%). 백업 생략."
  fi
  exit 0
fi
