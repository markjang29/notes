# [impl] 구현 기록
- jira: RELAY-42
- 구현 담당: codex_dev_1 (이사님 직접 지정: “너야 담당자”)
- 배포일: 2026-08-23 KST

## 커밋 목록(해시 + 한 줄)

- `music_video` `2fe9000e09d1dd0d0f37a314fbd85a88e26e3ac5` — `RELAY-42 여행·일상 분리와 혼인 준비 페이지 추가`
- 설계 근거 `notes-registry` `14f8bf7` — `RELAY-42 여행·일상 분리 설계 및 승인 기록`

## 구현 요약

- `/` 첫 화면에 `여행` / `일상` 선택 추가.
- 기존 여행 DOM/API를 보존하고 `#travel` hash로 진입·새로고침 가능.
- `#daily`에 혼인·TOPIK·F-6 일정/서류 CRUD, 상태·비용 요약, JSON export 추가.
- 신규 데이터는 `aloha-daily-marriage-v1` localStorage에만 저장하고 `/api` POST를 사용하지 않음.
- KO/EN/VI 일상 UI 전환과 공식 출처·기준일 카드 추가.
- 2026-09-11 베트남 Apostille 발효, 한국 선혼인신고 관할기관 확인, TOPIK 비유일성, D-4→F-6 비단정 표현 반영.
- 외부 `unpkg` 실행 스크립트 제거.
- `daily-core.js` 순수 검증/집계/백업 로직과 Node 단위 테스트, 최상위 `check.sh` 추가.

## 테스트 결과(명령과 출력 요약)

- `./check.sh`
  - `node --test tests/daily-core.test.js`: **4/4 pass**
  - `node --check daily-core.js daily.js app.js`: pass
  - `python3 -m py_compile server.py`: pass
  - `git diff --check`: pass
- Playwright 임시 서버 `http://127.0.0.1:18021`: **2/2 pass**
- Playwright 공개 서비스 `http://13.125.131.126:8020`: **2/2 pass**
  - viewport 390x844, 1440x1000
  - 홈→여행→일상, hash 직접 진입, KO/EN/VI, 여행 촬영 5필드 dialog
  - 일상 CRUD·새로고침 localStorage 유지
  - 일상 작업 중 POST 요청 0건
  - 가로 overflow 없음
- 배포 후:
  - systemd `music-video.service`: active
  - `/`: 200
  - `/#daily`: 200
  - `/api/health`: `ok=true`, `git=true`, `translation=true`, model `glm-4.7`
  - `/.git/config`, `/.env`: 404
  - 배포 전후 `content.json` 사용자 데이터 변경 없음(SHA-256 `db0df0add5e86de30f233f608320f44b636934ed3135b666820bed5ef7fad406`)

## spec 대비 이탈 및 사유

- JSON **가져오기(import)**는 구현하지 않았다. spec에서 import는 선택사항이며, 개인정보·스키마 위험을 줄이기 위해 export만 제공한다.
- 사용자 입력 자동 번역은 하지 않는다. spec대로 원문을 보존한다.
- 첨부 HTML의 모든 seed 날짜·서류를 그대로 복제하지 않았다. 확인되지 않은 TOPIK 회차 날짜와 단정적 인증 요구를 제거하고, 공식 확인 중심의 최소 seed만 제공한다.
- 구현 담당자가 원래 6-코드리뷰 전관이므로 자기리뷰를 하지 않는다. 6단계는 codex_dev_2 또는 독립 리뷰어 재배정이 필요하다.

---

# 재검토 대응 — 반려 1~3·5~7 수정 (2026-08-27 KST)

- 구현 담당: codex_dev_1
- 수정 커밋: `music_video` `b23cb3a` (origin/main non-force push, `99c8796..b23cb3a`)
- RELAY-57 함께 구현: `music_video` `560f69a` (?debug=1 P/C 배지 — 5-impl 범위 외 기록)

## 반려 사유별 수정 내역

1. **분기 단위 테스트 부족 → 21→22건 확장, 분기 커버리지 80.43%→92.16%**
   - `node --test --experimental-test-coverage tests/daily-core.test.js`:
     `daily-core.js` line 99.32% · branch 92.16% · functions 100% (전체 파일 합산 branch 94.95%)
   - 추가 커버: 잘못된 version/collections, document 101개, null/array item, 빈 문자열·1,000자 초과,
     issue date 형식, validity NaN/음수/상한 초과, cost NaN/상한 초과, exportPayload 기본 시각(ISO 정합).
   - 잔여 미커버 분기는 UMD 로더 조건(`module.exports` vs `root.*`) 1곳뿐 — Node 테스트 도달 불가 영역.
   - 부수 수정: 기존 `Number(item[field] || 0)`가 NaN을 0으로 삼키던 구멍을 제거했다.
     빈값/undefined/null만 0으로 정규화하고 `Number("abc")`=NaN은 `invalid cost/validity`로 거부.

2. **status enum 검증 부재 → enum 제한 + 허용/거부 전값 테스트**
   - `DailyCore.STATUSES = ["todo","check","done"]`. timeline/document 모두 enum 외 값 거부.
   - 테스트: 허용 3값 전수 통과 + `<not-enum>`/빈문자/`DONE`/공백/undefined/null 거부 확인.

3. **실패 저장 원자성 → 복사본 검증 후 반영 + 회귀 테스트**
   - `DailyCore.applyItem(state, kind, item)`: state 복사본에 반영→전체 재검증→새 state 반환. throw 시 원본 불변.
   - `daily.js saveForm`은 applyItem 성본만 `persist`에 전달. 삭제도 `removeItem`(복사본 기반)으로 전환.
   - 테스트: 유효 저장은 원본 미변경·신규 항목 반영 확인 / 무효 저장(status enum 위반)은 throw 후
     원본 state가 JSON 직렬까지 byte 동일함을 검증.

5. **v1 데이터 미보존 → v1→v2 자동 마이그레이션 + 테스트**
   - `DailyCore.migrateV1(v1State, seedState)`: v1 timelines/documents 전부 보존하고,
     v2 seed 서류 중 이름/slug 겹치지 않는 것만 추가. v1 localStorage 키는 삭제하지 않아 원본 복구 경로 유지.
   - `daily.js load()`: v2 키 없음 + v1 키 존재 → 마이그레이션 결과를 v2에 적재.
   - 무효 v1 페이로드는 기존대로 초기 seed로 폴백(추측 복구 금지).
   - 테스트: 사용자 문서·일정 생존 + seed 12종 부착(총 13) + v1 입력 객체 불변 + 무효 version 거부.

6. **서류별 공식 근거 부재 → 전 카드 sourceLabel/sourceUrl/checkedAt**
   - `daily-seeds.js`(신규)로 seed 분리: 서류 12종 전 건에 `sourceUrl`(https 강제 검증)·`checkedAt`(2026-08-23)·
     언어별 `sourceLabel`. 카드 하단에 "출처 · 라벨 · 기준일" 클릭 가능 링크(`rel="noopener"`)로 렌더.
   - 180일/90일/25,195,752원 등 수치는 해당 카드 note와 sourceUrl로 추적 가능.
   - URL은 index.html 하단 공식 출처 8종과 동일한 상수에서만 공급(신규 외부 링크 0건).
   - 테스트: 전 seed https URL·날짜 형식·라벨 비빈 검증 + `validateState`가 http/javascript: URL 거부 확인.

7. **KO/EN/VI seed 계약 → 안정 slug 기반 번역 projection**
   - timeline 4종·서류 12종 × ko/en/vi 전 언어 seed. 언어 전환 시 `DailyCore.project(state, dict)`가
     slug 일치 항목만 해당 언어 필드로 치환해 표시(사용자 추가·편집 항목은 원문 유지).
   - seed 편집 저장 시 slug를 제거해 커스텀 항목으로 전환 — projection이 사용자 입력을 덮어쓰지 않음.
   - facts 라벨(번역/공증/인증/최신본)·출처 라벨·안내 문구도 3개 언어 제공.
   - 테스트: ko≠en 문서명 검증, 알 수 없는 언어는 한국어 폴백, dict 미제공 시 무변경, 3개 언어 seed가
     모두 `validateState` 통과.

## 재현 가능한 브라우저 회귀 (review 요청 사항)

- `tests/browser-checklist.md` 커밋: 마이그레이션/원자성/출처링크/언어전환/여행회귀 5절·재현 콘솔 명령 포함.
- 본 서버 환경에 Chrome/Playwright 미설치로 화면 자동재현은 체크리스트로 대체하며, 순수 로직은 전부 Node 테스트로 고정.

## 게이트 결과

- `./check.sh`: **22/22 unit pass** + daily-core/daily-seeds/daily/app 문법 + server.py 컴파일 + `git diff --check` 통과.
- 라이브 실측(2026-08-27): `/` 200 · `daily-seeds.js` 200 · `daily-core.js?v=2`/`daily.js?v=2` 신규 코드 반영 ·
  `/.git/config`·`/.env` 404 · `/api/health` ok/git/translation=true · 일상 사용 중 POST 0건(정적 서버 405/404 회귀).

## 재검토 요청

- 위 커밋(`99c8796..b23cb3a`) 범위로 6-코드리뷰 재요청. 리뷰어: codex_dev_2 재검토 또는 매니저 지정 독립 리뷰어.
