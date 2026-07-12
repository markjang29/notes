---
title: Scenario repo freeze (리뉴얼 전까지 수정 금지)
date: 2026-07-12
status: decided
decided_by: 이사님(markjang29, 대표이사)
tags: [scenario, freeze, renewal, cron]
---

# Scenario repo freeze — 2026-07-12

## 결정 (이사님 직접, 07-12 KST)

이사님 원안: "시나리오 git 갈아엎는다 리뉴얼 되기 전까지 수정금지, 리뉴얼 된 룰 따를것"

- scenario repo **리뉴얼(갈아엎기)** 확정.
- 리뉴얼 완료·룰 통보 전까지 **일체 수정 금지(freeze)**.
- 리뉴얼 룰 통보 시 새 룰 적용.
- 경위: scenario 팀장이 매니저 야간 배정(부가설명 작업 등 repo 파일 수정)을 본 이사님 직접 지시와의 충돌로 보류 보고 → 이사님 사실확인.

## 매니저 방침

- **scenario 야간 배정 사이클 전면 중단** (리뉴얼 룰 통보 전까지).
- RPG·autotrader는 영향 없음 — 정상 진행.
- scenario 봇·매니저의 scenario repo git/file 조작 금지. 리뉴얼 작업은 이사님(노트북 Codex) 주도.
- 미커밋 잔류(`drafts/d1`, `drafts/d2`, `OVERNIGHT_2026-07-12.md`): 보존, 조치 없음 (갈아엎기 예정).
- 재개 조건: 이사님 리뉴얼 룰 통보.

## 크론 조치

| ID | schedule | 내용 | 조치 |
|---|---|---|---|
| `0FC5A6F0` | (야간) | 시나리오 야간 | 팀장 제거 완료 (07-12) |
| `C9804825` | `0 8 * * *` | 시나리오팀 자율 창작 리포트 | 매니저 제거 → 리뉴얼 후 재등록 |
| `2D8F5150` | `0 1 * * *` | 3팀 공통 야간 배정 | 유지 — work-queue 본 결정 읽고 scenario 제외 |

### C9804825 재등록용 백업

- provider: `claude`
- schedule: `0 8 * * *`
- prompt: 시나리오팀 자율 창작 리포트. 사칙(scenario-team-purpose v1) 준수: RISU 자산 기반 창작·창작 자유·이사님 컨펌 후 디벨롭·창작 도구 자체 디벨롭. ★매니저가 시드 전달 안 함(사칙 위반 정정). 시나리오팀이 자율로 RISU 자산(catalog/examples/templates) 활용 창작·도구 디벨롭 결과 보고. 모든 산출에 PROVENANCE 블록 의무. 컨펌 안건 명시.
