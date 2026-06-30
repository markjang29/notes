# 복구 게이트 번들 축소 — 2026-06-30

## 문제
- COKACDIR recovery gate(`~/.claude/hooks/cokacdir-recovery-gate.sh`)가 매니저 봇 세션 차단.
- 원인: 복구 번들(MEMORY.md + current-work-state.md + work-queue.md) = **10503B > 9000B** 제한.
- SessionStart 가 `additionalContext` preview 대체 위험으로 주입 포기 → `.fail` → UserPromptSubmit 차단.

## 원인 비중
- MEMORY.md 1373B / current-work-state.md 1736B / **work-queue.md 7394B(70%)** ← 주범.

## 오진 기록 (정직 보존)
- 중간 진단: "userprompt 모드 CWD 가드 누락 버그" → 스크립트에 가드 추가(변경1).
- **Codex 리뷰 + 시뮬 검증 = 오진 판명.** 34-37줄 전역 가드가 이미 userprompt에도 적용됨(원본으로 Works cwd → exit0 확인). 변경1은 중복.
- 이사님 결정: "변경1 빼고 work-queue만 반영" → 변경1 원복.

## 해결
- **work-queue.md 축소:** 7394B → 4384B. 번들 10503→**7493B**(9000 이하, 1507B 여유).
  - 과거 상세(세션 노트·아이디에이션 v1 상세·백테스트 상세 숫자) → 파일 경로로 대체.
  - 핵심 의사결정/ADR 대기/다음 스텝/야간운영 승인경계는 보존.
- **스크립트:** 원복(변경1 철회). 백업 해시 `ecacf372…`와 동일.

## 검증
- `bash -n` OK.
- 시뮬(원복본): Works→exit0 / 매니저(`.cokacdir/workspace/*`)→block 정상.
- Codex 리뷰: work-queue 축소 **OK** 판정(핵심 복구 정보 손실 없음).

## 효과
- 매니저 봇 다음 SessionStart 시 복구 번들 정상 주입 → `.ok` 생성 → 게이트 자동 해제.
- 컨텍스트 절약: 매 세션 약 3KB(10503→7493).

## 백업
- `~/.claude/recovery-gate/backup-20260630-045043/{cokacdir-recovery-gate.sh.orig, work-queue.md.orig}` (sha256 기록 보존).
