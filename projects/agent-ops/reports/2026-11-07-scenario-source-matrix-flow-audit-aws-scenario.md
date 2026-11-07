---
title: "[3a301711 분담1] 원천·매트릭스엔진 제품흐름 조사 (읽기 전용)"
status: submitted
date: 2026-11-07
author: aws-scenario (heav_lnx_scenario_bot)
linked: 3a301711-bc42-49f3-93dc-99389f29658d (매트릭스 조직 정렬·리모델링 작업지시)
work_order: notes@c3f459e projects/agent-ops/work-orders/2026-11-07-matrix-org-remodeling-mandate.md §5
comm_msg: idem-98e529cf0a263b2eb7c567b8c3b9ce81 (ACK id 1794059068187-23, progress id 1794059319717-27)
constraints: read-only — 운영 변경·배포·삭제 없음. 미커밋 작업 보존(scenario 1건·matrix_asset_agent 5건 그대로 둠).
measured_at: 2026-11-07 13:36~13:55 UTC (22:36~22:55 KST)
---

# 원천·매트릭스엔진 제품흐름 조사 — 3a301711 분담1 (aws-scenario)

## 0. 한 줄 결론

원천→시나리오 카탈로그까지는 **실자료 파이프라인이 실재하고 지금도 진행 중**이지만
(정독 커밋 11/7까지), 카탈로그→매트릭스 엔진 소비의 마지막 홉은 **계약·코드·배포만 실재하고
실측 증거가 없다** — 출판물은 3 situation_recipe(테스트 대기), 8012 런타임의 42 works는
2026-07-28 시나리오 커밋에 고정, 마지막 work 7/29, 승인(approvals) 0, 8011은 다운.
즉 "매트릭스 엔진 중심 제품 흐름"은 **설계·계약은 완결형, 운영은 7월 말에 멈춘 상태**다.

## 1. 조사 범위·커버리지

- 정의한 대상: 저장소/배포 실행체 10 — scenario, matrix_asset_agent, matrix-studio(8021),
  matrix-home(8018), projects/matrix-engine(프로토타입), 홈 `matrix`(의미 정본),
  `matrix_codex` 배포(8012), `matrix_zcode` 배포(8011), `matrix`(~/matrix-repo 여부),
  rpg_game 소비 인용(분담2). 실행 포트 7종(8009·8011·8012·8017·8018·8021·8024) + mongo 27017.
- 확인: 저장소/배포 10/10 실측(git 상태·코드·런타임 DB 읽기 전용 조회), 포트 7/7 리슨 실측.
- 미확인 2: GitHub 오픈 PR 상태(scenario·matrix_asset_agent) — gh 미설치·비공개 API.
  단 원격 브랜치는 백업 브랜치 외 없음(로컬 관점).

## 2. 원천 → 시나리오 카탈로그 (실재·진행 중)

- scenario 저장소 catalog 실측: `extracted_raw` 762파일, `prompt_fragments` 67,
  `normalized` 24, `rpg_cards` 1, `sources/`(수집 원장 NDJSON), `import_staging/`
  (matrix_component_candidates 포함), `publications/`.
- 규칙 준수: HARD_RULES의 parser-backed·provenance(source_sha256 등) 체계가
  파일 구조로 실재. 신규 작업은 계속 진행 — 최근 커밋 34c1750(11/7, 소설 75화 정독),
  29a5d06(1422만 110/150화). 원천 수집·정독이 본업으로 살아 있다.

## 3. 카탈로그 → 매트릭스 엔진 소비 (계약 실재, 실측 증거 없음)

### 3-1. 출판 계약과 실물

- `scenario/catalog/publications/runtime_assets_8011_8012.ndjson`: **3행** — 전부
  `situation_recipe`(소설 기반 regress-lord-rest·1-200-250929·warp-infinite-growth),
  review_status=reviewed, runtime_status=active, availability_verdict=usable, sha256 근거 포함.
- `asset_migration_lock.json`: 원천은 matrix_asset_agent@1bf95a46, source_units 105,
  상태 **`ready_for_8011_8012_test`** — "3 runtime assets — minimal test set",
  legacy_direct_read=forbidden. 즉 정상 경로 출판물은 준비됐으나 **테스트 대기**.

### 3-2. 소비자 8012(matrix_codex) 실측 — 가동이지만 7월 데이터에 고정

- 프로세스: 8012 리슨 중, 릴리스 `releases/5559eb2f…`(full sha 고정 배포), 2026-09-20 기동(48일).
- 코드: `publication.py`(matrix-scenario-publication-v1 엄격 리더 — 배포 묶음·sha256·
  component 유형 검증), `catalog.py`(시나리오 Git 커밋 고정 판독, DEFAULT 467faa92).
- 런타임 DB(읽기 전용): works 42, candidates 78, checks 14, **approvals 0**, sessions 8,
  turns 11, harness_runs 130, model_calls 103.
- **works 42건 전부 scenario_commit=467faa92…(2026-07-28) 고정**, 최신 work created 2026-07-29.
  candidates payload에서 runtime.novel.*/situation 검색 **0건** — 출판물 3건이 8012에
  적재됐다는 증거 없음. DB 파일 mtime 8/17 이후 신규 쓰기 없음(유휴 가동).
- 배포 입력 `inputs/scenario-<full-sha>` 5종(7/28~8/1) — 해당 커밋은 origin/main에 존재 확인.

### 3-3. 소비자 8011(matrix_zcode) — 다운

- 8011 리슨 없음. receipts에 arcade-canary-8011, reviewed-source c2~c4(카탈로그·조회)까지
  존재 = 과거 실사용 흔적. 현재 실행체 없음.

### 3-4. 판정

원천→카탈로그 **실재(진행중)** / 카탈로그→출판물 **실재(3건, 테스트 대기)** /
출판물→엔진 런타임 섭취 **증거 없음(8012는 구커밋 워크만, 8011 다운)** /
엔진→RPG 소비 **0** (분담2 aws-rpg 보고 인용) / 상호작용 피드백 **없음**.

## 4. 매트릭스 계열 실행체 현황 (2026-11-07 실측)

| 실행체 | 상태 | 실측 근거 |
|---|---|---|
| 8024 matrix-studio-spring | 가동 | java 리슨, comm API 오늘 whoami/inbox/ack/send 전부 200 |
| 8021 matrix-studio (RELAY-58) | 가동 | FastAPI, mongo 127.0.0.1:27017 workbench db 소비, git e3466c0 |
| 8018 matrix-home (RELAY-57) | **충돌** | 수동 python(9/17~)이 포트 점유, systemd 유닛은 "Address already in use"로 exit 1 반복(저널 11-07 13:47) — 서비스는 수동 프로세스가 내줌 |
| 8012 matrix_codex | 가동·유휴 | §3-2 |
| 8011 matrix_zcode | **다운** | 리슨 없음 |
| projects/matrix-engine | 프로토타입 | **git 저장소 아님**, config 기본값이 Windows 경로, data/sessions 빈, DB cores·arca_assets·novel_progress·knowledge 전부 0(잔재: sessions 7·turns 8, 8월), 기본 `~/matrix-repo` 부재 → 이 호스트에서 실데이터 미연결 |
| 홈 `matrix` | 문서 중심 git | 최근 커밋 949fef3(docs·역할 지도), 의미·계약 정본 |

## 5. 예시·fixture·정적 화면·미연결 API 구분

- **실자료 기반**: scenario catalog(762 extracted_raw 등), publications 3건, 8012 런타임
  (42 works·103 model_calls는 실호출 기록 — 단 7월분), 8021 mongo basket, 8024 comm 원장(655건).
- **테스트·예시(정상 분리)**: matrix_codex/matrix_zcode의 `fixtures/`(계약 테스트용,
  소비 코드와 분리 배치 — 위험 낮음), 8012의 7월 말 하네스 워크(개발 검증 흔적).
- **미연결/모순**: projects/matrix-engine(프로토타입 — 실데이터 0, Windows 경로 기본값,
  git 아님), `matrix-engine-app`(홈의 빈 디렉터리), matrix-home systemd 유닛(포트 충돌로
  실제 서빙과 분리). "matrix-engine"이라는 이름이 실제 배포 consumer(matrix_codex/matrix_zcode)와
  달라 문서·인지 정리 필요.

## 6. Git·미커밋·배포 현황

- **scenario**: main(로컬=origin/main 34c1750) + 원격 backup/* 6종. 미커밋 1건
  `novel_assets/images/manifest.ndjson`(M) — **보존함, 소유자 확인 필요**.
  열린 로컬 브랜치 없음. PR 미확인(도구 부재).
- **matrix_asset_agent**: main 2752d59(11/3 release 커밋) + backup 1종. 미커밋 5건 전부
  `*.bak-*`(RELAY-56·IP 백업) — **보존함**. PR 미확인.
- **배포 버전**: 8012=릴리스 full-sha 5559eb2f(9/20~), 8021=git e3466c0, 8018=수동 프로세스
  (배포 버전 미확정), 8011=미가동.
- 세션·문서·배포 버전 불일치: 매니저 README 지도(8011/8012 consumer)는 실측과 부합하나,
  "매트릭스 엔진" 문서들(matrix-engine·MATRIX-SUCCESSOR)이 가리키는 실체가 호스트마다 다름.

## 7. 불일치 목록 (영향 순)

1. **엔진 소비 흐름 정지** — 의도: 매트릭스 엔진 중심 제품 흐름 / 실제: 출판 3건 테스트 대기,
   8012 신규 work 0(7/29~), approvals 0, 8011 다운 / 근거: §3 / 영향: 제품 목표 자체 진행 없음 /
   원인: 리뷰→승인→Build→세계 실행 단계의 운영 주체·트리거 부재 / 처리안: 유지+운영 재개
   (재출판·승인 루프 지정) / 담당: 매니저(조정)+이사님(승인) / 검증: 8012 신규 work·approval
   레코드 / **결정 필요**.
2. **카탈로그 762 vs 출판 3 공급 병목** — 원천은 계속 쌓이나 엔진 재공급 트리거 없음 /
   처리안: 출판 기준·주기 설계(예: 소설 정독 체인 근거→situation_recipe 후보) / 담당:
   aws-scenario 제안→매니저 / 검증: publications 행수 증가 / 결정 필요(기준 확정).
3. **8011 matrix_zcode 다운** — 과거 receipts 있음, 현재 미가동 / 처리안: 재기동 or 역할
   정리(8012로 통합 여부) / 담당: 매니저+운영 / **결정 필요(운영 변경)**.
4. **8018 포트 충돌(RELAY-57 미완)** — 수동 프로세스(9/17~) vs systemd 유닛 크래시 루프 /
   영향: 재부팅 시 서비스 불명확 / 처리안: 수동 프로세스 정리 후 유닛 인계 / 담당: 운영(INFRA) /
   **결정 필요(운영 변경, 본 조사 범위 밝)**.
5. **matrix-engine 프로토타입 실체 정리** — git 아님·실데이터 0·Windows 경로 / 처리안:
   문서화(프로토타입 명시) 또는 폐기 후보 / 담당: 매니저 / 결정 필요(폐기 여부만).
6. **PR 상태 미확인** — gh 미설치·비공개 / 처리안: gh 설치 또는 매니저 일괄 확인 / 담당: 운영.

## 8. 역할 확인서 (§7 — aws-scenario 자기 서술)

- **제품 목적과 내 기여**: 이사님이 준 RISU/소설 원천을 검증·가공해 매트릭스 엔진이 새
  인물·세계를 만드는 창작 인프라. 나는 그 **입구(원천→카탈로그→리뷰 출판)** 와
  가용성 판정을 담당한다. 창작은 본업이되 디벨롭은 컨펌 후(시나리오 사칙).
- **입력 / 출력 / 의존**: 입력 = Arca·소설 원문(로컬 evidence), 관제(Codex) 패킷, 매니저
  지시(mail·comm). 출력 = parser-backed catalog, publications(정상 경로 출판물), 소설
  정독 근거(reading-map·체인), 보고서. 의존 = windows-codex(로그인·게시글 선정),
  matrix_asset_agent(입고·lifecycle), 8012/8011(소비자), aws-audit(검증).
- **권한과 완료 입증**: 등록 repo 읽기·쓰기·commit·push. 금지: unreviewed_asset_promotion,
  controller_secret. 완료 입증 = 원격 origin/main full commit + 원문 경로 제시(본 보고서가 그 예).
- **현재 목표와 어긋난 점**: (1) 내 산출(카탈로그·정독 근거)이 엔진 재공급과 연결 안 됨 —
  출판 트리거 부재 (2) 8012가 7/28 스냅샷에 고정 — 최신 카탈로그 미반영 (3) 소비 루프
  (RPG→엔진 피드백) 미착수.
- **다음 한 가지 실행**: 매니저 조정 아래 소설 정독 체인 근거에서 situation_recipe 후보
  목록을 만들어 리뷰 패킷으로 제안(실행은 별도 intent=execute mail 필요). 책임: aws-scenario.

## 9. 결정 필요 사항 (decisions_needed)

1. 8012 publication 테스트·승인 루프 운영 재개 여부와 담당 지정(이사님 승인 포함).
2. 카탈로그→엔진 재공급 기준·주기(무엇을 언제 출판할지).
3. 8011 재기동 vs 폐기, 8018 포트 충돌 정리(운영 변경 — 본 조사는 읽기 전용으로 준비만 제공).

— 이상. 모든 실측은 읽기 전용(파일·sqlite mode=ro·journal·프로세스 목록)으로 수행했고,
운영 변경·배포·삭제는 없음. 토큰값·세션 ID·비밀은 본문에 없음.
