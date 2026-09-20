---
title: 리수 로드셋·장바구니·자산화 설계 v1 (PocketRisu 객체 모델 기반)
date: 2026-09-20
status: 초안 — 이사님 확인 대기
tags: [agent-ops, risu, loadset, asset-pipeline]
---

# 리수 로드셋·장바구니·자산화 설계 v1

> 이사님 09-20: "WSL이 개발 환경. risu에서 돌아가는 기준이 되도록 자산관리. 온톨로지 객체가
> 연결되듯 rawdata에서부터 조합을 세트로 묶고, 모듈의 nsfw·COT 토글 on/off처럼 조합이 생기는 걸
> 객체화·모듈화된 로드셋 구성 + 로드셋 장바구니 + 리수검증 + 자산화까지 설계."
> 기존 정본 흡수: org-charter-v1.md 11단계 파이프라인(3 바구니 · 4 로드셋 · 5 3회검증) ·
> asset-pipeline-graph-design-v1.md(게이팅 3종) · arca-pipeline-handover-v1.md.
> **모든 필드·함수는 PocketRisu v1.12.0 실측**(server 소스 `getEnabledModuleDefinitions`,
> `parseToggleKeysFromTemplate`, `applyToggleValues` + duradev 실DB 8모듈 디코딩) 기준 —
> 추상 설계가 아니라 리수가 실제로 읽는 값으로 바로 굴러가는 설계.

## 0. 실측 기반 (설계가 의존하는 리수 실제 동작)

- **모듈 활성화 해석** — `getEnabledModuleDefinitions(db, char, chat)`: 활성 모듈 ID 집합 =
  `db.enabledModules[]` + `char.modules[]` + `chat.modules[]` + `db.moduleIntergration`(콤마
  문자열). `db.modules[]` 목록에서 id 일치 **또는 namespace 일치**로 매칭 → 로드셋이 조작할
  부착 지점은 이 4곳뿐.
- **토글 해석** — `parseToggleKeysFromTemplate`: `db.customPromptTemplateToggle` + 활성 모듈들의
  `customModuleToggle`을 줄바꿈 결합 → 각 줄 `key=기본값?type` 파싱, `toggle_<key>` 키 생성.
  `group/groupEnd/divider/caption` 줄은 UI 전용이라 키 아님.
- **토글 값 보관소** — `db.globalChatVariables["toggle_<key>"]` (전역 단일 값소). 켜고 끄면 이
  맵의 값이 바뀐다. 값소가 **모듈 조합에 종속**되므로 로드셋 전환 시 값 재적용 필요.
- **프리셋/챗 바인딩** — `TogglePreset{name, values: Record<toggle_key,value>,
  promptPresetName?}`가 `db.togglePresets[]`에 저장, `applyToggleValues()`로 복원. 챗 단위 스냅샷은
  `chat.savedToggleValues`. 프리셋 전환(`changeToPreset`) 시 챗 바인딩 토글 재적용.
- **duradev 실DB 현황(2026-09-20 디코딩)** — 모듈 8개, **`customModuleToggle` 전부 null**
  (토글 조합면이 아직 미정의), `db.customPromptTemplateToggle=""`, `toggle_*` 변수 0개.
  namespace: `삶은계란`(라이프 모듈), `city-import`(그림체·모드팩 등 6개 공유). 즉 1단계
  부트스트랩 과제 = 기존 모듈에 토글 면(customModuleToggle) 정의를 붙이는 것.

## 1. 객체 모델 (온톨로지 5계층)

```
rawdata (원천)            ─ 아카 글·소설·이미지 · asset_ledger.jsonl에 이미 원장 등록
  └─ asset (자산)          ─ 원천에서 추출한 재사용 단위: 캐릭터 카드·로어북·모듈·레극스·프롬프트 조각
      └─ variant (변형)     ─ 한 자산의 기능적 조합면: nsfw on/off × COT on/off …
          └─ loadset (로드셋) ─ asset·variant의 "착용 세트" — 리수에 실제로 올리는 단위
              └─ asset (자산화) ─ 검증 통과해 원장에 승인 등록된 로드셋
```

- **객체 ID 규약**: `rs-<계층1글자>-<slug>-<hex6>` (예: `rs-a-ragna-card-a1b2c3`,
  `rs-v-ragna-nsfw-3f4d5e`, `rs-l-ragna-base-9e8d7c`). provenance 6필드(그래프 설계 v1 §2)에
  parent ID를 추가해 계층 연결 — 새 원장 만들지 않고 asset_ledger.jsonl에 연결.
- **객체 파일 규약** — WSL `~/risu/loadset/` 아래:
  ```
  ~/risu/loadset/
    assets/<asset-id>/           asset.json + 원본(rawdata 참조)
    variants/<variant-id>.json   자산 ID + 토글 패치 + 차등 설명
    loadsets/<loadset-id>.json   부착 명세(§3) + 검증 결과 링크
    baskets/<basket-id>.json     장바구니(§4)
    ledger/rs-ledger.jsonl       상태 전이 원장(그래프 설계 v1의 원장 연계)
  ```

## 2. 조합면 (variant) — 토글 객체화

- **토글은 모듈에 정의**(customModuleToggle 템플릿 줄: `nsfw=default?type:toggle` 스타일),
  **variant는 그 토글의 값 조합**:
  ```json
  { "id": "rs-v-ragna-nsfwcot", "asset": "rs-a-ragna-mod",
    "toggles": { "toggle_nsfw": "on", "toggle_cot": "off" },
    "label": "NSFW ON / COT OFF", "basis": "comb-1" }
  ```
- **조합 확장 규칙**: 한 모듈의 토글 키 n개의 값 조합 전체를 나열하지 않고, **의미 있는 조합만
  named variant로 등록**(조합 폭발 방지). 미등록 조합은 자동 유효(리수는 값소만 보므로) —
  named variant는 "자산화 후보" 표시용.
- **부트스트랩(즉시 과제)**: duradev 8모듈 전부 토글면 null → 라이프 모듈·올인원 모듈부터
  `customModuleToggle`에 `nsfw`, `cot` 등 키 정의 추가. 값소(`toggle_*`)는 로드셋 적용 시점에
  `globalChatVariables`에 써진다.

## 3. 로드셋 (loadset) — "아이템 착용" 명세

- 로드셋 = 리수 부착 지점 4곳의 **선언적 명세**(리수 API로 실제 적용):
  ```json
  { "id": "rs-l-ragna-base", "name": "라그나로크 베이스",
    "attach": {
      "enabledModules": ["rs-a-ragna-mod"],        → db.enabledModules
      "charModules":   { "<charId>": ["rs-a-art"] }, → char.modules (id 또는 namespace)
      "chatModules":   { "<chatId>": ["rs-a-hub"] }, → chat.modules
      "integration":   "rs-a-x,rs-a-y"               → db.moduleIntergration
    },
    "variants": ["rs-v-ragna-nsfwcot"],
    "personaCount": 1,                                ← charter 4단계: 페르소나 1개 강제
    "validation": { "status": "pending", "chats": [] } ← 5단계 게이트 결과
  }
  ```
- **적용 방식**: PocketRisu v1.12.0 서버 API로 (a) 백업 export→DB 수정→import 방식(이미 E2E 검증된
  경로: encodeRisuSaveLegacy·backup/import) 또는 (b) 클라 UI 수동. 초기엔 (a) 스크립트
  `/tmp`→정착 시 `~/risu/loadset/tools/apply_loadset.cjs`(내장 node 사용 — better-sqlite3 버전
  충돌 주의).
- **정합성 사전검사(charter 4단계 validation)**: 페르소나 중복 0 · 모듈 ID/namespace 실존 ·
  토글 키가 대상 모듈 customModuleToggle에 정의됨 · 레극스 충돌 스캔(같은 패턴 2중 적용 금지) —
  통과 못 하면 장바구니에서 꺼낼 수 없음(자동 게이트).

## 4. 장바구니 (basket) — charter 3단계 "담기·꺼내기"

- **basket = 로드셋 후보 큐**:
  ```json
  { "id": "rs-b-202609w38", "items": [
      { "loadset": "rs-l-ragna-base", "added": "2026-09-20", "state": "staged" } ],
    "note": "주간 검증 대상" }
  ```
- **state 전이**: `picked`(담김) → `staged`(정합성 사전검사 통과) → `verifying`(리수 3회 검증 중)
  → `validated`(검증 통과) → `promoted`(자산화 완료) / `rejected`(반려 — 사유 기록).
- **꺼내기 = loadset 적용**: 장바구니에서 staged 항목을 리수(WSL 8013)에 적용 → 5단계 검증으로.
  장바구니는 선착순 1개 적용 원칙(동시 다중 로드셋 적용 금지 — 토글 값소 충돌 방지).

## 5. 리수 검증 게이트 — charter 5단계 "최소 3회"

- **자동 게이트(WSL PocketRisu 8013 대상)**:
  1. 적용 성공(부착 4지점 값 일치 확인 — apply 후 재조회 비교)
  2. 채팅 3회 실행(조합별 최소 1회 — variant의 토글 값으로 실제 요청) · 각 회 응답 수신·빈 응답
     아님 · 레극스 에러 없음
  3. 결과 기록: `loadsets/<id>.json` validation.chats에 3회 로그(시각·프롬프트 해시·응답 길이·
     판정) 남김 → 릴레이 티켓 첨부 근거
- **검수 게이트(사람)**: 3회 로그 + 결과물 표본을 이사님·매니저 승인(그래프 설계 v1의 인가
  게이트 계승). 승인 시 `promoted`.

## 6. 자산화 (promoted) — charter 7단계 승인과 연결

- promoted 로드셋은 `rs-ledger.jsonl`에 상태 `원장`으로 기록: loadset ID · 구성 자산 ID들 ·
  variant 조합 · 검증 3회 근거 링크 · 승인자·일시.
- 승인 로드셋은 **원천데이터의 특정 가공 조합**으로 취급(charter 7단계) → 매트릭스 코어(8) →
  엔진(9) → 앱서비스(10)로 이어지는 기존 그래프에 엣지로 연결. 새 파이프라인을 만들지 않는다.
- 역참조: 매트릭스 쪽에서 "이 씬은 rs-l-ragna-base의 nsfw=on 조합으로 생성"처럼 소급 조회 가능.

## 7. 담당·게이팅 요약 (그래프 설계 v1 스타일)

- 수집·variant 정의 — 클로드(WSL 개발환경, 02_[파뱃 윈도][로드셋_장바구니] 역할 계승)
- 정합성 사전검사 — 자동 게이트(스크립트)
- 3회 검증 실행 — 자동(리수 API) + 결과 판정은 검수 게이트(사람 승인)
- 자산화 승인 — 인가 게이트(이사님)
- 데이터 원천: asset_ledger.jsonl · 리수 DB(export) · rs-ledger.jsonl — 신규 원장 최소화,
  기존 원장 연결 우선.

## 8. 다음 액션 (초안 승인 시)

1. `~/risu/loadset/` 골격 + rs-ledger.jsonl 생성
2. 라이프 모듈·올인원 모듈에 토글 면(customModuleToggle) 정의 부트스트랩
3. apply_loadset.cjs + 정합성 사전검사 스크립트(E2E: 기존 임포트 경로 재사용)
4. 기존 라그나로크 카드로 1개 로드셋 파일럿 → 장바구니 → 3회 검증 → 승인 플로우 실증
