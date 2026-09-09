---
name: devpass-coupon-gate
description: DevPass(llmgateway) 비상 우회는 이사님 허락제 — 특정 단어 시에만 매니저가 X시간 쿠폰 발행 (2026-08-30 지시)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cce3341b-14d0-489d-b80d-ff5fde73af91
  modified: 2026-08-30T12:47:39.712Z
---

이사님 2026-08-30 지시: LLM 게이트웨이(DevPass) 폴백은 **당분간 안정화될 때까지 이사님 허락 받고만**
사용. 이사님이 특정 단어를 말하면 그때만 X시간 쿠폰이 발행되는 방식.

**Why:** 유료 구독 회선을 봇들이 자동으로 쓰는 것에 대한 비용·통제 우려. 허락 없는 사용 방지.

**How to apply:**
- 8788 프록시(`~/scripts/zai-fallback-proxy.js`)의 DevPass 우회는 `~/.cokacdir/devpass-coupon.exp`
  (만료 EPOCH ms) 파일이 유효할 때만 동작(쿠폰 게이트). 현재 기본 = 잠금.
- 이사님 지정 단어 **"게웨"** 확정(08-30). "게웨" = 2시간 기본, "게웨 4" = 4시간, "게웨 닫아" = 즉시 잠금.
  들으면 `bash ~/scripts/devpass-coupon.sh <시간>` 발행 후 만료 시각을 이사님께 보고. 상태 확인 = `status`.
- 발행·사용은 ADR `notes/decisions/2026-08-30-devpass-emergency-fallback.md` 참조.
- 관련 [[glm-proxy-environment]] · [[manager-recovery-principle]].
