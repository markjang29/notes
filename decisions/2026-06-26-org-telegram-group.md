---
title: ADR — Telegram 그룹 기반 매니저-팀장 조직 구조
date: 2026-06-26
tags:
  - adr
  - org
  - telegram
---

# ADR — Telegram 그룹 매니저-팀장 조직 구조

## 상태
accepted

## 날짜
2026-06-26

## 프로젝트 / 적용 범위
공통 (모든 프로젝트 봇 조직)

## 결정
모든 담당 봇을 **Telegram 한 그룹 채팅**에 배치. 총 매니저(`@heav_lnx`)가 중심이 되어 보고·조율·아이디어 회의·의사결정 support 사이클을 운영. 하위 직원은 팀장이 **subagent로 task 단위 소환** (영구 봇 아님).

## 맥락
- 멀티 프로젝트(RPG, trader) 멀티 봇 운영 필요.
- Z.AI / Codex 가 5시간 쿼터제 → 토큰·시간 효율 필수.
- 이전엔 매니저→팀장 통신이 공유 파일(notes) 비동기만 가능 → 실시간 조율 부족.
- cokacdir 그룹 채팅(공유 로그 + `/contextlevel`)이 실시간 협업 계층을 제공함을 확인.

## 제약
- 5시간 쿼터(Z.AI·Codex) — 봇 동시 활성 시 경쟁.
- Telegram 그룹 — `/contextlevel` 값이 토큰 직결 (모든 봇에 공유 로그 주입).
- Telegram 프라이버시모드 off 필요 (BotFather).

## 선택한 이유 / 버린 대안
- **선택:** Telegram 그룹 + 매니저 주도 사이클 + 직원=subagent.
- 버린 — **직원을 일일히 영구 봇으로**: 쿼터 경쟁·온보딩·컨텍스트 N배. subagent가 경량.
- 버린 — **Discord 그룹**: Telegram 하나로 통일(매니저·사용자 채널 일원화).
- 버린 — **파일 비동기만**: 실시간 조율·회의 불가. 그룹+파일 병용으로 보완.
- 버린 — **높은 contextlevel 전 봇**: 토큰 폭발. 매니저만 8, 팀장 0+mention으로 절약.

## 트레이드오프
- 얻은 것: 실시간 매니저-팀장 통신, mention 기반 선택적 활성(쿼터 절약), 매니저 가시성.
- 잃은 것: 팀장이 다른 팀장 활동을 직접 못 봄(contextlevel 0) → 매니저가 라우팅/요약으로 보완.

## 검증 기준
- 그룹 세팅 후 첫 온보딩 사이클(팀장 사칙 인증) 정상 동작.
- token-report로 그룹 토큰 소비가 예산 내 유지.
- 수면 batch(cron)가 5h 쿼터 윈도우에서 큐를 깎음.

## 실패 / 복구 과정
- contextlevel 로 토큰 폭발 시 → 전 봇 0 + mention 전용으로 회귀(context-budget §3 인계).
- 매니저 라우팅 병목 시 → 사용자가 팀장에 직접 `@mention` 우회.

## 후속 재검토 조건
- 팀장 3개 이상 추가 시 contextlevel/역할 재조정.
- 쿼터 정책 변경(5h→다른 윈도우) 시 수면 batch 재설계.
- 그룹 로그 과다로 토큰 누적 시 파일 위임 비중 확대.

## 관련 링크
- `org-structure.md` (상세 구조·프로토콜)
- `onboarding.md` (그룹 협업 프로토콜 섹션)
- `principles/context-budget.md` (토큰/쿼터 원칙)
