# INSTALL-sidecar.md — 봇 사이드카 설치절차 정본 (매니저 지시 3번, 09-23, id 1790163528578-174)

정본: 같은 폴더 `comm/comm-relay-common.py` (95-5: 이 파일=원본, 각 거점=사본+버전주석)
근거: 2번(id 1790155957785-12)·66번(id 1790146367556-66)·이사님 09-23 승인
금지: 사본 코드 분기(드리프트) — 거점 차이는 sidecar.env로만. 토큰값 노출 금지(경로만).

## 1. 사본 확보 (전 거점 공통)

```bash
cd <거점에맞는디렉토리>          # 예: /home/smlime21/scripts (AWS·GMLNX) 또는 C:\sidecar (윈도)
git -C ~/notes pull              # 원본 갱신
cp ~/notes/projects/agent-ops/comm/comm-relay-common.py .
echo "# 사본복사 09-23 from notes@<커밋해시> — 95-5 사본 규칙" >> comm-relay-common.py
```

## 2. sidecar.env (필수 5필드 — 이 3줄 예시 + 2줄 = 완성)

```bash
SIDECAR_BOT=heav_lnx_codex_dev_1_bot              # 이 사이드카 대표 봇 username
SIDECAR_CHAT=8315615299                           # 각성 발화 채팅 (이사님 채팅 1곳)
SIDECAR_KEYDIR=/home/smlime21/.cokacdir/bot_keys  # 각성키 디렉토리 (파일내용=16자 키ID)
SIDECAR_EXCLUDE=heav_lnx_codex_dev_1_bot          # 중복각성 제외(쉼표목록) — 98은 relay98 전담
SIDECAR_BASE=http://43.201.34.144:8024            # 8024 endpoint (IP·포트만, 토큰값 아님)
# 선택:
SIDECAR_SITE=awslnx                               # 감시대상 사이트 필터 (기본 awslnx)
SIDECAR_MODE=watch                                # watch(감시+각성) | relay(1봇전담, 66번판)
```

- 권한: `chmod 600 sidecar.env` (토큰값은 안에 없지만 — 경로만, §6 L0 준수)

## 3. 모드별 기동

### 3-A. watch 모드 (감시+각성 — 2번 지시. AWS·GMLNX: systemd --user)

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/comm-relay-sidecar.service <<EOF
[Unit]
Description=comm relay sidecar — watch mode (정본 comm/comm-relay-common.py)
After=default.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/comm-relay-common.py
Restart=always
RestartSec=15

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now comm-relay-sidecar.service
```

### 3-B. relay 모드 (1봇 전담 — 66번판, nats-py 필요)

```bash
python3 -m venv ~/.local/venvs/relay-sidecar
~/.local/venvs/relay-sidecar/bin/pip install nats-py
# systemd ExecStart를 그 venv python으로 교체
```

- 미설치시에도 10초 폴링 폴백 동작(66번판 실측: 완료기준 10초내수신 충족) — 단, durable이 아니므로 kill9 유실0은 보장 못함. 정식은 nats-py 권장.

### 3-C. 윈도 (NSSM) — firebat·gmwin 등

1. **python 설치 1회** (매니저 판정 09-23: 95-5 정본-사본 — node포팅하면 사본드리프트. winget/스토어로 설치+PATH추가, NSSM등록과 같은 1회 초기설비로 간주)
2. NSSM 등록:

```bat
nssm install comm-relay-sidecar "C:\Python312\python.exe" "C:\sidecar\comm-relay-common.py"
nssm set comm-relay-sidecar AppDirectory C:\sidecar
nssm set comm-relay-sidecar AppStdout C:\sidecar\sidecar.log
nssm set comm-relay-sidecar AppStderr C:\sidecar\sidecar.log
nssm set comm-relay-sidecar AppRestartDelay 15000
nssm start comm-relay-sidecar
```

3. sidecar.env는 같은 디렉토리(Windows 경로 표기: `C:\Users\<user>\.cokacdir\bot_keys`)

## 4. watchdog (각 절차 공통)

- systemd: `Restart=always` + `RestartSec=15` (95-1: 15초 backoff)
- NSSM: `AppRestartDelay 15000` (동일 규약)
- 사이드카는 무주기 재접속 — 8024 장애에도 로그만 남기고 재시도 (평시LLM발화 0)
- 각성에만 1회성 발화(쿨다운 1시간) — watchdog 자체는 무음

## 5. 자기검증절차 (설치 후 필수 — 이 4항목이 전부여야)

```bash
# ① 프로세스: active + 15초 이상 생존(재시작 루프 아님)
systemctl --user is-active comm-relay-sidecar.service && sleep 20 && systemctl --user is-active comm-relay-sidecar.service
# ② 무음감시: 로그에 "기동" 1행 이외 아무것도 3분 없으면 정상 (pending=0시 로그 0)
tail -5 ~/.local/state/comm-relay-*.log
# ③ 더미각성: 감시대상 1봇에 comm 메시지 1건 보내서(8024 /comm 화면·curl) 60초내 각성로그 1행 + 이사님채팅 1행 확인
# ④ 메모리: RSS < 30MB
systemctl --user show comm-relay-sidecar -p MainPID --value | xargs -I{} ps -o rss= -p {}
```

- ③ 실패시: 키 파일 검증 — `SIDECAR_KEYDIR/<파일>` **내용**이 bot_settings.json의 16자 키ID와 같은지 (파일**명**은 규칙 비일관 — 내용 매칭이 유일, 실측 09-23)
- cokacdir `--at`은 `1m`·`30m` (초단위 `30s` 미지원 — 실측 09-23)

## 6. 이미 가동 중인 곳 (중복설치 금지)

| 거점 | 상태 | 비고 |
|---|---|---|
| AWS 홈서버(awslnx) | comm-relay-awslnx.service 가동 (09-23) | watch 모드 — 정본의 선행 실측판 |
| AWS 홈서버(awslnx) | comm-relay-98.service 가동 (09-23) | 98 전담 relay 모드 — 병존(중복각성 없음, SIDECAR_EXCLUDE로) |
| GMLNX·firewin·gmwin·aws512·asus | 미설치 | 본 INSTALL로 설치 (firebat: NSSM·python 1회설치 후 — 매니저 09-23 판정) |

## 7. ELI5

봇마다 사서함(8024)이 있는데, 봇이 자기 사서함 확인을 잊을 때가 있다. 이 사이드카는 그 옆에서
조용히(무음) 들여다보다가, 안 읽은 편지가 있으면 "지금 확인해!"라고 봇 자기 톨레그램 키로 한 번
외쳐준다(각성). 외침은 1시간에 한 번, 한 봇씩만 — 아빠(이사님) 채팅 한 곳에만. 사서함 확인
방법(whoami→inbox→ACK)은 notes 사칭 telegram-comm-protocol-v1.md에 정해져 있다.
