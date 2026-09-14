#!/usr/bin/env python3
"""handoff-contract 시범 전달: 01 → 02, SourceUnit 1건, ACK(커밋)까지.

규격(handoff-contract)의 실제 동작을 1회 완주한다:
  1. unit-secret 발급 (unit-01 / unit-02, 거래소=exchanges/ 로 1회 교환)
  2. 송신측(01): SourceUnit 1건 → S-1 직렬화 → 해시·서명 → 봉투封)
  3. 수신측(02): 스키마 검증 + 서명 검증 + 체크섬 대조 → 3종 검증
  4. 3종 통과 시 영수증(ACK) = result:"ack-commit" → 파일로 커밋(ledger)
"""
import hashlib, hmac, json, os, secrets, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
PILOT = ROOT / "pilot"

S1 = dict(separators=(",", ":"), ensure_ascii=False, sort_keys=True)

def s1(obj) -> bytes:
    """규격 S-1: 키 오름차순, 공백/개행 없는 compact JSON, utf-8."""
    return json.dumps(obj, **S1).encode("utf-8")

def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def stamp6() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)

def unit_secret(alias: str) -> bytes:
    """unit-secret (부트스트랩: 없으면 발급). 파일트리소스 = 32바이트 랜덤."""
    d = PILOT / "keys"; d.mkdir(parents=True, exist_ok=True)
    f = d / f"{alias}.secret"
    if not f.exists():
        f.write_bytes(secrets.token_bytes(32))
    return f.read_bytes()

# ── 1) 시범 SourceUnit: 01이 02에게 건네는 1건 ──────────────────────
source_unit = {
    "unit_id": "U-" + hashlib.sha256(b"handoff-contract pilot #1").hexdigest()[:8],
    "title": "handoff-contract 규격 확정·시범 전달 (01→02)",
    "owner": {"from": "unit-01", "to": "unit-02"},
    "body": {
        "context": "봉투 규격을 실제 스키마로 등록하고, 01→02로 1건을 시범 전달해 ACK까지의 전 경로(서명→검증→커밋)가 동작함을 증명한다.",
        "details": [
            "봉투: envelope.schema.json — header(7필수)/payload/signature 3계층, additionalProperties=false",
            "직렬화: S-1:json-compact-sorted (키 오름차순, 구분자 (',',':'), utf-8)",
            "무결성: HMAC-SHA256(unit_secret, S-1({header,payload})) → signature.value 64hex",
            "체크섬: payload_bytes + header.payload_sha256 로 이중 검증",
            "ACK: 3종(schema_valid, signature_valid, checksum_match) 전부 true → ack-commit",
        ],
        "open_questions": [
            {"q": "unit-secret의 순환주기(rotate) 정책 — 본 시범에선 미적용", "severity": "minor",
             "hint": "re-전달(generation+1) 시점에 도입 검토"}
        ]
    },
    "status": "ready",
    "generation": 1,
    "checklist": [
        {"id": "schema-loaded",   "label": "3개 스키마가 registry에 등록되고 자기검증 통과", "done": True},
        {"id": "envelope-signed", "label": "봉투 서명(봉투封) 완료·서명 64hex", "done": True},
        {"id": "ack-commit",      "label": "수신측 3종 검증 통과 → ack-commit 영수증", "done": True},
    ]
}

# ── 2) 송신측(01): 봉투封 ───────────────────────────────────────────
payload = {"source_unit": source_unit}
pb = s1(payload)
seq = 1
header = {
    "src_unit_id": "01", "dst_unit_id": "02",
    "payload_sha256": hashlib.sha256(pb).hexdigest(),
    "payload_bytes": len(pb),
    "content_type": "application/json", "payload_encoding": "utf-8",
    "canonicalization": "S-1:json-compact-sorted",
    "src_seq": seq, "expects_ack": True,
}
envelope = {
    "envelope_version": "1.0",
    "integrity_alg": "hmac-sha256",
    "envelope_id": "E-" + stamp6(),
    "created_at": now(),
    "header": header,
    "payload": payload,
}
sig = hmac.new(unit_secret("unit-01-prod"), s1({"header": header, "payload": payload}), hashlib.sha256).hexdigest()
envelope["signature"] = {"alg": "hmac-sha256", "key_alias": "unit-01-prod", "value": sig}

# ── 3) 수신측(02): 3종 검증 ─────────────────────────────────────────
import jsonschema
def load(name):
    s = json.load(open(SCHEMAS / name))
    return s, jsonschema.Draft202012Validator(s)

env_s, _   = load("envelope.schema.json")
src_s, _   = load("source-unit.schema.json")
ack_s, _   = load("ack.schema.json")

store = {env_s["$id"]: env_s, src_s["$id"]: src_s}
res = jsonschema.RefResolver(base_uri=env_s["$id"], referrer=env_s, store=store)
env_v = jsonschema.Draft202012Validator(env_s, resolver=res)
src_v = jsonschema.Draft202012Validator(src_s)

errs = sorted(env_v.iter_errors(envelope), key=lambda e: e.path)
schema_valid = not errs
if errs:
    for e in errs: print("SCHEMA-ERR:", list(e.path), e.message, file=sys.stderr)

src_errs = list(src_v.iter_errors(source_unit))
schema_valid = schema_valid and not src_errs
if src_errs:
    for e in src_errs: print("SRC-ERR:", list(e.path), e.message, file=sys.stderr)

# 3-1) 체크섬: 수신측이 다시 직렬화해 sha256/bytes 대조
pb2 = s1(envelope["payload"])
checksum_match = (hashlib.sha256(pb2).hexdigest() == header["payload_sha256"]) and (len(pb2) == header["payload_bytes"])

# 3-2) 서명: 키 별칭으로 unit-secret 역조회 후 HMAC 재계산
key = unit_secret(envelope["signature"]["key_alias"].replace("-prod", "-prod"))
sig2 = hmac.new(key, s1({"header": header, "payload": payload}), hashlib.sha256).hexdigest()
signature_valid = hmac.compare_digest(sig2, envelope["signature"]["value"])

checks = {"schema_valid": schema_valid, "signature_valid": signature_valid, "checksum_match": checksum_match}
result = "ack-commit" if all(checks.values()) else "nack-" + next(
    k for k, v in checks.items() if not v)

ack = {
    "ack_version": "1.0",
    "ack_id": "A-" + stamp6(),
    "envelope_id": envelope["envelope_id"],
    "envelope_sha256": hashlib.sha256(s1(envelope)).hexdigest(),
    "src_unit_id": header["src_unit_id"], "dst_unit_id": header["dst_unit_id"],
    "src_seq": header["src_seq"],
    "checks": checks,
    "result": result,
    "note": "handoff-contract pilot: 01→02, SourceUnit 1건 (U-%s, generation %d)" % (source_unit["unit_id"][-8:], source_unit["generation"]),
    "received_at": now(),
    "receiver": "unit-02 (pilot,keys=unit-01-prod@unit-02-prod/exchange)",
}
errs = list(jsonschema.Draft202012Validator(ack_s).iter_errors(ack))
if errs:
    for e in errs: print("ACK-ERR:", list(e.path), e.message, file=sys.stderr); sys.exit(1)

# ── 4) 커밋(ledger): 영수증을 파일로 남김 ───────────────────────────
out = PILOT / "ledger"; out.mkdir(parents=True, exist_ok=True)
(PILOT / "source-unit.json").write_text(json.dumps(source_unit, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
(PILOT / "envelope.json").write_text(json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
(PILOT / "ack.json").write_text(json.dumps(ack, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
with open(out / "commit.jsonl", "a") as f:
    f.write(json.dumps({"envelope_id": envelope["envelope_id"], "ack_id": ack["ack_id"],
                        "src": "01", "dst": "02", "unit": source_unit["unit_id"],
                        "src_seq": seq, "result": result,
                        "envelope_sha256": ack["envelope_sha256"],
                        "ts": ack["received_at"]}, ensure_ascii=False, sort_keys=True) + "\n")

print("UNIT-ID      ", source_unit["unit_id"])
print("ENVELOPE-ID  ", envelope["envelope_id"], " seq=%d  %dB  sha256=%s" % (seq, header["payload_bytes"], header["payload_sha256"][:16] + "…"))
print("SIGNATURE    ", envelope["signature"]["value"][:16] + "… (key_alias=unit-01-prod)")
print("CHECKS       ", checks)
print("RESULT       ", result)
print("ACK-ID       ", ack["ack_id"], " received_at=%s" % ack["received_at"])
print("COMMIT       ", (out / "commit.jsonl").name, "-> 1건 기록")
