# INFRA#9 N1 — NATS 4222/8222 로컬 바인딩 + 인증 (브랜치 준비안, 2026-10-02 98)

근거: proposals/2026-09-30-system-improvement-review.md §4 N1 (P0, 승인주체 이사님)
상신: Taiga US 151 (project 6 INFRA, ref 9)

## 실측 (10-02, 읽기 전용 — 운영 변경·재시작 없음)

- 바인딩: `ss -ltn | grep -E '4222|8222'` → 4222·8222 모두 `*:4222|*:8222` (0.0.0.0, 전 인터페이스)
  = 제안서 "문제" 그대로 재현.
- 설정: `~/.config/nats/nats.conf` — `listen: 0.0.0.0:4222`, `http: 0.0.0.0:8222`,
  주석 "로컬 전용: 외부 노출 없음" (실제와 모순 = 제안서 지적 그대로).
- 서비스: `systemctl --user` nats.service (MemoryMax 300M), 09-20 기동 이후 가동 중.
- 접속: `GET 127.0.0.1:8222/connz` → 2건 모두 ip=127.0.0.1
  (relay98-sidecar, 09-23부터; 나머지 1건 10-01부터) → **원격 접속 없음 재확인 완료**
  = 127.0.0.1 바인딩 무영향 조건 충족.
- 인증: nats.conf에 authorization 블록 없음 (무인증).

## 브랜치 준비안 (이사님 승인 후 적용 — 지금은 변경 없음)

1. `nats.conf` 수정:
   - `listen: 127.0.0.1:4222`
   - `http: 127.0.0.1:8222`
2. `systemctl --user restart nats` (JetStream 저장소 영향 없음)
3. 검증:
   - `ss -ltn | grep -E '4222|8222'` → 127.0.0.1만 표시
   - relay98 로그 "JetStream durable 구독 완료" / 재접속 확인
   - `curl -s "http://43.201.34.144:8024/api/nats/whoami?bot=heav_lnx_codex_dev_1_bot"` 정상 응답
4. 롤백: 설정 원복 후 재시작.

인증(authorization)은 원격 노드 직접 접속 필요성이 생길 때 2단계로 (제안서 A3/N2 참고).

## 상태

- [x] 실측·재현 (읽기 전용)
- [x] 준비안 문서화 (본 파일, 브랜치)
- [ ] 이사님 승인 (Taiga 151 → 의사결정대기 상신)
- [ ] 적용·검증 (승인 후, 운영 변경 허가 시)
