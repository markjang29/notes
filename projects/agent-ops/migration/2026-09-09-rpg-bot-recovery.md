# rpg_bot 자가 백업·복구 정본 (2026-09-09 긴급 이관)

작성: `@heav_lnx_rpg_bot` ([AWS 8G][그림] rpg 팀) — 이사님 09-09 긴급 이관 지시에 따른 자가 백업.
방법론: `2026-09-09-arcade-bot-recovery.md` 선례 준용.

## 1. 내 정체 (부활에 필요한 최소 정보)

| 항목 | 값 |
|---|---|
| username | `heav_lnx_rpg_bot` |
| display | `[AWS 8G][그림] rpg 팀` |
| bot_settings.json 엔트리 키 | `c5bb2c97036d3741` |
| bot_keys 파일 | `ed553704fb7782f09d794aaa462e43ad54ba77c6ec0342dcddeb954a6fbdcce9.key` (17B) |
| owner_user_id | `8315615299` (이사님) |
| 주 그룹 chat_id | `-5365038823` |
| 역할 | RPG 팀장 — `/home/ubuntu/projects/rpg_game` (전술 RPG) 담당 |
| 담당 repo | https://github.com/markjang29/rpg_game |

- Telegram 봇 **토큰은 git에 없음**(시크릿 원칙). `~/.cokacdir/bot_settings.json`의 `c5bb2c97036d3741` 엔트리에 있음 → 이관 시 `bot_settings.rpg_entry.json`에서 해당 엔트리만 병합.
- 부활 시 L0 부트스트랩은 canonical 메모리를 읽음 → §2의 메모리 스냅샷이 곧 내 "원칙 체계" 원본.

## 2. 백업 상태 요약 (사이즈 단위 체크, 2026-09-09 23:17 KST 실측)

| 자산 | 크기 | 보존처 | 상태 |
|---|---|---|---|
| rpg_game 코드·문서·demo·web 전체 | 167M(워크트리)/26M(.git) | GitHub `main` (`8a12144`) | ✅ 미반영 0 — 완전 push |
| canonical 복구 메모리(akl0hdys, 35파일) | 160K | notes `backup/rpg-bot-self-20260909` (`2dc7da3`) + tarball | ✅ 이중 |
| rpg_game 세션 메모리(17파일) | 92K | 동일 브랜치 + tarball | ✅ 이중 |
| rpg_game 대화 트랜스크립트(jsonl 2개) | 12M | tarball 전용 | ✅ |
| 그룹 채팅 로그 `-5365038823.jsonl` | 84K | tarball 전용(git 제외 — 시크릿 유사문자열 감지) | ✅ |
| 봇 키(17B) + settings 엔트리 추출본 | <2K | tarball 전용(시크릿) | ✅ |
| rpg_game 미트래킹 잔류(photo jpg 62K, `demo/debug.keystore`) | 62K+1K | tarball 전용 | ✅ |
| **tarball 합계** | **6.6MB** | `/home/ubuntu/rpg_bot_backup_20260909.tar.gz` | ✅ 이사님 전송 |

- rpg_game ignored 파일(`*.import`·`venv`·`__pycache__`·`export/`·`server.log`)은 전부 재생성 가능 — 백업 불요.
- **공용 자산(매니저 스코프, 내 단독 소유 아님):** `memory_store` 956K · `schedule_history` 4.8M · `group_chat` 4.7M · `bot_settings.json` 43K(전 봇 토큰). `.cokacdir` 전체 1.8G 중 `debug/` 1.5G는 폐기 검토 가능.
- 홈서버(duradev) 이관: 내 스코프는 웹서비스가 아닌 **repo+에이전트 상태**라 별도 배치 건 없음 — 부활은 신규 서버에서 클론+복원으로 충분.

## 3. 복구 절차 (새 서버)

```bash
# (1) 코드 복원 — 정본은 GitHub main과 동일
git clone https://github.com/markjang29/rpg_game
cd rpg_game && git checkout main   # 8a12144

# (2) 봇 부활 — 신규 서버 cokacdir에 복사
#   ~/.cokacdir/bot_settings.json  ← 기존 파일에 rpg 엔트리(c5bb2c97036d3741) 병합
#     (엔트리 단독본: tarball 안 cokacdir/bot_settings.rpg_entry.json)
#   ~/.cokacdir/bot_keys/ed553704fb7782f09d794aaa462e43ad54ba77c6ec0342dcddeb954a6fbdcce9.key

# (3) 메모리 복원 — 부트스트랩이 읽는 canonical 경로로
mkdir -p ~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys
cp -r <해제경로>/claude-memory/akl0hdys-canonical-memory \
      ~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory
# (tarball 없으면 git에서: git clone -b backup/rpg-bot-self-20260909 https://github.com/markjang29/notes)
cp -r <해제경로>/claude-memory/rpg-game-session-memory \
      ~/.claude/projects/-home-ubuntu-projects-rpg-game/memory

# (4) 비-git 상태 복원 (대화로그·키·keystore·잔류파일)
tar xzf rpg_bot_backup_20260909.tar.gz -C /tmp   # 상대경로 구조 — /tmp에서 확인 후 배치
```

## 4. 검증 코드

```bash
# (a) 코드 정합 — 로컬 main = GitHub main
cd rpg_game && git status -sb        # ## main...origin/main (차이 없음)
git log -1 --format='%h %s'          # 8a12144 PROJECT-RULES.md §9~§11 추가 ...

# (b) 메모리 백업 브랜치 존재
git ls-remote origin refs/heads/backup/rpg-bot-self-20260909
# 기대: 2dc7da3399c0b2bec4ad88e8d653827b0d97fec5
git clone -q -b backup/rpg-bot-self-20260909 --depth 1 https://github.com/markjang29/notes /tmp/nv \
  && find /tmp/nv/projects/agent-ops/memory-snapshot/2026-09-09 -type f | wc -l
# 기대: 52 (canonical 35 + rpg 세션 17)

# (c) tarball 무결성
tar tzf rpg_bot_backup_20260909.tar.gz | wc -l    # 기대: 69
```

복구 소요: 클론 + settings 병합 + 메모리 복원 = **5분 이내**. 대형 파일 이관 불요(rpg_game 전체는 GitHub에 있음).
