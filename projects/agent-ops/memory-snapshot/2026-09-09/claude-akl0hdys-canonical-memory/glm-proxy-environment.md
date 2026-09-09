---
name: glm-proxy-environment
description: 실제 LLM 환경 구조 — ANTHROPIC_AUTH_TOKEN + 로컬 GLM 프록시(127.0.0.1:8788) + 모델 라우팅. 스크립트 작성 시 반드시 고려.
metadata:
  type: project
---

# GLM 프록시 환경 (실제 LLM 호출 구조)

2026-07-02 healthcheck 스킬 개발 중 발견.

## 환경 변수 (이 서버의 실제 값)

- **인증:** `ANTHROPIC_AUTH_TOKEN` (← `ANTHROPIC_API_KEY` 아님)
- **엔드포인트:** `ANTHROPIC_BASE_URL=http://127.0.0.1:8788` (로컬 GLM 프록시)
- **모델 라우팅:**
  - `ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-4.7`
  - `ANTHROPIC_DEFAULT_SONNET_MODEL=glm-5.1`
  - `ANTHROPIC_DEFAULT_OPUS_MODEL=glm-5.2`

## 핵심 의미

- 이사님이 말한 **"라우팅해서 모델 바꾸는 거"** = 위 환경 변수로 Anthropic 호환 호출을 GLM 모델로 매핑.
- 레이트 리밋(529/429)은 **GLM 프록시 뒤에서 발생**.
- Claude 모델 ID(`claude-haiku-4-5-...`)를 하드코딩하면 안 됨 → 환경 변수 사용.

## 스크립트 작성 규칙 (★)

LLM 호출 스크립트는 반드시:
1. 인증: `ANTHROPIC_AUTH_TOKEN` 우선, fallback `ANTHROPIC_API_KEY`
2. 엔드포인트: `${ANTHROPIC_BASE_URL:-https://api.anthropic.com}`
3. 모델: `${ANTHROPIC_DEFAULT_HAIKU_MODEL:-claude-haiku-4-5-20251001}` 등
4. curl 헤더: `x-api-key` + `Authorization: Bearer` 둘 다 (GLM 프록시 호환)

이 규칙 안 지키면 full mode 헬스체크가 api.anthropic.com으로 가버림.

## 폴백 정책 한계 (A안)

같은 GLM 프록시 뒤의 glm-5.2/glm-5.1/glm-4.7로 폴백 → **같은 레이트 리밋 풀**이면 폴백도 동시 429/529 가능.
→ `AdaptiveModelRouter`는 모델별 풀이 다르다는 가정(A안). **B안(직접 endpoint/다른 key 우회)은 대기 결정.**

## 설정 실체 (2026-07-02 검증 완료)

**위치:** `/home/ubuntu/.claude/settings.json` → `env` 블록. 모든 봇이 **동일 매핑** (bot_settings.json `models`는 전부 빈 `{}`, 봇별 오버라이드 없음).

| Claude 슬롯 | 실제 GLM | 동시성 |
|------------|---------|--------|
| Opus | glm-5.2 | 10 |
| Sonnet | glm-5.1 | 10 |
| Haiku | glm-4.7 | **2** |

**"Haiku" 실체 = glm-4.7, 동시성 2.** 이사님 2026-07-02 지적: "haiku haiku 하는데 실체가 뭔지 알아야." → 이제 명확.

## 프록시 폴백 시스템 (★ 진실의 1차 방어선 — 재발명 금지)

`~/scripts/zai-fallback-proxy.js` (2026-07-01 ADR, systemd `zai-proxy.service`, 127.0.0.1:8788).

- **과부하 감지(OVERLOAD_MODELS):** glm-5.2, glm-5.1, glm-5.2[1m], glm-5-turbo → 529/503/429 시
- **폴백 대상(FALLBACK_MODEL):** **glm-4.6** (동시성 3)
- 텔레그램 자동 알림(이사님), 로그 `~/.local/state/cokacdir/zai-fallback-proxy.log`
- **★ 내 AdaptiveModelRouter는 사실상 dead code** — 프록시가 1차에서 529를 잡아 4.6으로 넘기면 앱은 200만 받음. 중복. 관측용으로만.
- **529 주범 = 큰 요청(729KB~).** 컨텍스트 관리가 곧 529 예방.
- **FALLBACK_MODEL 4.6→4-plus 보류(2026-07-02):** 4-plus 컨텍스트 한계 미확정. 4.6이 729KB 처리 검증됨. 동시성만 보고 바꾸면 큰 요청이 4-plus에서 터질 위험.

## 동시성 기준 폴백 정책 (이사님 2026-07-02)

GLM 공식: **concurrency limit** = 동시 실행 요청 수 (RPM 아님). 동시성 표 `~/scripts/healthcheck/glm_concurrency.json`.

- **정책:** 동시성이 클수록 폴백 유리. 동시성 ≤2는 폴백 체인에서 **제외** (역효과).
- **폴백 체인(앱 계층, 프록시 후 2차):** `['glm-5.2', 'glm-5.1', 'glm-4-plus']`. **glm-4.7(2) 자동 제외**.
- 단, 프록시가 1차 폴백하므로 앱 체인은 거의 발동 안 함 — 관측/보조 위치.

관련 [[manager-recovery-principle]] · [[current-work-state]] · [[context-percent-reporting]].
