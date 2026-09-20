# [design] RELAY-30 — P-5 모듈 센스 큐레이션: 기능 묶음·정리 (본편)

- date: 2026-09-21
- actor: heav_lnx_codex_dev_1_bot (98 통신 dev1)
- taiga: PIPE ref 24 (story id 89) · 상태: 구현 → 설계승인대기 전이 예정
- 정본 repo: markjang29/matrix_asset_agent · tools/city_mcat.py·llm_tagger.py·workbench_web.py

## 1. 현황 실측 (1차 완료분)

- mcat 9카테고리 규칙 기반 1차 분류 완료(city_mcat.py, 커밋 2f83cdb) — 설문 Q3·게시판 필터·칩·취향순
  전부 mcat 기준으로 전환됨.
- /guide 사전 페이지 완료(ZONES.use·MCATS 정본화, 커밋 08-24분) — 이용흐름 3단계·운영 규칙 안내.
- **잔여(티켓 요구 본편)**: ① LLM 정밀 재분류 — 규칙 1차에서 못 나눈 것, 특히 `etc` 잔량 ②
  400종 기능분류(func IMG58/SYS38/FMT22…) 기반 **슬롯별 대표 선정** ③ **충돌표 완성** ④
  계열별 추천 스택.

## 2. 구조

- **② 슬롯별 대표**: module_catalog 조인 필드 `func`·`slot`(city_ingest.py:99-116 실측) 기준.
  `GET /city/modules/representative?slot=<slot>` — 슬롯별 post_rate 상위 1~3건(취향 프로필 있으면
  취향 mcat 가중). 결과를 `city_assets.module_rep={slot,rank}` 필드로 캐싱(재적재 시 보존 규칙 동일).
- **③ 충돌표**: 동일 슬롯 다중 장착 충돌 규칙표 — `tools/city_conflicts.py` 신설.
  소스: 모듈 이름·brief의 상호 배타 키워드(예: 서로 다른 상태창 스킨) + func=동일&slot=동일 조합.
  산출을 `module_conflicts` 컬렉션(양방향 쌍, 근거 키워드 포함)으로 적재, 상세 페이지에 경고 배지.
- **④ 추천 스택**: 계열(char/world/game…)별 "추천 묶음" — 슬롯별 대표 + mcat 균형으로
  프리커브 시드 3세트, `/city?zone=MODULE` 상단 "추천 스택" 카드. 로드아웃 저장 API(/city/loadout,
  id 실재 검증 있음) 재사용해 원클릭 담기.
- **① LLM 재분류**: city_mcat.py 규칙 미적중(특히 etc) 대상만 llm_tagger.py의 call_glm 인프라
  재사용 — 배치 스크립트 `city_llm_reclassify.py`, mcat 후보 9종 중 Top-1+확신도, 저확신은 수동
  검토 큐. 이사님 지시로 확정된 Inlay 프롬프트 사례를 따라 프롬프트는 별도 파일 관리.
- 노출: workbench_web.py page_city MODULE 섹션 + page_guide 사전에 충돌·대표 표기 연결.

## 3. 검토한 대안과 기각 사유

- 전량 LLM 분류(규칙 폐기): 비용·비결정성으로 기각 — 규칙 1차를 정답 기준으로 유지하고 LLM은
  잔여분만. (RELAY-65 §6-2: 문서·코드·DB 불일치 방지 — MCATS 9종 어휘 단일 진실 유지)
- 충돌표 수동 작성(400종 전수): 유지보수 불가라 기각 — 키워드 규칙 자동 생성 + 저확신만 수동.

## 4. 제약 준수

- 신규 웹 페이지 아님 — 8015 사이드카 기존 화면 내 카드·배지 추가(taiga-governance 2-4 (b) 존치).
- 도커·포트·인프라 변경 0. 폴링 추가 0(LLM 배치는 수동 실행·티켓 보고 기반).

## 5. 테스트 계획

- 단위: 충돌 규칙 생성기(키워드 쌍 → 양방향 테이블), 슬롯 대표 선정(정렬·가중) 순수 로직 테스트.
- E2E: 실DB dry-run — etc 잔량 N건 재분류 후보 샘플 20건 사람 눈 검증, 충돌표 생성 후
  대표 슬롯 실측, 추천 스택 카드 렌더 200 확인.

## 6. 완료조건

- ①~④ 산출물 커밋(티켓 키 포함) + 실측 증거 티켓 코멘트 · Taiga 설계승인대기 → 이사님 보드 판정.
