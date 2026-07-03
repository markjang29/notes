# cokacdir recovery bundle 재설계 검토

작성: 2026-07-01 KST  
검토 대상: Telegram 봇 + Claude Code hooks + git/notes 기반 세션 복구

## 현황 진단

실제 소스 기준으로 `~/.claude/settings.json`에는 `SessionStart` 훅 4종(`startup`, `clear`, `resume`, `compact`)과 `UserPromptSubmit` 훅이 모두 `/home/ubuntu/.claude/hooks/cokacdir-recovery-gate.sh`를 호출하도록 등록되어 있다.

현재 hook 스크립트는 매니저 세션만 대상으로 삼는다. `cwd`가 `*/.cokacdir/workspace/*`인 경우에만 복구 게이트를 적용하고, 팀장/기타 cwd는 no-op으로 종료한다. 매니저 세션에서는 `MEMORY.md`, `current-work-state.md`, `~/notes/work-queue.md` 3파일을 읽어 `SessionStart.additionalContext`로 주입하고, 성공 시 `~/.claude/recovery-gate/$session_id.ok`를 남긴다. `UserPromptSubmit`은 이 `.ok`가 없으면 프롬프트를 차단한다.

장애 로그도 원인과 맞다. `/home/ubuntu/.cokacdir/schedule_history/D3AF1AE1.log`와 `3CD0408F.log`에서 cron 실행 cwd는 `/home/ubuntu/.cokacdir/workspace/20bkmfvt`였고, 응답은 `UserPromptSubmit operation blocked by hook`이었다. 즉 cron 자체가 미발화한 것이 아니라, 매니저 workspace에서 시작된 cron 프롬프트가 recovery gate의 fail-closed 경로에 걸렸다.

단, 현재 디스크의 hook은 `COKACDIR_RECOVERY_MAX_BYTES` 기본값이 이미 `20000`으로 올라가 있다. 현재 3파일 합계도 `10218B`다. 따라서 "9000B 한계 초과"는 사고 당시 상태 또는 과거 정책에 대한 진단으로 보아야 한다. `notes/decisions/2026-06-30-recovery-gate-bundle-shrink.md`에는 사고 당시 `10503B > 9000B`, 특히 `work-queue.md`가 70%였다고 기록되어 있고, 그 후 축소 및 정책 조정이 있었던 상태다.

핵심 문제는 컨텍스트 윈도우가 아니다. 1M 컨텍스트에서 2.5K~3K 토큰은 작다. 문제는 "주입된 내용을 모델이 감당하느냐"가 아니라, hook이 정한 byte guard를 넘으면 `SessionStart`가 `.ok`를 만들지 않고, 그 결과 `UserPromptSubmit`이 모든 운영 프롬프트를 차단하는 구조다.

## 1. 계층 구조가 gate 문제를 확실히 푸는가

대체로 푼다. L1을 항상 byte guard 아래로 유지하고, `.ok` 판단도 L1 주입 성공만으로 하도록 바꾸면 gate 문제의 직접 원인은 제거된다.

중요한 조건은 "L2/L3를 읽지 않았다는 이유로 UserPromptSubmit을 막지 않는 것"이다. 현재 게이트의 의미는 "세션이 운영상 최소 복구 상태에 도달했는가"다. 그러므로 L1은 다음 정보를 포함해야 한다.

- 매니저 정체성, 팀장/프로젝트 바인딩, 현재 운영 모드
- 활성 작업과 대기 결정의 초압축 요약
- canonical notes/git 경로
- 복구 절차: 언제 `~/notes/work-queue.md`를 Read해야 하는지
- 안전 경계: 승인 필요 작업, cron/야간 작업의 허용 범위

반대로 `work-queue.md` 전체, 과거 상세, ADR 본문, 긴 회의록은 L1에 넣으면 안 된다. L1이 "복구 완료의 증명"이고 L2/L3가 "업무 수행 중 필요한 근거"가 되어야 한다.

다만 "확실히"라는 말에는 운영상 주의가 붙는다. L1이 수작업 요약이면 시간이 지나면서 stale해질 수 있다. 따라서 L1은 수동 요약 파일 하나에 의존하기보다, 가능하면 `work-queue.md`의 작은 front matter/상단 섹션을 canonical L1으로 삼거나, hook이 `head`/마커 섹션만 잘라 읽는 방식이 낫다.

## 2. SessionStart/recovery-gate 구현 시 주의점과 단순화

첫째, `.ok`의 의미를 축소해야 한다. 현재는 3파일 전체 주입 성공이 `.ok` 조건이다. 재설계 후에는 "L1 bootstrap 주입 성공"만 `.ok` 조건으로 삼고, L2/L3는 모델 지시와 운영 규칙으로 처리한다. 이렇게 해야 L2가 커지거나 ADR이 늘어도 게이트가 다시 장애점이 되지 않는다.

둘째, hook의 byte 검사는 실제 주입 문자열 기준이어야 한다. 현재는 파일 3개 크기 합산을 검사한 뒤 헤더까지 붙여 주입한다. L1 구조로 바꾸면 `BUNDLE` 생성 후 `wc -c`를 재거나, L1 파일 자체를 고정 상한으로 관리하는 편이 더 명확하다.

셋째, fail-closed 범위를 세분화할 필요가 있다. 매니저의 대화형 운영은 fail-closed가 맞지만, cron은 같은 강도로 막으면 자동 운영 전체가 멈춘다. 최소한 차단 사유와 세션 id, bundle bytes, cwd, source를 로그/Telegram에 더 짧고 명확히 남겨야 한다.

넷째, 현재 cwd 스코프 가드는 유지하되, "매니저가 항상 `.cokacdir/workspace/*`에서 뜬다"는 가정은 ADR에 남기고 주기적으로 검증해야 한다. 소스상 이 가정이 깨지면 게이트가 우회된다.

다섯째, hook을 단순화하려면 L1 파일을 하나로 분리하는 편이 좋다. 예: `~/.claude/.../memory/recovery-bootstrap.md` 또는 `~/notes/memory/recovery-bootstrap.md`. 이 파일은 4KB 이하 강제, 안에는 포인터만 둔다. `MEMORY.md` 전체와 `current-work-state.md` 전체를 매번 합치는 구조보다 실패면이 작다.

## 3. L1/L2/L3 대신 COKACDIR_RECOVERY_MAX_BYTES 상향만 하는 방안

상향은 응급처치로는 합리적이다. 실제 현재 hook도 기본값이 `20000`으로 올라가 있어 현 10218B 번들은 통과 가능하다. 운영 중인 자동 cron을 즉시 살리는 목적이라면 가장 작고 빠른 변경이다.

하지만 단독 해법으로는 약하다. `work-queue.md`는 활성 작업과 기록이 쌓이는 파일이라 계속 커진다. 9000을 20000으로 올리면 오늘의 장애는 풀리지만, 나중에 20000을 넘으면 같은 형태로 재발한다. 더 큰 문제는 매 턴 주입되는 텍스트가 업무 상세까지 포함하면서 컨텍스트 잡음과 역할 혼동을 계속 만든다는 점이다.

계층화는 구조적 해법이다. gate의 성공 조건을 작은 L1으로 고정하고, 상세는 필요 시 Read하게 만들어 번들 크기 증가와 게이트 실패를 분리한다. 비용은 구현 복잡도와 L1 최신성 관리다. 그러나 현재 장애의 원인이 "크기 초과가 운영 차단으로 전파됨"이므로, 장기적으로는 계층화가 더 직접적인 대책이다.

권장 트레이드오프는 둘을 조합하는 것이다. `MAX_BYTES=20000` 같은 넉넉한 안전판은 유지하되, 실제 L1 목표는 4KB~6KB 이하로 둔다. 이렇게 하면 L1이 조금 늘어도 장애로 바로 이어지지 않고, 상향값은 임시 여유분으로만 기능한다.

## 4. cron 세션만 gate 우회하는 방안

부분적으로 합리적이지만, 단독으로는 위험하다.

cron 프롬프트가 "이미 구체적으로 닫힌 작업"이라면 복구 게이트를 완전히 통과하지 않아도 된다. 예를 들어 특정 파일을 읽고 요약 보고하는 아침 브리프는 프롬프트 안에 필요한 입력이 명시되어 있다. 이런 경우 gate 때문에 전체 자동 운영을 멈추는 것은 손해가 크다.

그러나 현재 cron은 단순 알람이 아니라 매니저 권한으로 팀장에게 작업을 배정하고 `work-queue.md`를 갱신하며, 승인 경계를 판단한다. 이 작업은 매니저 정체성, 팀장 바인딩, 승인 금지선 같은 L1 복구 정보가 필요하다. cron을 무조건 우회하면 "제로 상태 매니저"가 팀장에게 잘못된 지시를 내릴 수 있다.

따라서 더 합리적인 방식은 cron 전면 우회가 아니라 "cron-safe L1"이다.

- cron도 L1 bootstrap은 반드시 받는다.
- L1 실패 시 cron은 운영 실행을 하지 않고, 짧은 장애 보고만 남긴다.
- L1 성공 후에는 L2 전체 주입 여부와 무관하게 진행한다.
- cron 프롬프트 자체에 필요한 Read 대상과 승인 경계를 명시한다.

만약 추가 안전장치를 둔다면 hook이 `source`나 프롬프트 메타데이터로 cron을 식별해, `.ok`가 없을 때도 완전 차단 대신 "복구 실패 알림 전송만 허용"하는 별도 모드를 둘 수 있다. 하지만 현재 hook stdin에서 cron 여부가 명시되는지는 소스만으로 확인하지 못했다. 확인된 것은 schedule history에 cron 실행 `workspace_path`가 남는다는 점뿐이다.

## 5. 최종 권장안

최종 권장안은 "L1 고정 bootstrap + L2/L3 온디맨드 + MAX_BYTES 안전판 + cron-safe 정책"이다.

구체적으로는 다음 순서가 좋다.

1. L1 전용 bootstrap을 만든다. 목표 4KB~6KB, hard cap 8KB. 내용은 매니저 정체성, 팀장/경로, 현재 활성 작업 3~5줄, 승인 경계, `work-queue.md`/ADR 포인터로 제한한다.
2. `SessionStart`는 L1만 주입하고 `.ok`를 만든다. `work-queue.md` 전체 주입은 제거한다.
3. `UserPromptSubmit`은 `.ok`만 본다. L2 미독해는 차단 조건이 아니라 모델 지시 조건이다.
4. `COKACDIR_RECOVERY_MAX_BYTES`는 20000 수준으로 유지하되, L1 실제 목표와 별도인 장애 안전판으로만 둔다.
5. cron은 완전 우회하지 말고 L1 필수로 둔다. L1 실패 시 운영을 실행하지 않고 장애 보고만 허용하는 별도 경로를 검토한다.

## 트레이드오프 비교

| 대안 | 장점 | 단점 | 판단 |
|---|---|---|---|
| 한계 상향만 | 즉시 복구, 구현 작음, 현재 10218B는 20000이면 통과 | 파일 증가 시 재발, 매 턴 잡음 계속, gate와 상세문서가 계속 결합 | 응급처치로만 적합 |
| L1/L2/L3 계층화 | gate 성공 조건 안정화, 컨텍스트 잡음 감소, git/notes 상세와 잘 맞음 | L1 최신성 관리 필요, hook 수정 필요 | 장기 권장 |
| cron 전면 우회 | 자동 작업 차단 방지 | 제로 상태 지시/잘못된 권한 판단 위험 | 단독 비권장 |
| cron-safe L1 | 자동 운영과 복구 안전성 균형 | cron 식별/장애 보고 경로 추가 필요 | 계층화와 함께 권장 |

## 구현 메모

현재 확인된 파일/근거:

- Hook: `/home/ubuntu/.claude/hooks/cokacdir-recovery-gate.sh`
- Claude settings: `/home/ubuntu/.claude/settings.json`
- 장애 로그: `/home/ubuntu/.cokacdir/schedule_history/D3AF1AE1.log`, `/home/ubuntu/.cokacdir/schedule_history/3CD0408F.log`
- 사고 기록: `/home/ubuntu/notes/decisions/2026-06-30-recovery-gate-bundle-shrink.md`
- 현재 번들 크기: `MEMORY.md 1523B`, `current-work-state.md 2506B`, `work-queue.md 6189B`, 합계 `10218B`

현재 소스는 이미 `MAX_CONTEXT_BYTES="${COKACDIR_RECOVERY_MAX_BYTES:-20000}"`이다. 따라서 지금 당장의 9000B 초과 장애는 완화되어 있을 가능성이 높다. 하지만 설계상 결합은 남아 있으므로, 재발 방지를 위해서는 `work-queue.md` 전체를 `.ok` 조건에서 빼는 방향으로 재설계하는 것이 맞다.
