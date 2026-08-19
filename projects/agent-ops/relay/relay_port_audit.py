#!/usr/bin/env python3
"""RELAY-15 포트 단속 감사 — 8000번대 서버 무단 운행 적발.

매일 09:10 KST 시스템 크론 실행. 승인보드 라우터 폴링이 requested 카드를
감지하면 매니저 라우터 세션이 이사님께 보고한다.

동작:
  1. 8000-8099 리스닝 포트 스캔 (ss -tlnp)
  2. 청취 프로세스의 환경변수 RELAY_TICKET 확인
  3. 레지스트리(port-registry.json) 대조 + Jira RELAY 티켓 존재 검증
  4. 무단(티켓 없음/부정 티켓/레지스트리 불일치) → approval-board 카드 발행
  5. 결과 JSON을 notes-registry relay/tickets/RELAY-15/audit/ 아래 기록

시크릿 없음: Jira 토큰은 /home/ubuntu/.jira-token에서만 읽는다.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
REGISTRY_PATH = Path(
    "/home/ubuntu/deploy/notes-registry/projects/agent-ops/relay/port-registry.json"
)
AUDIT_DIR = Path(
    "/home/ubuntu/deploy/notes-registry/projects/agent-ops/relay/tickets/RELAY-15/audit"
)
JIRA_TOKEN_PATH = Path("/home/ubuntu/.jira-token")
JIRA_USER = "heavenlyiris@gmail.com"
JIRA_BASE = "https://heavenlyiris-matrix.atlassian.net"
BOARD_TOKEN_PATH = Path("/home/ubuntu/projects/approval-board/auth_token.txt")
BOARD_BASE = "http://localhost:8005"
PORT_RANGE = range(8000, 8100)


def now_kst() -> datetime:
    return datetime.now(KST)


def scan_listening_ports() -> dict[int, list[str]]:
    """8000번대 리스닝 포트 → pid 목록."""
    out = subprocess.run(
        ["ss", "-tlnp"], capture_output=True, text=True, timeout=30
    ).stdout
    ports: dict[int, list[str]] = {}
    for line in out.splitlines():
        m = re.search(r":(80\d\d)\b", line)
        if not m:
            continue
        port = int(m.group(1))
        if port not in PORT_RANGE:
            continue
        for pm in re.finditer(r"pid=(\d+)", line):
            ports.setdefault(port, []).append(pm.group(1))
    return ports


def pid_environment(pid: str) -> dict[str, str]:
    try:
        raw = Path(f"/proc/{pid}/environ").read_bytes()
    except OSError:
        return {}
    env: dict[str, str] = {}
    for entry in raw.split(b"\0"):
        if b"=" in entry:
            k, _, v = entry.partition(b"=")
            env[k.decode("utf-8", "replace")] = v.decode("utf-8", "replace")
    return env


def pid_cmdline(pid: str) -> str:
    try:
        return Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(
            "utf-8", "replace"
        )[:180]
    except OSError:
        return "(gone)"


def jira_ticket_exists(key: str) -> bool:
    token = JIRA_TOKEN_PATH.read_text().strip()
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/issue/{key}",
        headers={"Authorization": "Basic " + _b64(f"{JIRA_USER}:{token}")},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise
    except urllib.error.URLError:
        raise


def _b64(s: str) -> str:
    import base64

    return base64.b64encode(s.encode()).decode()


def board_post_card(title: str, body: str, done_criteria: str) -> dict:
    token = BOARD_TOKEN_PATH.read_text().strip()
    payload = json.dumps(
        {
            "title": title,
            "target_bot": "manager",
            "body": body,
            "done_criteria": done_criteria,
        }
    ).encode()
    req = urllib.request.Request(
        f"{BOARD_BASE}/api/request",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def main() -> int:
    ts = now_kst()
    registry = json.loads(REGISTRY_PATH.read_text())
    reg_by_port = {r["port"]: r for r in registry.get("registered", [])}
    pending = {p["port"]: p for p in registry.get("pending_registration", [])}
    board_token_ok = BOARD_TOKEN_PATH.exists()

    listening = scan_listening_ports()
    findings: list[dict] = []
    for port, pids in sorted(listening.items()):
        entry = reg_by_port.get(port)
        pend = pending.get(port)
        for pid in pids:
            env = pid_environment(pid)
            env_ticket = env.get("RELAY_TICKET")
            reg_ticket = entry["ticket"] if entry else None
            verdict = "ok"
            reasons: list[str] = []
            if entry is None and pend is None:
                verdict = "unregistered"
                reasons.append("레지스트리에 포트 없음")
            elif entry is None and pend is not None:
                verdict = "pending_registration"
                reasons.append("레지스트리 pending — 등록 티켓 미완료")
            if env_ticket is None:
                if verdict == "ok":
                    verdict = "env_missing"
                reasons.append("환경변수 RELAY_TICKET 없음")
            elif reg_ticket and env_ticket != reg_ticket:
                verdict = "ticket_mismatch"
                reasons.append(
                    f"env 티켓 {env_ticket} != 레지스트리 {reg_ticket}"
                )
            findings.append(
                {
                    "port": port,
                    "pid": pid,
                    "cmd": pid_cmdline(pid),
                    "env_ticket": env_ticket,
                    "registry_ticket": reg_ticket,
                    "verdict": verdict,
                    "reasons": reasons,
                }
            )

    # Jira 티켓 존재 검증 (env or registry 티켓이 있는 경우만, 오류 시 fail-closed)
    jira_checked: dict[str, bool] = {}
    for f in findings:
        key = f["env_ticket"] or f["registry_ticket"]
        if key and key.startswith("RELAY-") and key not in jira_checked:
            try:
                jira_checked[key] = jira_ticket_exists(key)
            except Exception as e:  # Jira 접근 불가 → 무단 판정 보류
                print(f"WARN jira check failed for {key}: {e}", file=sys.stderr)
                jira_checked[key] = None  # type: ignore[assignment]
    for f in findings:
        key = f["env_ticket"] or f["registry_ticket"]
        if key and jira_checked.get(key) is False:
            f["verdict"] = "ticket_invalid"
            f["reasons"].append(f"Jira에 {key} 없음")

    violations = [
        f for f in findings if f["verdict"] != "ok"
    ]

    report = {
        "schema": "relay-port-audit-v1",
        "ticket": "RELAY-15",
        "ran_at_kst": ts.isoformat(timespec="seconds"),
        "listening_ports": sorted(listening),
        "total_findings": len(findings),
        "violations": violations,
        "jira_checked": jira_checked,
        "board_token_available": board_token_ok,
    }

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = AUDIT_DIR / f"port-audit-{ts:%Y%m%d-%H%M%S}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))

    if violations:
        # 동일 위반 집합이면 매일 카드가 반복 발행되지 않도록 직전 보고와 비교.
        sig = sorted(
            (v["port"], v["verdict"], v["env_ticket"], v["registry_ticket"])
            for v in violations
        )
        prev_reports = sorted(AUDIT_DIR.glob("port-audit-*.json"))[:-1]
        deduped = False
        for prev_path in reversed(prev_reports):
            try:
                prev = json.loads(prev_path.read_text())
            except (OSError, ValueError):
                continue
            prev_sig = sorted(
                (v["port"], v["verdict"], v["env_ticket"], v["registry_ticket"])
                for v in prev.get("violations", [])
            )
            if prev_sig == sig:
                deduped = True
            # 위반이 감소했거나 그대로면 재발행하지 않고, 새로 생긴 위반만 알린다.
            if set(sig) <= set(prev_sig):
                deduped = True
            break
        lines = [
            f"- {v['port']} pid={v['pid']} ({v['verdict']}): {'; '.join(v['reasons'])}"
            for v in violations
        ]
        body = (
            f"RELAY-15 자동 포트 감사({ts:%Y-%m-%d %H:%M} KST) 무단 운행 적발 "
            f"{len(violations)}건.\n레지스트리: relay/port-registry.json\n"
            + "\n".join(lines)
        )
        if violations and not deduped and board_token_ok:
            try:
                card = board_post_card(
                    f"[감사] RELAY-15 포트 단속 — 무단 서버 {len(violations)}건 적발",
                    body,
                    "위반 항목 전부 등록 완료 또는 운행 중지 후 재감사 통과",
                )
                report["board_card_id"] = card.get("id")
                report_path.write_text(
                    json.dumps(report, ensure_ascii=False, indent=2)
                )
            except Exception as e:
                print(f"WARN board card post failed: {e}", file=sys.stderr)
        if deduped:
            report["card_suppressed"] = "직전 감사와 동일 위반 집합 — 카드 중복 발행 생략"
            report_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2)
            )

    print(json.dumps({
        "ran_at_kst": report["ran_at_kst"],
        "listening": len(listening),
        "violations": len(violations),
        "report": str(report_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
