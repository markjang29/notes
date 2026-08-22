# NSFW 카테고리 · 토글 — 요구사항 명세 (RELAY-39)

> 2026-08-23 · novel_col · 이사님 지시 원문: "NSFW 관련 토글 켜서 따로 뽑을수 있는 카테고리 만들어주고 NSFW는 니가 구현 못하면 요구사항 명세만 작성해"
> **본 문서는 명세만 작성한 것 — 구현은 승인 후 별도 티켓(RELAY-40)에서.**

## 1. 배경 · 목표

- 수집 자산(works 완결 체크리스트·RISU 카탈로그) 중 성인向け 로어북/소설이 다수. 현재 스튜디오(v3)는 SFW 전용(`DEFAULT_NEG` 고정)이라 이들 자산의 원격표현이 불가.
- 목표: 성인용 이미지를 **별도 카테고리·별도 저장소·별도 승인 절차**로 분리 생성 — SFW 파이프라인과 물리 분리.

## 2. 기능 요구사항 (FR) — 2026-08-23 이사님 수정: 나이인증·접근통제 제거, 토글만

- **FR-1 NSFW 토글**: `app/nsfw_config.json`(`enabled: false` 기본) + UI 토글. `false`면 NSFW 탭·프리셋·API 전부 비활성(403). **연령 인증·IP 화이트리스트·PIN 없음.**
- **FR-2 카테고리 필드**: 생성 요청에 `category: "sfw"|"nsfw"` (manifest 스키마 v1→v1.1, 후방호환 기본 sfw).
- **FR-3 프리셋 물리 분리**: NSFW 태그 사전·negative 프리셋은 별도 파일 `app/nsfw_presets.json` — SFW 사전 코드와 같은 파일에 두지 않는다.
- **FR-4 저장소 분리**: 로컬 `/home/ubuntu/nai_out/studio_nsfw/`, 구글드라이브 `소설자산이미지/NSFW/<배치>/`. SFW 폴더에 한 파일도 섞이지 않게 업로드 경로를 생성 시점에 분기.
- **FR-5 카탈로그 분리**: 스튜디오 카탈로그는 NSFW 토글 ON일 때만 별도 섹션("🔒 NSFW") 표시. 정적 카탈로그(`web_catalog.html`)에는 미포함.
- **FR-6 파라미터 프리셋**: NAI `negative_prompt`에서 성인 차단 태그를 제거하는 별도 NSFW negative 프리셋 + **이미지 카테고리 태그 사전 7종(works/catalog 자산 기반 — 인수인계서 §4.2 표 참조: 의상·코스튬/장소·상황/포즈·구도/액세서리·도구/신체·체형/분위기·조명/관계·상호작용)** — 전부 `nsfw_presets.json`에서 관리, 코드 하드코딩 금지.
- **FR-7 감사 로그**: NSFW 생성은 manifest `provenance`에 `"category":"nsfw"` 명시 + 생성 로그 별도 파일(`nsfw_generation.log`).

## 3. 정책 요구사항 (POL)

- **POL-1 승인**: NSFW 이미지 `review_status`는 candidate → reviewed 부여가 이사님 직접만(기존 자산 규칙 승계). 봇 자동 reviewed 금지.
- **POL-2 저작권**: 수집 원문 quote는 근거용 짧게만 — 기존 규칙 동일 적용.
- **POL-3 NAI 약관**: Opus 플랜의 성인 생성 허용 범위를 구현 직전 재확인(2026-08 검토 시점 기준 허용이나 약관 개정 가능).
- **POL-4 하드 차단**: 미성년 묘사·실존 인물 묘사는 태그 사전 차단(하드코드) — 프리셋 파일로 우회 불가하게 서버 검증.

## 4. 데이터 스키마 변경 (v1 → v1.1)

```json
"subject":   { ..., "category": "nsfw" },
"provenance": { ..., "policy_gate": "nsfw_approved_v1" }
```

## 5. 구현 예상 규모 (승인 시 RELAY-40)

- `main.py`: NSFW 브랜치(설정 로드·프리셋 로드·경로 분기·게이트 검증) ≈ 80줄
- `index.html`: 토글 + 🔒 NSFW 카테고리 섹션 ≈ 60줄
- 검사: `check.sh`에 ①게이트 OFF 기본 동작 ②OFF 상태 NSFW API 403 케이스 추가 (render_test.js 연동)
- 테스트 생성물은 로컬만(드라이브 업로드는 게이트 ON 확인 후)

## 6. 열린 질문 (이사님 결정 필요)

- **Q-1 태그 사전 소스**: 아카라이브 19금 태그 위키 참조 vs 자체 큐레이션 (정확성·저작권)
- **Q-2 드라이브 폴더 깊이**: `NSFW/<날짜배치>/`까지 갈지, `NSFW/` 평면 + manifest로 관리할지
- **Q-3 1차 대상**: RISU 성인 로어북 중 우선 노출할 캐릭터 우선순위
