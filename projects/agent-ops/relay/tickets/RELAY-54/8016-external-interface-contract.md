# 8016 이미지 스튜디오 외부 인터페이스 계약 (novel_col)

> RELAY-54 정합성 장부 novel_col 항목 "외부에서 전달된 core/scene을 이미지 생성에 쓰는 인터페이스"의 공식 계약.
> 기준 코드: scenario `novel_assets/images/app/main.py` + `static/index.html` (8676ae2·147449e·a32562e).
> 대상: 8015 Matrix Workbench, 매트릭스 파이프라인 6단계, 외부 봇(다ossier 리롤 링크 등).

## 1. URL 프리필 (사람·링크용) — GET /

외부에서 만든 조합을 스튜디오 UI에 프리필해 연다. 자동 생성은 하지 않고, 이사님/사용자가
열린 시트에서 "이 조합으로 리롤" 버튼으로 생성을 확정한다(승인 게이트 보존).

| 파라미터 | 필수 | 설명 | 기본값 |
|---|---|---|---|
| `core` | 권장 | identity_core — 캐릭 핵심 태그 문자열 | 현재 ED 값 |
| `scene` | 권장 | scene_layer — 장면 태그 문자열 | 현재 ED 값 |
| `entity` | 선택 | 캐릭터/개체 이름 | `다ossier` |
| `work` | 선택 | works/ 디렉토리명 또는 `RISU_카탈로그` | `RISU_카탈로그` |
| `category` | 선택 | `sfw` 또는 `nsfw` | `sfw` |
| `basis` | 선택 | 근거 문구(채팅 3턴 발췌·작품 근거). RELAY-56 scene_basis로 보존 | 빈 값 |

- `core` 또는 `scene` 하나라도 있으면 프리필 동작(시트 자동 오픈 + toast 안내).
- 값은 URL 인코딩(한국어 포함). 예: `http://13.125.131.126:8016/?core=1girl%2C%20silver%20hair&scene=rain%2C%20umbrella&work=전지적_독자_시점&basis=3화%20우산%20장면`

## 2. 생성 API (기계용) — POST /api/generate

```json
{
  "work": "전지적_독자_시점",        // 필수 — works/ 디렉토리명 또는 RISU_카탈로그
  "entity": "김독자",               // 필수 — 개체 이름
  "identity_core": "1girl, ...",     // 필수 — 캐릭 핵심 태그
  "scene_layer": "rain, ...",        // 필수 — 장면 태그
  "kind": "character",              // 선택 — character | scene
  "category": "sfw",                // 선택 — sfw(기본) | nsfw
  "scene_basis": "3화 우산 장면 근거", // 선택 — 근거 문구(장부 정합성 핵심)
  "quality": "balanced"             // 선택 — 스튜디오 프리셋 key
}
```

응답: 생성된 이미지 레코드 전체(JSON). `image_id`, `render.*`(프롬프트·시드·negative), `provenance.*`(bot·ticket·review_status=candidate) 포함.

에러 계약:
- `400` 필수 필드 누락 / `works에 없는 작품` / 차단 태그(BLOCKED_TAGS — 코드 하드코드, 우회 금지)
- `403` `category=nsfw`인데 NSFW 토글 OFF (RELAY-41 게이트 — 먼저 `POST /api/nsfw/toggle`)

## 3. 리롤·조회 보조 — 기존 기능 (삭제 금지)

- `POST /api/reroll` `{image_id}` — core·scene 고정, 시드만 파생(+1).
- `GET /image/<image_id>` — 해당 이미지 생성 JSON 전체(프롬프트·시드·negative·provenance). 외부 파이프라인이 근거를 검증할 때 이 경로가 정본.
- `POST /api/delete` `{image_id}` — 로컬·구글드라이브 제거 + 카탈로그 tombstone.

## 4. 게이트·보안 (공통)

1. 모든 외부 생성물 `review_status=candidate` — 자동 reviewed 부여 금지(이사님 전용).
2. `category=nsfw`는 토글 ON 상태에서만 생성(기본 OFF).
3. `BLOCKED_TAGS`는 코드 하드코드 — 목록 축소 시 POL-4 변경 승인 필요.
4. 원본 byte·쿠키·토큰 금지 — 프롬프트 태그와 근거 문구만 전달.

## 5. 변경 절차

이 계약의 파라미터 추가·변경은 ① scenario repo 코드 반영 → ② 이 문서 갱신 → ③ 장부
`site-reconciliation-ledger-2026-08-26.md`의 novel_col 상태 표시 갱신 순서로. 파라미터 제거는
기존 기능 삭제에 해당하므로 이사님 승인 필요.
