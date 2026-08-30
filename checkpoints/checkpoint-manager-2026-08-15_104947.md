# 컨텍스트 방전 체크포인트 — manager
- 시각: 2026-08-15 10:49:47 KST
- 모드: check
- 측정: 📊 glm-5.3[1m] | 한계 1,000,000 | 745,336 (74.5%) | 10.7MB
- 퍼센트: 74.5%

## 활성 작업 (work-queue.md 상단)
```
# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`) 전관. 활성 작업·대기 결정·다음 스텝만 유지한다.
> 과거 상세는 Git 이력, `work-archive.md`, checkpoints를 본다.

## 최상위 원칙

- 이사님 최종 결정.
- 팀장은 자기 산출물만. 통합·우선순위·ops는 매니저 전관.
- 중요한 `.md`/ADR/checkpoint/work-queue 변경은 Git 보존 후 세션 클리어.
- 긴 문서 전체 재독 금지. 필요한 부분만 읽는다.

## ★ Scenario 현재 정본 (2026-07-14)

아래의 과거 freeze·야간 배정·110558063 진행 문구는 역사 기록이며 현재 상태가 아니다.
Scenario의 질문·방향·우선순위는
`projects/scenario/README.md`와 `projects/scenario/roadmap.md`를 우선한다.
실행 상태는 scenario repo의 `catalog/asset_lifecycle.ndjson`을 직접 확인한다.

## 매니저 크론/알람 원칙 (07-12 사고 반영)

★ 타 봇 key + 그룹 chat(`--chat -N`)으로 cron 예약을 등록할 때는 **`--once` 단발만 허용, recurring(반복 cron) 금지**. recurring이 정말 필요하면 매니저 본인 key + 라우터(`scripts/request_router_poll.py`) 경유만.

- 사유: (i) recurring은 빈 폴링이라도 매 틱 LLM 토큰을 태운다; (ii) **07-04 결함 회귀** — 타 봇 key recurring은 no-op·자기송신 결함으로 진단·fix된 바 있다(`decisions/2026-07-04-manager-cron-key-fix.md`); (iii) 대상 봇이 그룹에서 추방/휴면이면 placeholder 송신이 실패하고, cokacdir 5초 스케줄러 틱이 `last_run` 갱신을 생략해 due 잔존 → **5초 간격 재발사 폭발**(07-12 220회 Forbidden 사고).
- 예외: 팀장 봇을 한 번 깨워 세션 기동시키는 용도는 `--once` 단발로 허용(`projects/scenario/docs/aws-request-bridge.md` 준수 — 세션 기동 확인 후 보고).

## 이사님 결정 — scenario repo freeze (07-12 KST, 이사님 직접)

★ 이사님 직접 확인(07-12): **scenario repo 리뉴얼(갈아엎기) 전까지 일체 수정 금지(freeze)**. 리뉴얼 룰 통보 시 새 룰 따름. 상세 · 크론 백업 → `decisions/2026-07-12-scenario-repo-freeze.md`.

- 매니저 방침: **scenario 야간 배정 사이클 전면 중단** (리뉴얼 룰 통보 전까지). RPG·autotrader 정상.
- `0FC5A6F0`(시나리오 야간) → 팀장 제거 완료. `C9804825`(08:00 시나리오팀 창작 리포트) → 매니저 제거, 리뉴얼 후 재등록.
- `2D8F5150`(01:00 3팀 공통 배정)은 유지 — 본 섹션 읽고 scenario 제외 처리. 아래 07-12 밤 배정(라인 하단)의 scenario 과제는 모두 **freeze로 무효**.
- 미커밋 잔류(`drafts/d1`, `d2`, `OVERNIGHT_2026-07-12.md`): 보존, 조치 없음. scenario 봇·매니저 git 조작 금지.
- 재개 조건: 이사님 리뉴얼 룰 통보.

★ **해제됨 (07-12 17:23 KST, 이사님 승인 "프리즈 전면 해제해")**. 코덱스 제안 리뉴얼 룰 7조 확정 적용 — reviewed 자산만 사용 / fragment ID·입력커밋·기여 기록 / `.extract`·`catalog/index.json`·crawler후보·`needs_review` 입력금지 / 게시물완결 / 보정재실행 / `usable`·`usable_with_changes`·`not_usable` 판정 / 생성물·검증근거·한국어해설 Git커밋. `ee11cc` running → 시나리오팀장 전달(msg_20260712_172300_5ca2ef60). 시나리오팀 야간 배정 사이클 재개 가능.

## 인바운드 작업요청 창구 (07-12 신설, approval-board 포트 8005)

외부 Codex/ZCODE → AWS 봇 작업요청. 원장 `requests.json`(Git), 클라이언트 토큰 `clients.json`(gitignore). 이사님 웹 `/requests`. 라우터: webhook(POST 즉시) + 1분 cron 폴백(A36A9120) + claim 잠금(멱등). commits: 509e857/74622a7/31c56ab. 코덱스 루프(게시물 110558063) 단계1(라우터)·2(룰확정) 완료, 단계3(ee11cc 실행) 진행 중.

## 이사님 결정 — 승인 보드 (07-10 18:57–59 KST)

★ 이사님이 승인 보드(http://13.125.131.126:8005)에서 직접 결정. `decisions.json` 반영됨.
```

## git 상태 — scenario
status:
log:
c43f05c docs(novel): RISU 다음단계 세분화 계획 + 카테고리 매핑 진단 + 모니터링 프레임
da454ed docs: show scenario in the Matrix repository map
9efb8cb docs(novel): 소설 지시어(토큰=소설이어) 명시 + RISU 자산화 성과 정리

## git 상태 — rpg_game
status:
?? OVERNIGHT_2026-07-12.md
?? ideation/DRAFT-parry-handfeel-one-breath.md
?? ideation/OVERNIGHT_2026-07-09.md
?? ideation/WIP-second-battle-full-match-script.md
?? ideation/WIP-second-battle-signature-fusion.md
?? ideation/WIP-second-battle-win-lose-fork.md
log:
79681e9 design: 공격 분류(상/중/하+타입, 격투게임식) — 패링 전 긴장 층 (이사님 2026-07-26 아이디어)
235feea design: core-incarnation 세계 간 이동 = 하이브리드 해금 확정 (이사님 2026-07-26, 옵션 2번 선택)
296c3a5 design: 코어 빙의(정체성 핵→세계 캐릭터) (이사님 2026-07-26 아이디어)

## git 상태 — autotrader
status:
 M research/WIP-weight-slide-results-v1-draft.md
?? OVERNIGHT_2026-07-12.md
?? research/OVERNIGHT_2026-07-09.md
?? research/WIP-adr-rest-api-port-ownership-v1-draft.md
?? research/WIP-compass-decision-flow-v1-draft.md
?? research/WIP-quarter-run-experience-v1-draft.md
?? research/WIP-strategy-instance-trade-v1-draft.md
log:
1277e72 야간배정 07-11: trader 팀장 지시문 (07-10 밤 결과 기반)
704e29e OVERNIGHT 2026-07-10: 2022 인플레 딥다이브 + weight-slide 하이브리드 대안
e20e9f5 보존(감사브리프 긴급): 미추적 산출물 일괄 — IDEATION/strategy-spec-v1/api/backtest/dashboard/research/run_backtest/analysis_exit_ratio

## 세션·복구 포인터
- canonical memory: /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory
- 복구入口: akl0hdys memory MEMORY.md → work-queue.md
- CLAUDE_CODE_SESSION_ID: a949cc9d-daae-4685-b830-bc68198473b9
- transcript 힌트: /home/ubuntu/.claude/projects/-home-ubuntu-projects-scenario/a949cc9d-daae-4685-b830-bc68198473b9.jsonl

## 복구 지침
1. /clear (또는 신규 세션). cron --session 으로 같은 세션 resume 금지(누적 폭발 원인).
2. 위 활성 작업·미커밋 변경부터 마무리.
3. memory + work-queue.md 기반 복구 (clear-recovery-map 참조).
4. 1M 폭발 재발 방지: work-queue/memory 통째 주입 억제, WebSearch dump 발췌만.
