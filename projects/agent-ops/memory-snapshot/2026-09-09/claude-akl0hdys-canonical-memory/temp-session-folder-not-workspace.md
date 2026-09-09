---
name: temp-session-folder-not-workspace
description: cokacdir 임시 세션 폴더(랜덤 id)를 진짜 작업 workspace로 헷갈리지 말 것 — 이사님 2026-07-02 반복 지적
metadata:
  type: feedback
---

이사님 2026-07-02 피드백: "eissgtmj 는 cokacdir 이 만드는 임시 세션 폴더야. 너 이거 자주 헷갈리더라?"

`~/.cokacdir/workspace/<랜덤8자>` (예: `eissgtmj`, `akl0hdys`, `ltgqjhx1`, `qrhpxeah` …) 폴더는 cokacdir이 세션마다 파는 **임시 세션 폴더**이지 작업 디렉토리가 아니다. 복구 게이트의 `Session cwd(무시)` 표시를 문자 그대로 따를 것. 진짜 산출물·코드는 프로젝트 repo(`~/projects/rpg_game` · `~/projects/autotrader` · `~/projects/scenario`)에 둔다.

**Why:** 임시 폴더는 보통 비어 있고, 세션 단위라 맥락·파일이 영속하지 않는다. 여기를 "내 workspace"로 삼고 파일을 두거나 상태를 보고하면 이사님께 잘못된 상황 인식을 전달하게 된다. 복구 게이트가 매번 `Session cwd(무시)`로 경고하는 데도 불구하고 반복적으로 헷갈렸다.

**How to apply:**
- 세션 시작 시 "workspace"/"cwd" 경로를 보면, 그것이 `~/.cokacdir/workspace/<랜덤id>`인지 프로젝트 repo인지 먼저 판별.
- 임시 세션 폴더면 작업 기준에서 제외. 내 진짜 작업 디렉토리는 `bot_settings.json`의 `last_sessions[<채팅id>]` 또는 온보딩의 `/start <프로젝트repo>` 값(`~/projects/<프로젝트>`)으로 확인.
- "workspace가 비어 있다" 같은 보고는 임시 폴더를 본 것일 확률이 높으니, 보고 전 경로 종류부터 확인.
- canonical memory dir(`…/akl0hdys/memory`)는 예외 — 이것은 메모리 저장소이지 작업 디렉토리가 아님.

관련 [[clear-recovery-map]] · [[current-work-state]] · [[context-explosion-causes]].
