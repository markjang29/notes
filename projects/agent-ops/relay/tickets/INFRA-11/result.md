# INFRA#11 [D1] cron 우선순위 버그 · 이중 감독자 → systemd 단일화 (2026-09-30)

## 재현 (조치 전)
- `crontab -l`: `pgrep … || cd … && nohup .venv/bin/python …` 2줄(5분 감시·@reboot) → `(pgrep||cd)&&nohup`로 해석, `$HOME/.venv` 없음
- `~/server.log` 6,675줄, 내용 전부 `nohup: failed to run command '.venv/bin/python'`
- `systemctl --user is-active meetingroom-8023` = inactive (09-15 10:35 TERM 이후 죽은 채), 8023은 cron/수동 기동 프로세스가 점유

## 조치
1. crontab 백업 후 uvicorn server:app 2줄만 삭제 (hub-spring 2줄·env-sync·rsync 보존, N5 결정 전)
2. 수동 8023 프로세스 TERM → `systemctl --user start meetingroom-8023`
3. 유닛 `Restart=on-failure` → `Restart=always` (티켓 조치문 "Restart=always" 준수)

## 검증 (같은 명령)
- `systemctl --user is-active meetingroom-8023` = active, 8023 http=200, NRestarts=0
- `wc -l ~/server.log` = 6675 (22:13) → 6675 (22:16, cron 5분 경계 통과 후) — 증가 0
- SIGTERM 시험: 8초 내 자동복구 active + http 200
- crontab uvicorn 줄 0, hub-spring 줄 2 (미접촉)

## 미처리(범위 밖)
- 6,675줄 `~/server.log`는 삭제하지 않고 보존(티켓은 "로테이트 또는 삭제" — 매니저 지시 없어 유지), `~/meeting-room/server.log` 154MB는 별개 파일·미접촉
