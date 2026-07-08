# 시나리오 팀장 529 과부하 사고 기록

- 일시: 2026-07-08 KST
- 대상: `heav_lnx_scenario_bot`
- 세션: `8f426d25-33e1-4010-9a61-2ca93d788822`
- transcript: `/home/ubuntu/.claude/projects/-home-ubuntu-projects-scenario/8f426d25-33e1-4010-9a61-2ca93d788822.jsonl`

## 사고 요약

시나리오 팀장이 10:59 KST 전후 `API Error: 529 [1305]`로 응답 실패했다.
이번 사고는 `context window limit`이 아니라 Z.ai/GLM backend 과부하다.

다만 해당 transcript는 약 1.20MB, 마지막 정상 사용량은 약 183k tokens로 이미 큰 편이었다.

## 마지막 사용자 지시

> 그리고 팀장급이 시나리오 요청했을 때도 지금 매트릭스 구조를 타서 돌려줘야지 바로 LLM 돌리거나 하지마. RPG 팀이 요청갈 거고 천천히 토큰 많이 써도 되니까 신중히 답장줘. 파일로 쓴 다음 그 파일 보고하라던지 해도 되고 그런 식으로 요청받은 것도 웹에서 볼 수 있게 해줘.

## 보존 조치

세션 클리어 전 미커밋 중요 변경을 확인하고 Git에 보존했다.

- repo: `/home/ubuntu/projects/scenario`
- commit: `be85fd0 pipeline: CASTING 배역 배정과 재해석 카드 역할 반영`

보존 내용:

1. `pipeline/refine.py`
   - `cast_roles()` 추가
   - 재해석된 캐릭터 카드에서 주인공/상대/조력/적 배역 자동 배정
   - 주인공은 casting 결과를 기준으로 deep refine

2. `pipeline/assemble.py`
   - 캐릭터 카드 출력 제목에 role tag 반영
   - 예: `#### 캐릭터명 — 주인공`

검증:

- `python3 -m py_compile pipeline/refine.py pipeline/assemble.py pipeline/generate.py` 통과

## 복구 지시문

시나리오 팀장에게 전달할 지시:

1. `/clear` 후 재시작한다.
2. L0/onboarding/`principles/scenario-team-purpose.md`를 읽고 사칙 인증한다.
3. `/home/ubuntu/projects/scenario`에서 최신 commit `be85fd0`를 기준으로 이어간다.
4. 이사님 마지막 지시를 반영한다:
   - RPG/팀장급 시나리오 요청도 바로 LLM 생성하지 말 것
   - 현재 매트릭스 구조를 통과시킬 것
   - 긴 요청은 파일 산출 후 보고하는 방식 허용
   - 요청/결과가 웹에서 볼 수 있게 하는 흐름을 설계할 것
5. 529 과부하가 다시 나면 같은 세션에서 반복 재시도하지 말고, 짧은 체크포인트를 남긴 뒤 clear/retry한다.

## 세션 클리어 판단

Git 보존 완료 후에는 clear 가능.

