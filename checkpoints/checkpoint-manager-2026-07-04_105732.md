# 컨텍스트 방전 체크포인트 — manager
- 시각: 2026-07-04 10:57:32 KST
- 모드: check
- 측정: 📊 glm-5.2[1m] | 한계 1,000,000 | 225,788 (22.6%) | 1.5MB
- 퍼센트: 22.6%

## 활성 작업 (work-queue.md 상단)
```
# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`)가 관리. 활성 작업 · 대기 결정 · 다음 스텝. **과거 상세는 `work-archive.md`**.
> 최근 갱신: 2026-07-04 08:55 — **★ 이사님 08:47 선회 확정: "임의로 뿌린 시드 전부 이어가지 마. RPG 팀장이 요청하는 시나리오만." → 시드1(헌터월드) 포함 worlds 전체 폐기 완료(커밋 `3d22856` push).** 01:09 결정(mfg 폐기)에서 더 나아가 **RPG=클라이언트·시나리오팀=서포터** 구도 확정. 양 팀장에 --message 통보(RPG→의뢰서 작성·시나리오팀→대기). RPG 의뢰 도착·ack 대기. Oracle=1521 LISTEN.

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

### 🆕 시나리오 — 사칙 정정: 존재 이유 재확립 (07-04 09:1x ★ 이사님 직접)
- **★ 사칙 신설:** `principles/scenario-team-purpose.md` (v1, 이사님 확정). 시나리오팀의 **존재 이유 명시**.
- **★ 오버피팅 정정 (이사님 09:1x):** 매니저가 08:47 "임의 시드 금지"를 **"시나리오팀은 임의 창작 금지·RPG 의뢰만 받는 도구"** 로 오해. **정정:** 시나리오팀 = **RISU 자산 기반 창작 스튜디오**, **창작(draft)은 자유**, **이사님 컨펌 후 디벨롭**. RPG 의뢰는 선택적 트리거(RPG=클라이언트·시나리오팀=창작 서포터, 단방향 아님). 잘못된 memory `feedback-no-arbitrary-seeds` 삭제 → `scenario-team-purpose`로 대체.
- **RISU 자산 (뼈대):** scenario repo `ecosystem/`(구조해설 7종) · `examples/` · `catalog/`(characters/pdfs/modules/prompts csv) · `templates/`(4종). 원본은 이사님 노트북 `D:\LLM\`, 발췌해 git에 넣음. **추가 자산 = 아카라이브 AI챈 크롤링** 구조로 확장(이사님 방침).
- **목표:** "고급 대화·고급 피드백"용 캐릭터·월드·시나리오 생산 + **창작 도구(LoRA·캐릭터 카드·페르소나·모듈) 자체 디벨롭** (내부 회의 주도).
- **유효 유지:** worlds/ 폐기(커밋 `3d22856`) — 그건 RISU 기반 아닌 자의적 자생서사라 폐기 유효. 단 시나리오팀의 RISU 기반 창작 역할 자체는 부정 아님.
- **첫 산출(07-04):** RPG 의뢰 first-boss-reasoning-parry → 시나리오팀 1차 draft(`deliverables/`, 합격). 매니저 검증 + RPG 팀장 승인 완료. **이사님 컨펌 대기** (컨펌 시 디벨롭).
- **시나리오팀 지시 정정(07-04 09:1x):** 앞서 보낸 "임의시드/월드 자체 생성 절대 금지"는 철회. 사칙(창작 자유 + 컨펌 게이트 + 도구 디벨롭)으로 전달.
- **✅ 시나리오팀 사칙 인증 완료(07-04 09:5x):** ack 정확. **컨펌 게이트 자가 정정** — 보강 3건(=디벨롭)을 컨펌 후로 스스로 미룸. 얼라인 3곳(이사님-매니저-시나리오팀) 맞춤 완료.
- **✅ 사칙 v1 확정 (07-04 이사님).** `principles/scenario-team-purpose.md` 공식 사칙.
- **⚠ 첫 산물(first-boss) 보류 (이사님):** *"시나리오팀이 만든 게 아무것도 없다"* — 의뢰서(RPG)를 글로 풀어쓰기만 했지, 사칙 역할 1(RISU 자산 기반 창작)·4(창작 도구 디벨롭)이 안 보임. 다음 산출은 RISU 자산(캐릭터 카드·페르소나·로어북)을 실제 활용한 독자적 창작 개입을 보여야.
- **★ 시나리오팀 대응 — scenario-generator 설계 v2 (07-04 10:27, commit `9e7f752`):** 보류 피드백에 대한 근본 대응으로 **창작 도구** 설계 제안(구현 아님, DESIGN.md 306줄). 이사님이 RISU에서 직접 하던 "자산 골라 조합해 이야기 만들기"를 툴로 대리 자동화. 주제 한 줄 → catalog(602점) 발굴·조합 → 2~3안 draft + **PROVENANCE 블록**(자산 활용 흔적). 7단 파이프라인(INTERPRET→DISCOVER→COMPOSE→LOAD→ASSEMBLE→GENERATE→PRESENT). Python. **매니저 검증: 사칙 역할 1·4 정합 양호.**
- **⏳ 이사님 컨펌 대기 (4점):** (1) 방향 RISU 대리자동화·자연어 주제·조합 바꿔가며 (2) Python 스택 (3) v0 범위 7단·2~3안 (4) PROVENANCE 블록을 컨펌 지표 채택. **매니저 의견:** 1·2·4 찬성, 3은 얇은 end-to-end 1패스 우선 제언. 컨펌 시 ADR + v0 구현 착수 지시.
- ADR `decisions/2026-07-04-scenario-pivot-rpg-driven.md`도 사칙에 맞춰 추후 갱신 예정.

## 대기 결정 (ADR)
- ~~RPG 엔진 Godot?~~ → **Godot 확정** (07-02).
- ~~trader 스택 Python+NautilusTrader?~~ → **FastAPI 웹 + Oracle DB** 확정 (07-02). 엔진은 기존 pandas.
- **남은 결정:** Oracle 설치 방식(Docker 컨테이너 vs 직접) — 매니저 판단 진행중.
- **★ 07-04 아침 승인 안건:** 매니저 cron 3종을 **매니저 본키(`f5c0501a3a7999ad`, `heav_lnx_bot`)** 로 이관 + 시나리오 봇을 그룹 `-5495363819` public/context 설정 → 시나리오 팀장 정상 가동. fix 초안 `decisions/2026-07-04-manager-cron-key-fix.md`.
```

## git 상태 — scenario
status:
?? deliverables/
log:
57ddde2 feat: scenario-generator v0 구현 — 파이프라인+FastAPI+웹
634bac1 feat: scenario-generator DB 셋업 — SCENARIO 유저 + 스키마
3479a13 설계: scenario-generator v3 — 웹 서비스 + Oracle DB

## git 상태 — rpg_game
status:
?? ideation/WIP-party-boss-godot-impl-design.md
?? ideation/WIP-second-battle-scene-reasoning-parry.md
log:
5144753 feat: 시나리오팀 의뢰서 — 첫 보스 한 판 체험 (Reasoning-Parry)
b7f7a9d feat: 이사님 결정 — manufacturing-coverup 폐기, RPG 시그니처 기반 시나리오 전환
a8cc999 feat: 시나리오 팀장 핸드오프 — 4인 파티 보스전 + AI 전략 + 보스 혼종 + 정당성

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
- CLAUDE_CODE_SESSION_ID: 41399726-2d71-4bca-a5d8-6322719533d3
- transcript 힌트: /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-ndznfeai/41399726-2d71-4bca-a5d8-6322719533d3.jsonl

## 복구 지침
1. /clear (또는 신규 세션). cron --session 으로 같은 세션 resume 금지(누적 폭발 원인).
2. 위 활성 작업·미커밋 변경부터 마무리.
3. memory + work-queue.md 기반 복구 (clear-recovery-map 참조).
4. 1M 폭발 재발 방지: work-queue/memory 통째 주입 억제, WebSearch dump 발췌만.
