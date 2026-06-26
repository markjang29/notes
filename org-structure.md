---
title: 조직 구조 — Telegram 그룹 매니저-팀장 협업
date: 2026-06-26
status: draft v0 (봇 ID 수집·사용자 확정 대기)
tags:
  - org
  - telegram
  - collaboration
---

# 조직 구조 — Telegram 그룹 중심 협업

> 모든 봇을 **Telegram 한 그룹 채팅**으로 모은다. 총 매니저가 중심이 되어 보고·조율·아이디어 회의·의사결정 support. 실시간은 그룹, 영구 기록은 `~/notes`.

## 그룹 구성 (Telegram)
- **사용자(준희)** — 최종 의사결정자, 아이디어/방향.
- **총 매니저 봇** — 조율·보고·회의 정리·ADR support·쿼터 감시.
- **RPG 팀장 봇** — 프로젝트 실행 + subagent 직원.
- **trader 팀장 봇** — 프로젝트 실행 + subagent 직원.
- (향후 팀장 추가 시 동일 패턴)

## 운영 사이클 (매니저 주도)
1. **진행 보고** — 매니저가 각 팀장 진행상황 수집·정리 → 사용자에게 요약 보고 (정기 cron 또는 사용자 호출 `@매니저 보고`).
2. **팀장 요청 라우팅** — 팀장이 리소스/결정/승인 요청 → 매니저가 정리 → 사용자 전달.
3. **아이디어 회의** — 사용자↔매니저(필요시 팀장 참여) 논의 → 매니저가 정리(옵션+트레이드오프).
4. **의사결정 support** — 매니저가 정리안 → 사용자 결정 → **ADR화**·팀장에 배포(`@팀장`).

## 메시지 프로토콜 (cokacdir 그룹)
- `@매니저 <...>` — 사용자→매니저 지시/질문.
- `@팀장 <...>` — 매니저→팀장 task 배정 (또는 사용자 직접).
- `;<...>` — 전체 브로드캐스트 (사칙 변경 등 공지).
- `/query@봇 <...>` — 특정 봇 쿼리.
- 매니저는 조율 역할이라 contextlevel을 높게, 팀장은 낮게(아래).

## 토큰/쿼터 관리 (context-budget 연계)
- **mention 기반** — 필요한 봇만 깨움, 비활성 봇은 토큰 0.
- **/contextlevel 제안** — 매니저 12(조율용 전망), 팀장 4–6(자기 관련 위주), 회의 중엔 일시 상향. 확정값은 운용하며 조정.
- **수면 batch** — 매니저가 cokacdir cron으로 팀장 task 예약 (5h 쿼터 윈도우 활용).
- token-report 훅으로 그룹 소비 감시 → 임계 시 인계(context-budget §3).

## 역할 분담
- **사용자:** 결정, 방향, 아이디어.
- **매니저:** work-queue 조율, 진행 보고, 회의 정리, ADR support, 쿼터 감시, 팀장 온보딩 감독(사칙 인증 확인).
- **팀장:** 프로젝트 실행, subagent 직원 소환, Codex 검증 루프, 진행 보고.
- **직원:** 팀장이 subagent로 task 단위 소환. 영구 봇 아님.

## 통신 계층 분담
- **실시간 조율·보고·회의** → Telegram 그룹.
- **영구 기록·인계·결정(ADR)·큐** → `~/notes` (`work-queue.md`, `decisions/`, `.reviews/`).

## 미해결 (봇 ID 수집 후 확정)
- [ ] 매니저 봇(이 봇) Telegram @username
- [ ] RPG 팀장 Telegram @username (현재 Discord → Telegram 신규/이전?)
- [ ] trader 팀장 Telegram @username (동일)
- [ ] 그룹 채팅 생성 + 봇 초대 + BotFather 프라이버시모드 off (모든 봇)
- [ ] /contextlevel 봇별 확정
- [ ] 본 구조 → ADR `decisions/2026-06-26-org-telegram-group.md`
