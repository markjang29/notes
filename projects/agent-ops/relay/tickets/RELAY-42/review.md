# [review] 코드리뷰
- jira: RELAY-42
- 리뷰어(bot): codex_dev_2 (`aws-codex-dev`)
- 검토일: 2026-08-23 KST
- 검토 커밋 범위:
  - `music_video` `a273c47054a83c6ba8cad25aea15ac657cccb250..2fe9000e09d1dd0d0f37a314fbd85a88e26e3ac5`
  - 설계 `notes-registry` `14f8bf791afe84e73b4e59ac6ee087fcb987efee`
  - 구현 기록 `notes-registry` `03b006262bd4d2e6178f0964f17d0571653bd24b`
- 판정: **반려**

## 반려 사유/요청 변경

1. **`daily-core.js` 분기 단위 테스트가 부족하다.**
   - 독립 실행: `node --test --experimental-test-coverage tests/daily-core.test.js`
   - 결과: line `98.67%`, branch `80.43%`, functions `100%`.
   - 현재 4개 테스트는 정상 요약·고정 시각 export, 잘못된 ID·timeline 101개, 잘못된 timeline date·음수 cost만 검증한다.
   - `validateState`의 잘못된 version/collections, document 101개, null/array item, 빈 문자열·1,000자 초과,
     issue date, validity의 NaN/음수/상한 초과, cost NaN/상한 초과, `exportPayload` 기본 시각 등 주요 분기가 테스트되지 않았다.
   - `design.md`의 순수 로직 단위 테스트 게이트와 매니저가 지정한 “테스트 없는 분기 있으면 반려” 조건을 충족하지 못한다.

2. **상태값 enum 검증이 없다.**
   - `daily-core.js:42`는 `status`를 일반 문자열로만 정리한다.
   - 독립 probe에서 timeline `status="<not-enum>"`이 `validateState`를 통과했다.
   - UI는 `todo/check/done`을 안내하고 `summarize`도 `done`만 완료로 집계하므로 임의 상태가 저장되면 표시·집계 계약이 어긋난다.
   - timeline/document 상태를 허용 enum으로 제한하고 각 허용값 및 거부값 단위 테스트를 추가해야 한다.

3. **실패 저장의 원자성을 회귀 테스트로 고정해야 한다.**
   - `daily.js:98-101`은 입력 item을 `state` 배열에 먼저 push/replace한 뒤 `persist()`에서 검증한다.
   - 검증 실패 시 catch는 alert만 하고 이미 변경된 in-memory state를 복원하지 않는다.
   - 검증 완료한 복사본을 만든 뒤 state에 반영하거나 실패 시 rollback하고, invalid 저장 후 기존 state/localStorage가
     불변임을 테스트해야 한다.

## 통과 확인

- `./check.sh`: 4/4 unit pass, JS syntax, Python compile, diff check 통과.
- 저장 namespace: `aloha-daily-marriage-v1`로 여행 데이터와 분리됨.
- 일상 사용자 입력 렌더: DOM 생성과 `textContent` 사용; 일상 코드에 `innerHTML`/네트워크 POST 없음.
- 여권번호·주민등록번호·외국인등록번호·문서 업로드 전용 입력 없음; 금지 안내 문구 존재.
- 외부 실행 스크립트 0건; 공식 출처는 `rel="noopener"` 링크로만 제공.
- `app.js` 변경은 여행 언어 selector를 `.lang-button`에서 `[data-lang]`으로 한정한 4줄이며 기존 여행 초기화
  흐름과 API 코드는 변경하지 않음.
- `server.py` 변경 없음.
- 공개 서비스 독립 smoke: `/` 200(14,183 bytes), `/api/content` 200, `/api/health`
  `ok/git/translation=true`, `/.git/config`·`/.env` 404, 신규 정적 자산 200.
- 저장소에 재현 가능한 Playwright 테스트 파일은 없어서 구현 기록의 2/2 브라우저 결과 자체는 재실행하지 못했다.
  수정 제출 때 브라우저 회귀 스크립트 또는 정확한 재현 명령/체크리스트를 커밋하면 재검토 가능하다.

## 재검토 조건

- 위 1~3을 수정한 `music_video` 후속 커밋과 테스트 결과를 RELAY-42 5-impl에 추가한다.
- 수정 커밋을 `origin/main`에 non-force push하고, 기존 여행 기능 및 일상 POST 0건 회귀 증거를 갱신한다.
- 새 구현 커밋 범위로 6-코드리뷰를 다시 요청한다.

---

## 재검토 1 — 실사용 피드백 후속 `99c8796`

- 요청 배경: 이사님 실사용 피드백 “서류 대부분 확인 필요 — 실사용 목적 미달”.
- 후속 구현: `music_video` `99c8796e301adbb6f95e006ca0d08e518f3d5c23`
  (`2fe9000`을 포함하는 origin/main).
- 변경: 서류 seed 4→12개, 발급처·방법·번역·공증·인증·최신본 안내, 공식 링크 추가,
  localStorage key `aloha-daily-marriage-v1`→`aloha-daily-marriage-v2`.
- 재검토 판정: **반려 유지**

### 미해결 기존 반려

1. `99c8796`은 `daily-core.js`와 `tests/daily-core.test.js`를 수정하지 않았다. 두 blob이 부모 커밋과
   byte-for-byte 동일하고 독립 coverage도 branch `80.43%` 그대로이므로 기존 사유 1이 미해결이다.
2. 임의 `status` 문자열 허용 검증기와 enum 테스트가 그대로이므로 기존 사유 2가 미해결이다.
3. `daily.js`의 검증 전 state push/replace 및 실패 rollback 부재가 그대로이므로 기존 사유 3이 미해결이다.
4. 단계 산출물 `5-impl.md`는 여전히 `2fe9000`과 namespace v1만 고정한다. 새 구현 커밋·배포·테스트와
   이사님 실사용 피드백/보완 이력이 5단계 산출물에 반영되지 않아 Relay 단계 갱신 규칙도 충족하지 않는다.

### 추가 반려 사유

5. **namespace v2 전환이 기존 v1 데이터를 보존하지 않는다.**
   - `daily.js`는 KEY 문자열만 v2로 바꾸고 v1 조회, migration, merge, export 안내 또는 복구 UI를 제공하지 않는다.
   - 따라서 v1 데이터가 브라우저에 존재하면 삭제되지는 않더라도 앱에서 즉시 사라진 것처럼 보이고 새 seed로 대체된다.
   - “오늘 잠깐 존재해 실사용 데이터가 없을 가능성이 높다”는 추정은 데이터 보존 증거가 아니다.
   - design/impact의 “localStorage 스키마 초기화·변경 전 JSON 내보내기” 조건에 따라 v1→v2 migration 또는
     v1 감지 후 export/recovery 선택을 제공하고 자동 테스트해야 한다.

6. **서류별 공식 근거와 기준일 연결이 부족하다.**
   - 페이지 하단에는 전역 기준일과 8개 공식 링크가 있으나, 12개 서류 카드 각각에는 source URL/기준일이 없다.
   - 특히 `180일`, `90일`, `2026년 2인 가구 연 25,195,752원`, 번역·공증·인증 안내가 어느 공식 링크의
     어느 기준일을 근거로 하는지 카드 데이터에서 추적할 수 없다.
   - eFamily 혼인신고와 TOPIK 공식 공지는 관련 페이지로 독립 확인했다. 베트남 국가공공서비스 링크는 검사 시
     timeout, 주호치민 F-6 소득 링크는 자동 조회 403이어서 내용 일치까지 독립 확인하지 못했다.
   - 각 seed에 `sourceLabel`, `sourceUrl`, `checkedAt`을 두고 카드에서 클릭 가능하게 표시하며 링크/수치 계약을
     테스트해야 spec의 “모든 법무·시험 정보 카드” 조건을 충족한다.

7. **기본 서류 seed의 KO/EN/VI 계약이 충족되지 않는다.**
   - `docSeeds`는 한국어 단일 배열이며 언어별 구조가 아니다. 언어 버튼을 바꿔도 12개 문서명·발급 방법·번역·
     공증·인증·메모 본문은 한국어로 남는다.
   - spec은 기본 데이터와 화면 문구를 KO/EN/VI로 제공하도록 요구한다. 언어별 seed 또는 안정 ID 기반 번역
     projection을 추가하고 브라우저 테스트로 본문 변경을 검증해야 한다.

### `99c8796`에서 통과한 항목

- `origin/main` 일치, `2fe9000` ancestry 확인.
- `./check.sh` 4/4와 syntax/compile/diff gate 통과.
- 서류 12개 렌더 구조는 `textContent` 기반 DOM node를 사용하며 새 server/API 변경 없음.
- 공개 서비스가 daily.js v2를 제공하고 health 정상이라는 매니저 실측과 코드가 일치한다.
- eFamily·TOPIK 링크는 공식 관련 페이지로 확인됨.

### 다음 재검토 입력

- 기존 반려 1~3과 추가 사유 5~7을 수정한 새 `music_video` 커밋.
- 새 커밋, namespace migration/rollback, 공식 출처 매핑, KO/EN/VI seed, 단위·브라우저 테스트를 반영한
  갱신 `5-impl.md` 커밋.
- 위 두 커밋이 origin/main에 도달한 뒤 재검토 요청.
