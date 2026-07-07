# Checkpoint — 시나리오 팀장 context window limit 사고

일시: 2026-07-07 12:31 KST  
대상: `heav_lnx_scenario_bot` / 시나리오 팀장  
세션: `d0a2acb0-35d4-4087-89bd-9401f83f01d8`  
상태: 조사·백업·Git 보존 확인 완료

## 현상

시나리오 팀장이 이사님 `ㄱㄱ` 지시 직후 응답하지 못하고 아래 에러로 종료.

```text
API Error: The model has reached its context window limit.
model: glm-5.2[1m]
contextWindow: 1000000
inputTokens/cacheReadInputTokens/outputTokens: 0
```

## 직전 맥락

직전 성공 응답에서 시나리오 팀장은 다음을 보고했다.

- 이사님 피드백 “특정 자산/캐릭터를 이사님이 아는 것처럼 말하지 말 것”을 상위 규칙으로 반영
- notes commit `948b177`
  - `principles/scenario-team-purpose.md`
  - 사칙 5.1 “자산 사용 전 컨펌” 추가
- scenario commit `af3739f`
  - `drafts/matrix-meeting-2026-07-07.md`
  - 매트릭스 v1 회의록 + 이사님 최종 결정 반영
- 다음 작업 예정:
  - 야간 품질 다듬기 파이프라인 설계

## Git 보존 확인

확인 완료:

- notes: `948b177 사칙 5.1 추가 — 자산 사용 전 컨펌 상위 규칙`
- scenario: `af3739f 매트릭스 v1 회의록 + 이사님 최종 결정 반영`
- scenario repo working tree clean

notes repo에는 기존 자동 로그 변경만 남음:

```text
M .reviews/session-reaper.log
```

## 백업

수동 백업 실행 완료:

```text
/home/ubuntu/chat_logs/scenario/heav_lnx_scenario_bot/2026-07-07/12_00.part001.jsonl
```

읽기 쉬운 Markdown 백업 생성 및 이사님께 전송:

```text
/home/ubuntu/.cokacdir/workspace/r2meshwa/scenario_team_crash_backup_2026-07-07.md
```

## 원인 판단

ai_sessions 파일 크기는 약 71KB, history 41턴으로 겉보기에는 작다.  
그러나 GLM adapter가 `inputTokens=0`으로 실패했으므로, 실제 실패는 사용자 대화 JSON 크기만으로 설명되지 않는다.

가능성이 큰 원인:

1. Claude/GLM 프록시가 내부 transcript, hidden context, tool 결과, recovery context를 합쳐 요청을 조립하는 단계에서 초과.
2. token report/usage가 마지막 성공 또는 실패 직전 계측을 반영하지 못함.
3. 이전에도 동일하게 “표시 토큰은 낮은데 context window limit”이 발생한 패턴과 일치.

## 복구 권장

시나리오 팀장 세션은 계속 이어가기보다 `/clear` 후 복구하는 것이 안전하다.

복구 지시문:

```text
L0-agent-boot.md를 읽고 key c6a54f44dab7dfe7 = heav_lnx_scenario_bot = 시나리오 팀장임을 인증하라.
notes/principles/scenario-team-purpose.md의 5.1 자산 사용 전 컨펌 규칙을 확인하라.
scenario repo 최신 commit af3739f와 notes commit 948b177 이후 상태에서 이어가라.
직전 이사님 지시는 “야간 품질 다듬기 파이프라인 설계 ㄱㄱ”이다.
긴 대화 전체를 재독하지 말고, 필요하면 scenario_team_crash_backup_2026-07-07.md의 마지막 10턴만 참고하라.
```

