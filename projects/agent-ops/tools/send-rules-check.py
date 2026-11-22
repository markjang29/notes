#!/usr/bin/env python3
"""공통 발송 규칙 검사기 — COMPANY-OPS-20261120 (서버측 미러, 텍스트 정적 검사).

규칙(이사님 2026-11-22 지시):
  R1 장문 자동 분할 — 3800자 초과 본문은 [n/N] 분할 마커 없으면 실패
  R2 파일 대체 금지 — 장문을 '파일로 전송했다'는 보고 문구 탐지 시 실패
  R3 도구 로그 제외 — 도구 입력/실행 독백·서명 URL·시스템 리마인더 블록 탐지 시 실패
  R4 이모지 남용 — 이모지 20개 초과 시 실패(요약 가독성)
  R5 분할 마커 정합 — [n/N] 조각은 n·N 양의 정수, 등차 오름차순

사용: python3 send-rules-check.py <보고텍스트파일>
출력: JSON {"rules": {"R1": "pass|fail", ...}, "findings": [...]}
"""
import json
import re
import sys
import unicodedata

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿]")
TOOL_LOG = [
    re.compile(r"Executing on server", re.I),
    re.compile(r"\*\*Input:\*\*", re.I),
    re.compile(r"imageSource|OSSAccessKeyId=|Signature=[A-Za-z0-9%/+]{20,}"),
    re.compile(r"glm-file\.bigmodel\.cn|cdn"),
    re.compile(r"<system-reminder>", re.I),
    re.compile(r"^Tool:\s", re.I),
    re.compile(r"task-notification|tool-use tool_call_id", re.I),
]
FILE_SUB = re.compile(r"(txt|파일)\s*(으로|로)\s*(전송|보내|드렸|보냈)|--sendfile.*보고|파일로\s*대체", re.I)
SPLIT = re.compile(r"\[(\d+)/(\d+)\]")


def check(text: str) -> dict:
    findings = []
    r = {}
    chunks = SPLIT.findall(text)
    # R1
    over = len(text) > 3800
    r["R1_장문분할"] = "fail" if over and not chunks else "pass"
    if over and not chunks:
        findings.append(f"본문 {len(text)}자, 분할 마커 없음")
    # R2
    m = FILE_SUB.search(text)
    r["R2_파일대체금지"] = "fail" if m else "pass"
    if m:
        findings.append("파일 대체 문구: " + m.group(0)[:40])
    # R3
    hits = [p.pattern for p in TOOL_LOG if p.search(text)]
    r["R3_도구로그제외"] = "fail" if hits else "pass"
    findings += ["도구로그 패턴: " + h[:40] for h in hits]
    # R4
    n_emoji = len(EMOJI.findall(text))
    r["R4_이모지한도"] = "fail" if n_emoji > 20 else "pass"
    if n_emoji > 20:
        findings.append(f"이모지 {n_emoji}개")
    # R5
    ok = all(a.isdigit() and b.isdigit() and 0 < int(a) <= int(b) for a, b in chunks) and \
        [int(a) for a, _ in chunks] == sorted({int(a) for a, _ in chunks})
    r["R5_분할마커정합"] = "pass" if (not chunks or ok) else "fail"
    if chunks and not ok:
        findings.append("분할 마커 비정렬: " + str(chunks))
    verdict = "pass" if all(v == "pass" for v in r.values()) else "fail"
    return {"verdict": verdict, "rules": r, "findings": findings,
            "length": len(text), "chunks": len(chunks)}


if __name__ == "__main__":
    path = sys.argv[1]
    text = unicodedata.normalize("NFC", open(path, encoding="utf-8").read())
    print(json.dumps(check(text), ensure_ascii=False))
