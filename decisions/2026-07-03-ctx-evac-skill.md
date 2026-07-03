# ADR — ctx-evac 스킬: 1M 컨텍스트 방전 자동화 — 2026-07-03

## 배경
- 2026-07-03 매니저 세션(`20bkmfvt/6c9938c5`, glm-5.2[1m])이 "context window limit" 에러로 사망.
- 진단(정량): ① work-queue.md·memory bootstrap 통째 재주입 반복 ② `cron --session` resume로 같은 세션 누적 ③ WebSearch dump(27KB) ④ 동일 ops 작업 4~6세션 반복.
- 기존 폴백(`recovery_middleware.py`, `emergency-write.sh`)은 **전부 529/429(레이트리밋)용**. 1M(컨텍스트한계) 도달 감지·방전 자동화 없었음.
- `settings.json` hooks = SessionStart/UserPromptSubmit/Stop. **PreCompact 비어있었음** → 자동 압축 시 백업이 안 끼어듦.

## 결정
신규 스킬 **ctx-evac** + **PreCompact 훅**으로 1M 도달 사전 방전 자동화.

### 산출물
- `~/scripts/ctx-evac.sh` — 방전 오케스트레이터 (precompact/manual/watch)
- `~/.claude/skills/ctx-evac/SKILL.md` — 스킬 정의
- `settings.json` → `PreCompact` 훅 추가

### 정책 (3단계)
- `< 85%`: 정상. watch/precompact는 백업 생략(과다 방지).
- `85~95%`: **Phase1** — checkpoint 백업(요약).
- `≥ 95%`: **Phase2** — 필수 백업 + `emergency-write` + `/clear` 권고.

### 재사용 (중복 구현 회피)
- 측정: `context-meter.sh` (transcript usage 실측)
- 백업: `emergency-write.sh` atomic 패턴 + checkpoint 자동 수집(work-queue 헤더·3레포 git status·세션포인터)

## 모델 교체 안 된 이유 (별건)
- glm-5.2[1m]이 이미 1M 최상위 → 더 큰 컨텍스트 모델 라인업 없음.
- `cron --session <SID>`가 매니저 야간/아침/리포트 cron을 같은 세션으로 resume → 리셋 안 됨.
- 해결은 "모델 교체"가 아니라 **세션 리셋(/clear 또는 신규 세션)**. ctx-evac이 그 타이밍을 잡고 백업 후 안내.

## 한계 / TODO
- 사후(context window limit 에러 후) 대응은 늦음. 사전 85/95% 방전이 핵심.
- `recovery_middleware.py`에 1M 분기(사후 emergency) 추가 — 별도 TODO. 라우팅 경로 영향 주의.
- 근본 예방(work-queue/memory 통째 주입 억제, WebSearch dump 발췌)은 `2026-06-30-recovery-gate-bundle-shrink.md` 연계 과제.

## 검증
- `bash -n ctx-evac.sh` 통과
- `ctx-evac.sh manual` dry-run (정상 범위 분기)
- PreCompact 훅 JSON 문법 (settings.json `python -m json.tool`)
- 기존 SessionStart/UserPromptSubmit/Stop 훅과 충돌 없음

## 백업
- 기존 `settings.json` → `settings.json.bak-20260703-ctx-evac`
