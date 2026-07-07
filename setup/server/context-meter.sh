#!/bin/bash
#
# context-meter.sh — 현재 세션 컨텍스트 실측 (모델명/한계/퍼센트 한 줄)
# 사칙: 매 답장 말미에 부착. 이사님 요구 2026-07-02.
#
# 측정원리: 세션 transcript JSONL의 마지막 assistant usage에서
#   input_tokens + cache_read_input_tokens + cache_creation_input_tokens
#   = 마지막 성공 요청의 컨텍스트 사용량.
#
# 주의(2026-07-07): GLM 프록시는 modelUsage.contextWindow=1,000,000 을
# 보고하지만 실제 실패는 128k~256k 근처에서 반복 확인됨. 따라서 기본
# 유효 한계는 보수적으로 128,000 으로 둔다. 필요 시
# CONTEXT_LIMIT_TOKENS 환경변수로 override.
#
# usage: context-meter.sh [--detail]
#   --detail: 줄바꿈 상세 출력. 기본은 한 줄.
#

set -euo pipefail

# transcript 경로 감지
TF="${CODEX_COMPANION_TRANSCRIPT_PATH:-}"
if [ -z "$TF" ] || [ ! -f "$TF" ]; then
    # fallback: 세션 ID 기반 검색
    SID="${CLAUDE_CODE_SESSION_ID:-}"
    if [ -n "$SID" ]; then
        TF=$(ls "$HOME"/.claude/projects/*/"$SID".jsonl 2>/dev/null | head -1 || true)
    fi
fi
if [ -z "$TF" ] || [ ! -f "$TF" ]; then
    echo "⚠ transcript 없음"
    exit 1
fi

# 컨텍스트 한계 (환경 변수 우선, 기본 128k effective)
LIMIT="${CONTEXT_LIMIT_TOKENS:-128000}"

DETAIL="${1:-}"

python3 - "$TF" "$LIMIT" "$DETAIL" <<'PY'
import json, sys, os

tf, limit_s, detail = sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else ""
last_model = "?"
last_usage = None
bytes_size = 0

try:
    bytes_size = os.path.getsize(tf)
except Exception:
    pass

with open(tf) as f:
    for line in f:
        try:
            ev = json.loads(line)
        except Exception:
            continue
        msg = ev.get("message") or {}
        m = msg.get("model") or ev.get("model")
        if m:
            last_model = m
        u = ev.get("usage") or msg.get("usage")
        # Synthetic API-error rows often carry usage=0 at the end of a crashed
        # transcript.  Do not let those hide the last successful real request.
        if u and u.get("input_tokens") is not None and not ev.get("isApiErrorMessage"):
            if (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)) <= 0:
                continue
            last_usage = u

if not last_usage:
    print("⚠ usage 없음")
    sys.exit(1)

it = last_usage.get("input_tokens", 0)
cr = last_usage.get("cache_read_input_tokens", 0)
cc = last_usage.get("cache_creation_input_tokens", 0)
total = it + cr + cc
pct = total / limit_s * 100
mb = bytes_size / 1024 / 1024

def fmt(n):
    return f"{n:,}"

# 모델명에 한계 접미사
tag = "[1m]" if limit_s >= 1_000_000 else f"[{limit_s//1000}k-eff]"

if detail == "--detail":
    print(f"모델:          {last_model}{tag}")
    print(f"한계 토큰:     {fmt(limit_s)}")
    print(f"사용 토큰:     {fmt(total)}")
    print(f"  input:       {fmt(it)}")
    print(f"  cache_read:  {fmt(cr)}")
    print(f"  cache_create:{fmt(cc)}")
    print(f"퍼센트:        {pct:.1f}%")
    print(f"transcript:    {fmt(bytes_size)} bytes ({mb:.2f} MB)")
else:
    print(f"📊 {last_model}{tag} | 한계 {fmt(limit_s)} | {fmt(total)} ({pct:.1f}%) | {mb:.1f}MB")
PY
