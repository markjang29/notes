#!/usr/bin/env bash
# stop-hook-throttle.sh — memory-tick 강제 발화 (throttle 게이트)
# Claude Code Stop hook에서 호출됨. 최소 간격을 두고 memory-tick 점검 메시지를 출력한다.
# hook은 실패하면 세션을 막을 수 있으므로, 본문을 래핑하고 항상 exit 0 한다.

throttle_main() {
  local THROTTLE_FILE="${HOME}/.claude/.memory-tick-last"
  local MIN_INTERVAL="${MEMORY_TICK_INTERVAL:-300}"   # 초 (기본 5분)
  [[ "$MIN_INTERVAL" =~ ^[0-9]+$ ]] || MIN_INTERVAL=300   # 숫자 검증

  local now last
  now=$(date +%s) || return 0
  last=0
  [ -f "$THROTTLE_FILE" ] && last=$(cat "$THROTTLE_FILE" 2>/dev/null || printf '0')
  [[ "$last" =~ ^[0-9]+$ ]] || last=0

  if [ $((now - last)) -ge "$MIN_INTERVAL" ]; then
    printf '%s' "$now" > "$THROTTLE_FILE" 2>/dev/null
    echo "[memory-tick] 저장 가치 점검: 최근 대화 구간에 후보(candidate) 메모가 있는지 확인하고, 있으면 memory-tick 스킬로 저장 (~/.claude/skills/memory-tick)."
  fi
}

throttle_main || true
exit 0
