#!/usr/bin/env bash
# RELAY-57 3단계 — 원클릭 서버 부트스트랩 (DR 복구·신규 서버 세팅)
# 사용: bash bootstrap_server.sh [phase]
#   phase: deps(기본의존성) | code(git clone/pull) | data(백업·COLD 수신) | services(기동) | all
# 전제: 우분투 24.04, rclone 설정(~/.config/rclone/rclone.conf)과 git 자격증명은 별도 복사 필요
set -euo pipefail
PHASE=${1:-all}
HOME_DIR=/home/ubuntu

log() { echo "[$(date +%H:%M:%S)] $*"; }

repos="notes matrix_asset_agent scenario matrix-home matrix_zcode matrix-candidate matrix-engine"

phase_deps() {
  log "의존성 설치"
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3 python3-venv python3-pip git curl nodejs npm jq sqlite3 > /dev/null
  python3 -m pip install --quiet --user pymongo flask flask-cors
  # rclone
  if ! command -v rclone >/dev/null; then curl -s https://rclone.org/install.sh | sudo bash; fi
  log "의존성 완료"
}

phase_code() {
  log "repo 확보 (clone or pull)"
  mkdir -p $HOME_DIR/projects
  cd $HOME_DIR/projects
  for r in matrix_asset_agent scenario matrix-home; do
    if [ -d "$r/.git" ]; then git -C "$r" pull --rebase -q || log "pull 실패: $r (수동 확인)";
    else git clone -q "https://github.com/markjang29/$r.git" || log "clone 실패: $r"; fi
  done
  cd $HOME_DIR
  for r in notes matrix_zcode matrix-candidate matrix-engine; do
    if [ -d "$r/.git" ]; then git -C "$r" pull --rebase -q || true; fi
  done
  log "코드 완료"
}

phase_data() {
  log "백업 수신 — mongo 스냅샷 최신본"
  mkdir -p /tmp/restore
  LATEST=$(rclone lsf "matrix-upload:백업/workbench-mongo/" | sort | tail -1)
  rclone copyto "matrix-upload:백업/workbench-mongo/$LATEST" "/tmp/restore/$LATEST"
  tar -xzf "/tmp/restore/$LATEST" -C /tmp/restore
  python3 - <<'EOF'
import sys, json, gzip, glob
import pymongo
db = pymongo.MongoClient("mongodb://127.0.0.1:27017")["workbench"]
for f in glob.glob("/tmp/restore/mongo_backup_*/[a-z]*.json.gz"):
    coll = f.split("/")[-1].replace(".json.gz", "")
    docs = json.load(gzip.open(f, "rt", encoding="utf-8"))
    if docs:
        db[coll].delete_many({})
        db[coll].insert_many(docs)
        print(f"{coll}: {len(docs)}건 복원")
EOF
  log "COLD 원본 수신(선택 — 4G+) 주석 해제 시 실행"
  # rclone copy "matrix-upload:백업/COLD-arcalive" "$HOME_DIR/Works/arcalive" --transfers 4
}

phase_services() {
  log "서비스 기동 (8015/8016/8018 + mongo 자동설치는 생략 — systemd 유닛 생성)"
  sudo tee /etc/systemd/system/matrix-sites.service >/dev/null <<UNIT
[Unit]
Description=Matrix sites (workbench 8015, studio 8016, home 8018)
After=network.target
[Service]
Type=simple
User=ubuntu
Environment=RELAY_TICKET=RELAY-57
ExecStart=/bin/bash -c 'cd $HOME_DIR/projects/matrix_asset_agent && python3 tools/workbench_web.py & cd $HOME_DIR/projects/matrix-home && $HOME_DIR/.venvs/novelweb/bin/python main.py & cd $HOME_DIR/projects/scenario/novel_assets/images/app && $HOME_DIR/.venvs/novelweb/bin/python main.py & wait'
Restart=on-failure
[Install]
WantedBy=multi-user.target
UNIT
  python3 -m venv $HOME_DIR/.venvs/novelweb 2>/dev/null || true
  $HOME_DIR/.venvs/novelweb/bin/pip install --quiet flask markdown
  sudo systemctl daemon-reload
  sudo systemctl enable --now matrix-sites
  sleep 2
  for p in 8015 8016 8018; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://127.0.0.1:$p/" || echo 000)
    log "port $p: $code"
  done
}

case $PHASE in
  deps) phase_deps ;;
  code) phase_code ;;
  data) phase_data ;;
  services) phase_services ;;
  all) phase_deps; phase_code; phase_data; phase_services; log "부트스트랩 완료" ;;
  *) echo "usage: $0 [deps|code|data|services|all]"; exit 1 ;;
esac
