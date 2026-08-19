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

## 2026-08-16 아카이브 (work-queue 5주치 공백 정리)

work-queue가 07-12에 정지한 뒤의 공백 기록. 07-10~07-12 승인보드·야간 사이클 상세를
여기로 옮겼다. 현재 상태는 `work-queue.md`(2026-08-16)를 우선한다.

### 07-10 이사님 승인 보드 결정 (18:57–59 KST)

- RPG 야간 결과 push → 보류("그 대본이 뭔지 사이트에서 볼 수 있게 표현해주세요" →
  매니저가 보드 카드에 §2.5 한 호흡 + Miss 임베드 완료, 재결정 대기).
- scenario 자산(Rio·Ji-Won) 사용 → 반려. 정책: "처음 봤는데 부가설명 없이 표현이 안되는
  캐릭터는 사용 금지" → 사칙 5.1 강화(모르는 자산 부가설명 동반 의무화).
- scenario 야간 결과 push → 반려(자산 반려 연동).
- autotrader WIP-adr / push → 대기(미결정).

### 07-11 밤 배정 (07-10 결과 반영, 중복 트리거 사고 포함)

- 01:02 선행 세션이 `--message`로 07-10 복사형 배정 송신, 01:00 본 세션이 repo 파일 작성.
  repo `OVERNIGHT_2026-07-11.md`를 정본 제안 → 07:00 이사님 결정.
- RPG: ① 1턴 패링 손맛 인터페이스 draft ② 2번째 씬 풀 1판 플레이스루 대본.
- autotrader: ① 세 시나리오→전략 선택 나침반(의사결정 트리) ② WS/exit/하이브리드 3-way 비교.
- scenario: ① d1(Rio) 부가설명 블록 ② d2(Ji-Won) 부가설명 + 가상제품 사칙 정위치.
  ★Rio·Ji-Won 디벨롭·창작 확장·새 자산 금지.

### 07-12 밤 배정 + 중복 트리거 재발

- 07-11 밤 과제 3팀 전체 미수행 → 재배정. 선행(01:02, commit `071d402` 정본) + 본 세션(01:04~05)
  방향 충돌 → 본 세션이 양보, 3팀 정정 송신 + repo `OVERNIGHT_2026-07-12.md` 3개 보류.
- 재발 방지(cron 중복 감지 락)가 긴급 안건이었으나 07-20 크론 전면 제거로 사실상 무산.
- 07-12 09:10 감사 실측: notes ahead 2(+로컬 수정 2건), autotrader ahead 2(+7건), rpg_game
  ahead 1(+6건), scenario ahead 2(+미추적 다수). 팀장 repo 기계적 push 금지, 정본/보류/폐기
  분류 후 이사님 확인 필요 — **08-16 현재까지 미처리, 대기 결정 #4로 이월**.

### 07-12 scenario freeze → 해제

- 07-12 freeze(리뉴얼 전 수정 금지) → 같은 날 17:23 이사님 승인 "프리즈 전면 해제"로 해제.
  리뉴얼 룰 7조 확정: reviewed 자산만 사용 / fragment ID·입력커밋·기여 기록 / `.extract`·
  `catalog/index.json`·crawler후보·`needs_review` 입력금지 / 게시물완결 / 보정재실행 /
  `usable`·`usable_with_changes`·`not_usable` 판정 / 산출·검증근거·한국어해설 Git커밋.

### 07-16 이후 조직 변동

- 07-16: `aws-trader` pause(이사님 지시). Agent Mail v1 registry 성립(07-14) → v2 rollout.
- 07-19: 공유 Git 접근 전 에이전트 복원(`b5c6559`).
- 08-08: `music_video` 저장소 매니저 범위 추가(`8af5683`).
- 08-16: Windows Codex·ZCode 구독 종료. Matrix 통합 후임 = `aws-manager`
  (`decisions/2026-08-16-matrix-successor-handoff.md`). actors.json v8에서 windows-codex/
  windows-zcode는 아직 `runtime_verified` 잔존 → 감사 안건(잔여 권한 처분).
