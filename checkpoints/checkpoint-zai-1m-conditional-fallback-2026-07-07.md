# Z.ai GLM 5.2 1M 조건부 fallback 적용

- 일시: 2026-07-07 KST
- 목적: 이사님 지시 — “1M을 쓰고 싶다”
- 대상:
  - `/home/ubuntu/.claude/settings.json`
  - `/home/ubuntu/scripts/zai-fallback-proxy.js`
  - `/home/ubuntu/.config/systemd/user/zai-proxy.service`

## 적용 정책

기본 모델을 `glm-5.2[1m]`로 두고, 1M을 실제 운영 기준으로 사용한다.

단, 표준 모델 백업은 완전히 제거하지 않고 **짧은 요청에만 조건부 허용**한다.

- 요청 크기 `<= 204800 bytes`: 1M 과부하 시 `glm-5.2` 표준 모델로 fallback 허용
- 요청 크기 `> 204800 bytes`: 표준 모델로 내리지 않고 `glm-5.2[1m]` 재시도

## 이유

표준 모델 fallback은 장애 대응 백업으로 의미가 있다.
하지만 긴 컨텍스트 작업에서 표준 모델로 몰래 내려가면 1M 사용 목적과 충돌한다.

따라서:

1. 짧은 작업은 가용성 우선
2. 긴 작업은 1M 보장 우선

으로 분리했다.

## 적용 값

### Claude settings

- `ANTHROPIC_DEFAULT_OPUS_MODEL=glm-5.2[1m]`
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`
- `CONTEXT_LIMIT_TOKENS=1000000`

### Z.ai proxy service

- `FALLBACK_MODEL=glm-5.2`
- `OVERLOAD_MODELS=glm-5.2[1m]`
- `STANDARD_FALLBACK_MAX_BYTES=204800`
- `MAX_ATTEMPTS=4`

## 동작 로그 키워드

- 짧은 요청 fallback: `FALLBACK-SHORT`
- 긴 요청 1M 고정 재시도: `RETRY-1M`

## 보존 사본

- `/home/ubuntu/notes/setup/server/zai-fallback-proxy.js`
- `/home/ubuntu/notes/setup/server/zai-proxy.service`

