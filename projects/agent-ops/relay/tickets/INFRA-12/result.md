# INFRA#12 [D2] notes 사본 stale·미원격 저장소 (2026-10-01, 98)

## 재현 (조치 전)
- 사본 `~/.cokacdir/workspace/8jkpubeh/notes` 최신커밋 6fadadd(09-22) vs 정본 0a1105e(10-01) → 9일 stale
- `comm/__pycache__` untracked: 제안서 작성 시점엔 그랬으나 현재 .gitignore 1행 `__pycache__/`가 전역 적용됨(check-ignore 일치, untracked 0) — 이미 해소
- `env-sync`·`tg-workspace`: git 저장소인데 remote 0개. env-sync 미커밋 24건(??20/M4), tg-workspace 6건

## 조치
1. 사본 `git pull --ff-only` → 0a1105e로 갱신 (수동 1회)
2. pull-on-boot 상록화: L0 부팅절차 §3.5에 4번으로 주입 — `git -C <notes> pull --ff-only`, 실패 무시·다음 부팅 재시도. 커밋 0ce0e2e
3. 미원격 2곳: 원격 생성은 이사님 계정 필요 → 티켓 규칙대로 **상신만**(운영변경·push 없음)

## 검증 (같은 명령)
- 사본: `git log -1` → 0a1105e 2026-10-01 (stale 9일→0일)
- pull-on-boot: L0-agent-boot.md에 1행 존재(grep 1건) — 다음 부팅부터 자동
- env-sync·tg-workspace: `git remote -v | wc -l` = 0 (변경 없음 — 상신 상태)

## 상신(이사님 계정 필요)
- private 원격 2곳 신설 요청: ① `~/env-sync` ② `~/tg-workspace` → github.com/markjang29 아래 생성 후, 생성 완료만 알려주시면 98이 remote 등록+첫 push까지 마칩니다.
