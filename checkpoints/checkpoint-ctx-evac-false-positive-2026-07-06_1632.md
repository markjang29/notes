# ctx-evac 오탐 조사 및 수정 — 2026-07-06 16:32 KST

## 증상

매니저 세션에서 컨텍스트가 낮은데도 emergency/checkpoint가 생성됨.

관측 예:

- 2026-07-06 07:02 — `컨텍스트 3.7%`인데 강제 방전
- 2026-07-06 00:21 — `18.9%`인데 강제 방전
- 2026-07-06 16:02 — `12.8%`인데 emergency 생성

메시지는 `>70% check 임계 또는 트리거 에러`라고 표시됐으나, 실제 측정 퍼센트는 임계 미만.

## 원인

`/home/ubuntu/scripts/ctx-evac.sh check`가 Stop 훅 stdin 전체 JSON을 `TRIGGER_TEXT`에 포함하고 있었다.

그 결과 UUID, skill 목록, 일반 메시지, 로그 등에 포함된 `429`, `529`, `quota` 문자열이 실제 장애가 아닌데도 `is_trigger_error`에 걸릴 수 있었다.

즉, 실제 컨텍스트 초과라기보다 **트리거 에러 판정 오탐**이었다.

## 수정

`ctx-evac.sh`에서 Stop 훅 stdin은 drain만 하고, 트리거 판정에는 넣지 않도록 변경했다.

변경 후 `TRIGGER_TEXT`는 명시 인자와 환경변수만 사용:

- script args
- `CLAUDE_ERROR`
- `ERROR_MESSAGE`

## 검증

수동 실행:

```bash
bash /home/ubuntu/scripts/ctx-evac.sh check
```

결과:

```text
[2026-07-06 16:32:25] [ctx-evac] 정상(15.8%). 백업 생략.
```

새 checkpoint/emergency가 생성되지 않았다.

## 남은 관찰

컨텍스트 오탐과 별개로, 일부 transcript에는 누적 token-report가 수천만 단위로 찍힌다.

예:

- `d6809134-...` 세션 token-report 총 22M+
- 원인 후보: 오래된 세션 resume 반복, `cron --session` 재사용, 큰 tool_result 적재, recovery/work-queue 주입 반복

따라서 오탐 수정과 별개로 큰 세션은 `/clear` 또는 신규 세션 전환 권장.

## 추가 확인 — 실제 GLM context window limit 별도 발생

이사님이 제공한 실행 결과에서 실제 API 에러 확인:

```text
result: API Error: The model has reached its context window limit.
session_id: 344f87ea-b159-4fc6-b0e2-7d784db3e589
model: glm-5.2[1m]
contextWindow: 1000000
usage.input_tokens: 93
usage.cache_read_input_tokens: 137536
```

판정:

- `ctx-evac`의 낮은 퍼센트 emergency는 오탐이 맞다.
- 그러나 `344f87ea-...` 세션에서 **GLM API의 실제 context window limit 에러도 별도로 발생**했다.

usage가 137k 수준인데 context limit 에러가 난 이유 후보:

1. 에러 경로의 usage는 전체 요청 payload가 아니라 마지막/부분 시도만 기록됐을 수 있다.
2. context-meter는 transcript의 마지막 성공 usage를 읽으므로, 다음 요청 조립 시 들어가는 system/recovery/tool_result 전체 payload를 과소평가할 수 있다.
3. 해당 세션은 사칙/온보딩/시나리오 문서/RisuAI 소스 `Read` 결과 등 큰 tool_result가 누적되어 실제 직렬화 payload가 모델 한계를 넘었을 가능성이 있다.

추가 결론:

- 예방은 퍼센트만 볼 게 아니라 `API Error: The model has reached its context window limit` 문자열 자체를 실제 장애로 취급해야 한다.
- 큰 `Read`/tool_result는 메인 세션에 누적하지 말고 파일분리·요약·신규 세션 전환을 기본값으로 한다.
