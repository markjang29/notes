---
title: Matrix RISU 대화 연속성 프로그램
status: active
updated: 2026-07-15
controller: windows-codex
---

# Matrix RISU 대화 연속성 프로그램

목표는 RISU의 매 턴 재주입, 로어북 trigger, 요약 기억, persona/module 조합을 Matrix의
검증 가능한 상태·event·reducer·checkpoint 구조로 발전시키는 것이다. 정적 Matrix compiler는
이미 있으나 실제 대화 재개와 branch 격리 runtime은 아직 없다.

시나리오 repo 정본 설계:
`docs/matrix-risu-continuity-program.md`와
`.agents/skills/matrix-factory/references/interactive-continuity-contract.md`.

## 작은 작업

- [x] Proton/Drive 같은 공유 폴더에서 현재 게시글 자산과 인접 발견을 분리하는 계약 작성
- [x] Arca 수정·사용 예시를 `interaction_examples`로 수집하는 규칙 작성
- [ ] `110558063`의 세션 요약·사용 명령을 첫 reviewed usage recipe로 작성
- [ ] `176729619`의 위치·부상·약속·관계·quest·기억 규칙을 reviewed recipe로 작성
- [ ] Mirka 수집 branch와 availability/lifecycle 이력을 한 input commit으로 정합화
- [ ] session/event/reducer/checkpoint/continuity receipt schema 작성
- [ ] 표준 라이브러리 기반 replay·resume·fork vertical slice 구현
- [ ] 8~12턴 후 process 재시작, 상태 유지, 요약 무오염, branch 격리 검증
- [ ] 사용자 상태 보기·사실 고정·정정·되감기·분기·내보내기 동작 설계
- [ ] actor별 client/backend/token pool과 실제 usage/latency/품질 측정

이 작업은 승인된 후보를 자동 구현하는 야간 ideation이 아니다. `windows-codex`가 장기 설계와
검증을 맡고, ZCode는 frozen schema/fixture 비교처럼 단순하고 범위가 고정된 작업만 맡는다.
