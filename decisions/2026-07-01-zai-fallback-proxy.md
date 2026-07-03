# 2026-07-01 — Z.ai 529 과부하 자동 폴백 프록시 + 텔레그램 알림

## 배경 / 원인 진단
이사님이 텔레그램 봇들에서 겪는 반복 `529` 에러. 진단(같은 날 직접 API 테스트로 확정):
- 529는 텔레그램이 아니라 **Z.ai LLM 게이트웨이 과부하** (`529 [1305]`).
- **원인 = `glm-5.2` 백엔드만의 포화.** 핵심 증거:
  - tiny 요청(6토큰)은 glm-5.2 포함 전 모델 200 통과 → RPM/TPM 한도 아님.
  - **glm-4.6으로 큰 요청(67KB) 4회 연속 → 전부 200** → TPM 전역 공유 아님, 모델별 백엔드 분리.
  - 반면 봇의 **큰 컨텍스트 요청만 glm-5.2에서 529** → glm-5.2 백엔드가 큰 prefill에 포화/용량 한계.
- 4개 봇이 **같은 Z.ai 키 + 같은 glm-5.2** 공유 → 백엔드 포화 순간 전부 동시 529 ("다른 봇도 안 됨").
- 백오프(4회)로 안 뚫림 → 일시적이 아니라 지속적 과부하.
- 기존 reaper(고아세션 정리)는 무관 — 유령세션 0인데도 529 반복. (이사님 예전 "컨텍스트 소모" 직관이 정답.)

## 결정
**로컬 폴백 프록시 도입.** cokacdir가 띄운 Claude Code 와 Z.ai 사이에 끼워, 529/503/429 시 자동으로 다른 백엔드 모델(`glm-4.6`)로 회피 + 백오프(1·2·4·8s) 재시도. A(재시도) + B(모델 교체)를 하나로 합침.

## 산출물 / 구성 (전부 적용 완료)
- 프록시 본체: `~/scripts/zai-fallback-proxy.js` (Node, 의존성 0)
- systemd 서비스: `~/.config/systemd/user/zai-proxy.service` (`systemctl --user`, cokacdir보다 먼저 기동 `Before=`, `Restart=always`)
- **폴백 설정 (systemd Environment):**
  - `FALLBACK_MODEL=glm-4.6` ← 529 시 회피 모델 (glm-5.2보다 품질 약간 낙후; 회피용).
  - `OVERLOAD_MODELS=glm-5.2,glm-5.1,glm-5.2[1m],glm-5-turbo` ← 이 모델들이 529면 폴백 대상.
  - `MAX_ATTEMPTS=4`, 백오프 1·2·4·8s.
- **설정 적용 지점: `~/.claude/settings.json` `env.ANTHROPIC_BASE_URL = http://127.0.0.1:8788`** (백업 `settings.json.bak-zai-proxy-20260701`). AUTH_TOKEN/모델/타임아웃 그대로.
- 로그: `~/.local/state/cokacdir/zai-fallback-proxy.log`

## 동작
- 2xx: Z.ai로 relay + 응답 pipe (스트리밍 통과, 지연 최소).
- 529/503/429: 본문 model이 OVERLOAD_MODELS에 해당 → `glm-4.6` 치환 + 백오프 재시도. 성공 시 `RECOVERED`. 전부 실패 시 `GAVE-UP`(원본 응답 반환).
- **폴백은 해당 요청 1회 한정(일회성).** 다음 요청은 다시 원본 모델(glm-5.2) 우선 → 백엔드 회복 시 자동 복귀.
- **실증 로그:** `OVERLOAD glm-5.2 529 → FALLBACK → glm-4.6 → RECOVERED 200`.

## 텔레그램 폴백 알림
폴백 발생 시 이사님 개인 채팅(`NOTIFY_CHAT=8315615299`, `heav_lnx_bot`)으로 알림. 봇 토큰은 `~/.cokacdir/cokacctl.json` tokens[0] 재사용(평문 비밀 추가 없음).
- 알림 내용: 모델 회피 정보 + **요청 KB + 입력/출력 토큰 수**(응답 usage에서 추출) + 최근 90초 복구 횟수.
- 빈도: RECOVERED는 첫 폴백 즉시 + 이후 90초 배치(`NOTIFY_BATCH_MS`). GAVE-UP는 분 단위 중복 억제 후 즉시.
- **제약:** 4개 봇이 같은 Z.ai 토큰을 써서 "어느 봇 요청인지" 식별 불가 → 통합 알림(모델/시간/토큰은 표시, 봇 식별 생략).

## 한계 / 후속
- 폴백 응답은 glm-4.6 품질. glm-5.2 작업이 잦으면 응답 품질 하락 체감 → `FALLBACK_MODEL=glm-5.1` 변경 또는 `/model` 봇별 분산 검토.
- Z.ai 백엔드 전역 다운이면 프록시도 못 살림(외부).
- 롤백: settings.json BASE_URL을 `https://api.z.ai/api/anthropic`로 복구(또는 백업 복원) + `systemctl --user disable --now zai-proxy`. AUTH_TOKEN은 프록시가 저장 안 하므로 즉시 직접 연결 복귀.
