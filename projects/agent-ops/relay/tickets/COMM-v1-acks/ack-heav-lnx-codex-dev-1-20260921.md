# [ACK·heav_lnx_codex_dev_1_bot] 전봇 공지 — 통신 채널 일원화 (2026-09-21)

- msg: 이사님 텔레그램 전봇 공지 09-21 10:40:38 · 정본: principles/telegram-comm-protocol-v1.md @ 2b0f4dc
- note: 무엇을 이해했는지 —
  1. 통신·공지·ACK 일원화 → 8024 comm 채널. 정본 §0~§8 실독 완료 (owner=98, 검증=감사95).
  2. L0 부팅절차 편입 확인 — 부팅마다 `GET /api/nats/whoami` → 미수신 inbox → 즉시 7필드
     ACK("봤음" 단독 불인정, note에 무엇을 이해했는지 + acknowledged|blocked).
  3. 발신은 roster.json 실명만(가명·약칭 금지), ref(근거) 필수, 토픽 3종 고정
     (bot.msg.<from>.<to> · notice.broadcast · bot.ack.<bot>), 임의 확장 금지.
  4. 8023 신규 task·notice 발행 금지(기존 큐 소진 예외) — 전환 완료 후 적용.
  5. 통신 실패 시 95-1: 먼저 98(자)에게 문의 → 이사님 직접 호출은 마지막 수단.
     장애는 8024 자동감지 → 이사님 텔레그램(§7).
- status: acknowledged
- 적용: 본 봇(98)은 본 사칙의 구현·운영 담당 — §1 현황문 갱신 의무 이행(가동 커밋 a02d691).
  1단계 API(inbox·send·ack·whoami) 09-21 12:29 가동 (matrix-studio-spring@4fe51a8).

(모델: glm-5.3-flash / LLM 게이트웨이 경유)
