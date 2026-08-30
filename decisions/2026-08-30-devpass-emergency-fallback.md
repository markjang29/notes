# ADR — DevPass(llmgateway) 비상 우회 회선 추가 (2026-08-30)

- 결정: 이사님 구독 DevPass를 zai-fallback-proxy(8788)의 **최후 폴백 회선**으로 추가.
- 배경: z.ai GLM 529 시 전 봇 마비. 기존 폴백(glm-5.2→5.1→4.6)은 같은 z.ai 안이라 본사 장애엔
  무력. 이사님 08-30 지시 "glm 529 로 터졌을 때 저기 쓸 수 있게" + 봇 분리 문의.
- 선택: 봇 분리 대신 **공동 프록시에 비상 홉** — 전 봇에 일괄 적용, 수동 스위치 불필요.

## 구조 (5단계)

1. z.ai glm-5.2[1m] (평소) → 2. 529: glm-5.2 → 3. glm-5.1 → 4. glm-4.6 →
5. **전부 실패 → DevPass glm-5.3 → gpt-5-mini → gpt-5** (Anthropic 호환, 모델 자동 치환)

## 구현

- `~/scripts/zai-fallback-proxy.js`: `tryDevpassRescue()` — GAVE-UP 직전 실행, Authorization만
  DevPass 토큰으로 교체(클라이언트 z.ai 토큰은 대체). `DEVPASS_FORCE=1`이면 z.ai 건너뛰고
  우회 검증(헬스체크용).
- 키: `~/.cokacdir/devpass.env` (0600, Git 밖) → systemd drop-in
  `zai-proxy.service.d/devpass.conf`가 EnvironmentFile로 주입. **키는 코드·Git·로그·보고에 없음.**
- 미설정 시 홉 완전 비활성(현행 동작 불변).

## 검증 (2026-08-30)

- 직접 API: glm-5.3·gpt-5-mini 정상 응답.
- 8789 테스트 인스턴스 DEVPASS_FORCE: `glm-5.2[1m]` → DEVPASS-RESCUED → glm-5.3 200.
- 운영 8788 재기동 후 STARTED 로그 `devpass=... chain=[glm-5.3,gpt-5-mini,gpt-5]` 확인,
  정상 경로 응답(매니저 세션 자체가 실측).

## 갱신 (2026-08-30, 이사님 지시) — 허락제 쿠폰 전환

- **자동 우회 폐지.** 안정화까지 DevPass는 이사님 허락제: 이사님이 지정 단어를 말하면
  매니저가 `scripts/devpass-coupon.sh <시간>`으로 쿠폰 발행(~/.cokacdir/devpass-coupon.exp,
  만료 EPOCH ms) → 그 시간 동안만 8788 프록시가 DevPass 우회 허용. 만료·폐기(off) 즉시 반영.
- 코드: `devpassActive()`가 쿠폰 파일 검사 후에만 우회/FORCE 동작. 쿠폰 없으면 DevPass 환경변수가
  있어도 완전 잠금. 발행·폐기 시 로그(DEVPASS-COUPON ON/OFF) 기록.
- 발행 시 매니저는 이사님께 만료 시각 포함 보고. 현재 상태: **잠금(쿠폰 없음)**.

## 남은 것

- 이사님 지정 단어 확정(제안: "비상구") · 실전 발동 시 최초 검증(텔레그램 🛟 알림) ·
  코덱스(OpenAI 호환) 쪽 동일 회선 확장.
