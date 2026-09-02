# 기본 모델 glm-5.3-flash 전환 (2026-09-03 이사님 지시, 매니저 실행)

- **지시**: "@전체 모두들 기본 모델을 glm-5.3-flash 로 바꾸고 테스트 후 인증해" (09-03 00:00:38)
- **원천**: `~/.claude/settings.json` `env.ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`
  — 회의방 11기 AWS 봇은 `server.py: gateway_env()`가 이 env를 계승하므로 여기만 고치면 전원 적용(서버 재시작 불필요)
- **변경 전**: opus/sonnet=glm-5.3 · haiku=glm-4.7 → **변경 후**: 전부 `glm-5.3-flash`
- **백업**: `~/.claude/settings.json.bak-flash-0002`
- **검증(실측)**: 신규 `claude -p` 1회 호출 성공(is_error=false) · 프록시 로그
  (`~/.local/state/cokacdir/zai-fallback-proxy.log`) 15:03Z 이후 `model=glm-5.3-flash`
  라우팅 확인, 폴백/오류 0 — 매니저 세션 자체도 전환 후 정상 응답
- **미적용(별도 경로)**: ① N100 firebat 3기 = llmgateway `claude-opus-4-8`
  (5-owner 지정분, `/api/bot/config?scope=llm` — llmgateway의 flash 제공 여부 미확인)
  ② @heav_lnx_zcode_bot = zcode 엔진 `ZCODE_MODEL=zai-plan/GLM-5.2` (server.py ZENV)
- **관측**: 09-03 00:00:59~00:01:02 @전체 공지로 11기 동시 ACK 시 glm-5.3에서 429 ×3
  — 프록시 자동 재시도로 회복. 동시 dispatch 다발 시 재발 가능.
