# 긴급 상황 — 2026-07-06 16:02:41 KST
## 봇: manager

### 상황
- 원인: context 12.8% (>70% check 임계 또는 트리거 에러)
- 마지막 작업: ctx-evac check 완료: /home/ubuntu/notes/checkpoints/checkpoint-manager-2026-07-06_160241.md
- 감지 시점: 2026-07-06 16:02:41 KST
- 후속 판정: **ctx-evac Stop 훅 오탐**. 실제 70% 초과가 아니라 Stop 훅 JSON 안의 `429/529/quota` 문자열 단순 검색 가능성이 원인.
- 조치: 2026-07-06 16:32 `ctx-evac.sh` 패치 완료. Stop 훅 stdin은 drain만 하고 트리거 판정에서 제외.

### 상태
- LLM 호출: 가능
- 복구 모드: 오탐 해제
- 세션: 강제 종료 불필요. 단, 큰 세션은 별도 판단으로 `/clear` 권장 가능.

### 보존된 작업
- 조사 기록: /home/ubuntu/notes/checkpoints/checkpoint-ctx-evac-false-positive-2026-07-06_1632.md

### 복구 지침
1. 이 emergency는 16:32 조사로 오탐 확인됨.
2. `ctx-evac.sh check` 수동 검증 결과: 정상(15.8%), 백업 생략.
3. 향후 실제 70% 초과 또는 명시적 `CLAUDE_ERROR`/`ERROR_MESSAGE` 발생 시에만 emergency 취급.

### 기술 정보
- 호스트: ip-172-26-2-127
- PID: 275020
- 사용자: ubuntu
