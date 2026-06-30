---
title: ADR — 529(overloaded) 예방: 유령 세션 자동 정리(reaper) + 동시 1M 캡
date: 2026-06-30
status: accepted (이사님 "다 알아서 해줘" 전권위임 + "529 더는 안 본다")
project: 공통(서버 운영)
source: 이사님 제안 "특정 시간 지나면 로그화→세션 kill→재연결 시 로그 읽기" → 냉정 분석 후 수정 채택
related:
  - decisions/2026-06-26-quota-checkpoint-resume.md
  - principles/context-budget.md
tags:
  - adr
  - ops
  - 529
  - session
  - glm-5.2
---

# ADR — 529 예방: 유령 세션 reaper + 동시 1M 캡

## 상태
`accepted` — 2026-06-30 이사님 전권위임으로 즉시 시행. 스크립트/크론 배포 완료.

## 배경 — 529의 진짜 원인 (CPU/메모리 아님)
- `uptime` load 0.02, 메모리 2.0G/7.6G → 서버 자원 여유. 529는 **LM API 서버 과부하**.
- 원인 = **1M 컨텍스트 모델(`glm-5.2[1m]`) 동시 호출**. 한 요청당 서버 부하가 커 과부하 임계 도달.
- 결정적 사례: `akl0hdys` workspace 세션 `a4db5139`(== [[context-explosion-causes]] originSessionId)가 **4일간 PPID=1 고아**로 살아 1M 컨텍스트 보유. 매 LM 호출마다 1M 요청 → 529 유발. → 2026-06-30 kill로 즉시 제거.

## 이사님 제안과 수정 — "재연결 시 로그 읽기"는 채택 안 함 ⚠️
이사님 원안: "시간 경과 → 로그화 → kill → 재연결 시 로그 읽어 복원". 직관(동시성↓ + 영속화 + 복원)은 맞으나 **한 축이 역효과**:
- **"재연결 시 로그 읽기" = 전체 트랜스크립트를 새 세션 컨텍스트에 재적재** = 곧 1M 폭발 = 529 자초. → **이 부분만 버림.**
- 대신 복원은 **체크포인트 요약**(목표·완료분·다음스텝·파일경로)만 — 이미 `quota-checkpoint` ADR + `recovery-gate` SessionStart 훅으로 구축됨. 세션 kill해도 디스크 jsonl + akl0hdys 메모리 + work-queue.md로 복구 가능(`/clear` 복구맵 검증 완료).

## 결정
1. **유령(고아) 세션 자동 정리** — `scripts/claude-session-reaper.sh`:
   - 정책(보수): `PPID=1`(고아) + 60분 이상 경과 Claude Code 세션만 kill.
   - 활성 세션(터미널·cokacdir·daemon이 부모)은 PPID≠1 → 절대 안 잡힘 → 작업 중 세션 손상 없음.
   - kill 전 jsonl 경로를 `notes/.reviews/session-reaper.log`에 영속(복구 닻).
   - 기본 DRY-RUN, `REAPER_DRY_RUN=0`이 실제 kill.
2. **crontab 매 30분** 자동 실행(실제 kill 모드) → 새 유령 자동 회수. 동시 1M 세션 수를 0~1로 통제.
3. **수동 즉시 조치**(2026-06-30): 45922(4일 된 1M 유령) SIGTERM 종료.

## 1M 강제해제는 하지 않음 (불가·불필요)
- Z.AI 코딩플랜이 Claude Code 엔드포인트의 `glm-5.2`를 **자동으로 1M으로 승격** (Z.AI 블로그: "GLM-5.2[1m] to enable 1M context length in Claude Code"). settings.json엔 `[1m]` 스위치 없음 → 계정/플랜 단위.
- 끄면 Codex rescue/장기 세션 품질 저하 위험.
- **대안 정답:** 1M을 끄지 않고 **동시 1M 세션 수를 캡**(reaper가 0~1 유지) → 동일 효과, 부작용 없음.

## 검증 기준
- 다음 529 발생 빈도가 현저히 감소하는지 (이사님 체감).
- reaper 로그에 kill 기록이 쌓이는지; 활성 작업 세션이 잘못 kill 안 당하는지 (PPID 가드).

## 참고 (출처)
- [Z.AI — How to Switch Models](https://docs.z.ai/devpack/latest-model) — `[1m]` 접미사로 1M 활성화
- [Z.AI GLM-5.2 블로그](https://z.ai/blog/glm-5.2) — Claude Code 1M 컨텍스트 안내
