# Work Archive — markjang29 dev

> 과거 완료/상세 기록. `work-queue.md` 다이어트를 위해 2026-07-01 분리. **활성 내용은 `work-queue.md`**.

## 갱신 이력 (과거)
- 2026-06-30 14:10 — 시나리오 팀 신설: `@heav_lnx_scenario_bot` → `~/projects/scenario`. 게임과 구분된 자생 세계관.
- 2026-06-30 08:40 — **529 해결**: reaper 스크립트+crontab 배포. `decisions/2026-06-30-session-reaper.md`.
- 2026-07-01 — 복구번들 다이어트(work-archive 분리). 야간 cron 01:00 / 아침 07:00(KST).

## autotrader: 라오어 상세 (완료분·이론)
- **지시:** 알고리즘 전략 중심. 라오어 이론 세미나 → 팀 의견 취합 → 이론 제안.
- **완료:** 라오어 조사 + 팀원 병렬 → 세미나 초안 `notes/.reviews/seminar-raoer-20260626-01.md`(+상세 2건).
- **핵심 통찰:** 라오어 엣지 = "행동편향 회피(기계적 분할매수)". 자동매매화 순간 엣지 증발(자동화의 역설). 단독 비추천.
- **팀 추천(하이브리드):** 라오어 분할매수 뼈대(현물 1배, TQQQ 배제) + VAA/DAA 레짔 필터(강세 매수·현금대파 킬스위치) + 주간/월간 빈도 완화 + DRIP.
- **첫 백테스트 결과:** 하이브리드 MDD -16%(방어 입증) vs 수익 +82%(B&H +1678%, 현금비중 발목). 레짔필터 과민(7회 전환).
- **v1(방향중립 차익)과 관계:** 충돌 아님 — v1 백본 + 전략 모듈 공존 가능.

## RPG: 걷기×전술 컨셉 수렴 상세 (2026-06-26 확정)
- **확정:** 걷기=입장재화(3겹 캡: 입장권 로그캡·하루 N판·걷기→전투력 0기여) + 동기화 전술 PvP + 지역 PvE + 로맨스(A안) + 진영 분기. P2W 0.
- **폐기:** 비동기 위치 영토 PvP/공성(구조적 불가, Codex 판정).
- **문서:** `projects/rpg_game/ideation/06-concept-convergence.md`(+원안 05·회의록·검증 7건 `.reviews/`).
- **인계(원래):** (1) 내러티브 작가 검증 (2) 엔진 ADR(Godot 권장) (3) CIPHER/RUMOR 결합 (4) MVP 범위.

## 시나리오 팀: 설계 원칙 상세 (codex 검토 · 이사님 승인 06-30)
- 시나리오 팀 = **"상태를 가진 자생 서사 시스템"** 운영팀(일반 작가팀 아님). 산출 = "이야기"가 아니라 "운영 가능한 세계 상태".
- 초기 설계 반영: (1) canonical 기록 체계(ADR 외 별도 — world state · character memory · canon policy · event log · retcon log) (2) 상태 라이프사이클 draft→observed→canon→deprecated→retconned (3) 캐릭터별 목표·금기·말투 제약 + 재사용 우선 정책 (4) 평가지표(충돌률·반복률·구분성·retcon 빈도) (5) RPG와 초기 완전 분리, 공유는 ADR 수출 절차(제한 자산만).
- 검토 파일: `.reviews/recovery-redesign-{pessimistic,optimistic,codex}.md` (복구번들 재설계 리뷰 — 시나리오 팀 설계와 다름).

## 야간 자율 운영 — 과거 스케줄
- 06-27 23:00 야간 트리거 / 06-28 07:00 아침 브리프(+Codex 크로스체크) — 과거 계획, 이미 경과.
- 06-27 밤 작업 2건: trader 비중 슬라이드 6안 백테스트, RPG 엔진 ADR 근거 비교표.

## 세션 노트 (과거 요약)
- 매니저 사칙 인증 완료. 팀장 3명 repo 바인딩(rpg_game·autotrader·scenario).
- 핸들 `_bot` 접미사 수정(commit bc4d04b).
- 이슈: 병렬 검색 과다 → search -429/529 → ADR 대응.
