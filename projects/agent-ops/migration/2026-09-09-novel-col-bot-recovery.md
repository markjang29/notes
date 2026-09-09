# novel_col(크롤드 소설수집) 서버 이관 — 자가 백업·복구 정본 (2026-09-09)

이사님 지시: 전 봇·로컬 파일 타 서버 이관 예정 → 자가 백업 + 복구법 보고. asset_agent 선례(`2026-09-09-asset-agent-recovery.md`) 패턴 준수.

## 1. 정체 (재가동 키)
- username `@heav_lnx_novel_col_bot` / 표시명 `[AWS 8G] 크롤드 소설수집`
- Telegram bot token: `~/.cokacdir/bot_settings.json` 내 보관 (git·아카이브 **미포함** — 비밀 규정)
- 봇 key 파일: `~/.cokacdir/bot_keys/c5a8134d782b476cc2e192786e0519191072b6fd2fc587bbebd4a7b995ec3b5e.key`
- model `glm-5.3-flash`, owner `8315615299`
- cron 스케줄: 없음(실측 `--cron-list` 0건)

## 2. 자산 실측 (원본 서버 기준, 2026-09-09 23시대)

### 2-1. git으로 이미 보존됨 ★추가 작업 불필요 (clone이 곧 복구)
| 대상 | 크기 | repo | 상태 |
|---|---|---|---|
| 수집 자산 문서 962파일 | 18M | `github.com/markjang29/scenario` → `novel_assets/` | main=origin 동기 ✓ |
| epub 인벤토리 대장 324K | — | `github.com/markjang29/matrix_asset_agent` → `inventory/novel_epub_manifest.json` | push 완료 `387895a` ✓ |
| 수집큐·운영상태 | 100K | `github.com/markjang29/matrix-home` → `novel_queue.json` `novel_ops.json` | push 완료 `ec6999a` ✓ |
| 파이프라인 코드 | — | `github.com/markjang29/matrix_zcode` → `novel_extractor.py` `novel_full_reader.py` | main=origin 동기 ✓ (untracked 5건은 타 봇 영역) |

### 2-2. tarball 아카이브 (git 밖 유일 사본)
- **`/home/ubuntu/novel-col-backup-20260909.tar.gz` 182K** (Telegram 전송 완료)
  - chat_logs/ 대화원본(104K) · memory_store/(60K) · claude 세션(152K) · 수집큐 스냅샷 · epub 대장 · 추출스크립트 · `restore-novel-col.sh`
- `_extract` 전체 96M → gz 29M: 파생물(epub에서 재추출 가능)이라 아카이브 미포함. 필요 시 `/home/ubuntu/Works/novel/_extract` 채로 이사님 이관

### 2-3. 대용량 원본 — 이사님 수동 이관 필수 ★git 불가
| 경로 | 크기 | 내용 | 비고 |
|---|---|---|---|
| `~/Works/novel/epub 파일/` | **4.9G** | epub 1,537화 | 유일 사본. 복원 검증은 `novel_epub_manifest.json`(count=1537 일치) |
| `~/Works/novel/[도서] 2026 06월 완결 웹소설 모음집/` | **785M** | 완결작 모음 424파일 | 유일 사본 |
| `~/Works/novel/_extract/` | 96M | 작품별 텍스트 추출본 | epub에서 재추출 가능(파생물) |
| `~/Works/novel` 합계 | **5.7G** | | |

### 2-4. 재생성 가능 (이관 불필요)
- `~/.venvs/novelweb` 50M — Flask/dnspython 등 pip 재설치
- `~/matrix_asset_agent/.runtime/novel` 323M — 런타임 작업물

## 3. 복구 절차 (새 서버)
1. Telegram: 기존 토큰 그대로 → 같은 username으로 부활 (BotFather 재발급 불필요)
2. cokacdir 설치 (`docs/how-to-install.md`)
3. 시크릿 수동 이관: `~/.cokacdir/bot_settings.json` + `~/.cokacdir/bot_keys/` (안전 채널)
4. tarball 풀고 `./restore-novel-col.sh` → `$HOME` 전개 + 대화로그/메모리/세션 정합 검사
5. `git clone github.com/markjang29/notes` → `~/notes` (본 문서 포함 원칙 정본)
6. `git clone` scenario → `novel_assets/` 복구, matrix_asset_agent → `inventory/novel_epub_manifest.json`
7. 이사님이 `~/Works/novel` 5.7G 이관해주면 → `python3 -c "import json;print(json.load(open('.../novel_epub_manifest.json'))['count'])"` vs `ls "epub 파일" | wc -l` = 1537 일치 확인
8. 과거 대화 회수: memory_store `-5365038823` / chat_logs 원본

## 4. 데이터 성격 요약 (이관 판단 기준)
- **정본(GitHub)**: 자산 문서·인벤토리·큐·파이프라인 코드 — 재구축 불필요
- **유일 사본 tarball**: 대화기록·메모리·세션 — 분실 시 복구 불가, 182K 소량
- **유일 사본 대용량**: epub 원본 5.7G — 이사님 수동 이관, manifest로 무결성 검증
