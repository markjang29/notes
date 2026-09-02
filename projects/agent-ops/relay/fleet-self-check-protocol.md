# 봇 플릿 셀프 점검 프로토콜 (전 봇 공통)

> 주관: novel_col (이사님 2026-09-02 지시 — "모델들은 사이트를 참고해 자기 모델·API 변경 및 셀프 점검, 점검일 업데이트")
> 기준 페이지: http://13.125.131.126:8018/novel-plan 🛡 봇 플릿 현황 섹션

## 각 봇은 언제 점검하나

- 8018 플릿 표에 자기 이름 옆 **"점검지시"** 배지가 떠 있을 때
- 세션 시작 직후 (주 1회 권장)
- provider(게이트웨이↔Z.ai)·전역 모델 매핑이 바뀐 직후

## 점검 절차 (4단계)

1. **현황 읽기**: `curl -s http://127.0.0.1:8018/api/bot-fleet`
   - `gateway.provider` — `gateway`(LMM Gateway) / `zai`(Z.ai 직접) 확인
   - `gateway.model_map` — haiku/sonnet/opus → GLM 매핑 확인
   - 자기 봇의 `models` 필드 — 채팅별 모델 지정 확인
2. **자기 확인**:
   - 이 세션이 응답 중 = API 경로 정상 (게이트웨이 or Z.ai)
   - 내가 쓸 모델이 매핑과 일치하는지 (codex 계열은 bot_settings models)
3. **자기 변경 (필요시)**: 모델 지정/해제는 8018 플릿 표 드롭다운 또는
   `bot_settings.json` 자기 `models` 필드 — 변경은 다음 세션부터 적용
4. **결과 보고**:
   ```
   curl -s -X POST http://13.125.131.126:8018/api/bot-fleet -H "Content-Type: application/json" \
     -d '{"action":"check_report","bot":"<자기 display_name>","status":"ok|fail","model":"<모델>","provider":"<provider>","detail":"<한 줄>"}'
   ```
   → 점검일이 8018 표에 자동 갱신되고 "점검지시" 배지가 해제됨.

## provider 전환 (이사님 전용 — 전 봇 영향)

- 🛡 Gateway ↔ ⚡ Z.ai 직접(`https://api.z.ai/api/anthropic`) 전환은 8018 버튼.
- Z.ai 직접은 **Z.ai API 키** 필요 (docs.z.ai/devpack/quick-start 발급).
- 양쪽 자격증은 `matrix-home/fleet_providers.json`(git 제외)에 보존 — 왕복 전환 가능.
- 적용 시점: **신규 세션부터** (진행 중 세션은 기존 연결 유지).

## 상태판정

- 🟢 ok — 매핑·응답 정상
- 🔴 fail — 응답 불가·매핑 불일치 → detail에 증상, 이사님 보고
- 미기록(—) — 아직 점검 전

## 기록

- 2026-09-02 novel_col 최초 점검 ok (gateway·glm-5.3) — 프로토콜 시범 적용.
