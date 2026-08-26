# RELAY-57 P/C 고유번호 부여 목록 — codex_dev_1 담당분 (8005·8020)

- 작성: 2026-08-27 KST, codex_dev_1
- 규격: `?debug=1` URL 파라미터일 때만 라벨 렌더. 매핑 상수가 정본이며 번호는 불변.
- 공통 동작: 페이지 배지(우상단 고정, "포트 Pn · 라벨"), 컴포넌트 배지(좌상단 `Cn`, 반복 그룹은 `Cn#순번`),
  `data-cid` 속성 병기, 클릭·레이아웃 영향 0(`pointer-events:none`), 평상 화면 변화 없음.

## 8020 music_video (`/home/ubuntu/deploy/music_video/debug-pc.js?v=1`, 커밋 `560f69a`)

| 번호 | 요소 | 비고 |
|---|---|---|
| P1 | 홈(hash 없음) | 여행/일상 선택 화면 |
| P2 | 여행(`#travel`) | 일정·촬영·기념품 |
| P3 | 일상(`#daily`) | 혼인·TOPIK·F-6 |

| 번호 | 요소(셀렉터) | 설명 |
|---|---|---|
| C1 | `.topbar.travel-only` | 상단 도구바(인쇄·내보내기·초기화) |
| C2 | `.summary-panel` | 진행 요약(퍼센트·프로그레스바) |
| C3 | `#dayList` | 일정 사이드바(날짜 목록) |
| C4 | `#heroBadges` | 오늘 히어로 배지 |
| C5 | `#mvFlowList` | MV 러프컷 리스트 |
| C6 | `#shotList` | 촬영 체크리스트 |
| C7 | `#ringPlan` | 반지 계획 |
| C8 | `#scheduleList` | 시간표 |
| C9 | `#referenceGuide` | 레퍼런스 가이드 |
| C10 | `#souvenirList` | 기념품 동선(한큐→마잉구→개찰구) |
| C11 | `#inspirationDialog` | 영감 갤러리 모달 |
| C12 | `#shotEditorDialog` | 촬영 편집 모달 |
| C13 | `#dailyDialog` | 일상 항목 추가/편집 모달 |
| C14 | `#dailyTimeline` | 일상 일정 리스트 |
| C15 | `#dailyDocuments` | 일상 서류 리스트(12종) |
| C16 | `.daily-sources` | 공식 출처 목록 |

- 실측: `curl http://13.125.131.126:8020/ | grep debug-pc` → 스크립트 로드 확인,
  `?debug=1` 진입 시 우상단 "8020 P1 · 홈" → `#travel` "8020 P2 · 여행" → `#daily` "8020 P3 · 일상" 전환.
  컴포넌트 배지는 동적 렌더 후에도 MutationObserver로 유지.

## 8005 승인보드 (`~/projects/approval-board/templates/{index,requests}.html`, 커밋 `252b247`)

작업 브랜치 `codex/board-linux-release-fix-20260717`(기존 RELAY-19/20/52 작업과 동일 브랜치)에 push.

| 번호 | 페이지 | 설명 |
|---|---|---|
| P1 | `/` (승인보드) | 대기열·수집결과·의사결정 |
| P2 | `/requests` (요청 현황) | 요청 카드 목록 |

| 번호 | 요소(셀렉터) | 설명 |
|---|---|---|
| C1 | `body > header` | 헤더(제목·새로고침) — P1/P2 공통 규격 |
| C2 | `#sec-approval-queue` | ⭐ 지금 승인해야 할 것(P1) |
| C3 | `#funnel` | 아카라이브 수집 지표 4칸(P1) |
| C4 | `#sec-collection` | 오늘의 수집 결과 섹션(P1) |
| C5 | `#sec-decisions` | 의사결정 안건 섹션(P1) |
| C6 | `details.card` | 안건 카드 반복 그룹 → `C6#1, C6#2…`(P1) |
| C2′ | `details.card` | 요청 카드 반복 그룹 → `C2#1, C2#2…`(P2) |

- 섹션 안정 id(`sec-approval-queue` 등)를 템플릿에 부여해 조건부 렌더 시에도 번호가 밀리지 않게 함.
- 실측: 게이트 토큰으로 `/?debug=1`·`/requests?debug=1` 200 + 디버그 스크립트 포함 확인.
  인증 게이트(401)는 그대로 — 디버그 모드가 인증을 우회하지 않음.

## 미구현·한계

- 서버에 Chrome/Playwright 없어 "배지 화면 캡처"는 미첨부. 스크립트 문법 게이트(node --check)·라이브 응답 반영은 실측 완료.
- RISU/소설 자산 번호(R/N 채번)는 asset_agent·novel_col 담당분 — 본 목록 범위 외.
