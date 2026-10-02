# INFRA#9 [N1] NATS 무인증·전 인터페이스 바인딩 — 승인게이트 (2026-10-02, 98)

## 재현 (조치전 — 운영 무변경)
- ~/.config/nats/nats.conf: `listen: 0.0.0.0:4222`, `http: 0.0.0.0:8222` (인증 없음)
- ss: `*:4222`·`*:8222` — 전 인터페이스 (같은 망 누구나 발행·구독 가능)
- **connz 재확인(티켓 지시)**: 접속 2개(98 relay·8024 java) 모두 127.0.0.1 — 원격접속 0 → 로컬바인딩 1순위 조건 충족

## 준비(브랜치 comm: notes@INFRA-9, 배포 승인 후 적용)
- 변경본: nats.conf.listen-127.0.0.1 (listen: 127.0.0.1:4222 / http: 127.0.0.1:8222)
- 선검증 완료(운영 무영향): 동일설정을 임시포트(14222·18222)로 기동 → 로컬 200, 공인IP 도달불가(타임아웃) 실측 — 로컬바인딩 동작 증빅

## 승인 후 적용 절차 (이 3줄이 전부)
1. `cp ~/.config/nats/nats.conf ~/.config/nats/nats.conf.bak`
2. `cp ~/notes/projects/agent-ops/relay/tickets/INFRA-9/nats.conf.listen-127.0.0.1 ~/.config/nats/nats.conf`
3. `systemctl --user restart nats` → 검증: ss 127.0.0.1만 / relay98 "durable 구독 완료" 로그 / 8024 whoami 정상

## 롤백
- 설정 파일 원복 후 재시작(JetStream 저장소 영향 없음 — 백업본 그대로)
