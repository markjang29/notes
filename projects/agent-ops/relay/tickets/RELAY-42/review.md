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
