---
title: 시나리오 자원 참조 — scenario repo
date: 2026-06-30
status: v1
tags:
  - references
  - scenario
  - writing
  - risuai
---

# 시나리오 자원 참조 — scenario repo

`D:\LLM`(RisuAI + 로컬 LLM 캐릭터·소설 창작 생태계)의 구조·방법론을 정리한 **private repo**.
시나리오가 들어가는 **모든 프로젝트**(RPG 게임·소설·캐릭터 창작)에서 범용 참고 자료로 쓴다.
**본 문서는 포인터** — 실제 자료는 scenario repo 에 있다.

> **repo:** `github.com/markjang29/scenario` (private)
> **clone:** `C:\Users\heave\projects\scenario`
> **원본 자산:** 로컬 `D:\LLM\` (RisuAI 작업실, 바이너리는 여기에 보관)

## 활용 가능 자원

- [ ] **생태계 구조 해설** → `ecosystem/`
  (overview · character-cards · lorebooks · prompts · modules · workflow · risuai-setup)
- [ ] **범용 빈 틀** → `templates/`
  (character-sheet · lorebook-entry · system-prompt · module-spec)
- [ ] **실제 샘플(NSFW 포함)** → `examples/` (characters · lorebooks · prompts)
- [ ] **자산 메타 인덱스** → `catalog/` (원본은 D:\LLM, 발췌 메타만)

## 접근 방식

1. `ecosystem/overview.md` 로 전체 그림을 잡는다.
2. `templates/` 에서 해당 프로젝트에 맞는 빈 틀을 복사해 채운다.
3. `examples/` 로 구체 예시를 참고한다 (NSFW 샘플은 private 접근 필요).
4. 특정 자산 원본이 필요하면 `catalog/*.csv` 의 `src` 경로 → `D:\LLM\...`.

## 핵심 (3줄)

- LLM 은 상태 없는 함수 — 모든 기억·세계관은 매 턴 프롬프트에 재주입.
- 4개 조립 부품: 캐릭터 카드 + 로어북(발동형 사실) + 시스템 프롬프트 + 모듈.
- 구조는 RisuAI 종속이 아님 — 게임 NPC·AI 보조작가·소설 세계관 DB 에 동일 적용.

## NSFW 안내

scenario repo 는 **private**. `examples/` 에 NSFW 샘플 포함.
공개 전환 시 `examples/` NSFW 샘플 먼저 정리. `ecosystem/`·`templates/` 는 구조만(세부 묘사 없음).

## 관련 원칙

- 장기 신념: [[ai-dev-신념]] (`principles/ai-dev-신념.md`)
- 외부 참조 목록: [[references]] (`principles/references.md`)
