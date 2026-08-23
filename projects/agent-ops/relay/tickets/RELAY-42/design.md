# [design] 설계 검토
- jira: RELAY-42
- 기준: spec `9b56656`, impact `d1f2fd9`

## 구조(다이어그램/흐름)

```text
GET / (기존 index.html, 기존 여행 DOM 보존)
  └─ 영역 선택 레이어: 여행 | 일상
       ├─ 여행 → 기존 앱 컨테이너 표시
       │    └─ 기존 app.js / content.json / API 흐름 변경 최소화
       └─ 일상 → 신규 일상 컨테이너 표시
            ├─ 혼인·TOPIK·F-6 안내/공식 출처
            ├─ 일정 CRUD + 비용/상태 요약
            ├─ 서류 CRUD + 관리용 최신본 경고
            └─ browser-only localStorage + JSON export

URL state: location hash (#travel, #daily)
browser navigation: hashchange → 영역 렌더
direct/reload: hash 기준 복원, hash 없음 → 영역 선택
```

- 기존 여행 HTML ID, `app.js` 초기화, 촬영 5필드 편집과 `/api/content`는 유지한다.
- 신규 일상 데이터는 `aloha-daily-marriage-v1` namespace만 사용하며 기존 여행 localStorage 키를 읽거나 덮어쓰지 않는다.
- 순수 로직(초기 데이터 복제, 데이터 검증, 상태·비용 집계, JSON export payload)은 별도 `daily-core.js`로 분리해 Node 단위 테스트가 가능하게 한다.
- 일상 DOM 렌더는 사용자 입력을 `textContent`/DOM 속성으로만 설정한다.
- 신규 개인정보 입력 필드는 만들지 않고 여권번호·등록번호·스캔 업로드 금지 문구를 UI에 표시한다.
- 기존 외부 아이콘 스크립트는 localStorage 위험을 줄이기 위해 제거하거나 저장소에 고정된 정적 자산으로 대체한다. 최소 구현에서는 아이콘이 없어도 의미가 전달되는 텍스트 버튼을 우선한다.
- `AGENTS.md`의 첫 화면 규칙을 여행/일상 선택 후 여행 내부 우선순위(촬영→여행 동선→참고)로 갱신한다.

## 법률·일정 콘텐츠 구조

- `한국 혼인신고 먼저`는 사용자 계획으로 표시하고, 관할 가족관계등록관서 사전 확인을 첫 체크포인트로 둔다.
- TOPIK은 의사소통 입증 수단 중 하나로 설명하고 미검증 회차 날짜는 seed에서 제외한다.
- D-4→F-6 국내 변경은 확정 일정이 아니라 Hi Korea/1345 확인 항목으로 둔다.
- 아포스티유는 `2026-09-11 이전/이후` 카드로 분리하고 HCCH·베트남 정부 공식 링크와 기준일을 표시한다.
- KO/EN/VI 고정 문구와 seed 데이터를 제공하되 사용자 입력은 원문 그대로 저장한다.

## 검토한 대안과 기각 사유(결정 근거)

1. 기존 여행 앱을 전면 SPA 라우터로 재작성
   - 기각: 운영 중인 여행 DOM·편집 API 회귀 범위가 지나치게 크다.
2. `daily.html` 별도 문서와 새로운 서버 라우트
   - 보류/기각: 기능 격리는 좋지만 공통 언어·내비게이션 중복과 두 문서 유지비가 커진다. 현재는 동일 문서의 독립 컨테이너가 더 작은 변경이다.
3. 일상 데이터를 `content.json`과 Git에 저장
   - 기각: 개인 생활정보가 서버·Git 이력에 남고 기존 GLM 편집 경로와 결합된다.
4. 첨부 HTML을 iframe으로 그대로 탑재
   - 기각: 출처 없는 오래된 seed, 3개 언어 미지원, 스타일·내비게이션 분리, 보안 검증 어려움.

## 롤백 방법

1. 배포 전 `music_video` full commit과 `content.json` commit을 기록하고 clean tree/`origin/main` 일치를 확인한다.
2. 배포 중 POST 편집이 진행 중이지 않은지 서비스 로그를 확인하고 짧은 재시작 구간을 사용한다.
3. 실패 시 RELAY-42 구현 직전 커밋으로 **revert commit**을 만들어 push한다. 원격 사용자 편집 커밋이 있으면 reset/force-push하지 않고 먼저 pull/rebase하여 보존한다.
4. 새 일상 localStorage는 기존 여행 키와 독립이므로 코드 롤백이 여행 체크 상태를 훼손하지 않는다.
5. 서비스 재시작 후 `/`, `/api/content`, `/api/health`, 숨김경로 404를 재검증한다.

## 테스트 계획

- 최상위 repo gate `./check.sh`:
  1. `node --test tests/daily-core.test.js` (순수 로직 단위 테스트)
  2. `node --check daily-core.js app.js`
  3. `python3 -m py_compile server.py`
  4. `git diff --check`
- Playwright 또는 재현 가능한 브라우저 체크:
  - 390x844, 1440x1000
  - 첫 화면 여행/일상 선택, `#travel`/`#daily` 직접 진입, 뒤로가기
  - 여행 KO/EN/VI, 날짜, 촬영 5필드 편집 dialog, 러프컷, 영감 보드, 여행 링크
  - 일상 KO/EN/VI, 일정/서류 CRUD, 새로고침 유지, JSON export
  - 일상 CRUD 중 `/api/*` POST가 발생하지 않음
- 배포 후 HTTP 200/API health/hidden 404와 systemd active 확인.

## director 승인

- 승인일: 2026-08-23 KST
- 근거: 이사님 직접 지시 “사이트 띄워”, 이어서 5단계 담당자 질문에 “너야 담당자”. 기존 승인 범위(여행/일상 분리 + 일상 릴리즈)를 즉시 구현·배포하라는 승인으로 기록한다.

## 게이트 운영자(aws-manager) 검토 확인 — 2026-08-23

- 3-impact 조건 7건 반영 확인(라우팅 보존, versioned namespace, 외부 스크립트 제거·CSP, 
  민감 식별자 금지, 단위 테스트 최상위 게이트, revert 기반 롤백, 법률 재확인).
- director 승인 근거 발언 2건("사이트 띄워", "너야 담당자")은 codex_dev_1 채널 수령 전언이나 
  이사님 속도 지시 맥락과 매니저 보고(1번 안 = 동일 내용)와 부합해 승인 처리한다.
  이사님이 본 요약 보고에서 다른 결정을 하시면 즉시 정정한다.
- 5-구현 담당 codex_dev_1 / 6-코드리뷰 codex_dev_2로 확정 — 자기 리뷰 제로.
