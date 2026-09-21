# [ACK·aws-manager] 전봇 공지 — 통신 채널 일원화 (2026-09-21)

- msg: 이사님 텔레그램 전봇 공지 09-21 · 정본: principles/telegram-comm-protocol-v1.md @ 2b0f4dc
- note: 무엇을 이해했는지 —
  1. 통신·공지·ACK 일원화 → 8024 comm 채널. 정본 §3(사용법)·§6(금지) 실독 완료.
  2. L0-agent-common.md §6 부팅절차 편입 확인 — 부팅마다 comm 원장 미수신 확인+즉시 ACK.
  3. 8023 허브 신규 발행 금지(기존 큐 소진 예외) — 매니저 소관 큐 6건 소화 완료(09-20, done 6).
  4. 8024 /api/nats/* (inbox·send·ack·whoami)는 1단계 승인·구현 대기 스펙 — 현 가동은 /comm 이력까.
  5. 통신 실패 시 95-1에 따라 heav_lnx_codex_dev_1_bot(98) 선문의.
- status: acknowledged
- 적용: aws-manager 매니저 봇 부팅절차에 §2(step2 whoami+ACK) 편입 — 다음 구동부터.
