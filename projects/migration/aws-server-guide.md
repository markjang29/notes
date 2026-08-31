---
title: AWS 서버 실체 안내서 (server-guide)
date: 2026-08-30
status: v1 — 실측 기반 최초 작성
verified_at: 2026-08-30 21:53 KST
author: aws-manager (이사님 08-30 지시, work-queue 마이그레이션 트랙)
tags:
  - ops
  - migration
  - server
---

# AWS 서버 실체 안내서

> 백지 상태의 봇(N100 파이어뱃 등)이 이 문서 하나로 서버 전모를 파악하게 하기 위한 통합 안내서.
> 마이그레이션 Phase 2(터널)·3(서비스 이전)의 기준 자료. 계획 정본은 같은 폴더
> `local-server-migration-plan.md`.

## 0. 이 문서의 규칙

- 모든 사실은 **2026-08-30 21:53 KST 실측**이다. 서버는 살아 있는 시스템이므로 사용 전 §11 재검증 명령으로 현황을 다시 확인한다.
- **보안**: 키·토큰·비밀 값은 절대 이 문서에 기록하지 않는다. 위치(경로)만 기록한다(§10).
- 포트 운행 권한(RELAY 티켓)의 정본은 `projects/agent-ops/relay/port-registry.json`이다. 이 문서의 표는 투영본이다.
- 봇 정체·역할의 정본은 `projects/agent-ops/actors.json`(부팅 규칙은 각 봇 시스템 프롬프트의 "Agent Mail boot v2").

## 1. 서버 기본

- AWS EC2, 리전 `ap-northeast-2`(서울), Ubuntu 24.04, 타임존 **KST**
- 기본 사용자 `ubuntu` (passwordless sudo)
- 디스크 `/` **154G 중 134G 사용(87%) — 여유 부족 주의**
  - 대형 순위: `~/Works/arcalive` 87G(아카 수집 원본) · Docker(이미지 9G+볼륨 5.3G) · `~/Works/novel` 5.7G · `~/risu` 2.8G · `~/matrix-candidate` 1.5G · `~/projects` 1.1G · `~/matrix_codex` 845M
- 네트워크 접근: SSH 22, 그리고 아래 Tailscale.

## 2. 인프라 계층

- `ssh` / `cron` / `chrony`(NTP) / `docker`+`containerd` / `amazon-ssm-agent`(snap) — 표준
- **Tailscale**(테일넷 `heaveniris@`, 이 서버 `ip-172-26-2-127` = `100.81.50.115`)
  - `https://ip-172-26-2-127.tail1cf879.ts.net` → 127.0.0.1:8006 (tailnet 전용)
  - `https://ip-172-26-2-127.tail1cf879.ts.net:8443` → **Funnel(외부 공개)**: `/`→8008(matrix-candidate), `/rpg-game`→8009
  - 마이그레이션 Phase 2(터널) 설계 시 이미 운용 중인 이 라우팅이 참고점이 된다.

## 3. 서비스 × 포트 지도 (2026-08-30 실측)

「기동」열: **sys**=시스템 유닛, **usr**=사용자 유닛(`systemctl --user`, linger=on으로 재부팅 시 자동 기동), **docker**, **cron**, **nohup**=유닛 없는 수동 기동.

| 포트 | 서비스 | 기동 | 코드/작업 경로 | RELAY | 비고 |
|---|---|---|---|---|---|
| 22 | sshd | sys | — | — | SSH |
| 1521 | oracle-free (Oracle 23ai Free) | docker | 이미지 `gvenzl/oracle-free:23-faststart` | — | autotrader DB. **0.0.0.0 노출**. 데이터 = docker volume `oracle-data` |
| 27017 | matrix-workbench-mongo (mongo:7) | docker | — | — | **127.0.0.1만**. 데이터 = `~/matrix-candidate/workbench-mongo`(bind) |
| 8003 | scenario-generator v5 | sys | `~/projects/scenario/tools/scenario-generator/backend` (uvicorn `app:app`, venv `~/.venvs/autotrader`) | RELAY-43 | |
| 8004 | Arcade PLAYABLE | usr | `~/projects/matrix_asset_agent` (`tools/arcade_playable_server.py`, env `~/.config/arcade-playable.env`) | RELAY-44 | |
| 8005 | 승인보드 approval-board | sys | `~/projects/approval-board` (uvicorn `main:app`) | RELAY-18 | 외부 작업요청 창구. 원장 `requests.json`(Git)·클라이언트 토큰 `clients.json`(gitignore) |
| 8006 | scenario 자동수집 설정 automation-settings | sys | 실행파일은 `~/projects/scenario/...`이나 **실행 cwd = `~/releases/scenario/current/tools/scenario-generator/backend`**(유닛 override) | RELAY-45 | Tailscale tailnet HTTPS의 실체 |
| 8008 | matrix-candidate | usr | `~/matrix-candidate/app` (`python -m matrix_candidate`, runtime `~/matrix-candidate/runtime`) | RELAY-46 | Funnel 8443 루트 |
| 8009 | RPG GAME 01 플레이어블 | sys | `~/apps/rpg-game-01/current`(→`releases/20260727-215555`) (gunicorn `web.app:app`, venv `.venv`) | RELAY-47 | Funnel 8443 `/rpg-game` |
| 8010 | matrix-web (엔진 웹) | sys | `~/projects/matrix-engine` (`python -m matrix.web`, venv `~/matrix-web-venv`, env `~/matrix-engine-app/.env`) | RELAY-48 | |
| 8011 | matrix-zcode-cli | sys | `~/matrix_zcode` (`service/cli_server.py`, env `~/matrix-engine-app/.env`) | RELAY-12 | |
| 8012 | matrix-codex-cli | usr | `~/matrix_codex/current` (`python -m matrix_codex.web`, DB `~/matrix_codex/runtime/matrix-codex.sqlite3`, 입력 `~/matrix_codex/input-scenario`) | RELAY-17 | |
| 8013 | PocketRisu (자체호스팅 RISU) | sys | `~/risu/PocketRisu-v1.9.0-linux-x64` (내장 node `server/node/server.cjs`) | RELAY-1 | 리수 채팅 프론트 |
| 8015 | matrix-workbench (검증 워크벤치) | usr | `~/projects/matrix_asset_agent` (`tools/workbench_web.py`) | RELAY-58 | |
| 8016 | 소설자산 이미지 스튜디오 | cron @reboot | `~/projects/scenario/novel_assets/images/app` (`main.py`, venv `~/.venvs/novelweb`) | RELAY-35 | 로그 `~/nai_out/studio_server.log` |
| 8017 | rpg asset workbench | **nohup** | `~/projects/rpg_game/tools/asset_workbench` (`app.py`) | RELAY-36 | 유닛 전환 전 프로토타입. **재부팅 시 자동 복귀 안 됨** |
| 8018 | matrix-home 통합 홈 허브 | **nohup** | `~/projects/matrix-home` (`main.py`, venv `~/.venvs/novelweb`) | RELAY-57 | telegram-zcode-bridge 자식 프로세스(§4 주의) |
| 8020 | music-video (일상 페이지) | sys | `~/deploy/music_video` (`server.py`, env `~/.config/music-video/editor.env`) | RELAY-42 | |
| 8021 | matrix-studio | **nohup** | `~/projects/matrix-studio` (uvicorn `api.main:app`) | (미등록) | telegram-zcode-bridge 자식. **port-registry 미등록 상태로 운행 중** — 포트 감사(09:10) 대상 |
| 8022 | matrix-nexus (Loadout Workspace) | docker(예정) | `~/projects/matrix-nexus` | RELAY-58 | **등록만 되고 현재 컨테이너 없음(미구동)** |
| 8023 | 관제 회의방 웹챗 (meeting-room) | nohup uvicorn (08-31 신설) | `~/projects/meeting-room` | — | 이사님↔봇 조직 소통. X-Token 인증, 세션은 `workspaces/<bot>/.session_id` |
| 8788 | zai-proxy (LLM 폴백 프록시) | usr | `~/scripts/zai-fallback-proxy.js` (node, env `~/.cokacdir/devpass.env`) | — | **127.0.0.1만**. 봇 LLM 라우팅의 관문(§9) |

포트 없는 상주 서비스:

| 서비스 | 기동 | 내용 |
|---|---|---|
| cokacdir | usr | 봇 프레임워크 본체. `~/.local/state/cokacdir/run.sh`. 설정 §9 |
| telegram-zcode-bridge | sys | zcode 클라이언트(승계자) 통신 다리. `~/zcode-cli/telegram_zcode_bridge.py`, env `~/zcode-cli/bridge.env`, cwd `~/tg-workspace`. **8018·8021을 자식 프로세스로 실행 중** |
| zai-529-watchdog | usr | `~/scripts/zai-529-watchdog.py` — 529(레이트리밋) 실시간 감시 |

## 4. 기동 방식 체계 (다섯 가지 계층)

같은 서버 안에 기동 방식이 5종 섞여 있다. 서비스를 다룰 때 먼저 §3 표에서 계층을 확인할 것.

1. **시스템 유닛** — `sudo systemctl restart <유닛>`, 로그 `journalctl -u <유닛> -f`
2. **사용자 유닛** — `systemctl --user restart <유닛>`, 로그 `journalctl --user -u <유닛> -f`. `Linger=yes`라 재부팅에도 자동 기동됨
3. **Docker** — `sudo docker ps` / `restart`. 데이터는 볼륨·bind(§6)
4. **cron @reboot / 반복** — `crontab -l`(§8). 8016이 대표 사례
5. **nohup 프로토타입(8017·8018·8021)** — 유닛이 없다. 8018·8021은 `telegram-zcode-bridge.service` cgroup의 자식이라 **브리지 재시작 시 함께 종료될 수 있음**(KillMode 기본 동작; 실측 전에는 확정 아님). 8017은 로그인 셸에서 수동 기동돼 재부팅 시 사라진다.

## 5. repo 지도와 배포 구조

### GitHub 원격 있는 작업 repo (전부 `github.com/markjang29/*`)

`notes`(작업노트·사칙·배당표·본 문서) · `approval-board` · `autotrader` · `matrix` · `matrix-engine` · `matrix-home` · `matrix_asset_agent` · `matrix_codex` · `matrix_zcode` · `rpg_game` · `scenario`

### 로컬 전용 (remote 없음 — **이전 전 push 또는 bundle 필요**)

`~/projects/matrix-nexus` · `~/projects/matrix-studio` · `~/matrix-repo` · `~/scenario-repo` · `~/matrix-candidate/input-matrix` · `~/matrix-candidate/input-scenario`

### 배포 구조(코드 이중화)

- `~/projects/*` = Git 작업본
- `~/releases/*` + `current` 심링크 = 릴리스 사본(approval-board 과거분, scenario `current`→커밋 `bff59f8…`)
- `~/apps/rpg-game-01/{current→releases/…}` = RPG 배포본
- `~/deploy/` = `music_video` 배포본 · `notes-registry`(크론이 쓰는 notes 배포 사본 — `relay_port_audit.py`가 여기서 실행됨) · `backup_daily.sh` · `bootstrap_server.sh`(§7) · `relay-assets`
- git 자격증명: `~/.git-credentials`(PAT — 값 비밀)

## 6. 데이터 저장 위치

| 데이터 | 위치 | 비고 |
|---|---|---|
| MongoDB (워크벤치) | 호스트 `~/matrix-candidate/workbench-mongo` → 컨테이너 `/data/db` | 접속 `sudo docker exec -it matrix-workbench-mongo mongosh` (127.0.0.1:27017) |
| Oracle 23ai | docker volume `oracle-data` (`/var/lib/docker/volumes/…`) | autotrader용. 컨테이너 통해서만 |
| matrix-codex 상태 | `~/matrix_codex/runtime/matrix-codex.sqlite3` (+ `input-scenario`) | SQLite |
| PocketRisu 세이브 | `~/risu/PocketRisu-v1.9.0-linux-x64/save/*.db` | |
| 아카 수집 원본 | `~/Works/arcalive` **87G** | Windows 파이프라인 산물 원본. 이전 최대 볼륨 |
| 소설 코퍼스 | `~/Works/novel` 5.7G | |
| 이미지 산출 | `~/nai_out` (63M) · `~/nai_concepts` | 8016 스튜디오 출력 |
| 챗 로그 | `~/chat_logs` | |
| 워크벤치 장면 | `~/matrix-candidate/workbench-scenes` | |
| 봇 상태 | `~/.cokacdir/`(설정·스케줄 히스토리·devpass) · `~/.claude/`(CLAUDE.md·memory·skills) | |
| zcode 브리지 작업 | `~/tg-workspace` | |

### 백업 체계

- `~/scripts/workbench-backup.sh` — 매일 04:00 → `~/matrix-candidate/backups/workbench-<date>`(웹워크벤치 mongo 캡처 + risu db + scenes)
- `~/deploy/backup_daily.sh` — 매일 05:30(RELAY-57) → mongo를 `/tmp`에 덤프 후 **rclone으로 Google Drive(`matrix-upload:` remote) 복제** + 로컬 백분
- `~/deploy/bootstrap_server.sh` — **원클릭 서버 부트스트랩(RELAY-57)**: `deps | code | data | services | all` 단계. 신규 서버/DR 복구 표준 경로. 전제: rclone 설정(`~/.config/rclone/rclone.conf`)과 git 자격증명은 별도 복사.

## 7. 운영 스크립트 (~/scripts + ~/deploy)

| 스크립트 | 용도 |
|---|---|
| `claude-session-reaper.sh` | 오래된 봇 세션 정리(크론 */30) |
| `chat-log-backup.py` / `chat-backup.py` / `export-chat-backup.py` | 챗 로그 백업·대화 내보내기 |
| `request_router_poll.py` | 승인보드(8005) 인바운드 폴백 폴링(크론 매분) |
| `workbench-backup.sh` | 워크벤치 일일 백업(04:00) |
| `zai-fallback-proxy.js` | LLM 폴백 프록시(8788, 서비스화됨) |
| `zai-529-watchdog.py` | 529 레이트리밋 실시간 감시(서비스화됨) |
| `devpass-coupon.sh` | DevPass 허락제 쿠폰(이사님 지정 단어→X시간). ADR 08-30 |
| `recovery-health-check.sh` / `healthcheck/` | 장애 복구 헬스체크 |
| `concurrency-meter.sh` / `context-meter.sh` / `ctx-evac.sh` | 동시성·컨텍스트 계량/방전 |
| `policy-notify.sh` | 사칙 갱신 시 팀장 공지 |
| `~/deploy/backup_daily.sh` | 일일 전체 백업+rclone(05:30) |
| `~/deploy/bootstrap_server.sh` | 서버 재구축 원클릭 |
| `~/deploy/notes-registry/…/relay_port_audit.py` | 무단 포트 감사(크론 09:10) — 정본은 notes의 `projects/agent-ops/relay/relay_port_audit.py` |

## 8. 크론 현황 (ubuntu crontab — 2026-08-30)

- `*/30` 세션 리퍼 · 매분 `request_router_poll.py` · 매시 :05 챗로그 백업 · 09:10 포트 감사 · 04:00 워크벤치 백업 · 05:30 일일 백업(RELAY-57) · 06:05 `module_watch.py`(RELAY-56) · `*/30` `s0_worker.py`(RELAY-57) · @reboot 8016 이미지 스튜디오(RELAY-35)
- root 크론탬·`/etc/cron.d` 커스텀 항목: **없음**
- cokacdir 스케줄(봇 크론)은 `--cron-list`로 별도 확인(현재 반복 스케줄 0건 — 07-20 전량 제거 후 재등록 안 됨)

## 9. 봇 조직과 LLM 라우팅

- **cokacdir**(사용자 유닛)이 Telegram 봇 10기를 구동: 매니저 `heav_lnx_bot` · rpg · scenario · trader · audit · asset_agent · arcade · novel_col · codex_dev_1/2 (설정 `~/.cokacdir/bot_settings.json` — **봇 토큰 포함, 값 비밀**)
- 세션 워크스페이스 `~/.cokacdir/workspace/*`, 스케줄 기록 `~/.cokacdir/schedule_history/`
- 봇의 LLM 호출은 `127.0.0.1:8788` zai-proxy(GLM, 1M 우선·단문 폴백) 경유. 프록시 잠기면 **전 봇 응답 불능** — 서버 이전 시 프록시를 맨 먼저 올릴 것.
- 정체·권한 배당표: `projects/agent-ops/actors.json` (v8)

## 10. 보안 경계 — 키 위치(값은 절대 기록·커밋 금지)

위치 목록(전부 값 비밀):

- `~/.git-credentials` — GitHub PAT
- `~/.cokacdir/bot_settings.json` — Telegram 봇 토큰 일괄
- `~/.cokacdir/devpass.env` — DevPass 쿠폰 게이트
- `~/matrix-engine-app/.env` — 매트릭스 계열 공통(8010·8011)
- `~/.config/arcade-playable.env` · `~/.config/music-video/editor.env` · `~/zcode-cli/bridge.env`
- `~/projects/approval-board/clients.json` (gitignore)
- `~/.config/rclone/rclone.conf` — 백업 Google Drive 자격증명
- 각 repo 내 `.env`(gitignore됨)

노출면:

- **0.0.0.0 리스닝**: 8003~8021 대부분 + Oracle 1521. 공인 직접 노출 여부는 EC2 보안그룹이 최종 결정 — 이전 설계 시 SG 규칙을 함께 점검할 것
- **Funnel(공개)**: 8443 → 8008·8009
- **localhost 한정**: mongo 27017, zai-proxy 8788
- 포트 운행 권한 표식: 서비스·크론에 `RELAY_TICKET` 환경변수 부여(미부여 시 09:10 감사가 승인보드 카드 발행)

## 11. 재검증 명령 (새 봇 부팅 체크리스트)

```bash
ss -tulpn | grep -w LISTEN                                   # 포트 실측
systemctl list-units --type=service --state=running --no-pager
systemctl --user list-units --type=service --state=running --no-pager
sudo -n docker ps -a --format '{{.Names}} | {{.Status}} | {{.Ports}}'
crontab -l | grep -v '^#'
jq -r '.registered[] | "\(.port) \(.service) \(.ticket)"' ~/notes/projects/agent-ops/relay/port-registry.json
df -h /
```

실측이 이 문서와 다르면 **이 문서가 아니라 실측이 사실**이다. 갱신은 이 파일을 고쳐 commit·push.

## 12. 마이그레이션 관점 메모 (관찰 — 결정 아님)

- **상태 저장 소스**(이전 시 데이터 동기화 필수): mongo(§6) · Oracle · 8012 SQLite · risu save · `~/Works`(93G) · `~/matrix-candidate/runtime` · `~/nai_out` · `~/.cokacdir`·`~/.claude`(봇 상태)
- **재기동 용이**: 대부분의 FastAPI 서비스(코드=Git, 설정=env 파일)
- **로컬 전용 repo 6건**은 이전 전 push/bundle 없으면 소실(§5)
- 터널 후보 검토 시 Tailscale Funnel 이미 운용 중(§2)
- 디스크 87% — `~/Works` 93G가 병목. 이전 설계와 무관하게 정리 안건
- 8017·8018·8021 nohup 계층은 유닛 전환 전까지 재부팅·브리지 재시작에 취약(§4)
- 8022는 등록만 있고 미구동 — Phase 3 전 정상화 또는 철회 판단 필요
