# RELAY-39 구현 기록 — 스튜디오 v3 (올랜덤·자동완성·크로스오버·NSFW 명세)

> 2026-08-23 · novel_col · 이사님 요청 4건 중 3건 구현 + 1건 명세

## 구현 내용

### 1) 🎲 올랜덤 생성 — "캐릭만 선택 후 올랜덤"
- 캐릭터 풀 → 자산 선택 → **🎲 올랜덤 생성 버튼**: 캐릭(자산·core)만 유지, 장면(템플릿 랜덤)·품질(3종 랜덤) 전부 자동 새 뽑기.
- 씬리롤(같은 캐릭 다른 장면) 시트에도 **🎲 올랜덤** 버튼 추가 — core 고정 원칙 유지.
- `autoFill(true)` — core는 사용자 입력 존중(비었을 때만 자동 제안/프리셋), scene·quality는 강제 새 랜덤.

### 2) 간단 모드 — "간단하게만 선택하고 생성했을 때 나머지 자동"
- `go()` 시작 시 `autoFill(false)`: 비어있는 항목만 자동 채움 + "🤖 자동 채움: scene · quality" 토스트로 무엇을 채웠는지 표시.
- core 비었으면 → 자동 제안(있다면) or 기존 프리셋 랜덤. 장면 비었으면 → 템플릿 랜덤. scene_basis 비었으면 → "랜덤 조합 — 템플릿: X" 근거 자동 기입.
- 검증 완화: work·개체명만 필수(풀/카탈로그에서 선택하면 자동 설정).

### 3) 크로스오버 — "작품 연계 서사 상황 + 다른 소설 것 불러오기"
- 💡 서사 상황 칩: **선택 작품의 아이디어를 ★ 표시와 함께 섹션 첫머리로 우선 정렬**, 나머지는 작품명 라벨로 표시(다른 소설 구분).
- 씬 프리셋 칩(타 캐릭 장면 재사용)에 **출처 작품 배지** 표시 — 현재 작품과 다를 때만.

### 4) NSFW — 요구사항 명세만 작성 (구현 없음, 이사님 지시 옵션)
- `NSFW-요구사항-명세.md` — FR 8건·POL 4건·스키마 v1.1·구현 규모·열린 질문 3건. 승인 시 RELAY-40로 분리 구현.

### 5) 아카라이브 참고자료 — 서버 내 크롤링본 채굴 (이사님 지적)
- **이미 크롤링되어 있었음** (`scenario/.extract/`): 🔦라이트보드 NAI 모듈 2.1.1~2.9(9종) + [라이트보드] NAI/ComfyUI 매뉴얼 PDF(아카 characterai 채널, 조회 1만). WebFetch 403만 보고 놓친 것을 이사님이 지적 → 크롤링본 기반으로 전환.
- **채굴→반영 (v3.1)**:
  - `[Quality]` 부스트 → QUALITY 프리셋에 `boost` 필드 (best quality, amazing quality, very aesthetic, masterpiece, detailed shading) — 조립 규칙 **v1.1**: `boost + core + scene_layer`, manifest `render.quality_boost` 기록, README·build_web.py 동시 갱신.
  - `[Negative]` 가중치 목록 → DEFAULT_NEG 강화 (worst quality, bad quality, unfinished, unclear fingertips, multiple views, monochrome, greyscale, sketch, flat color, 3d, realistic, nsfw).
  - `[Angle]` 3분할 → 씬 템플릿 12종에 앵글 태그 보강 (from below/cowboy shot/wide shot 등) + 태그 사전에 '앵글·프레이밍' 카테고리.
  - NAI 액션 태그 `mutual#`/`source#`/`target#` → 태그 사전 '상호작용' 카테고리.
  - 태그 작성 규칙(Frozen Moment·Danbooru 표준·이름 금지·구체>포괄) → README 3-1절로 표준화.
- **보류**: `artist:` 화풍 태그 10종 프리셋([Author] 블록)은 NAI v4 전용 — 우리 v3 파이프라인에 비적용. 원본은 `.extract/modules/🔦라이트보드 NAI 2.9.json` lorebook 프리셋1~10에 보존.
- 아티스트 프리셋 카탈로그: 같은 폴더 `아티스트-프리셋-카탈로그.md` 참조.

## 검증 (기능실행검수 — RELAY-37)

- `check.sh` 4/4 통과 (JS 문법·API·페이지·실렌더).
- `render_test.js` v3 확장: autoFill(빈 항목)·autoFill(true)(core 유지+장면·품질 변경)·올랜덤 버튼 2곳·★ 정렬 — 전 항목 pass, pageError 0.
- ★ 우선정렬: ts-swordsman 아이디어 6건 → ★ 6개 섹션 첫머리 배치 확인.
- **실생성 증거**: img_20260823_002 — RISU 요셀라, 자동 core 제안 + 랜덤 템플릿(영웅 등장) + 랜덤 품질(vivid), seed 1001, 구글드라이브 업로드 완료. 이미지 Telegram 전송.

## 변경 파일

- `novel_assets/images/app/static/index.html` — autoFill/randomGo/sceneBlock(work)·버튼 2·go() 자동채움
- `novel_assets/images/app/render_test.js` — v3 흐름 3종 추가 (백엔드 main.py 변경 없음 — 프론트 완결)
