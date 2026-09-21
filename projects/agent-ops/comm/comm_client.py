#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comm_client.py — 봇 표준 통신 클라이언트 (stdlib 0의존, 8024 comm 채널)
정본: notes/projects/agent-ops/comm/comm_client.py (원본 1개 — 각 봇은 복사본+버전주석 필수)
사칙: principles/telegram-comm-protocol-v1.md (2026-09-21, 이사님 지시)
용도: hub_client.py(8023) 후계. 봇간 송수신·공지 수신·ACK을 전부 이 클라이언트로.

사용 예 (각 봇의 세션 부팅 루틴에서):
    from comm_client import CommClient
    c = CommClient("http://43.201.34.144:8024", "heav_lnx_codex_dev_1_bot",
                   token=MY_TOKEN)          # 토큰값은 본문에 기입 금지 — 파일경로만
    # 1) 부팅 미수신 처리: 수신→handler→자동ACK
    for m in c.poll():
        print(m["from"], "->", m["to"], m["text"])
    # 2) 송신 (봇간)
    c.send("heav_gmwin_codex_bot", "task", {"ref": "RELAY-67"})
    # 3) 수동 ACK (note에 무엇을 이해했는지·acknowledged|blocked)
    c.ack("<msg_id>", note="사칙개정 확인 — acknowledged")
    # 4) 자기 신원·미수신 요약
    print(c.whoami())

API (8024): GET /api/nats/inbox?bot=&token= · POST /api/nats/send
            POST /api/nats/ack · GET /api/nats/whoami?bot=&token=
            — 1단계(이사님 승인) 구현본. 실패 시 재시도 3회(1/2/4초 backoff) 후 []/False.
"""

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, List, Optional

BASE = "http://43.201.34.144:8024"
VERSION = "comm-client-1.0 (2026-09-21, 사칙 통신표준 v1)"
RETRIES = 3


def _req(url: str, method: str = "GET", body: Optional[Dict] = None) -> Any:
    last = None
    for attempt in range(RETRIES):
        try:
            data = None
            headers = {"Accept": "application/json"}
            if body is not None:
                data = json.dumps(body, ensure_ascii=False).encode("utf-8")
                headers["Content-Type"] = "application/json"
            req = urllib.request.Request(url, data=data, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as res:
                if res.status == 200:
                    return json.loads(res.read().decode("utf-8") or "[]")
                return None
        except Exception as e:  # 네트워크·브로커·8024 일시장애 — 95-1: backoff 후 재시도
            last = e
            time.sleep(2 ** attempt)
    return [] if method == "GET" else {"status": "error", "message": str(last)}


class CommClient:
    """comm 채널 클라이언트 — 1봇 1인스턴스 (token은 본문 기입 금지, 파일경로만)."""

    def __init__(self, base: str = BASE, bot: str = "", token: str = ""):
        if not bot:
            raise ValueError("bot(username) 필수 — roster.json 실명만 (가명·약칭 금지, 사칙 §2)")
        self.base = base.rstrip("/")
        self.bot = bot
        self.token = token

    # --- GET ---
    def poll(self) -> List[Dict]:
        """미수신함 조회. 빈 [] = 새것 없음(정상). 수신한 것은 각자 즉시 ack() 의무."""
        q = urllib.parse.urlencode({"bot": self.bot, "token": self.token})
        return _req(f"{self.base}/api/nats/inbox?{q}")

    def whoami(self) -> Any:
        """자기 신원·미수신 요약(부팅 체크리스트 2번)."""
        q = urllib.parse.urlencode({"bot": self.bot, "token": self.token})
        return _req(f"{self.base}/api/nats/whoami?{q}")

    # --- POST ---
    def send(self, to: str, msg_type: str = "task", payload: Any = None,
             text: str = "", ref: str = "") -> Any:
        """봇간 송신. 헤더 7필드(id·ts·subject·from·to·text·payload)는 8024가 부여·검증."""
        return _req(f"{self.base}/api/nats/send", "POST", {
            "from": self.bot, "token": self.token, "to": to, "type": msg_type,
            "text": text, "ref": ref, "payload": payload or {}})

    def broadcast(self, msg_type: str = "notice", text: str = "", ref: str = "") -> Any:
        """공지 발행(매니저·이사님 — 전봇 fanout)."""
        return _req(f"{self.base}/api/nats/send", "POST", {
            "from": self.bot, "token": self.token, "to": "@all", "type": msg_type,
            "text": text, "ref": ref, "payload": {}})

    def ack(self, msg_id: str, note: str = "acknowledged") -> Any:
        """수신확인영수증 — 관제 7필드 준용. '봤음' 단독은 ACK 아님(사칙 §3-3)."""
        return _req(f"{self.base}/api/nats/ack", "POST", {
            "from": self.bot, "token": self.token, "msg_id": msg_id, "note": note})

    # --- 루프 헬퍼 ---
    def poll_forever(self, handler: Optional[Callable[[Dict], Any]] = None,
                     interval: int = 30, one_shot: bool = False) -> None:
        """30~60초 주기 폴링(사칙 §3-1). 수신→handler→자동ACK. 1회만(one_shot=True)은 부팅시 권장."""
        while True:
            for m in self.poll():
                note = "acknowledged"
                if handler:
                    try:
                        note = handler(m) or "acknowledged"
                    except Exception as e:
                        note = f"blocked: handler 실패 {e!r}"
                self.ack(m.get("id", ""), note=note)
            if one_shot:
                return
            time.sleep(interval)


if __name__ == "__main__":
    import os
    import sys
    # 실무: 토큰은 커밋·채팅에 넣지 말고 파일경로에서만 읽는다 (L0 금지 §6, 사칙 §6)
    tok = sys.argv[1] if len(sys.argv) > 1 else ""
    c = CommClient(bot=os.environ.get("COMM_BOT", "heav_lnx_codex_dev_1_bot"), token=tok)
    print(json.dumps(c.whoami(), ensure_ascii=False, indent=2))
    for m in c.poll():
        print(m.get("from"), "->", m.get("to"), ":", m.get("text"))
        c.ack(m.get("id", ""), note="부팅 미수신 처리 — acknowledged")
