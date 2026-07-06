---
date: 2026-07-06
to: heav_lnx_scenario_bot (시나리오 팀장)
from: Windows 에셋 공급 (heave)
type: handoff-report
tags: [scenario, 에셋파이프라인, catalog]
---

# 시나리오 에셋 파이프라인 정비 보고 — 2026-07-06

> **팀장(@heav_lnx_scenario_bot) → 이사님께 보고 지시**: 아래 "이사님 보고용 요약"을 이사님께 전달. 핵심은 **catalog 소비 방식은 그대로, source_path만 사라졌다**는 것.

## 이사님 보고용 요약 (3줄)

- 오늘 Windows에서 scenario repo 에셋 **전수 발췌 602건 완료** + **repo 절대경로(사용자명·D:\LLM) 전면 제거**.
- 매니저 소비 방식은 **변경 없음** — `name`+`kind`+`subtype`으로 식별. `catalog/index.json` 그대로 소비.
- 바뀐 것은 **경로 익명화뿐** (공개 repo에서 PC 경로 노출 제거). 발췌 내용·메타 구조는 동일.

## 변경 상세 (팀장 확인용)

### 1. catalog 경로 익명화 (주요)
- `catalog/` 메타에서 `source_path` / `src` 컬럼 **전부 제거** (index.json 602건 + characters/modules/prompts/pdfs/assets.csv).
- 원본 추적은 **로컬 `.extract/_source` (gitignore)** 로만 유지.
- **매니저 소비 영향**: `source_path` 의존 코드가 있으면 제거 필요. 식별은 `name`+`kind` 조합(중복 시 `subtype`/`metric` 참고).

### 2. 발췌 스크립트 환경변수화
- 발췌 스크립트(`tools/extract_*.py`, `rpack_decode.js`)가 PC 절대경로 하드코딩을 제거하고
  - repo 경로 → 스크립트 위치 기반(`os.path.dirname`)
  - 에셋 루트 → `LLM_ROOT` 환경변수, wasm → `RISU_WASM_PATH`
- **서버(소비층)는 발췌 안 하므로 영향 없음**. Windows 재발췌 시에만 env 설정.

### 3. 전수 발췌 완료 (602)
- character 53 / module 343 / prompt 205 / persona 1
- **prompt 205 완수**: `💻창작용 프롬 4.0.risupreset` 역변환 (표준 `preset` 키 대신 `pres` 축약형 사용 → 스크립트 지원 추가).
- **persona 발췌 추가** (`extract_persona.py` 신규): PNG `chara` 청크 보유 1건.
- 발췌본 총 602개(50MB)는 `.extract/` (gitignore) — 본문은 repo 미반영.

## 커밋 (markjang29/scenario, main)
- `5a93be7` 발췌 버그 수정 — character 덮어쓰기·prompt JSON 손상 복구, persona 발췌 추가
- `c6f272c` `pres` 키 역변환 지원 — prompt 205 완수
- `e6baf17` catalog/repo 절대경로 익명화 (32파일)

## 팀장 액션
1. `catalog/index.json` 소비 코드에 `source_path` 참조 있으면 제거.
2. 위 "이사님 보고용 요약" 이사님께 전달.
3. (선택) 발췌 스크립트 재실행은 Windows에서만 — `LLM_ROOT`/`RISU_WASM_PATH` 설정.

## 경계 (유지)
- 미성년 성적 마커(module 3건)는 발췌·카탈로그에서 제외 — 법적.
- 프리셋 타인 API키/URL은 발췌 단계에서 자동 제거 (검증 0건 누출).
- 발췌 본문은 저작권 콘텐츠 — repo 미반영, 분석/열람 지양.
