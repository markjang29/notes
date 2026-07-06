# 문서 대청소 L0 적용 — 2026-07-06

## 배경

봇들이 사칙/온보딩/워크큐/체크포인트를 과하게 읽으면서 집중도가 떨어지고, 정체 확인·역할 경계·컨텍스트 관리가 흔들리는 문제가 반복됨.

## 조치

### 1. L0 도입

새 파일:

- `L0-agent-boot.md`

역할:

- 첫 응답 전 최소 정체·역할·보존·컨텍스트 원칙 확인
- 1~2KB 수준의 초단문 부트 문서

### 2. 온보딩 압축

- `onboarding.md`: 약 10.6KB → 약 2.6KB
- 긴 원문은 Git 이력에서 복구 가능

### 3. work-queue 압축

- `work-queue.md`: 약 10.1KB → 약 2.5KB
- 현재 활성 작업·대기 결정·다음 스텝만 남김
- 과거 상세는 Git 이력, `work-archive.md`, checkpoints 참조

### 4. recovery gate L0 전환

운영 파일:

- `/home/ubuntu/.claude/hooks/cokacdir-recovery-gate.sh`

변경:

- 기존 L1 주입: `MEMORY.md + current-work-state.md`
- 변경 L1 주입: `L0-agent-boot.md + current-work-state.md`
- `MEMORY.md`와 `work-queue.md`는 필요 시 온디맨드 Read

검증:

- 샘플 SessionStart 입력 시 `L0-agent-boot.md`가 정상 주입됨

## 기대 효과

- 첫 턴 집중도 개선
- "아래 두 파일이 무엇인지 모르겠다" 같은 핑계 감소
- 긴 문서 재독으로 인한 context 폭발 감소
- 팀장/매니저 역할 경계 확인 빨라짐

## 남은 일

- recovery-gate `DISABLE` 제거 여부 결정
- `.reviews/session-reaper.log` 커밋/무시 정책 결정
- 팀장들이 새 L0/onboarding 기준으로 재인증하는지 확인

