# codex_dev_1 서버 이관 — 자가 백업·복구 정본 (2026-09-09)

이사님 지시: 전 봇·로컬 파일 타 서버 이관 예정 → 각 봇 자가 백업 + 복구법 보고.

## 1. 정체 (재가동 키)
- username `@heav_lnx_codex_dev_1_bot` / 표시명 `[소통][AWS 8G] 코덱스 dev_1`
- Telegram bot token: `~/.cokacdir/bot_settings.json` 내 보관 (git·아카이브 **미포함** — 비밀 규정)
- 봇 key 파일: `~/.cokacdir/bot_keys/fddb22a8be6e1dd80e46b8a65f4996686df65ff393aa8fd5696a51e2377dcee4.key`
- model `glm-5.3-flash`, owner `8315615299`

## 2. 자산 실측 (원본 서버 기준)
| 자산 | 경로 | 크기 | 백업 상태 |
|---|---|---|---|
| DM 대화 메모리 | `~/.cokacdir/memory_store/v2/8315615299` (168건) | 808K | ✅ tarball |
| 그룹챗 메모리 | `~/.cokacdir/memory_store/v2/-5365038823` (7건) | 40K | ✅ tarball |
| 세션 전사 | `~/.claude/projects/-home-ubuntu--cokacdir-workspace-khipihck` | 216K | ✅ tarball |
| 세션 전사(DM) | `~/.claude/projects/-home-ubuntu--cokacdir-workspace-i5fi5gyy` | 4.4M | ✅ tarball |
| 공용 복구 메모리 L0 | `~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory` (35파일) | 160K | ✅ tarball |
| DM 워크스페이스 | `~/.cokacdir/workspace/i5fi5gyy` (ui-tests 등) | 13M | ✅ tarball (node_modules 12M 제외) |
| 그룹챗 원본 로그 | `~/.cokacdir/group_chat/-5365038823.jsonl` | 20K | ✅ tarball |
| 세션 워크스페이스 | `~/.cokacdir/workspace/khipihck` | 4K (빈 폴더) | 불필요 |
| **아카이브** | `/home/ubuntu/codex_dev_1-backup-20260909.tar.gz` | **4.1M** | Telegram 전송 완료 |

## 3. 서버 전체 관점 (참고)
- `~/.cokacdir` 1.8G 중 **debug 1.5G는 폐기 가능** → 실이관 대상 약 300M
- `~/.claude/projects` 424M (전 봇 전사·메모리 포함)
- cokacdir 바이너리 37M (`/usr/local/bin/cokacdir`) — 재설치 문서 `~/.cokacdir/docs/how-to-install.md`

## 4. 복구 절차 (새 서버)
1. Telegram: 기존 토큰 그대로 → 같은 username으로 부활 (BotFather 재발급 불필요)
2. cokacdir 설치 (docs/how-to-install.md) 또는 바이너리 이관
3. 시크릿 수동 이관: `~/.cokacdir/bot_settings.json` + `~/.cokacdir/bot_keys/` (안전 채널)
4. `restore-codex-dev-1.sh` + tarball을 같은 디렉토리에 두고 실행 → `$HOME`에 자동 전개·정합 검사
5. 봇 재가동 → 기존 chat 재진입 → 세션 시작 시 L0 부트 메모리(akl0hdys) 자동 주입 확인
6. 과거 대화 회수: memory_store 검색으로 재생 (세션 자체 재개는 전사 JSONL 참조)

## 5. 스크립트
- 아카이브 내 `restore-codex-dev-1.sh` 동봉 (전개 + 시크릿/바이너리/메모리 정합 체크)
