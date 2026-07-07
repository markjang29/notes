# Checkpoint — 매니저/팀장별 채팅 백업 로테이션

일시: 2026-07-07 KST  
처리: 감사봇(Codex)  
상태: 구현·테스트·스케줄 등록 완료

## 목적

세션 clear, context window limit, 모델 교체 실패 등으로 대화 맥락이 유실될 때 복구할 수 있도록 매니저/팀장별 채팅 백업을 시간 단위로 남긴다.

## 저장 위치

운영 위치:

```text
/home/ubuntu/chat_logs
```

스크립트:

```text
/home/ubuntu/scripts/chat-log-backup.py
```

Git 보존 사본:

```text
notes/setup/server/chat-log-backup.py
```

## 저장 규칙

- 매니저/팀장/감사봇별 분리
- 1시간 단위 파일
- 단일 파일 최대 512KB
- 512KB 초과 시 `part001`, `part002` 식으로 넘버링
- D+7 이전 날짜 로그 자동 삭제
- raw 대화는 Git에 넣지 않음

## 폴더 예시

```text
/home/ubuntu/chat_logs/
  manager/heav_lnx_bot/YYYY-MM-DD/HH_00.part001.jsonl
  rpg/heav_lnx_rpg_bot/YYYY-MM-DD/HH_00.part001.jsonl
  scenario/heav_lnx_scenario_bot/YYYY-MM-DD/HH_00.part001.jsonl
  trader/heav_lnx_trader_bot/YYYY-MM-DD/HH_00.part001.jsonl
  audit/heav_lnx_bot_codex_audit/YYYY-MM-DD/HH_00.part001.jsonl
  telegram_raw/<chat_id>/YYYY-MM-DD/HH_00.part001.jsonl
```

## 데이터 소스

1. `~/.cokacdir/ai_sessions/*.json`
   - User/Assistant 전체 턴을 포함하므로 봇별 복구의 주 소스.
2. `~/.cokacdir/logs/telegram_YYYY-MM-DD.jsonl`
   - Telegram raw 입력 로그.
   - private chat은 특정 봇을 항상 식별할 수 없으므로 `telegram_raw/<chat_id>`로 별도 보관.

## cron

매시 5분:

```cron
5 * * * * /usr/bin/python3 /home/ubuntu/scripts/chat-log-backup.py --root /home/ubuntu/chat_logs --max-bytes 524288 --retention-days 7 >> /home/ubuntu/chat_logs/.run/chat-log-backup.log 2>&1
```

## 검증 결과

초기 실행:

- ai_session 기록 210건 백업
- telegram_raw 기록 737건 백업
- 두 번째 실행 중복 기록 0건
- D+7 이전 날짜 파일 26개 삭제
- 512KB 초과 파일 없음
- Python 문법 검사 통과

추가 정리:

- notes repo 안에 미추적으로 남아 있던 기존 Markdown 대화 백업 `chat-backups/`는 raw 로그 성격이므로 Git에 넣지 않고 `/home/ubuntu/chat_logs/legacy_markdown/` 하위로 이동해 보존했다.

현재 주의:

- 과거 세션 중 current_path가 현재 bot_settings 매핑에 없는 것은 `unknown/unknown`으로 백업됨.
- 이는 과거 임시 workspace 세션 보존용이며, 현재 운영 봇 매핑에는 영향 없음.
