---
title: 소설 자산화 재개 설정 — firewin zcode (이사님 09-07 토큰 지시)
date: 2026-09-07
status: 정합성 확인 완료 + 45분 루프 설정
tags:
  - novel
  - asset
  - firewin
---

# 소설 자산화 재개 설정 (2026-09-07)

이사님 지시: 주간 토큰 만료일(리셋 23:28)까지 남은 토큰을 기존 자산담당의 소설 파싱·자산화로
지속 소비. 기존 파이프라인을 찾아 정합성을 맞추고 루프로 진행.

## 정합성 확인 결과 (기존 자산담당 = asset_agent/novel_col 계승)

- **정본**: scenario repo `novel_assets/` — HANDOVER.md · 자산화-운용대책.md(7항 체크리스트) ·
  collection-protocol.md · 자산화-진행체크포인트.md
- **산출 형식**: `works/<제목>/` 7항(overview · capsules · craft_notes · components.ndjson(matrix-component-v1,
  sha256:pending 0) · situation_chains/<제목>.md · reading-map.md · 전수심독/)
- **push 대상**: GitHub `markjang29/scenario` — 작품당 커밋(`novel(<작품>): … 7항 완결`) + push.
  09-06 현재 origin/main 최신 커밋까지 novel_col이 같은 규약으로 운행 중(RELAY-51 수집 W4).
- **원문 소스**: AWS `~/Works/novel/epub 파일/` 1,537종(manifest 08-19) + 추출 노트
  `~/matrix_asset_agent/.runtime/novel/<slug>/`
- **원칙**: 1작품 완결 우산 확장 금지 / placeholder 금지(실제 SHA) / 원문 byte·쿠키 Git 금지 /
  pending_human_review 자동 부여 금지 / 전체 번역·판매 산출 금지

## 이번 루프 타깃 (체크포인트 08-18 재개 대상 + 이후)

1. 반 고흐(vangogh) — 459화 추출 + ep_notes 보유, works 미등재 → 7항 신규 자산화
2. 동로마(byzantium) — 307화 추출 + batch 노트 1~160화 → 7항 신규 자산화
3. 갑질하기(gapjil100) — 311화 추출, `works/100조로_갑질하기` 와 동일작 여부 확인 후 미완 항목 보완
4. 이후 대형 후보: 망나니 PD 487화 · 지구식 구원자 368화 · 이것이 법이다 4743화판 (epub)

## 운용 규칙 (자동 루프 45분)

- 작업 장소: AWS scenario clone(원문·노트 인접). firewin에서 ssh 경유.
- 타 봇 WIP(untracked·modified) 절대 add 금지 — 자기 산출 경로만 `git add`.
- push 전 `git pull --rebase`, 충돌 시 해당 작품 파일만 해소.
- 매 세션: 체크포인트에 날짜 섹션 append + 결과 보고(작품·파일·커밋·push 여부).
- 23:40 KST 이후 세션은 작업 중단하고 마무리 보고만. 이사님 "그만" 시 루프 삭제.

## 사이트 정합성

- components.ndjson(matrix-component-v1) 규약 유지 = matrix_zcode novel-pipeline-spec·
  s0_worker 입고 규약과 동일 포맷 → 향후 8018 캡슐/자산 등록(매트릭스화 단계)과 호환.
- 시나리오 repo 산출은 publication 계층(work-queue 운영 경계) — 원본 lifecycle은 asset_agent.
