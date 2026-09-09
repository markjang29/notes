# 2026-09-09 서버 이관 마스터 복구 문서 (8GB AWS → 신규 홈 서버)

> 작성: 매니저 `@heav_lnx_bot` · 이사님 긴급 지시에 따른 전체 자산 실측·백업·복구 절차 정본.
> 원칙: git에 올라가는 것은 최대한 git으로, 시크릿·대용량은 수동 이관. **이 문서 자체가 복구의 시작점.**

## 0. 복구 요약 (TL;DR)

```bash
# 1) 이 문서가 있는 repo 복구
git clone https://github.com/markjang29/notes.git ~/notes
# 2) 매니저 운영자산 아카이브 복원 (이사님 수동 이관 받은 뒤)
tar xzf manager-migration-backup-20260909.tar.gz -C /tmp/mgr && bash /tmp/mgr/restore-manager-ops.sh
# 3) repo 전체 클론
mkdir -p ~/projects && for r in notes rpg_game scenario autotrader matrix matrix-engine matrix-home matrix-nexus matrix-studio matrix-studio-spring matrix_asset_agent matrix_codex matrix_zcode approval-board bot-dashboard meeting-room; do git clone https://github.com/markjang29/$r.git ~/projects/$r; done
# 4) systemd·crontab·시크릿 확인 후 서비스 기동
```

## A. Git 보존 완료 (클론 = 복구)

| repo | 이관 전 상태 | 조치 |
|---|---|---|
| `notes` | reaper 로그만 dirty | commit+push ✓ (`de13055`) |
| `bot-dashboard` | **원격 없음·미푸시 4커밋** | 신규 비공개 repo 생성·push ✓ |
| `meeting-room` | 미푸시 3커밋(`legacy-local-history` 브랜치) | push ✓ |
| `matrix-studio-spring` | topology/ 신규 소스 미추적 | commit+push ✓ (`0e1d34d`) |
| `approval-board` | requests.json dirty | commit+push ✓ (`4225a72`) |
| `rpg_game` `scenario` `autotrader` `matrix*`(8개) | clean | 기존 원격 그대로 ✓ |

## B. 아카이브 보존 — `manager-migration-backup-20260909.tar.gz` (27M→압축)

매니저 관할·git 불가 데이터 전부. 내역(압축 전):

| 내용 | 크기 | 비고 |
|---|---|---|
| `deploy/notes-registry`+스크립트 | 11M | 릴레이·백업 스크립트 원본 |
| `schedule_history/` | 4.8M | 예약작업 실행 이력 전체 |
| `group_chat/` | 4.7M | 그룹챗 공유 로그 |
| `ai_sessions/` | 3.1M | 봇 세션 상태 |
| `chat_logs/` | 1.8M | 봇별 대화 로그 |
| `memory_store/` | 964K | 공유 대화 메모리 코퍼스(전 봇) |
| `claude-memory/` | 720K | `.claude/projects/*/memory` 전체(정체·사칙·work-state 포함) |
| `cokacdir-config/` | 364K | **bot_settings.json·bot_keys·devpass.env·cokac_ops_key (시크릿 — 절대 git 금지)** |
| `scripts/` | 176K | 서버 관리 스크립트(로그·pycache 제외) |
| `systemd-units/` | 72K | 커스텀 서비스 17개 유닛 |
| `crontab.txt` | 4K | cron 9개 항목 |
| `restore-manager-ops.sh` | — | 자동 복원 스크립트 |

기타 봇 자체 백업(각 봇 생성, 홈 루트): `rpg_bot_backup_20260909.tar.gz` 6.4M · `codex_dev_1-backup-20260909.tar.gz` 4.1M · `asset-agent-backup-20260909.tar.gz` 2.0M · `novel-col-backup-20260909.tar.gz` 182K(+동 봇 복구 문서 `2026-09-09-novel-col-bot-recovery.md`)

## C. 이사님 수동 이관 대상 (git 불가·유일 사본)

| 경로 | 크기 | 판단 |
|---|---|---|
| `~/Works/arcalive` | **87G** | 수동 이관 필수 |
| `~/Works/novel` | 5.7G | 수동 이관 필수 (novel_col epub 원본 1,537화) |
| `~/risu` | 2.8G | 수동 이관 (앱 데이터) |
| `~/releases` | 1.6G | 빌드 산출물 — 재빌드 가능하면 생략 가능 |
| `~/matrix-candidate` | 1.5G | workbench 백업 포함 — 판단 필요 |
| `~/.cokacdir/debug` | 1.5G | **폐기 가능 (디버그 로그)** |
| `~/matrix_codex` | 846M | 판단 필요 (repo와 무관 런타임 데이터 추정) |
| `~/tools` | 654M | 설치형 툴 — 재설치 가능성 |
| `~/matrix_asset_agent` | 539M | 판단 필요 |
| `~/apps` | 275M | 판단 필요 |
| `~/backups` | 166M | 과거 백업 — 판단 필요 |
| `~/.cokacdir/values` 28M · `~/.cokacdir/backups` 21M | 49M | 런타임 값·설정 이력 — 선택 |

## D. 복구 순서

1. **토큰** — 이사님 보유 토큰으로 봇 username 재가동(부팅 자체는 토큰만으로 됨)
2. **cokacdir 설치** → `cokacdir-config/`의 `bot_settings.json`·`bot_keys/` 배치
3. **`restore-manager-ops.sh` 실행** — 메모리·세션·로그·스크립트·systemd·crontab 자동 복원
4. **repo 클론** (위 TL;DR 3번)
5. **대용량 수동 이관분** 원위치 (C절)
6. **검증** — `ls ~/.cokacdir/bot_keys | wc -l`, `systemctl status` 주요 서비스, notes repo에서 이 문서 존재 확인

## E. 최종 잔류물 처리 결과 (09-09 23:58 기준, 전 repo 재스캔)

- `matrix-studio-spring` — 운영 중 발생 변경(WebConfig.java·main.jsx·README·런타임 DB) 추가 커밋·push ✓ (`a01c97f`)
- `rpg_game` — 사진 원본 git 보존 커밋·push ✓ (`b1e2bf5`, rpg tarball과 이중 백업)
- `scenario .runtime/` — scenario 봇이 sqlite tar(3.4K)로 보존 후 이사님 전송 완료 ✓
- `scenario-worktree` — scenario 봇이 미커밋분 커밋 후 backup/* 브랜치로 push ✓
- `approval-board.pre-49d70e5-20260717T163033` — 7월 17일자 구(舊) 스냅샷 디렉토리. 현재본은 원격 동기 완료. **미푸시 3커밋·dirty 존재하나 폐기/선택 보존 가능** (현재 approval-board 기준 과거 시점 복제본)
- 그 외 전 repo unpushed 0 확인. 팀 봇 6개 자체 백업 완료 보고 접수 (rpg·scenario·codex_dev_1·novel_col·asset_agent)

**결론: git 원격에 없는 소스코드 0. 남은 것은 C절 대용량 수동 이관 + 아카이브 3종(매니저 6.0M + 각 봇 tarball) 이사님 보관뿐.**
