# RPG·시나리오 동시 529 과부하 사고

- 일시: 2026-07-08 10:59 KST 전후
- 대상:
  - RPG 팀장: `heav_lnx_rpg_bot`
  - 시나리오 팀장: `heav_lnx_scenario_bot`

## 결론

두 팀장이 거의 같은 시각에 `API Error: 529 [1305]`로 실패했다.
이번은 개별 세션 context window limit이 아니라 Z.ai/GLM backend 과부하 패턴이다.

다만 두 세션 모두 이미 큰 요청이었다.

## RPG 팀장

- session: `e102f9cf-b5a2-41d4-ba65-349362fe7fd8`
- transcript: `/home/ubuntu/.claude/projects/-home-ubuntu-projects-rpg-game/e102f9cf-b5a2-41d4-ba65-349362fe7fd8.jsonl`
- 마지막 정상 context 추정:
  - input: 186,295
  - cache_read: 7,872
  - total: 194,167 tokens
- transcript size: 약 1.44MB
- Git 상태: 미반영 중요 변경 없음

마지막 사용자 지시:

> 시나리오팀 회신을 받으면 RPG 팀 입장에서 구조를 탔는지 크로스 체크하고, 구현/아이디어를 더해 보고할 수 있나?

## 시나리오 팀장

- session: `8f426d25-33e1-4010-9a61-2ca93d788822`
- transcript: `/home/ubuntu/.claude/projects/-home-ubuntu-projects-scenario/8f426d25-33e1-4010-9a61-2ca93d788822.jsonl`
- 마지막 정상 context 추정:
  - input: 1,272
  - cache_read: 182,080
  - total: 183,352 tokens
- transcript size: 약 1.20MB
- Git 보존 완료:
  - `be85fd0 pipeline: CASTING 배역 배정과 재해석 카드 역할 반영`

## 운영 판단

1. 두 팀 모두 clear 가능.
2. 동시에 재시도하지 말고 순차 재시작/순차 요청 권장.
3. RPG → 시나리오 → RPG 크로스체크 흐름은 파일 산출 기반으로 끊어 진행해야 한다.
4. 대형 요청은 한 팀장이 긴 응답을 직접 Telegram으로 뿌리기보다 repo/file 산출 후 짧게 보고하는 방식이 안전하다.
5. 기존 세션은 `glm-5.2` 흔적이 있어, clear 후 새 설정(`glm-5.2[1m]`, auto compact 1M)을 다시 물고 시작하는 것이 좋다.

## 복구 지시 — RPG

1. `/clear` 후 L0/onboarding 확인.
2. `/home/ubuntu/projects/rpg_game` 최신 commit 기준.
3. 마지막 지시를 이어간다:
   - 시나리오팀 회신을 받으면 시나리오 repo 자산/매트릭스 구조를 탔는지 검증
   - RPG 구현/게임 아이디어 관점으로 추가 의견 보고
4. 시나리오 회신이 없으면 먼저 시나리오팀 재요청문을 짧게 만들고 대기.

## 복구 지시 — 시나리오

1. `/clear` 후 L0/onboarding/`principles/scenario-team-purpose.md` 확인.
2. `/home/ubuntu/projects/scenario` 최신 commit `be85fd0` 기준.
3. RPG 요청을 바로 LLM 생성하지 말고 매트릭스 구조/자산 연결 구조를 통과시켜 파일 산출.
4. 결과는 웹에서 볼 수 있게 하는 흐름까지 설계.

