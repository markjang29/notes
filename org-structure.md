---
title: 조직 구조 — Telegram 그룹 매니저-팀장 협업
date: 2026-06-26
status: 확정 v1 (2026-06-26, Telegram 그룹 세팅 완료)
tags:
  - org
  - telegram
  - collaboration
---

# 조직 구조 — Telegram 그룹 중심 협업

> 모든 봇을 **Telegram 한 그룹 채팅**으로 모은다. 총 매니저가 중심이 되어 보고·조율·아이디어 회의·의사결정 support. 실시간은 그룹, 영구 기록은 `~/notes`.

## 그룹 구성 (Telegram) — 확정
- **사용자(준희)** — 최종 의사결정자, 아이디어/방향.
- **총 매니저 봇 `@heav_lnx_bot`** (이 봇) — 조율·보고·회의 정리·ADR support·쿼터 감시.
- **RPG 팀장 봇 `@heav_lnx_rpg_bot`** — 프로젝트 실행 + subagent 직원.
- **trader 팀장 봇 `@heav_lnx_trader_bot`** — 프로젝트 실행 + subagent 직원.
- **시나리오 팀장 봇 `@heav_lnx_scenario_bot`** — **자생 세계관 시나리오**: 캐릭터 챗(character.ai류)처럼 세계관·캐릭터가 자생적으로 생성·운영되는 독립 시나리오 생태계. RPG 세계관과 **분리**. repo `~/projects/scenario`. 2026-06-30 신설.
- (향후 팀장 추가 시 동일 패턴)

## 운영 사이클 (매니저 주도)
1. **진행 보고** — 매니저가 각 팀장 진행상황 수집·정리 → 사용자에게 요약 보고 (정기 cron 또는 사용자 호출 `@heav_lnx_bot 보고`).
2. **팀장 요청 라우팅** — 팀장이 리소스/결정/승인 요청 → 매니저가 정리 → 사용자 전달.
3. **아이디어 회의** — 사용자↔매니저(필요시 팀장 참여) 논의 → 매니저가 정리(옵션+트레이드오프).
4. **의사결정 support** — 매니저가 정리안 → 사용자 결정 → **ADR화**·팀장에 배포(`@팀장`).

## 메시지 프로토콜 (cokacdir 그룹)
- `@heav_lnx_bot <...>` — 사용자→매니저 지시/질문.
- `@heav_lnx_rpg_bot <...>` / `@heav_lnx_trader_bot <...>` / `@heav_lnx_scenario_bot <...>` — 매니저→팀장 task 배정 (또는 사용자 직접).
- `;<...>` — 전체 브로드캐스트 (사칙 변경 등 공지).
- `/query@봇 <...>` — 특정 봇 쿼리.

## 토큰/쿼터 관리 (context-budget 연계)
- **mention 기반** — 필요한 봇만 깨움, 비활성 봇은 토큰 0.
- **/contextlevel 확정값:** 매니저 `8` (팀장 활동 가시) / 팀장 `0` (mention 수신만). 그룹에서 `@봇 /contextlevel N` 설정. 운용하며 조정.
- **수면 batch** — 매니저가 cokacdir cron으로 팀장 task 예약 (5h 쿼터 윈도우 활용).
- token-report 훅으로 그룹 소비 감시 → 임계 시 인계(context-budget §3).

## 역할 분담
- **사용자:** 결정·방향·아이디어 추가. (작업 기획·배분은 **매니저 영역** — 이사님이 일일이 지시할 필요 없음. 이사님 피드백 06-30.)
- **매니저:** **작업 기획·배분 주도** — 매니저가 판단해 팀장에게 배정. **실행(실제 작업)은 팀장이 하고, 매니저는 직접 작업 금지**(보고·조율만 — 팀장 둔 의미 살리기). 이사님께는 정해진 시간에 **결과 + 결정 안건** 보고 (할 일/지시 내용 반복 금지 — **결과 중심**). 시간 보고는 항상 **KST**. work-queue 조율, 회의 정리, ADR support, 쿼터 감시, 팀장 온보딩 감독(사칙 인증 확인).
- **팀장:** 프로젝트 실행, subagent 직원 소환, Codex 검증 루프, 진행 보고.
- **직원:** 팀장이 subagent로 task 단위 소환. 영구 봇 아님.

## 통신 계층 분담
- **실시간 조율·보고·회의** → Telegram 그룹.
- **영구 기록·인계·결정(ADR)·큐** → `~/notes` (`work-queue.md`, `decisions/`, `.reviews/`).

## 체크리스트
- [x] 봇 ID: 매니저 `@heav_lnx_bot`, RPG `@heav_lnx_rpg_bot`, trader `@heav_lnx_trader_bot`, 시나리오 `@heav_lnx_scenario_bot`
- [x] 그룹 채팅 생성 + 봇 초대
- [ ] BotFather 프라이버시모드 off (각 봇 `/setprivacy` → Disable) — 확인 필요
- [ ] 그룹에서 `/contextlevel` 설정 (매니저 8 / 팀장 0)
- [x] 본 구조 → ADR `decisions/2026-06-26-org-telegram-group.md`
