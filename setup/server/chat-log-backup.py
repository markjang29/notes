#!/usr/bin/env python3
"""Cokacdir chat backup rotator.

Creates per-bot JSONL chat backups under /home/ubuntu/chat_logs.

Policy:
- split by bot/role
- split by hour
- rotate partNNN when a file exceeds max bytes
- keep only D+7 by default
- avoid duplicate records by tracking processed ai_session history indexes

Primary source is ~/.cokacdir/ai_sessions/*.json because it contains both
User and Assistant turns. Telegram raw logs are copied into a separate raw
bucket because they do not reliably identify which bot handled a private chat.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Any


DEFAULT_ROOT = Path("/home/ubuntu/chat_logs")
AI_SESSIONS_DIR = Path("/home/ubuntu/.cokacdir/ai_sessions")
TELEGRAM_LOGS_DIR = Path("/home/ubuntu/.cokacdir/logs")
BOT_SETTINGS = Path("/home/ubuntu/.cokacdir/bot_settings.json")

KST = dt.timezone(dt.timedelta(hours=9), name="KST")


ROLE_BY_USERNAME = {
    "heav_lnx_bot": "manager",
    "heav_lnx_rpg_bot": "rpg",
    "heav_lnx_scenario_bot": "scenario",
    "heav_lnx_trader_bot": "trader",
}

FALLBACK_PATHS = [
    ("/home/ubuntu/projects/rpg_game", ("c5bb2c97036d3741", "heav_lnx_rpg_bot", "heav_lnx_rpg", "rpg")),
    ("/home/ubuntu/projects/scenario", ("c6a54f44dab7dfe7", "heav_lnx_scenario_bot", "heav_lnx_scenario", "scenario")),
    ("/home/ubuntu/projects/autotrader", ("e802e57aacbe8f8b", "heav_lnx_trader_bot", "heav_lnx_trader", "trader")),
    ("/home/ubuntu/.cokacdir/workspace/r2meshwa", ("f5c0501a3a7999ad", "heav_lnx_bot", "heav_lnx", "audit")),
]


def now_kst() -> dt.datetime:
    return dt.datetime.now(tz=KST)


def safe_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_") or "unknown"


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except Exception:
        return default


def save_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def load_path_map() -> dict[str, tuple[str, str, str, str]]:
    data = load_json(BOT_SETTINGS, {})
    out: dict[str, tuple[str, str, str, str]] = {}
    if isinstance(data, dict):
        for key, cfg in data.items():
            if not isinstance(cfg, dict):
                continue
            username = cfg.get("username") or "unknown"
            display = cfg.get("display_name") or username
            role = ROLE_BY_USERNAME.get(username, "unknown")
            for path in (cfg.get("last_sessions") or {}).values():
                if isinstance(path, str) and path:
                    # r2meshwa is the Codex audit chat, not ordinary manager work.
                    path_role = "audit" if path.endswith("/r2meshwa") else role
                    out[path] = (key, username, display, path_role)
    for prefix, meta in FALLBACK_PATHS:
        out.setdefault(prefix, meta)
    return out


def identify_bot(current_path: str | None, provider: str | None, path_map: dict[str, tuple[str, str, str, str]]) -> dict[str, str]:
    current_path = current_path or ""
    if current_path in path_map:
        key, username, display, role = path_map[current_path]
    else:
        key = username = display = role = "unknown"
        for prefix, meta in FALLBACK_PATHS:
            if current_path.startswith(prefix):
                key, username, display, role = meta
                break
    if provider == "codex" and current_path.endswith("/r2meshwa"):
        role = "audit"
        username = "heav_lnx_bot_codex_audit"
        display = "heav_lnx_codex_audit"
    return {
        "bot_key": key,
        "bot_username": username,
        "bot_display_name": display,
        "role": role,
    }


def hourly_base(ts: dt.datetime) -> tuple[str, str]:
    ts = ts.astimezone(KST)
    return ts.strftime("%Y-%m-%d"), ts.strftime("%H_00")


def write_rotated(root: Path, bucket_parts: list[str], ts: dt.datetime, record: dict[str, Any], max_bytes: int) -> Path:
    date_dir, hour = hourly_base(ts)
    dest_dir = root.joinpath(*[safe_name(p) for p in bucket_parts], date_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    encoded = line.encode("utf-8")
    part = 1
    while True:
        path = dest_dir / f"{hour}.part{part:03d}.jsonl"
        if not path.exists() or path.stat().st_size + len(encoded) <= max_bytes:
            with path.open("ab") as f:
                f.write(encoded)
            return path
        part += 1


def process_ai_sessions(root: Path, state: dict[str, Any], max_bytes: int) -> dict[str, int]:
    path_map = load_path_map()
    ai_state = state.setdefault("ai_sessions", {})
    stats = {"sessions_seen": 0, "records_written": 0, "unknown_sessions": 0}
    export_ts = now_kst()

    for path in sorted(AI_SESSIONS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime):
        data = load_json(path, None)
        if not isinstance(data, dict):
            continue
        history = data.get("history") or []
        if not isinstance(history, list):
            continue
        session_id = data.get("session_id") or path.stem
        provider = data.get("provider")
        current_path = data.get("current_path")
        meta = identify_bot(current_path, provider, path_map)
        if meta["role"] == "unknown":
            stats["unknown_sessions"] += 1
        key = str(session_id)
        prev = int(ai_state.get(key, {}).get("count", 0))
        if prev > len(history):
            # Session file was compacted/rebuilt. Start over but preserve that this happened.
            prev = 0
        stats["sessions_seen"] += 1
        for idx in range(prev, len(history)):
            item = history[idx]
            if not isinstance(item, dict):
                continue
            record = {
                "schema": "chat-log-ai-session-v1",
                "source": "ai_session",
                "exported_at": export_ts.isoformat(),
                "session_id": session_id,
                "provider": provider,
                "current_path": current_path,
                **meta,
                "idx": idx,
                "item_type": item.get("item_type"),
                "content": item.get("content", ""),
            }
            bucket_user = meta["bot_username"] if meta["bot_username"] != "unknown" else "unknown"
            write_rotated(root, [meta["role"], bucket_user], export_ts, record, max_bytes)
            stats["records_written"] += 1
        ai_state[key] = {
            "count": len(history),
            "path": str(path),
            "provider": provider,
            "current_path": current_path,
            **meta,
            "updated_at": export_ts.isoformat(),
        }
    return stats


def process_telegram_raw(root: Path, state: dict[str, Any], max_bytes: int) -> dict[str, int]:
    tg_state = state.setdefault("telegram_raw", {})
    stats = {"files_seen": 0, "records_written": 0}
    for path in sorted(TELEGRAM_LOGS_DIR.glob("telegram_*.jsonl")):
        key = str(path)
        offset = int(tg_state.get(key, {}).get("offset", 0))
        size = path.stat().st_size
        if offset > size:
            offset = 0
        stats["files_seen"] += 1
        with path.open("rb") as f:
            f.seek(offset)
            for raw in f:
                try:
                    rec = json.loads(raw.decode("utf-8"))
                except Exception:
                    continue
                ts_s = rec.get("ts")
                try:
                    ts = dt.datetime.fromisoformat(ts_s).astimezone(KST) if ts_s else now_kst()
                except Exception:
                    ts = now_kst()
                chat_id = str(rec.get("chat_id", "unknown"))
                out = {
                    "schema": "chat-log-telegram-raw-v1",
                    "source": "telegram_raw",
                    "exported_at": now_kst().isoformat(),
                    **rec,
                }
                write_rotated(root, ["telegram_raw", chat_id], ts, out, max_bytes)
                stats["records_written"] += 1
            tg_state[key] = {"offset": f.tell(), "updated_at": now_kst().isoformat()}
    return stats


def purge_old(root: Path, retention_days: int) -> dict[str, int]:
    now = now_kst()
    cutoff = now.timestamp() - retention_days * 86400
    cutoff_date = (now.date() - dt.timedelta(days=retention_days))
    stats = {"files_deleted": 0, "dirs_deleted": 0}
    if not root.exists():
        return stats
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file() and "/.state/" not in str(path) and "/.run/" not in str(path):
            try:
                dated = None
                for part in path.parts:
                    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", part):
                        try:
                            dated = dt.date.fromisoformat(part)
                        except ValueError:
                            dated = None
                        break
                old_by_date = dated is not None and dated < cutoff_date
                old_by_mtime = dated is None and path.stat().st_mtime < cutoff
                if old_by_date or old_by_mtime:
                    path.unlink()
                    stats["files_deleted"] += 1
            except FileNotFoundError:
                pass
    for path in sorted([p for p in root.rglob("*") if p.is_dir()], key=lambda p: len(str(p)), reverse=True):
        if path.name in {".state", ".run"}:
            continue
        try:
            path.rmdir()
            stats["dirs_deleted"] += 1
        except OSError:
            pass
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--max-bytes", type=int, default=512 * 1024)
    ap.add_argument("--retention-days", type=int, default=7)
    ap.add_argument("--source", choices=["all", "ai", "telegram"], default="all")
    args = ap.parse_args()

    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    (root / ".run").mkdir(parents=True, exist_ok=True)
    state_path = root / ".state" / "state.json"
    state = load_json(state_path, {})
    if not isinstance(state, dict):
        state = {}

    summary: dict[str, Any] = {
        "ts": now_kst().isoformat(),
        "root": str(root),
        "max_bytes": args.max_bytes,
        "retention_days": args.retention_days,
    }
    if args.source in {"all", "ai"}:
        summary["ai"] = process_ai_sessions(root, state, args.max_bytes)
    if args.source in {"all", "telegram"}:
        summary["telegram_raw"] = process_telegram_raw(root, state, args.max_bytes)
    summary["purge"] = purge_old(root, args.retention_days)
    save_json_atomic(state_path, state)

    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
