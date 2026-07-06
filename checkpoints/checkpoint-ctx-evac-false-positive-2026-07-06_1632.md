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

