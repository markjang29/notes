# 컨텍스트 방전 체크포인트 — manager
- 시각: 2026-07-04 01:15:26 KST
- 모드: check
- 측정: 📊 glm-5.2[1m] | 한계 1,000,000 | 37,823 (3.8%) | 0.2MB
- 퍼센트: 3.8%

## 활성 작업 (work-queue.md 상단)
```
# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`)가 관리. 활성 작업 · 대기 결정 · 다음 스텝. **과거 상세는 `work-archive.md`**.
> 최근 갱신: 2026-07-04 01:08 — 야간 배정(07-04) 3팀장 전송 완료. autotrader=비중슬라이드 정량 숫자표+재진입설계 / RPG=Reasoning-Parry 2번째 씬+party-boss blink Godot설계 / scenario=시드2(재배정+ack요청). **★근인 진단: 매니저 cron 3종이 시나리오봇 key(`c6a54f44dab7dfe7`)로 등록 → 시나리오봇 세션 점유 + 자기자신 --message=no-op = 07-01 이후 비활성 원인. 아침 승인 안건(`decisions/2026-07-04-manager-cron-key-fix.md`).** Oracle=1521 LISTEN.

## 활성 작업

### 🔧 autotrader — 백테스트 웹 REST API 시뮬레이터 (07-02 신규 배정)
- **스택 확정:** FastAPI (Streamlit 정정 — REST 서빙 부적합). 기존 `backtest/{data,engine,strategies}` 3-레이어 재사용(분리 양호).
- **엔드포인트:** `POST /backtest`(전략+파라미터 base/k/cap/exit_ratio+심볼+날짜 JSON → 결과 JSON: 메트릭+equity curve+거래내역), `GET /strategies`.
- **전략 토글:** 하이브리드(★)/순수DCA/Buy&Hold + exit_ratio {0,0.3,0.5,0.7,1.0} 자동비교 모드.
- **DB:** Oracle Database Free 23ai (매니저 세팅중, 포트 1521) — 백테스트 결과 히스토리 저장. 팀장은 연결 인터페이스만 준비, 연결정보는 매니저 전달.
- **포트 8001 할당.** 산출물 `app/main.py` + Dockerfile.
- 기존 라오어 하이브리드 백테스트(MDD -16% / 수익 +82%)는 이 웹의 첫 전략으로 흡수.
- **진행(07-02 완료):** `api/` 패키지 구현(main·schemas·repository·__init__) + `backtest/strategies.py` target 일반화. uvicorn 포트8001 기동·엔드포인트(`/strategies`·`/backtest` 단일+자동비교·`/health`·`/docs`) 테스트 통과. **경로:** `api/main.py`(매니저 예상 app/main.py — 유지 OK 확정).
- **Oracle E2E 완료(07-02):** NoopRepo→OracleRepo 교체. 연결 v23.26(23ai Free). 스키마 `bt_runs`(run_id·ts·strategy·target·start_date·end_date·params·metrics). 저장·조회 검증. 비번=`~/.oracle-env`. 서버 재기동 시 환경변수 export 필요.
- **리서치(07-02):** 기간(2020/2010/2007-26)×심볼(QQQ/SPY)×exit_ratio. **exit=0(매도X=라오어원형)가 전 기간·심볼서 수익 압도** (QQQ 2007-26: +1271% vs exit=1 +119%). 매도 비용 = 복리 폭증. SPY서 동일(견고). MDD는 exit=1 우수 but Sharpe는 exit=0 최고. **결론: 레짔 "매도" 룰이 라오어 본질 엣지(하락매수·평단가하락) 훼손.** 후보: (a)★ 비중 슬라이드 (b) 라오어 원형 정밀 (c) 재진입 개선.
- **이사님용 대시보드(07-02):** Streamlit UI 포트8002 + 80(`0.0.0.0`, dashboard.py, nohup/sudo 세션분리). 비금융친화(용어 풀어쓰기·차트·자동비교). **로컬 기동 OK(둘 다 HTTP200, LISTEN). 외부접속 URL: http://13.125.131.126/ (80) 및 :8002.** ⚠ **접속 안 됨 = AWS 보안그룹 인바운드 80·8002 미오픈. 매니저 ops 처리 대기(이 서버 AWS CLI 권한 無).** FastAPI(8001) REST는 별도 유지.

### 🎮 RPG — Reasoning-Parry 시그니처 (07-02 이사님 콜 확정 ★)
- **엔진 Godot 확정** (07-02). **전투 시그니처 = "참모 추론 × 지휘관 결정 × 패막 손맛"(Reasoning-Parry)** — **이사님 07-02 세션 직접 콜 확정**, Codex 검증. (CIPHER/LUMEN/RUMOR 후보 폐기)
- **데모 프로토타입 완료:** `demo/modules/reasoning/`(reasoning.gd/.tscn) + `grid_parry/` 모듈 + **APK export 성공**(Reasoning.apk·GridParry.apk). 모듈식 개발 방향. push 완료.
- **시나리오 팀장 핸드오프(07-03 05:48):** RPG 최신 컨셉을 `WIP-scenario-handoff-reasoning-parry.md` 로 시나리오 팀장에 전달(세계관·연결 포인트 공유).
- 컨셉 1안(걷기=입장재화·색염색 표현층·동기화 PvP·로맨스 A안·진영 분기·P2W 0) 유지. 상세 `ideation/08-reasoning-parry-signature.md`·`06`·`07`.

### 🆕 시나리오 — 제조공장 은폐팩 + 매일 리포트 (07-02 방향 확정)
- 팀장 "방향 감각 상실" 진단 → 다음 월드 **단일 지정**으로 해소.
- **① 다음 월드 = 제조공장 사고 은폐팩 (★).** `worlds/manufacturing-coverup-B01/`. oracle-audit-A01 복제 템플릿(README + lorebook 3-tier + scenes + case JSON). 핵심 갈등: 회사 사전튜닝→노동자 안전불만 위험발화, 산재→은닉접촉 재분류. "한 명 구하기 vs 시스템 건드리기". 1차 WIP: 튜토리얼 scene 1 + case JSON 1.
- **⚠ 07-03 07:00 이슈: 01:00 야간 배정 미이행.** 팀장 마지막 활동 = 07-01 12:55. `manufacturing-coverup-B01/` **미생성**, scene/case JSON 산출 0건. 원인 점검(팀장 비활성? 세션 미시작?) + 재배정 필요.
- **시드 1 (07-03) 완료 — 매니저 폴백(팀장 비활성).** 셋: 한지원(S급 서포터·'진실의 시선') × 이하은(D랭크 헌터) × 유키하(교사). 사전 튜닝 던전 은폐 시나리오 → Reasoning-Parry(참모 추론→지휘관 결정→패링 손맛) 3단 루프 드라마화. **다음 시드=2.**
- **★ 근인 진단(07-04 01:00):** 시나리오 팀장 "비활성" = 설정 결함. 매니저 cron 3종(`432D035D`/`3CC484D7`/`E755367D`)이 **시나리오 봇 key(`c6a54f44dab7dfe7`)** 로 등록 → 매니저 사이클이 시나리오 봇 세션(`ndznfeai`)에서 실행 → `--message --to heav_lnx_scenario_bot` 가 자기자신에게 송신(no-op). 시나리오 봇은 그룹 `-5495363819` 의 `as_public_for_group_chat` 설정도 없음(rpg/trader는 true → 정상 작동). 상세 `decisions/2026-07-04-manager-cron-key-fix.md`.
- **야간 배정 07-04(재배정):** 시드2(B01 scene-02 + case-002 draft) + lorebook 확장. ack 요청함. → 한 번 더 미이행 시 구조적 fix(아침 승인)로 이관.
- **✅ 07-04 01:시나리오 팀장 ack 수신:** "01:00 야간 WIP 배정 정상 수신. 시드1(2019-fire) 완료 인지. 시드2 작업 착수: scene-02 + case-002 draft, B01 lorebook 확장. 07:00 브리프용 보고 예정." **팀장 정상 복귀 확인.** 구조적 cron key fix 안건은 아침 승인으로 유지(정상 작동에도 예방적 이관 권장).
- 영감 메모: "의미의 국경" 엔진(Papers, Please류) · 게임 자체가 ORACLE 자기지시적 메타. 상세 `work-archive.md`.

## 대기 결정 (ADR)
- ~~RPG 엔진 Godot?~~ → **Godot 확정** (07-02).
- ~~trader 스택 Python+NautilusTrader?~~ → **FastAPI 웹 + Oracle DB** 확정 (07-02). 엔진은 기존 pandas.
- **남은 결정:** Oracle 설치 방식(Docker 컨테이너 vs 직접) — 매니저 판단 진행중.
- **★ 07-04 아침 승인 안건:** 매니저 cron 3종을 **매니저 본키(`f5c0501a3a7999ad`, `heav_lnx_bot`)** 로 이관 + 시나리오 봇을 그룹 `-5495363819` public/context 설정 → 시나리오 팀장 정상 가동. fix 초안 `decisions/2026-07-04-manager-cron-key-fix.md`.
- 팀장 사칙 인증: 결정·commit 전 필수.

## 🔧 인프라 (매니저 직접 ops, 07-02 착수)
- **포트 정책:** `decisions/2026-07-02-port-allocation-policy.md`. 8000-8099 API / 1521 Oracle / 80·443 nginx 리버스 프록시.
- **Oracle DB Free 23ai:** 설치 예정(RAM 7.6G·disk 143G·2 core → 가능). 완료 시 팀장에 연결정보 전달.
```

## git 상태 — scenario
status:
?? worlds/manufacturing-coverup-B01/cases/case-002-precision-cutting-2022.json
?? worlds/manufacturing-coverup-B01/scenes/scene-02-second-accident.md
log:
f895377 feat: RPG 시그니처 인수 — Reasoning-Parry·Walk-to-Play·4인 파티 보스전
e7215c5 feat: 제조공장 은폐팩 manufacturing-coverup-B01 1차 산출
feb1372 [ADR] 자생 서사 시스템 설계 + oracle-audit-A01 로어북 구조화 + Case 001 JSON 설계

## git 상태 — rpg_game
status:
?? ideation/WIP-party-boss-godot-impl-design.md
?? ideation/WIP-second-battle-scene-reasoning-parry.md
log:
a8cc999 feat: 시나리오 팀장 핸드오프 — 4인 파티 보스전 + AI 전략 + 보스 혼종 + 정당성
1cd2b89 feat: ideation 10 갱신 — 보스 카테고리·혼종·상태 감지 추가
b3d0ee3 feat: ideation 10 갱신 — AI 전략 레벨업 + WALK 관계 추가

## git 상태 — autotrader
status:
?? IDEATION.md
?? analysis_exit_ratio.py
?? api/
?? backtest/
?? dashboard.py
?? research/
?? research_exit_ratio.py
?? run_backtest.py
?? strategy-spec-v1.md
log:
f89bb80 초기 세팅: 자동매매 프로젝트 README + .gitignore

## 세션·복구 포인터
- canonical memory: /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory
- 복구入口: akl0hdys memory MEMORY.md → work-queue.md
- CLAUDE_CODE_SESSION_ID: 191fd855-42e2-43bf-838c-72845770b877
- transcript 힌트: /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/191fd855-42e2-43bf-838c-72845770b877.jsonl

## 복구 지침
1. /clear (또는 신규 세션). cron --session 으로 같은 세션 resume 금지(누적 폭발 원인).
2. 위 활성 작업·미커밋 변경부터 마무리.
3. memory + work-queue.md 기반 복구 (clear-recovery-map 참조).
4. 1M 폭발 재발 방지: work-queue/memory 통째 주입 억제, WebSearch dump 발췌만.
