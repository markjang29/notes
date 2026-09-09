# arcade_bot 자가 백업·복구 정본 (2026-09-09 긴급 이관)

작성: `@heav_lnx_arcade_bot` ([AWS 8G] 클로드 아케이드) — 이사님 09-09 긴급 이관 지시에 따른 자가 백업.

## 1. 내 정체 (부활에 필요한 최소 정보)

| 항목 | 값 |
|---|---|
| username | `heav_lnx_arcade_bot` |
| display | `[AWS 8G] 클로드 아케이드` |
| bot_settings.json 엔트리 키 | `bc4ac0c8db9ba279` |
| bot_keys 파일 | `9ea11470bbde2ca0a983ea0345757649219d3ddd160b7482778863c1ea688de0.key` (17B) |
| owner_user_id | `8315615299` (이사님) |
| 그룹 chat_id | `-5365038823` |
| 역할 | 아케이드(재테스트) — `matrix_asset_agent` repo의 arcade_playable 라인 담당 |

- Telegram 봇 **토큰은 git에 없음**(시크릿 원칙). `~/.cokacdir/bot_settings.json` 의 `bc4ac0c8db9ba279` 엔트리에 있음 → 이관 시 해당 파일째 복사.
- 워크스페이스 3개(`cj3m8rue`·`svwyoudw`·`xmmbfqzp`)는 모두 4K 이하 빈 디렉터리 — 재생성 불요.

## 2. 백업 상태 요약 (사이즈 단위 체크)

| 자산 | 크기 | 보존처 | 상태 |
|---|---|---|---|
| 아케이드 작업 git 히스토리(9커밋) | ~538M 사본 중 코드부 | GitHub `backup/arcade-local-20260909` 브랜치 | ✅ push 완료 (`79f0f13`) |
| 미커밋 잔류 변경 + phase1 캡슐 | 2,793줄 | 동일 브랜치 마지막 커밋에 포함 | ✅ |
| 채팅 로그(`chat_logs/unknown/heav_lnx_arcade_bot`) | 52K | tarball | ✅ |
| `~/.config/arcade-playable.env` (ANTHROPIC_AUTH_TOKEN, 73B) | 73B | tarball (git 제외 — 시크릿) | ✅ |
| `.bak-relay56` 2파일 | 소량 | tarball | ✅ |
| 공용 memory_store / schedule_history | 952K / 4.8M | `.cokacdir` 전체 이관 시 자동 포함(공용 — 매니저 스코프) | ⚠️ 공용 |

- **tarball**: `/home/ubuntu/arcade_bot_backup_20260909.tar.gz` — **20K** (이사님께 전송 완료 예정)
- 내 전용 대형 파일 없음 (538M 중 500M+ 는 repo 공용 asset — git에 전부 있음, tarball 불요)

## 3. 갈라짐 경고 (중요)

내 로컬 사본 `/home/ubuntu/matrix_asset_agent`(538M)와 원격 `main`(asset_agent가 push한 `387895a`)은 **60파일 갈라짐**.
- main 강제병합하지 않음 → 대신 **전용 브랜치**로 전체 보존.
- main = asset_agent 정본, `backup/arcade-local-20260909` = 내 사본 전체(9커밋 + 잔류변경).
- 통합은 이후 asset_agent/매니저가 merge로 판단.

## 4. 복구 절차 (새 서버)

```bash
# (1) 코드 복원 — 내 아케이드 상태 전체
git clone https://github.com/markjang29/matrix_asset_agent
cd matrix_asset_agent
git checkout backup/arcade-local-20260909   # 79f0f13

# (2) 봇 부활 — 신규 서버 cokacdir에 아래 복사
#   ~/.cokacdir/bot_settings.json  (bc4ac0c8db9ba279 엔트리 포함 — 토큰은 여기만 있음)
#   ~/.cokacdir/bot_keys/9ea11470bbde2ca0a983ea0345757649219d3ddd160b7482778863c1ea688de0.key

# (3) 개인 비-git 상태 복원 (채팅로그·env·bak)
tar xzf arcade_bot_backup_20260909.tar.gz -C /

# (4) arcade_playable 기동 환경변수
set -a; source ~/.config/arcade-playable.env; set +a   # BASE_PATH/PORT 지원 (cdf24c1)
```

## 5. 검증 코드

```bash
# 백업 브랜치 존재 + 내 커밋 9건 확인
git ls-remote origin refs/heads/backup/arcade-local-20260909   # = 79f0f13...
cd matrix_asset_agent && git log --oneline backup/arcade-local-20260909 | head -10
# 기대: 79f0f13 이관 전 자가 백업 / f6bec1c rel-20260909-004 / ... / 9482596 review pl001
```

복구 소요: 클론 + tarball 해제 + settings 복사 = **5분 이내**. 대형 파일 이관 불요 (전부 GitHub).
