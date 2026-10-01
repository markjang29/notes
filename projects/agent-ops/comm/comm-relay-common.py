#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comm-relay-common.py — 봇 사이드카 정본 (매니저 지시 3번, 09-23, id 1790163528578-174)
근거: 2번(id 1790155957785-12)·66번(id 1790146367556-66) · 이사님 09-23 승인
      사칭 principles/telegram-comm-protocol-v1.md §5 · 95-5(정본-사본: 이 파일=원본, 거점=사본+버전주석)

구조: 감시대상(사이트 내 active 봇)·각성키·endpoint를 sidecar.env로 분리 — 하드코딩 0.
      봇이름·키경로·채팅ID 모두 env값 (사본 거점은 env만 고쳐 쓴다 — 코드 분기·드리프트 금지, 95-5).

배치 모드 2종 (기동시 SIDECAIR_MODE... *오타금지* SIDECAIR_MODE 없음 — SIDECAIR_MODE가 아닌
      SIDECAR_MODE로 지정 — 실측 09-23):
  - mode=watch : 감시+각성 (서버공통판 — 2번 지시. relay98류 1봇전담판과 병존)
  - mode=relay : 1봇 전담 durable consume (66번판 — nats-py 필요, 미설치시 10초 폴링 폴백)
  지시 3번은 watch 모드 정본화만 (relay는 66번본 comm-relay-98.py가 원본 — 병존 유지).

완료기준(2번, 여기서 확정): 감시대상 6봇 소진(pending=0) + 무음각성 실측로그. 메모리 <30MB.
금지: 98(relay98) 중복각성 · relay98 소스 파괴적 수정 · 그림7종 · 타노드 확산 · 화면격상 ·
      cokacdir 소스수정 · 토큰값 본문/커밋 노출(경로만).

설치: 같은 폴더 INSTALL-sidecar.md (AWS·GMLNX: systemd --user / 윈도: NSSM)
"""

import json
import os
import subprocess
import time
import urllib.request
from datetime import datetime, timezone

# ---- sidecar.env (필수 5필드 — 예시는 INSTALL-sidecar.md §2) ----
def load_env():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, "sidecar.env"),
                 os.path.expanduser("~/.config/comm-sidecar/sidecar.env")):
        if os.path.exists(cand):
            with open(cand) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
            break
    # 필수값 검증 — 기본값 없음(하드코딩 재발 방지)
    need = ["SIDECAR_BOT", "SIDECAR_CHAT", "SIDECAR_KEYDIR", "SIDECAR_EXCLUDE", "SIDECAR_BASE"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"sidecar.env 필수필드 누락: {missing} — INSTALL-sidecar.md §2 참조")

load_env()

BOT = os.environ["SIDECAR_BOT"]                 # 이 사이드카의 대표 봇(로그·watch 모드 감시 주체)
CHAT = os.environ["SIDECAR_CHAT"]               # 각성 발화 채팅 (이사님 채팅 1곳)
KEYDIR = os.environ["SIDECAR_KEYDIR"]           # 각성키 디렉토리 (파일내용=16자 키ID)
EXCLUDE = {x.strip() for x in os.environ["SIDECAR_EXCLUDE"].split(",") if x.strip()}
BASE = os.environ["SIDECAR_BASE"]               # 8024 endpoint (예: http://43.201.34.144:8024)
SITE_FILTER = os.environ.get("SIDECAR_SITE", "awslnx")          # 감시대상 사이트 필터(roster)
ROSTER = os.environ.get("SIDECAR_ROSTER",
                        os.path.expanduser("~/notes/projects/agent-ops/roster.json"))
MODE = os.environ.get("SIDECAR_MODE", "watch")  # watch | relay
SYNC_EVERY = int(os.environ.get("SIDECAR_SYNC_EVERY", "60"))
WATCH_EVERY = int(os.environ.get("SIDECAR_WATCH_EVERY", "60"))
WAKE_GAP = int(os.environ.get("SIDECAR_WAKE_GAP", "30"))
COOLDOWN = int(os.environ.get("SIDECAR_COOLDOWN", "3600"))
LOGFILE = os.environ.get("SIDECAR_LOG", os.path.expanduser(
    "~/.local/state/comm-relay-" + ("awslnx" if MODE == "watch" else BOT) + ".log"))
STATE = os.environ.get("SIDECAR_STATE", os.path.expanduser(
    "~/.local/state/comm-relay-" + ("awslnx" if MODE == "watch" else BOT) + ".json"))
COKACDIR = os.environ.get("SIDECAR_COKACDIR", "/usr/local/bin/cokacdir")
# N3 (PIPE#60, 2026-10-01): 메시지 TTL·각성 지수백오프 — 미ACK 공지 영구루프·스킴 스팸 방지
MSG_TTL_H = int(os.environ.get("SIDECAR_MSG_TTL_H", "72"))     # 미ACK 만료 폐기 시간
BACKOFF_MAX = int(os.environ.get("SIDECAR_BACKOFF_MAX", "8"))  # 백오프 상한 (COOLDOWN의 배수)


def log(msg):
    line = f"{datetime.now(timezone.utc).strftime('%H:%M:%S')} relay[{BOT}/{MODE}]: {msg}"
    print(line, flush=True)
    try:
        os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
        with open(LOGFILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def http_json(url, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw.strip() else {}


def roster_wake_map():
    """username → roster wake:false 여부 (N3-d: 키 없는 봇 감시 제외 표기)."""
    try:
        with open(ROSTER) as f:
            return {b.get("username", ""): bool(b.get("wake", True))
                    for b in json.load(f)["bots"]}
    except Exception:
        return {}


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(st, f)


def sync_targets():
    """roster.json → 감시대상 (site 필터·active, EXCLUDE 제외). 신규봇 자동편입·제거 자동반영."""
    targets = []
    try:
        with open(ROSTER) as f:
            bots = json.load(f)["bots"]
        for b in bots:
            if b.get("site") == SITE_FILTER and b.get("status") == "active":
                u = b.get("username", "").strip()
                if u and u not in EXCLUDE:
                    targets.append(u)
    except Exception as e:
        log(f"roster 판독 실패 — 이전 대상 유지: {e}")
    return targets


def keyfile_of(username):
    """username → 각성키 파일. 경유: bot_settings.json(키ID) → 키 디렉토리 파일내용 역탐색.
    (파일명 규칙 비일관 — 내용 매칭이 유일 신뢰. 실측 09-23. 토큰값 노출 없음 — 경로만 반환)"""
    try:
        with open(os.path.expanduser(
                os.environ.get("SIDECAR_SETTINGS", "~/.cokacdir/bot_settings.json"))) as f:
            settings = json.load(f)
        kid = next((k for k, v in settings.items() if v.get("username") == username), None)
        if not kid:
            return None
        for fn in os.listdir(KEYDIR):
            try:
                if open(os.path.join(KEYDIR, fn)).read().strip() == kid:
                    return os.path.join(KEYDIR, fn)
            except Exception:
                continue
    except Exception as e:
        log(f"키ID 역산 실패({username}): {e}")
    return None


def pending_count(bot):
    try:
        w = http_json(f"{BASE}/api/nats/whoami?bot={bot}")
        return len(w.get("pending", [])) + len(w.get("deliveredNotAcked", []))
    except Exception as e:
        log(f"whoami 실패({bot}): {e}")
        return -1    # 네트워크 오류 — 각성 판정 보류(오탐 방지)


def wake(bot, keyfile, pend):
    """각성 — 봇 자기키로 발화 1회. 쿨다운 1시간 + 실패마다 지수백오프(최대 BACKOFF_MAX배, N3-a).
    스킵 로그는 상태 변화시 1회만 (N3: 주기 반복 스팸 금지).
    cokacdir 응답(status ok)이 각성성공 판정 — 실측: --at은 1m/30m(초단위 미지원, 09-23)."""
    st = load_state()
    now = time.time()
    fails = st.get(bot, {}).get("fails", 0)
    cd = min(COOLDOWN * (2 ** fails), COOLDOWN * BACKOFF_MAX)
    if now - st.get(bot, {}).get("waked_at", 0) < cd:
        if st.get(bot, {}).get("last_note") != "cooldown":
            st[bot] = {**st.get(bot, {}), "last_note": "cooldown"}
            save_state(st)
            log(f"각성 대기({bot}) — 백오프 {int(cd // 60)}분 (연속실패 {fails})")
        return False
    prompt = (f"[relay 자동각성] {bot} — comm 사서함 미수신 {pend}건. "
              f"지금 즉시: whoami→inbox→7필드준용ACK (사칭 principles/telegram-comm-protocol-v1.md §3.5·L0). "
              f"이 메시지 확인 후 본업 복귀.")
    try:
        r = subprocess.run(
            [COKACDIR, "--cron", prompt, "--at", "1m", "--chat", CHAT,
             "--key-file", keyfile, "--once"],
            capture_output=True, timeout=60, text=True)
        ok = '"status":"ok"' in (r.stdout or "") or '"status": "ok"' in (r.stdout or "")
        if ok:
            st[bot] = {"waked_at": now, "pend": pend, "fails": 0, "last_note": "ok"}
            save_state(st)
            log(f"각성 성공: {bot} (미수신 {pend}건, key={os.path.basename(keyfile)[:16]}…)")
            return True
        # 개정1 (부록A1/PIPE#60): 1차(--cron) 실패 시 2차 경로 — cokacdir --prompt 직접 호출(큐 적체 무관, 즉시 동기실행)
        try:
            r2 = subprocess.run([COKACDIR, "--prompt", prompt, "--key-file", keyfile],
                                capture_output=True, timeout=300, text=True)
            if r2.stdout and r2.stdout.strip():
                st[bot] = {"waked_at": now, "pend": pend, "fails": 0, "last_note": "ok2"}
                save_state(st)
                log(f"각성 성공(2차 --prompt): {bot} (미수신 {pend}건)")
                return True
            log(f"각성 2차 실패({bot}): {(r2.stdout or '')[:80]} {(r2.stderr or '')[:80]}")
        except Exception as e2:
            log(f"각성 2차 예외({bot}): {e2}")
        # 3단(텔레그램 경보): 1·2차 모두 실패 — 사이드카 무음 원칙 유지 위해 8024로 1회 경보(쿨다운은 같은 백오프 주기)
        try:
            http_json(f"{BASE}/api/nats/send", "POST",
                      {"from": BOT, "to": "heav_lnx_bot", "type": "task", "ref": "wake-fail",
                       "text": f"[각성 경보] {bot} 1·2차 경로 모두 실패 — 미수신 {pend}건. 사이드카({BOT}) 수동 점검 필요."})
            log(f"각성 경보 발행({bot}) — 매니저 notice")
        except Exception as e3:
            log(f"경보 발송 실패({bot}): {e3}")
        st[bot] = {**st.get(bot, {}), "fails": fails + 1, "last_note": "fail"}
        save_state(st)
        log(f"각성 실패({bot}, 백오프 x{2 ** (fails + 1)}): {(r.stdout or '')[:120]} {(r.stderr or '')[:120]}")
        return False
    except Exception as e:
        # 1차 경로 예외(cokacdir 미존재·timeout 등)도 2차로 폴백 — 이중화 사각지대 제거(부록A1)
        log(f"각성 1차 예외({bot}) → 2차 폴백: {e}")
        try:
            r2 = subprocess.run([COKACDIR, "--prompt", prompt, "--key-file", keyfile],
                                capture_output=True, timeout=300, text=True)
            if r2.stdout and r2.stdout.strip():
                st[bot] = {"waked_at": now, "pend": pend, "fails": 0, "last_note": "ok2"}
                save_state(st)
                log(f"각성 성공(2차 --prompt, 1차예외 폴백): {bot} (미수신 {pend}건)")
                return True
        except Exception as e2b:
            log(f"각성 2차 폴백 예외({bot}): {e2b}")
        return False


def mem_mb():
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) / 1024
    except Exception:
        pass
    return 0


def run_watch():
    """watch 모드 — 서버공통판 감시+각성 (2번 지시 본체)."""
    log("기동 — watch 모드 (감시: roster site=" + SITE_FILTER + "·active, 제외:" + ",".join(EXCLUDE) + ")")
    targets, tick = [], 0
    while True:
        if tick % SYNC_EVERY == 0 or not targets:          # 지시 1번: 하드코딩→동기화
            new_t = sync_targets()
            if new_t:
                added = set(new_t) - set(targets)
                if targets and added:
                    log(f"신규봇 자동편입: {added}")
                targets = new_t
        tick += 1

        debt = {}                                           # 무음감시 — 정상시 로그 0
        wake_map = roster_wake_map()                        # N3-d: wake:false 표기봇
        st = load_state()
        for bot in targets:
            if wake_map.get(bot) is False:
                continue                                    # roster wake:false — 각성 대상 외 (N3-d)
            n = pending_count(bot)
            if n > 0:
                # N3-b: 미ACK 만료(TTL) 메시지 폐기 — 영구 재시도 루프 차단
                try:
                    rows = http_json(f"{BASE}/api/nats/messages?to={bot}&limit=200")
                    fresh = 0
                    import datetime as _dt
                    for m in rows:
                        if str(m.get("ts", "")) < "2000": continue
                        try:
                            age_h = (_dt.datetime.now(_dt.timezone.utc)
                                     - _dt.datetime.fromisoformat(str(m["ts"]).replace("Z", "+00:00"))
                                     ).total_seconds() / 3600
                        except Exception:
                            fresh += 1; continue
                        if age_h > MSG_TTL_H and not m.get("ackedAt"):
                            http_json(f"{BASE}/api/nats/ack", "POST",
                                      {"from": bot, "msg_id": m["id"],
                                       "note": f"만료 폐기 (TTL {MSG_TTL_H}h, N3-b/PIPE#60) — 재시도 루프 차단"})
                            log(f"TTL 만료 폐기: {m['id']} → {bot} ({int(age_h)}h경과)")
                        else:
                            fresh += 1
                    n = fresh
                except Exception:
                    pass                                    # 폐기 실패 시 기존 카운트 유지
            if n > 0:
                debt[bot] = n
            time.sleep(0.3)                                 # 8024 부하 최소화

        st = load_state()
        for bot, n in debt.items():                         # 1회 1봇 순차 (지시 3번)
            kf = keyfile_of(bot)
            if not kf:
                if st.get(bot, {}).get("last_note") != "nokey":
                    st[bot] = {**st.get(bot, {}), "last_note": "nokey"}
                    save_state(st)
                    log(f"키 파일 미발견 — 각성 불가: {bot} (roster wake:false 권장 — 이후 침묵)")
                continue
            wake(bot, kf, n)
            time.sleep(WAKE_GAP)

        if debt:
            tot = st.get("_stats", {"wake_ok": 0, "wake_try": 0})
            rate = (100 * tot["wake_ok"] // tot["wake_try"]) if tot.get("wake_try") else -1
            log(f"주기종료 — 미수신 {sum(debt.values())}건 / {len(debt)}봇 · 각성성공률 {rate}% ({tot['wake_ok']}/{tot['wake_try']}) (mem={mem_mb():.1f}MB)")
        time.sleep(WATCH_EVERY)


def run_relay():
    """relay 모드 — 1봇 전담 (66번판 정신: 기동시 전량회수+durable, 미설치시 10초 폴백)."""
    log("기동 — relay 모드 (1봇 전담: " + BOT + ")")
    import nats
    import nats.js.api as jsapi
    import asyncio

    def drain_inbox(note_base="relay 기동회수"):
        try:
            pend = http_json(f"{BASE}/api/nats/inbox?bot={BOT}")
            for m in (pend if isinstance(pend, list) else []):
                try:
                    http_json(f"{BASE}/api/nats/ack", "POST",
                              {"from": BOT, "msg_id": m.get("id", ""),
                               "note": f"actor_id:{BOT}|맡은일:{note_base}|정본ref:comm/comm-relay-common.py|acknowledged"})
                except Exception as e:
                    if "404" not in str(e):
                        log(f"drain ACK 실패: {e}")
        except Exception as e:
            log(f"drain 실패: {e}")

    drain_inbox()
    if not _nats_ok():
        log("nats-py 미설치 — 10초 폴링 폴백 (66번판 실측: 완료기준 10초내수신 충족)")
        while True:
            drain_inbox("relay 폴백수신")
            time.sleep(10)

    async def main():
        while True:
            try:
                nc = await nats.connect(servers=[os.environ.get("SIDECAR_NATS", "nats://127.0.0.1:4222")],
                                        connect_timeout=10, name=f"relay-{BOT[:20]}")
                jsm, js = nc.jsm(), nc.jetstream()
                await jsm.stream_info("BOTLOG")
                sub = await js.pull_subscribe(
                    f"bot.msg.*.{BOT}", durable=f"relay-{BOT}",
                    config=jsapi.ConsumerConfig(durable_name=f"relay-{BOT}",
                                                deliver_policy=jsapi.DeliverPolicy.ALL,
                                                ack_wait=30, max_deliver=-1,
                                                filter_subject=f"bot.msg.*.{BOT}"))
                log("durable 구독 완료")

                async def consume():
                    while True:
                        try:
                            msgs = await sub.fetch(batch=10, timeout=5)
                            for m in msgs:
                                try:
                                    p = json.loads(m.data.decode())
                                except Exception:
                                    p = {}
                                note = (f"actor_id:{BOT}|맡은일:relay 수령|"
                                        f"정본ref:comm/comm-relay-common.py|acknowledged")
                                try:
                                    http_json(f"{BASE}/api/nats/ack", "POST",
                                              {"from": BOT, "msg_id": p.get("id", ""), "note": note})
                                except Exception as e:
                                    if "404" not in str(e):
                                        log(f"ACK 실패: {e}")
                                log(f"수령: {p.get('id')} {p.get('subject','')}")
                                await m.ack()
                        except Exception:
                            await asyncio.sleep(0.5)

                async def inbox_drain():                 # 듀얼채널 — 배달장부 정리(66번판 실측 09-23)
                    while True:
                        await asyncio.sleep(30)
                        await asyncio.get_event_loop().run_in_executor(None, drain_inbox, "relay inbox정리")

                tasks = [asyncio.ensure_future(consume()),
                         asyncio.ensure_future(inbox_drain())]
                await asyncio.gather(*tasks)
            except Exception as e:
                log(f"연결 끊김 — 15초 backoff 후 재개 (95-1): {e}")
                await asyncio.sleep(15)

    asyncio.run(main())


def _nats_ok():
    try:
        import nats  # noqa
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    try:
        run_watch() if MODE == "watch" else run_relay()
    except KeyboardInterrupt:
        log("종료")
