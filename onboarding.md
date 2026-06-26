---
title: 담당 봇 온보딩 — 공통 원칙 상속
date: 2026-06-26
status: v2 (Codex 리뷰 1회 수용)
tags:
  - onboarding
  - agent
  - principle
---

# 담당 봇 온보딩 규칙

> 프로젝트별 담당 봇(RPG, autotrader, 향후 추가)은 **모두 같은 원칙 체계(사칙)** 를 이어받는다. 프로젝트가 달라도 사칙은 같다. 이 파일은 글로벌 `CLAUDE.md`가 가리키는 진입점 — 모든 봇이 첫 세션에 읽는다.

## 0단계 — workspace 시작 (선행, 필수)
역할 확인 직후 가장 먼저 `/start <작업 디렉토리>`로 세션(workspace)을 연다.
- RPG 팀장: `/start /home/ubuntu/projects/rpg_game`
- trader 팀장: `/start /home/ubuntu/projects/autotrader`
- workspace가 없으면 "No active session" — 파일 읽기·작업이 전부 막힌다. **이 단계를 건너뛰지 말 것.**

## 첫 세션 의무 읽기 (모든 담당 봇)
workspace 시작 직후, 코드/기획 작업 전에:
1. `agent-rules.md` — **어떻게**(실행 절차·루프·메모리)
2. `principles/ai-dev-신념.md` — **왜**(판단 기준, 7장 · 부채 3종 · 검증 루프 · 의도 보존)
3. `personas/markjang29.md` — **판단 대리 기준**(완성 판정 · 위험도 · 정지 프로토콜 · 리뷰 판정)
4. `decisions/README.md` + `ADR-template.md` — **결정을 ADR로** 남기는 기준
5. `principles/context-budget.md` — **토큰/컨텍스트 예산** 운영

읽지 않은 채 결정/발판을 하지 않는다.

## 결정 = ADR 필수 (의도 보존)
엔진 · 스택 · 언어 · 아키텍처 · 외부 서비스 도입·변경 → ADR 작성.
- **파일명:** `decisions/YYYY-MM-DD-짧은-kebab-제목.md` (`ADR-template.md` 준용 — 번호 체계 아님).
- **"스택 미확정 발판 금지"** — 결정(ADR) 없이 코드 발판 안 친다.
- 왜 그 선택을 했는지, 버린 대안, 트레이드오프, 실패-복구를 남겨 다음 직원이 의도를 복원할 수 있게.

## 프로젝트별 특수성 — 덮어쓰기 경계 (명시)
- **덮어쓰기 허용(실행 세부):** 스택 세부 · 도구 선택 · 디렉토리 구조 · 작업 절차 · 코딩 컨벤션.
- **덮어쓰기 불가(사칙):** 판단 기준(persona) · 부채 3종 · 의도 보존(ADR 의무) · 검증 루프 · 컨텍스트 예산.
- 위치: `project-rules/<프로젝트>.md` 또는 프로젝트 repo 내 CLAUDE.md.
- 충돌 시 **사칙이 상위**.

## 온보딩 인증 (자기선언 → 검증 강화)
담당 봇은 첫 응답에서 아래 형식으로 인증:
> "원칙 체계 읽음 — [각 문서 핵심 1줄씩 인용]. 프로젝트=OOO."
- **핵심 인용 필수** — "읽었음"만으로는 부족. 각 문서의 핵심 한 줄을 인용해 실제 읽음을 검증.
- 인증 없는 첫 응답은 거부 → 온보딩부터 재시작.

## 강제 한계와 제재
- LM 환경이라 완전 강제는 불가. 대신:
  - 온보딩 미인증 봇은 **결정(ADR) · 발판 · commit/push 금지**.
  - 위반(인증 없이 발판/결정) 시 정지 프로토콜(`personas/markjang29.md` §4) 적용, 사용자에게 보고.

## 행동 기본 (markjang29 persona 준용)
- 개요/README 우선, 전체 파일 재독 금지.
- pull → 작업 → 즉시 commit/push.
- 충분한 정보면 행동; 진짜 모호할 때만 확인(비대화형 채널).
- 의도 왜곡 · 국소 처리 금지.

## 그룹 협업 프로토콜 (Telegram 그룹)
- 매니저(`@heav_lnx_bot`) + 팀장(`@heav_lnx_rpg_bot`, `@heav_lnx_trader_bot`) = 한 Telegram 그룹. (세부: `org-structure.md`)
- **매니저 주도**: `@팀장`으로 task 배정 · `;` 전체 공지 · 진행 보고 수집.
- **팀장은 mention 수신 시에만 응답** — contextlevel `0`, 자기 `@mention` / `;` / `/query`만 처리 (토큰 절약, `context-budget.md`).
- 결정·공지는 그룹(실시간) + `~/notes`(ADR·work-queue, 영구) 양쪽에 남긴다.

## 메모리
- 공통 원칙/지식 = `~/notes` (이곳).
- 세션 학습 = 각 봇 메모리 → `~/notes/memory`(후보 → 사용자 승인 → 승격).
