# [spec] RELAY-57 4단계 — 리수 자산 조합 좌표화·군집화 설계 (zcode, 2026-08-28)

## 목표
다양한 리수 자산 조합을 (1) 테스트·사용하기 쉽게 분류하고 (2) 검증 결과로 군집화하여
매트릭스 자산화 후보를 시스템이 제안하게 한다.

## 설계

### 1. 조합 좌표계 (4차원)
모든 자산(MA)에 좌표 부여 — `combo_coords`:
- `persona_axis` — 페르소나 계열 (무협/현대/판타지/로맨스/… RELAY-14 3축 기반)
- `module_axis` — 모듈 계열 (라이프/라이트보드/감정/… module_catalog 그룹)
- `lore_axis` — 로어 계열 (내장/추가/월드빌딩)
- `world` — 세계 (works/RISU_카탈로그)

좌표는 파싱 시 자동 태깅(llm_tagger 재사용) + H9 인덱스가 소급 부여.

### 2. 테스트 = 격자 샘플링
- 커버리지 엔진(coverage_engine.py)이 격자별 실시 횟수를 계산 → "미탐 격자" 큐.
- 스케쥴러가 미탐 격자에서 플랜 생성(연속 3턴 러너) — 사람이 조합 상상 불필요.
- 산출: 격자별 점수(왕복 성공률·응답 품위 길이·이미지 반응).

### 3. 군집화 → 매트릭스 후보
- 점수 상위 격자들이 인접(같은 world + 2축 이상 일치)하면 클러스터로 묶음.
- 클러스터 ≥ N개(초기 5) 충족 시 H4에 "세계 승격 제안" 카드 발행 —
  1플랜=1카드를 넘어 "이 계열 n조합이 좋았음 → 매트릭스 세계 후보".
- director 승인 → release 발행(기존 게이트 그대로).

### 4. 데이터 구조 (mongo, append-safe)
- `combo_coords`: {ma: "MA-0001", axes: {...}, tagged_at}
- `combo_grid`: {grid_key: "무협×라이프×내장×RISU", runs: n, score_avg, last_run}
- `combo_clusters`: {cluster_id, grids: [...], proposed: bool}
- 소설 파싱 추가·신규 모듈 등록 → 좌표만 append, 격자 재계산은 지연 계산.

## 일정 (RELAY-57 내)
- 4-1 좌표 태깅 (기존 MA 11 + module_catalog 400 소급) — zcode
- 4-2 격자 큐 + 스케쥴 연동 — zcode (asset_agent 협의)
- 4-3 클러스터→승인카드 연결 — zcode (manager 게이트)
