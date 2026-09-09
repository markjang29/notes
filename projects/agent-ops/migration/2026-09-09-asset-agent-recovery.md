# asset_agent(리수·창고 관리) 서버 이관 — 자가 백업·복구 정본 (2026-09-09)

이사님 지시: 전 봇·로컬 파일 타 서버 이관 예정 → 각 봇 자가 백업 + 복구법 보고. codex_dev_1 선례(`2026-09-09-codex-dev-1-recovery.md`) 패턴 준수.

## 1. 정체 (재가동 키)
- username `@heav_lnx_asset_agent_bot` / 표시명 `[AWS 8G] 클로드 리수및 창고 관리`
- Telegram bot token: `~/.cokacdir/bot_settings.json` 내 보관 (git·아카이브 **미포함** — 비밀 규정)
- 봇 key 파일: `~/.cokacdir/bot_keys/420d4aa353fab67687ee96e6dda97fa6410a205a726bfe159c7573d5ad0918b2.key`
- 담당 repo `~/projects/matrix_asset_agent` (github.com/markjang29/matrix_asset_agent, main push 완료 `387895a`)
- model `glm-5.3-flash`, owner `8315615299`

## 2. 자산 실측 (원본 서버 기준)
- 공용 복구 메모리 L0 `~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory` (36파일) 160K → tarball
- 전 봇 대화 메모리 `~/.cokacdir/memory_store` 948K → tarball
- 서버 관리 스크립트 `~/scripts` (**git 없음 — 유일 사본**) 304K → tarball ★이관 필수
- 스케줄 실행 이력 `~/.cokacdir/schedule_history` 4.8M → tarball
- 그룹챗 원본 로그 `~/.cokacdir/group_chat` 4.6M → tarball
- cokacdir 문서 `~/.cokacdir/docs` 204K → tarball
- **아카이브** `/home/ubuntu/asset-agent-backup-20260909.tar.gz` (Telegram 전송)
- 세션 워크스페이스 `~/.cokacdir/workspace/icetejfu` — restore 스크립트 보관용(내용물은 아카이브에 동봉)

## 3. 이관 시 주의 (창고 관점 전수 실측)
- `~/.cokacdir/debug` 1.5G는 폐기 가능 → 실이관 대상 약 300M
- `~/projects` 1.9G: 전부 git repo, origin push 완료 기준 clone 복원 가능. 대형 repo = matrix-studio-spring 552M / scenario 293M / matrix-nexus 240M / rpg_game 167M (node_modules·빌드물 포함이라 clone이 tarball보다 유리)
- **git 밖 미반영 잔류물** (이관 전 커밋 권장 — 담당 봇 몫): approval-board(M 3건), matrix-studio-spring(M 3건), scenario(novel_assets M 2건+`.runtime/`), scenario-worktree(M 3건+upstream gone), rpg_game(untracked 사진 1건), `~/notes` .reviews 로그
- `~/scripts` 304K는 git 미관리 → **아카이브가 유일 사본**, 분실 주의
- 시크릿 2종(합계 88K)은 이사님 수동 이관: `bot_settings.json` 44K + `bot_keys/` 44K

## 4. 복구 절차 (새 서버)
1. Telegram: 기존 토큰 그대로 → 같은 username으로 부활 (BotFather 재발급 불필요)
2. cokacdir 설치 (`docs/how-to-install.md`) 또는 바이너리 37M 이관
3. 시크릿 수동 이관: `~/.cokacdir/bot_settings.json` + `~/.cokacdir/bot_keys/` (안전 채널)
4. `restore-asset-agent.sh` + tarball을 같은 디렉토리에 두고 실행 → `$HOME` 자동 전개·정합 검사
5. `git clone github.com/markjang29/notes` → `~/notes` 복구 (원칙·onboarding·migration 정본)
6. `~/projects/matrix_asset_agent` clone → 봇 재가동 → L0 부트 메모리(akl0hdys) 자동 주입 확인
7. 과거 대화 회수: memory_store 검색 / 그룹챗 로그는 `group_chat/*.jsonl` 참조

## 5. 스크립트
- 아카이브 내 `restore-asset-agent.sh` 동봉 (전개 + 메모리/스크립트/로그 정합 체크 + 시크릿 누락 안내)
