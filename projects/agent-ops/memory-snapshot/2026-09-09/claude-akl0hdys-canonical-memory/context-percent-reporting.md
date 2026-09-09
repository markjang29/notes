---
name: context-percent-reporting
description: 매 답장 말미에 실측 컨텍스트(모델/한계/%) 부착 의무. 추정 금지, API 실측 usage 사용.
metadata:
  type: feedback
---

이사님 2026-06-30 최초 요구("컨텍스트 % 안줘?") → 2026-07-02 강화: **매 답장 말미에 현 사용 모델명/한계토큰/퍼센트**를 실측으로 부착. 추정치 사용 중단.

**Why:** 이사님이 텔레그램 대화에서 컨텍스트가 너무 빨리 찬다고 느꼈고, 정합성(실제 토큰/Byte)을 요구. 추정 %는 200K/1M 기준 혼선으로 신뢰 잃음.

**How to apply:**
- 매 답장 말미에 `~/scripts/context-meter.sh` 출력 부착.
- 측정원 = transcript JSONL 마지막 assistant usage의 `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` (API 실측값).
- 한계 = `CONTEXT_LIMIT_TOKENS` (기본 1,000,000).
- 형식: `📊 {모델}[1m] | 한계 {N} | {사용} ({%.1f}%) | {MB}`
- 위반(추정치/누락) 시 보고 불인정. 사칙: `~/notes/onboarding.md` § 매 답장 컨텍스트 보고.

**"빨리 차는" 진짜 원인(통찰):** 모델은 1M(glm-5.2[1m])이나 실제 운용 한계 200K 추정. 1M 기준 16%여도 200K 기준 80% → 체감 과충전. 한계 명시로 혼선 해소.

관련 [[context-explosion-causes]] · [[glm-proxy-environment]] · [[manager-recovery-principle]].
