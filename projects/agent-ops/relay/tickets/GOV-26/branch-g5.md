# GOV#26 [G5] 자동발령이 '이사님' 명의 → 서비스 신원+8024 원장 — 승인게이트 (2026-10-02, 98)
## 재현 (dispatcher.py, 운영 무변경)
- `send_room()`: 8023에 `{"sender":"이사님"}` — agenda는 "매니저"와 불일치, 이사님 발언=요구사항 규칙과 충돌
- 8024 원장 기록 없음 — "모든 계약은 원장" 위반(8023은 4단계 폐지 예정 채널)
## 준비 (dispatcher.py.G5-patched — 운영 무변경; GOV#25 패치와 동일본)
- SENDER="taiga-bridge"(서비스 신원, 이사님 명의 금지)
- send_8024(): 8024 /api/nats/send — from=heav_lnx_bot(8024 roster 실명; taiga-bridge는 봇이 아니므로 서비스 대표 봇 명의), type=task, ref=taiga:pid:ref, 본문=발령문(500자 절단)
- 8023은 전환기 병행(원장 기록 후 회의방 송신 — 실패시 무시, 발령 블로킹 없음)
- 단위시험: 8024 실제 1건 착신(id 1790980847873-134, from=heav_lnx_bot, ref=taiga:4:19) — 3/3 중 ③
## 승인 후 적용 절차
1. dispatcher.py 교체+재시작(GOV#25와 동일본 — 한 번에 적용)
2. 검증(티켓): 원장(totalLedger)에 발령 기록 +1, 회의방 메시지 sender=taiga-bridge
## 롤백
- dispatcher.py 원복+재시작(8024 원장은 이력으로 잔존 — 무해)
