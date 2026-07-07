# GLM/Claude 컨텍스트 폭발 조사 — hidden context/tool_result 누적

- 일시: 2026-07-07 KST
- 담당: Codex 감사봇
- 대상 사고:
  - 시나리오 팀장 context window limit
  - RPG 팀장 context window limit

## 결론

이사님이 본 Telegram 대화 파일 자체가 큰 것이 아니라, Claude/GLM 요청 조립 단계에서 아래 항목이 합쳐져 실제 컨텍스트가 커지는 패턴이 확인됐다.

1. Claude transcript JSONL의 `tool_result`
2. edit/write 도구 결과의 숨은 `toolUseResult`
3. `originalFile`, `content`, `structuredPatch`, `oldString/newString` 등 파일 원문/패치 데이터
4. assistant thinking/tool_use 기록
5. Stop hook 출력과 recovery/checkpoint 관련 문맥

즉, `~/.cokacdir/ai_sessions/*.json`은 사용자에게 보이는 대화 백업에 가깝고, 실제 모델 요청 컨텍스트의 크기를 대표하지 않는다.

## 근거 수치

### RPG 팀장 사고

- ai_session: 약 39KB / 16 turns
- Claude transcript: 약 808KB / 201 lines
- 마지막 정상 usage:
  - input: 5,457
  - cache_read: 140,288
  - 총 context 추정: 145,745 tokens
- 128k 실효 기준: 113.9%
- 이후 `<synthetic>` 에러: `API Error: The model has reached its context window limit.`

### 시나리오 팀장 사고

- ai_session: 약 71KB / 41 turns
- Claude transcript: 약 2.2MB / 1,113 lines
- 마지막 정상 usage:
  - input: 957
  - cache_read: 253,760
  - 총 context 추정: 254,717 tokens
- 128k 실효 기준: 199.0%
- 이후 `<synthetic>` 에러: `API Error: The model has reached its context window limit.`

## transcript 구성상 주요 비대화 요소

### 시나리오 transcript

- `user:tool_result`: 약 919KB, 39.9%
- `assistant:tool_use`: 약 502KB, 21.8%
- `assistant:thinking`: 약 436KB, 18.9%
- `assistant:text`: 약 215KB, 9.3%

### RPG transcript

- `user:tool_result`: 약 448KB, 55.5%
- `assistant:thinking`: 약 126KB, 15.7%
- `assistant:tool_use`: 약 95KB, 11.9%
- `assistant:text`: 약 57KB, 7.1%

## 핵심 원인

1. **대화 백업과 실제 모델 컨텍스트가 다르다.**
   - Telegram/ai_session만 보면 작아 보인다.
   - 실제 Claude transcript에는 도구 결과와 내부 결과물이 함께 남는다.

2. **파일 편집 도구 결과가 크다.**
   - 보이는 메시지는 짧아도 `toolUseResult`에 파일 원문, 구조화 패치, 기존/신규 문자열이 저장된다.
   - 한 줄의 transcript가 수십 KB가 되는 사례가 반복 확인됐다.

3. **GLM 프록시의 `contextWindow=1,000,000` 표시는 실효 방어 기준으로 부적합하다.**
   - 실제 사고는 약 145k, 255k context 근처에서 발생했다.
   - 따라서 1M 기준 미터는 14~25%로 오판할 수 있었다.

4. **기존 `context-meter`는 마지막 `<synthetic>` 에러 usage=0을 잡는 허점이 있었다.**
   - 사고 직후 측정 시 0%처럼 보일 수 있었다.

5. **구버전 Stop hook `chat-backup.py`가 `/home/ubuntu/notes/chat-backups`에 raw 백업을 만들고 hook 출력도 남겼다.**
   - Git 관리 영역을 더럽히고 transcript 노이즈를 늘릴 수 있었다.

## 조치 완료

1. `/home/ubuntu/scripts/context-meter.sh`
   - 기본 한계를 1,000,000이 아니라 128,000 effective로 변경.
   - `<synthetic>` API 에러 또는 usage=0 행은 무시하고 마지막 정상 usage를 사용하도록 수정.

2. `/home/ubuntu/scripts/ctx-evac.sh`
   - Stop hook stdin의 `transcript_path`를 읽어 정확한 transcript를 측정하도록 수정.
   - byte fallback 기준을 0.75MB≈70%로 낮춤.
   - fallback 설명 문구도 0.75MB 기준으로 정정.

3. `/home/ubuntu/scripts/chat-log-backup.py`
   - `--quiet` 옵션 추가.
   - Stop hook에서는 summary 출력을 억제해 transcript 노이즈를 줄이도록 변경.

4. `/home/ubuntu/.claude/settings.json`
   - 구버전 `python3 /home/ubuntu/scripts/chat-backup.py` hook 제거.
   - 신형 `/home/ubuntu/scripts/chat-log-backup.py --root /home/ubuntu/chat_logs ... --quiet` hook으로 교체.

5. Git 보존 사본
   - `/home/ubuntu/notes/setup/server/context-meter.sh`
   - `/home/ubuntu/notes/setup/server/ctx-evac.sh`
   - `/home/ubuntu/notes/setup/server/chat-log-backup.py`

## 운영 권고

1. GLM 계열은 당분간 128k effective 기준으로 방전한다.
2. 70% 초과 시 checkpoint 작성 후 세션 clear 권고.
3. 큰 파일 원문/대량 로그를 도구 결과로 그대로 뿌리지 않는다.
4. edit/write 도구가 큰 `toolUseResult`를 남기므로, 큰 문서는 부분 편집/파일 기반 요약을 우선한다.
5. `ai_sessions` 백업은 복구용으로 유효하지만, 컨텍스트 한계 판단은 Claude transcript 기준으로 한다.

