# [ACK·heav-gmwin-claude] 전봇 공지 — 통신 채널 일원화 (2026-09-21)

- msg: 이사님 텔레그램 전봇 공지 09-21 + ACK 형식 공지(관제 id 1789987238566) · 정본: principles/telegram-comm-protocol-v1.md @ 2b0f4dc
- actor_id: heav_gmwin_claude_bot (인사99, roster.json 실명)
- POLICY_SHA: cce8fd57cfc3 (telegram-comm-protocol-v1) · c406d5eecfe6 (gwanje-ack-protocol)
- note: 무엇을 이해했는지 —
  1. 통신·공지·ACK 일원화 → 8024 comm 채널. 사칙 §3(사용법)·§6(금지) 실독 완료.
  2. L0-agent-common.md §6 부팅절차 편입 — 부팅마다 comm 원장에서 자기 미수신 확인+즉시 ACK. 상시 규칙(메모리) 등록 완료.
  3. 수신 즉시 ACK — '봤음' 단독 불인정, 관제 7필드 준용(본 ACK가 그 형식).
  4. 발신은 roster.json 실명 username만, 가명·약칭 금지, ref 필수, 토큰값은 채팅·커밋 본문 아닌 파일경로만.
  5. 통신 실패 시 95-1: 이사님 호출 전 heav_lnx_codex_dev_1_bot(98) 선문의 — 09-21 실행(허브 m1a0c38fecb3859d45).
  6. 8023 허브 신규 발행 금지(기존 큐 소진까지만 예외). comm_client.py는 notes 원본 복사본 사용(버전주석 포함, newux5m2/comm/).
  7. 인사 통합보드 독촉 버튼의 8023 송신은 전환 완료 전 예외 허용 구간 — comm 개통 시 이관 대상으로 등록해 둠.
- 맡은 일: comm 일원화 공지 수신·본 ACK + 부팅 미수신 폴링 편입 유지
- 금지: 가명 발신 · 토큰값 노출(경로만) · 전환 완료 후 8023 신규 발행
- 완료조건: 본 공지에 대한 본 ACK 등록(본 파일) — 완료. 1단계 쓰기 API(/api/nats/inbox·send·ack·whoami) 개통 시 comm ACK·폴링으로 즉시 전환.
- 실측: 09-21 12:03 KST — /api/nats/* 쓰기 4종 404(1단계 미배포) · /comm·messages·stats·brokers 200 · NATS 4222는 AWS 127.0.0.1 바인딩(외부 폐쇄) → 본 ACK는 매니저 ACK와 같은 형식·경로(notes 커밋)로 발행.
- status: acknowledged
- 적용: 인사99 부팅절차(관제방 감시 예약 작업)에 ①8024 /comm 미수신 확인 ②창구 개설 시 comm ACK 전환 편입 — 다음 구동부터.
