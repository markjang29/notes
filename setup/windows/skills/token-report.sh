#!/usr/bin/env bash
# token-report.sh — Stop 훅에서 이 세션의 누적 토큰 사용량을 집계해 출력.
# 매 응답 종료(Stop)마다 발화 → 터미널/텔레그램으로 토큰 가시화.
# bash로 직접 실행하므로 실행권한 불필요. 실패해도 exit 0 (세션 막지 않음).
token_report_main() {
  command -v jq >/dev/null 2>&1 || { echo "[token-report] jq 없음 — 스킵"; return 0; }

  # Stop 훅은 stdin에 JSON(transcript_path 등)을 받는다.
  local input transcript
  input="$(cat 2>/dev/null)"
  if [ -n "$input" ]; then
    transcript="$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null)"
  fi

  # 폴백: 가장 최근 수정 jsonl
  if [ -z "$transcript" ] || [ ! -f "$transcript" ]; then
    transcript="$(ls -t "${HOME}/.claude/projects"/*/*.jsonl 2>/dev/null | head -1)"
  fi
  if [ -z "$transcript" ] || [ ! -f "$transcript" ]; then
    echo "[token-report] transcript 없음 — 스킵"; return 0
  fi

  # jsonl 라인별 → message.usage 합산
  local stats in out cr cc total
  stats="$(jq -s '
    map(.message.usage // {})
    | {
        input:      (map(.input_tokens // 0) | add),
        output:     (map(.output_tokens // 0) | add),
        cache_read: (map(.cache_read_input_tokens // 0) | add),
        cache_cre:  (map(.cache_creation_input_tokens // 0) | add)
      }
  ' "$transcript" 2>/dev/null)" || { echo "[token-report] 집계 실패 — 스킵"; return 0; }

  in="$(printf '%s' "$stats" | jq -r '.input // 0')"
  out="$(printf '%s' "$stats" | jq -r '.output // 0')"
  cr="$(printf '%s' "$stats" | jq -r '.cache_read // 0')"
  cc="$(printf '%s' "$stats" | jq -r '.cache_cre // 0')"
  total=$((in + out + cr + cc))

  echo "🧮 세션 토큰 — 입력 ${in} / 출력 ${out} / 캐시읽기 ${cr} / 캐시생성 ${cc} | 총 ${total}"
}
token_report_main || true
exit 0
