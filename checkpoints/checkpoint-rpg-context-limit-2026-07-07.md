# Checkpoint — RPG 팀장 context window limit 사고

일시: 2026-07-07 12:47 KST  
대상: `heav_lnx_rpg_bot` / RPG 팀장  
세션: `d8e96b50-2faf-4d01-8167-b0642d4f419f`  
상태: 조사·백업·중요 문서 Git 보존 완료

## 현상

RPG 팀장이 이사님 요청 직후 아래 에러로 응답 실패.

```text
API Error: The model has reached its context window limit.
model: glm-5.2[1m]
contextWindow: 1000000
inputTokens/cacheReadInputTokens/outputTokens: 0
```

## 직전 이사님 요청

```text
8004 포트 웹에다가 우리가 지금 그리는 RPG의 시스템적인 특성을 광고처럼 나타내 줄 수 있나?
정책이 바뀌면 그 페이지 내용도 바뀌고 대외 직관적으로 알 수 있게.
애니메이션/데모가 있으면 더 좋지만, 웹게임으로 만든다는 뜻은 아님.
```

## 직전 맥락

RPG 팀장은 시나리오팀 매트릭스 구조를 읽고, 이사님 지적에 따라 “특정 인스턴스는 이사님 체감·컨펌 전 방법론에 끌어오지 않는다”는 상위 원칙을 만들었다. 이후 `DRAFT-matrix-scenario-factory-request.md` v3 명세를 작성하고, 위 8004 광고/설명 페이지 요청 직후 터졌다.

## 중요 Git 누락 발견 및 처리

터진 시점에 RPG repo에 아래 중요 문서 3개가 미추적 상태였다.

```text
?? ideation/DRAFT-first-boss-one-turn-instance.md
?? ideation/DRAFT-matrix-scenario-factory-request.md
?? ideation/PRINCIPLE-instance-requires-director-confirm.md
```

내용상 이사님 결정/상위 원칙/시나리오팀 연계 명세라 직접 보존 처리했다.

커밋/push:

```text
13cbfb3 docs: 매트릭스 RPG 명세와 인스턴스 컨펌 원칙 보존
```

## 백업

수동 백업 실행 완료:

```text
/home/ubuntu/chat_logs/rpg/heav_lnx_rpg_bot/2026-07-07/12_00.part001.jsonl
```

읽기 쉬운 Markdown 백업 생성 및 이사님께 전송:

```text
/home/ubuntu/.cokacdir/workspace/r2meshwa/rpg_team_crash_backup_2026-07-07.md
```

## 추가 정리

notes repo 안에 다시 생긴 raw Markdown 백업 `chat-backups/`는 Git에 넣지 않고 아래로 이동했다.

```text
/home/ubuntu/chat_logs/legacy_markdown/
```

## 원인 판단

ai_sessions 파일 크기는 약 39KB, history 16턴으로 겉보기에는 작다.  
그러나 실패 로그는 시나리오팀 사고와 동일하게 `inputTokens=0`으로 `context window limit`을 냈다.

따라서 원인은 사용자 대화 JSON 크기 자체보다, Claude/GLM 프록시가 hidden context, 내부 transcript, tool 결과, recovery context를 합쳐 요청 조립하는 단계에서 초과한 패턴으로 판단한다.

## 복구 권장

RPG 팀장 세션은 `/clear` 후 복구하는 것이 안전하다.

복구 지시문:

```text
L0-agent-boot.md를 읽고 key c5bb2c97036d3741 = heav_lnx_rpg_bot = RPG 팀장임을 인증하라.
rpg_game repo 최신 commit 13cbfb3 이후 상태에서 이어가라.
ideation/PRINCIPLE-instance-requires-director-confirm.md 원칙을 확인하라.
직전 이사님 지시는 “8004 포트 웹에 RPG 시스템 특성을 광고/설명 페이지처럼 보여줄 수 있나? 정책이 바뀌면 페이지 내용도 바뀌고, 애니메이션/데모가 있으면 좋지만 웹게임은 아님”이다.
긴 대화 전체를 재독하지 말고, 필요하면 rpg_team_crash_backup_2026-07-07.md 마지막 8턴만 참고하라.
```

