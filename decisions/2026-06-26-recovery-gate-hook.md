---
title: ADR — /clear 후 복구 강제 게이트 (Claude Code hooks)
date: 2026-06-26
tags:
  - adr
  - hooks
  - recovery
  - manager-bot
---

# ADR — /clear 후 복구 강제 게이트

## 상태
accepted (사용자 승인 후 적용, 재발 검증 대기)

## 날짜
2026-06-26

## 프로젝트 / 적용 범위
공통 인프라 — cokacdir/Telegram 매니저 봇(`@heav_lnx_bot`). 팀장 봇(rpg/trader)은 제외.

## 결정
`~/.claude/settings.json`에 Claude Code hooks 2종을 설치해, 매니저 봇이 새 세션(/clear·resume·startup·compact) 진입 시 **자동으로** akl0hdys 복구 메모리(`MEMORY.md` + `current-work-state.md` + `~/notes/work-queue.md`)를 주입받고, 주입 전엔 첫 사용자 프롬프트를 차단(fail-closed)한다.

- `SessionStart`(matchers: startup/clear/resume/compact) → 복구 번들 주입(`additionalContext`) + `.ok` 마커 생성.
- `UserPromptSubmit` → `.ok` 부재 시 `{decision:"block", suppressOriginalPrompt:true}`.
- 스크립트: `~/.claude/hooks/cokacdir-recovery-gate.sh`.

## 맥락
/clear 후 새 세션이 복구入口(akl0hdys memory)를 **읽지 않고** 제로 상태로 첫 응답을 만드는 재발 발생. 글로벌 CLAUDE.md가 akl0hdys를 가리키더라도 (1) 복구 경로는 자동 주입되지 않고, (2) 새 세션 시스템 프롬프트의 메모리 경로는 세션 고유 workspace(ltgqjhx1)라 akl0hdys와 불일치 → 읽기가 모델 자율 판단에 의존해 강제가 없었음. 사칙("읽기 전 결정/발판 금지") 위반.

## 제약
- **3봇 설정 공유**: cokacdir 서버 1프로세스가 토큰 3개로 매니저+rpg+trader를 같은 `ubuntu` 계정·같은 `~/.claude/settings.json`로 서빙 → 글로벌 훅은 3봇 모두 발화.
- cokacdir는 `claude -p --resume <session_id>` 로 구동 → SessionStart가 `resume`/`clear` 소스로 발화.

## 선택한 이유 / 버린 대안
- **선택:** SessionStart 강제주입 + UserPromptSubmit fail-closed 이중 게이트(Codex 설계, 공식 hooks 문서로 필드명 검증).
  - 버린 대안 A — "세션 메모리 최상단 고정 포인터" → 모델 자율 의존, 강제 없음(근본 원인과 동일).
  - 버린 대안 B — 3봇 공유 그대로 전체 적용 → 팀장 봇에 매니저 복구 메모리가 주입되는 의도왜곡. → **cwd 스코프 가드**로 해결(아래 트레이드오프).

## 트레이드오프
- **얻은 것:** 복구 주입의 기계적 보장(모델 자율 제거). 복구 없이 응답 불가.
- **잃은 것/리스크:**
  - fail-closed = 브리킹 리스크(SessionStart가 안 끝나면 모든 프롬프트 차단). → 탈출구 2종: `~/.claude/recovery-gate/DISABLE` 파일, 또는 settings.json `disableAllHooks:true`.
  - resume마다 ~9KB 재주입 → 컨텍스트 예산 약간 증가(수용 범위).
  - cwd 스코프 가드(`*/.cokacdir/workspace/*` = 매니저만 적용) — 매니저가 프로젝트 repo로 /start하면 우회됨. 현재 매니저는 항상 workspace 기동이라 유효.

## 검증 기준
- [x] 공식 hooks 문서로 필드명·matcher 검증 (Claude Code v2.1.195).
- [x] 스크립트 단위 4케이스: 주입/통과/fail-closed 차단/DISABLE 우회.
- [x] 스코프 4케이스: 매니저 cwd→주입+.ok / 팀장 cwd→no-op(주입·차단 없음).
- [x] settings.json JSON valid, 기존 Stop/env/plugins 보존.
- [ ] **실제 /clear 후 첫 응답이 akl0hdys 3경로 명시** (사용자 검증 대기).

## 실패 / 복구 과정
- Codex 1차안이 복구 파일 경로를 틀림(`/home/ubuntu/.cokacdir/workspace/akl0hdys/`에 파일 없음) → 그대로 적용 시 fail-closed 전면 발동 브리킹. 실제 경로(`~/.claude/projects/.../akl0hdys/memory/`)로 수정.
- 현재 세션(5cc24223)은 훅 설치 전에 시작돼 .ok 없음 → 다음 프롬프트 차단될 뻔 → `.ok` 사전 생성으로 회피.

## 후속 재검토 조건
- cokacdir가 claude 구동 방식 변경(예: --resume 폐지) → SessionStart 발화 재확인.
- 매니저가 프로젝트 repo를 직접 /start하게 되면 스코프 가드 우회 → 패턴 재조정.
- 팀장 봇도 자체 복구게이트 필요시 동일 패턴(각 repo cwd용) 적용.
- Claude Code 버전업으로 hooks JSON 필드명 변경 시 재검증.

## 관련 링크
- 구현: `~/.claude/hooks/cokacdir-recovery-gate.sh`, `~/.claude/settings.json`
- 복구 메모리: `~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory/` ([[clear-recovery-map]] · [[current-work-state]])
- 선행: `decisions/2026-06-26-org-telegram-group.md`
- 근거: https://code.claude.com/docs/en/hooks
