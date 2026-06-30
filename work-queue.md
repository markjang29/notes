# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`)가 관리. 활성 작업 · 대기 결정 · 다음 스텝. 마무리/새 작업 시 갱신.
> 최근 갱신: 2026-06-30 14:10 — **시나리오 팀 신설**: `@heav_lnx_scenario_bot` → `~/projects/scenario`. 게임과 구분된 독립 시나리오/세계관(데이팅 앱 등). org-structure·onboarding·본 큐 갱신.
> (이전 06-30 08:40 — **529 해결**: reaper 스크립트+crontab 배포. `decisions/2026-06-30-session-reaper.md`.)

## 활성 작업

### 🔥 autotrader: 라오어 기반 알고리즘 전략 — 백테스트 진행 중
- **지시:** 알고리즘 전략 중심. 라오어 이론 세미나 → 팀 의견 취합 → 이론 제안.
- **완료:** 라오어 조사 + 팀원 병렬 → 세미나 초안 `notes/.reviews/seminar-raoer-20260626-01.md`(+상세 2건).
- **핵심 통찰:** 라오어 엣지 = "행동편향 회피(기계적 분할매수)". 자동매매화 순간 엣지 증발(자동화의 역설). 단독 비추천.
- **팀 추천(하이브리드):** 라오어 분할매수 뼈대(현물 1배, TQQQ 배제) + VAA/DAA 레짔 필터(강세 매수·현금대피 킬스위치) + 주간/월간 빈도 완화 + DRIP.
- **대기 ADR:** (a) 라오어 단독 / (b) 하이브리드★ / (c) 타 방향 / (d) 추가 조사.
- **진행(백테스트 착수):** 스택=Python+pandas(`decisions/2026-06-26-autotrader-backtest-stack.md`), 엔진 구축 완료(`autotrader/backtest/`, venv `~/.venvs/autotrader`), 데이터 yfinance(QQQ·SHV 2010-26). **첫 결과:** 하이브리드 MDD -16%(방어 입증) vs 수익 +82%(B&H +1678%, 현금비중 발목). 레짔필터 과민(7회 전환). 다음 실험: (a) 파라미터 튜닝 / (b)★ 비중 슬라이드 개량 / (c) 타 전략.
- **v1(방향중립 차익)과 관계:** 충돌 아님 — v1 백본 + 전략 모듈 공존 가능.

### ✅ 걷기×전술 RPG 컨셉 수렴 — 2026-06-26
- **상태:** 컨셉(1안) 확정. 내러티브는 작가 검증 대기(메커니즘은 확정).
- **확정:** 걷기=입장재화(3겹 캡: 입장권 로그캡·하루 N판·걷기→전투력 0기여) + 동기화 전술 PvP + 지역 PvE + 로맨스(A안) + 진영 분기. P2W 0.
- **폐기:** 비동기 위치 영토 PvP/공성(구조적 불가, Codex 판정).
- **문서:** `projects/rpg_game/ideation/06-concept-convergence.md`(+원안 05·회의록·검증 7건 `.reviews/`).
- **인계(다음 세션):** (1) 내러티브 작가 검증 (2) 엔진 ADR(Godot 권장) (3) CIPHER/RUMOR 결합 (4) MVP 범위.

### 🆕 시나리오 팀 — 자생 세계관 시나리오 (2026-06-30 신설)
- **팀장:** `@heav_lnx_scenario_bot` → `/home/ubuntu/projects/scenario` (github.com/markjang29/scenario).
- **역할(이사님 확정 06-30):** 캐릭터 챗(character.ai류)처럼 — 세계관·캐릭터가 상호작용 속에서 **자생적으로 생성·운영**되는 독립 시나리오 생태계. **RPG 세계관과는 분리**(RPG 세계관은 RPG 팀 소유, 이관 없음).
- **소스:** 이사님 윈도우 PC 정리 중(진행 중) → scenario repo로 push 예정. **현재 repo 비어있음**(이사님 push 대기) → 매니저/팀장은 초기화 금지, push 후 작업.
- **설계 원칙(codex 검토 · 이사님 승인 06-30):** 시나리오 팀 = **"상태를 가진 자생 서사 시스템"** 운영팀(일반 작가팀 아님). 산출 = "이야기"가 아니라 "운영 가능한 세계 상태". 초기 설계 반영: (1) canonical 기록 체계(ADR 외 별도 — world state · character memory · canon policy · event log · retcon log) (2) 상태 라이프사이클 draft→observed→canon→deprecated→retconned (3) 캐릭터별 목표·금기·말투 제약 + 재사용 우선 정책 (4) 평가지표(충돌률·반복률·구분성·retcon 빈도) (5) RPG와 초기 완전 분리, 공유는 ADR 수출 절차(제한 자산만).
- **첫 지시(시나리오 팀장):** (1) 온보딩 사칙 인증 (2) 위 프레임워크 기반 자생 세계관 시스템 초기 설계 draft(notes) + 이사님 소스 push 대기.

### 아이디에이션 v1 → v2 대기
- 산출: RPG `projects/rpg_game/IDEATION.md`(+ideation/), trader `projects/autotrader/IDEATION.md`(+`notes/.reviews/`).
- 피드백: "기술 분석 과다, 실체화 부족" → v2는 show-don't-tell(체감 시나리오·구체 숫자). 기술 분석은 뒷받침. `personas/markjang29.md` §10 승격 제안(검증 대기).

## 대기 결정 (ADR 대기)
- RPG 엔진: Godot? Unity? 웹? — 컨셉 수렴 후 ADR.
- trader 스택: Python + NautilusTrader? — v2 이후 ADR.
- 팀장 사칙 인증: v1은 미인증 '초안'이라 허용. 결정·commit 전엔 인증 필수.

## 🔥 야간 자율 운영 (이사님 승인)
> 야간 = 아침 결정 1개씩의 근거 패키지를 까는 시간. 열린 탐색 금지.

**승인 경계선(매니저 판정):**
- 야간 자동 = 사전 합의 실험 · 로컬 계산 · 리서치(읽기) · draft · 숫자표. WIP 팀당 2건.
- 아침 승인 필수 = 전략 채택 · 엔진 확정 · commit/push · ADR · 외부 송신 · 실거래.

**오늘 밤 작업 2건:**
1. **trader 비중 슬라이드 6안 백테스트**: exit_ratio {0,0.3,0.5,0.7,1.0} × 매수중단 on/off. 로컬 pandas. 산출=숫자표만 → `notes/.reviews/nightly-sweep-20260627.md`. 아침 결정: "exit_ratio 채택값 1개".
2. **RPG 엔진 ADR 근거**: Godot/Unity/웹 요구사항 매핑 비교표 → `notes/decisions/2026-06-27-rpg-engine-adr-draft.md`. 아침 결정: "엔진 1개".

**스케줄(cokacdir --cron):** 06-27 23:00 야간 트리거 / 06-28 07:00 아침 브리프(+Codex 크로스체크, 결정 2건).
**fallback:** 팀장 비활성 시 매니저가 양 repo 직접 실행.

---

## 다음 스텝 (사용자 재개 시)
1. v2 아이디에이션 지시(체감 우선).
2. 팀장 사칙 인증 완료 여부 확정.
3. 쿼터/검색 장애 대응 → `decisions/2026-06-26-quota-checkpoint-resume.md`.

## 세션 노트 (요약)
- 매니저 사칙 인증 완료. 팀장 3명 repo 바인딩(rpg_game·autotrader·scenario).
- 핸들 `_bot` 접미사 수정(commit bc4d04b).
- 이슈: 병렬 검색 과다 → search -429/529 → ADR 대응.
