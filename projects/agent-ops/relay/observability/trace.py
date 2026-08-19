#!/usr/bin/env python3
"""
relay trace — 봇 공용 LangSmith 계측 헬퍼 (의존성: langsmith SDK)

모든 봇이 모델 호출 지점에서 import 해 쓴다.
메타데이터 3필드(jira_ticket, relay_stage, bot_id)가 강제된다.

사용:
    from trace import relay_trace
    with relay_trace(name="parse-persona", jira_ticket="RELAY-1",
                     relay_stage="5-구현", bot_id="asset_agent") as run:
        run.inputs = {...}      # 선택
        ...
        run.result = value      # 선택 — 컨텍스트 나가기 전 채우면 기록됨

모드 (환경 RELAY_TRACE_MODE):
    all       — 전량 기록
    failures  — 예외 발생 시만 기록 (기본; 무료 월 5k 트레이스 보존용)
"""
import contextlib
import json
import os
from datetime import datetime, timezone

KEY_FILE = os.environ.get("LANGSMITH_KEY_FILE", "/home/ubuntu/.langsmith-key")
MODE = os.environ.get("RELAY_TRACE_MODE", "failures")
PROJECT = "relay-observability"
REQUIRED = ("jira_ticket", "relay_stage", "bot_id")
_client = None


def _client():
    global _client
    if _client is None:
        os.environ.setdefault("LANGCHAIN_API_KEY", open(KEY_FILE).read().strip())
        os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
        from langsmith import Client
        _client = Client()
    return _client


def _safe(v, limit=4000):
    try:
        s = json.dumps(v, ensure_ascii=False, default=str)
    except Exception:
        s = str(v)
    return s[:limit]


@contextlib.contextmanager
def relay_trace(*, name="bot-call", inputs=None, jira_ticket, relay_stage, bot_id):
    if not all([jira_ticket, relay_stage, bot_id]):
        raise ValueError(f"relay_trace 필수 메타데이터 누락: {REQUIRED}")

    import types
    box = types.SimpleNamespace(inputs=inputs, result=None)
    started = datetime.now(timezone.utc)
    error = None
    try:
        yield box
    except Exception as exc:
        error = repr(exc)
        raise
    finally:
        if MODE == "all" or error is not None:
            try:
                _client().create_run(
                    name=name,
                    run_type="chain",
                    inputs=_safe(box.inputs or {}),
                    outputs=None if error else _safe(box.result),
                    error=error,
                    project_name=PROJECT,
                    metadata={"jira_ticket": jira_ticket, "relay_stage": relay_stage,
                              "bot_id": bot_id, "trace_mode": MODE},
                    start_time=started,
                )
            except Exception:
                pass  # 계측 실패가 본 작업을 죽이지 않는다
