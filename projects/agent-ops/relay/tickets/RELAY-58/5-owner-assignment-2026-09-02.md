# [owner] matrix-studio-spring 담당 지정 (2026-09-02 이사님)

- **담당**: `n100-zcode` (@heav_firebat_claude_bot, N100 firebat claude)
- **LLM**: llmgateway 오푸스 — 회의방 `/api/bot/config?scope=llm`(ROOM_BOT_TOKEN)에서
  base_url·api_key·모델(claude-opus-4-8) 수신, 엔진 env 적용. 키는 AWS 서버에만 상주.
- **첫 할일**: README 작성 · 2-design(Next.js+FastAPI) 대비 Spring 전환 사유 기록 ·
  기본포트 정정(8a0c390) 확인 · 진행/완료는 관제 회의방 보고.
- 지정 경위: 09-02 설계 확인 매니저 보고(대기결정 #7) → 이사님 지정.

## [갱신 09-02 저녁] 이사님 결정 — "B를 zcode 시키게"

- **담당 = firebat claude 유지(B안)**. 단 N100 잠금(settings.json git 허용 미조치) 해제 전까지
  작업 정지 대기.
- **실무 대행 = AWS zcode**(@heav_lnx_zcode_bot, 회의방 엔진) — ③ 포트 8a0c390 확인 →
  ② Spring 전환 사유 기록 → ① README 작성. repo 직접 commit/push, 결과는 회의방 보고.
- 경과: firebat claude 자가조치·codex 대리(read-only) 전부 차단 → 이사님 수동 조치 회피 결정.
  firebat 잠금 해제 시 인계 절차 진행.
