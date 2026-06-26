---
title: 담당 봇 온보딩 — 공통 원칙 상속
date: 2026-06-26
tags:
  - onboarding
  - agent
  - principle
---

# 담당 봇 온보딩 규칙

> 프로젝트별 담당 봇(RPG, autotrader, 향후 추가)은 **모두 같은 원칙 체계(사칙)** 를 이어받는다. "직원"이 공통 판단 기준 아래에서 일한다. 프로젝트가 달라도 사칙은 같다.

## 첫 세션 의무 읽기 (모든 담당 봇)
역할 확인 직후, 코드/기획 작업 전에 아래를 읽는다:
1. `agent-rules.md` — **어떻게**(실행 절차·루프·메모리)
2. `principles/ai-dev-신념.md` — **왜**(판단 기준, 7장 · 부채 3종 · 검증 루프 · 의도 보존)
3. `personas/markjang29.md` — **판단 대리 기준**(완성 판정 · 위험도 · 정지 프로토콜 · 리뷰 판정)
4. `decisions/README.md` + `ADR-template.md` — **결정을 ADR로** 남기는 기준
5. `principles/context-budget.md` — **토큰/컨텍스트 예산** 운영

읽지 않은 채 발판/결정을 하지 않는다.

## 결정 = ADR 필수 (의도 보존)
엔진 · 스택 · 언어 · 아키텍처 · 외부 서비스 도입·변경 → `decisions/ADR-NNNN-<주제>.md` 작성.
- **"스택 미확정 발판 금지"** — 결정(ADR) 없이 코드 발판을 안 친다.
- ADR에 왜 그 선택을 했는지, 제외된 대안, 트레이드오프, 실패-복구를 남긴다. 다음 직원이 의도를 복원할 수 있게.

## 프로젝트별 특수성
`project-rules/<프로젝트>.md` 또는 프로젝트 repo 내 CLAUDE.md. 공통 원칙(이 문서 + `principles/`) 위에 덮어쓰되, **충돌 시 공통 원칙이 상위**.

## 행동 기본 (markjang29 persona 준용)
- 개요/README 우선, 전체 파일 재독 금지.
- pull → 작업 → 즉시 commit/push.
- 충분한 정보면 행동; 진짜 모호할 때만 확인(비대화형 채널).
- 의도 왜곡 · 국소 처리 금지. 짜증 신호 = 정지 프로토콜(persona §4).

## 메모리
- 공통 원칙/지식 = `~/notes` (이곳).
- 세션 학습 = 각 봇 메모리 → `~/notes/memory`(후보 → 사용자 승인 → 승격).

## 온보딩 체크 (첫 응답에 보여줄 것)
담당 봇은 첫 응답에서 아래를 한 줄로 인증:
> "원칙 체계 읽음: agent-rules · ai-dev-신념 · markjang29 · ADR · context-budget. 프로젝트=OOO."
