# [design] RELAY-27 — P-2 구역 게시판: 무한스크롤 전환 (v6안 잔여분)

- date: 2026-09-21
- actor: heav_lnx_codex_dev_1_bot (98 통신 dev1)
- taiga: PIPE ref 21 (story id 85) · 상태: 구현 → 설계승인대기 전이 예정
- 정본 repo: markjang29/matrix_asset_agent · tools/workbench_web.py (포트 8015)

## 1. 현황 실측 (이미 구현된 v6안 선행분)

- 구역별 리스트뷰·필터 칩·취향순·인기순 정렬·로드아웃(서버 저장)·취향 설문·맞춤 피드·
  행 brief·해시태그 외 설명 추출까지 완료 (티켓 경과 2026-08-22 4건, 커밋 435577d·5812e6c·5789691).
- **잔여 요구 = "무한스크롤"**: 현재 페이지네이션(`‹ 이전 / 1/N / 다음 ›`, per=100,
  workbench_web.py page_city 내 `pnav`)으로 동작 중. 이것을 무한스크롤로 전환한다.

## 2. 구조 (변경점 최소화)

- 데이터 계열 불변: MongoDB `city_assets` 쿼리·정렬 축(name/popularity=post_rate/taste) 그대로.
- API 추가 1건: `GET /city/items?zone=…&k=…&m=…&lv=…&q=…&sort=…&after=<offset>` →
  JSON 100건+`next_offset`(null이면 끝). 기존 page_city의 쿼리 조립부를 공용 함수로 추출해
  HTML/JSON 양쪽이 같은 필터 로직을 쓰게 한다(문서·코드·API 불일치 방지 — RELAY-65 §6-2).
- 프론트: IntersectionObserver로 sentinel 도달 시 `/city/items` append.
  URL·공유·검색엔진용으로 페이지네이션 링크도 유지(점진 강화 — JS 없으면 기존처럼 동작).
- 로드아웃 바·취향 칩은 기존 DOM 재사용, append된 행에 addbtn 이벤트 재바인딩.

## 3. 검토한 대안과 기각 사유

- (a) 프론트에서 전체 fetch 후 슬라이스: 2,000+건 전송이라 기각(초기 응답 지연).
- (b) 커서 기반(_id 범위): 정렬 축이 name/post_rate/taste 3종이라 오프셋이 단순·안전. 커서는 취향순의
  in-memory 정렬과 결합 시 복잡해져 기각(100건 페이지 단위라 성능 이슈 없음 실측 근거: 기존 per=100).

## 4. 제약 준수

- 파이썬 신규 페이지 금지(09-17 공지 ③) 준수 — 신규 페이지가 아니라 기존 8015 사이드카
  (taiga-governance 2-4 분류 (b): 계산·데이터 처리형 존치) 내 엔드포인트 1건 추가.
  향후 Spring 흡수 4단계 게이트 대상임을 유지(본 티켓은 흡수 범위 변경 없음).

## 5. 테스트 계획

- 단위: 쿼리 조립 공용 함수 — zone/필터/정렬 조합 파라미터 → Mongo 쿼리 동치 테스트.
- E2E: 실서버 `/city?zone=CARD` 렌더 → 스크롤 append 3페이지 실측(행 수 100→400),
  필터 유지 확인, JS 비활성 시 페이지네이션 폴백 확인.
- 롤백: workbench_web.py 단일 커밋 revert로 완전 복구(외부 상태 없음 — 읽기 전용 API).

## 6. 완료조건

- 무한스크롤 실측 증거(행 수·네트워크 로그) 티켓 코멘트 · Taiga 설계승인대기 → 이사님 보드 판정.
