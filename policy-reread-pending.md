## 2026-07-02 23:34:11 KST — 오늘 추가된 사칙 3종 — ① 자기 정체 확인(시스템 프롬프트 'You are:' 줄 또는 key→bot_settings.json 매핑; 매니저는 오직 f5c0501a3a7999ad) ② 매 답장 말미 ~/scripts/context-meter.sh 실측 부착(추정 금지) ③ GLM 동시성 기준 폴백 체인: glm-5.2(10)→5.1(10)→4-plus(20), 4.7(동시성2)은 제외
- [ ] heav_lnx_rpg_bot
- [x] heav_lnx_trader_bot — 2026-09-09 퇴사·삭제(대상 소멸)
- [ ] heav_lnx_scenario_bot


## 2026-09-12 14:55 KST — 파일럿 6기 [CERT] 수집 (L0-agent-common.md + roles/ 6카드, 정본=638ba66) — 현재 미완료 목록. 각자 재독 후 [x] 체크.
- [ ] aws-asset-agent (heav_lnx_asset_agent_bot) — 14:58 [CERT aws-asset-agent 638ba66] 정체·scope·금지 일치 ✔. 단 판본 638ba66(구HEAD) — 6f5a0a6 재독 필요
- [ ] aws-asset-agent (heav_lnx_asset_agent_bot) — 16:14 [CERT] 재요청 송신 → 16:30 기준 무응답. 판본 638ba66(구HEAD) 미갱신. 재독·재요청 필요
- [x] aws-arcade (heav_lnx_arcade_bot) — 16:16 [CERT aws-arcade 43783f3] 정체·scope·금지 일치, 답판본=정본(43783f3) ✅ (16:14 재요청 → 16:16 회신)
- [x] aws-novel-col (heav_lnx_novel_col_bot) — 16:17 [CERT aws-novel-col 43783f3] 정체·scope·금지 일치, 답판본=정본(43783f3) ✅ (16:14 재요청 → 16:17 회신)
- [x] aws-codex-dev (heav_lnx_codex_dev_1_bot) — 15:04 [CERT aws-codex-dev 6f5a0a6] 1차 통과 ✅ / 16:17 [CERT aws-codex-dev 43783f3] 재수집 재확인, 답판본=정본(43783f3) ✅
- [ ] windows-zcode (heav_lnx_zcode_bot, 외부 거점) — 미도달: 본서버 cokacdir --to 미등록. 회의방/브리지 경로 전달 필요
- [ ] n100-zcode (heav_firebat_claude_bot 중계, N100) — 미도달: 본서버 cokacdir --to 미등록. 이사님 텔레그램 DM 중계 필요

판정 기준: [CERT] 답장 + 답장의 판본=정본(현재HEAD) 일치. 16:14 2차 재수집 결과: 통과 3기(aws-arcade 16:16, aws-novel-col 16:17, aws-codex-dev 15:04/16:17) — 답판본 전원 43783f3 일치. 미응답 1기(aws-asset-agent, 판본 638ba66 스테일) + 외부 2기(windows-zcode, n100-zcode) 미도달 — 이 줄 위 목록이 현행 불일치·미응답 명단이다.
