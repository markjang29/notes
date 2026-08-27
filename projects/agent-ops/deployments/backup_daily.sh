#!/usr/bin/env bash
# RELAY-57 1단계 — mongoDB → gdrive 일일 백업 (mongodump 없이 JSON 스냅샷)
# 산출: matrix-upload:백업/workbench-mongo/workbench-YYYYMMDD.tar.gz (30일 보관)
set -euo pipefail
TS=$(date +%Y%m%d)
DEST_DIR=/tmp/mongo_backup_$TS
GDRIVE="matrix-upload:백업/workbench-mongo"
mkdir -p "$DEST_DIR"
python3 - "$DEST_DIR" <<'EOF'
import sys, json, gzip, datetime
import pymongo
out = sys.argv[1]
db = pymongo.MongoClient("mongodb://127.0.0.1:27017")["workbench"]
for coll in db.list_collection_names():
    docs = []
    for d in db[coll].find():
        d.pop("_id", None)
        for k, v in list(d.items()):
            if isinstance(v, datetime.datetime):
                d[k] = v.isoformat()
        docs.append(d)
    with gzip.open(f"{out}/{coll}.json.gz", "wt", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, default=str)
    print(f"{coll}: {len(docs)}건")
EOF
tar -czf "/tmp/workbench-$TS.tar.gz" -C /tmp "mongo_backup_$TS"
rclone copyto "/tmp/workbench-$TS.tar.gz" "$GDRIVE/workbench-$TS.tar.gz" --transfers 2
# 30일 넘은 백업 정리
rclone delete "$GDRIVE" --min-age 30d 2>/dev/null || true
rm -rf "$DEST_DIR" "/tmp/workbench-$TS.tar.gz"
echo "백업 완료: $GDRIVE/workbench-$TS.tar.gz"
