---
title: 홈서버 이관·통합 종합 설계 v1 승인
date: 2026-09-06
status: accepted
tags: [agent-ops, infra, decision]
---

# 홈서버 이관·통합 종합 설계 v1 승인

- 이사님 2026-09-06 승인("1.승인"). 대상: `projects/agent-ops/homeserver-target-design-v1.md` (v1.1).
- 함께 소결: ①테일스케일 조직망 채택 ②Spring=스트랭글러 흡수 ③AWS=엣지 축소(완전 퇴출 아님)
  ④Task 하네스 표준(7필드·게이트·worktree) ⑤"규칙 먼저·이관은 마지막" 실행 순서.
- 실물 진척(당일): 신규 엣지 aws512-edge(512MB) 봇 가동·tailnet 편입 완료, 조직망 6노드 지도 확정.
- **미결정(보류)**: 0단계 신규 기능 개발 동결 — 이사님 "동결은 모르겠다" → 동결 없이 진행.
  인벤토리(짐 목록)는 기록만 하는 작업이라 동결과 무관하게 착수 가능.
- 첫 실무 분장(매니저=관제·분배 집중 원칙, 09-06): 티켓 템플릿(Task Contract 7필드)은 매니저,
  provenance 6필드 표준 초안은 현지 담당 봇(n100-zcode/firebat, matrix-studio-spring 소유)에게
  회의방 경유 배정.
