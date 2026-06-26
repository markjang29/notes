---
title: 참조 / 영감 출처
date: 2026-06-26
tags:
  - references
---

# 참조 / 영감 출처

이 시스템을 설계할 때 참고한 패턴·도구. 원칙 문서 본문에는 두지 않고 여기에 보존 (나중에 "왜 이렇게 설계했는가" 추적용).

## 암묵지 캡처 / 인터뷰 스킬
- `grill-me` — 질문 폭격으로 암묵지를 끌어내는 인터뷰 패턴. 페르소나·판단기준 캡처에 차용.
- mattpocock/skills — https://github.com/mattpocock/skills. 스킬 설계 패턴(선언적 발화 트리거) 참고.

## AI 자기개선 루프 도구
- ouroboros — 자기 참조적 개선 루프(출력이 다시 입력). §4 closed loop 발상.
- oh my codex — Codex 런타임 래퍼. 검증·비판 루프(§2)의 구현 계보.
- oh my openagent — 범용 에이전트 런타임 강화. 다중 에이전트 협업 참고.

## 외부 메모리 시스템 후보
- Mem0 — 외부 메모리 서비스. company-wide 메모리(§5)의 참고 구현.
- seCall — https://github.com/hang-in/seCall. 세션/호출 기반 메모리 캡처 패턴.
