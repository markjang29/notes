---
title: Matrix 통합 후임과 Clear 경계
status: accepted
date: 2026-08-16
authority: 이사님 직접 지시
---

# Matrix 통합 후임과 Clear 경계

## 결정

Windows Codex와 ZCode의 구독 종료 이후 Matrix 전체 업무는 등록 actor `aws-manager`가
통합 후임으로 이어받는다. 이 결정은 Matrix 범위에서만 `org-structure.md`의 매니저 직접
구현 금지보다 우선한다. 다른 프로젝트의 역할 분담이나 권한을 확대하지 않는다.

후임의 Git 범위는 `matrix_asset_agent`, `scenario`, `matrix`, `matrix_zcode`,
`matrix_codex`, `matrix-engine`, `matrix-living-drama`다. 각 Git의 역할·쓰기 경계와 다음
카드는 `matrix_asset_agent@a9090058255277a2d7cfd3690bd8ff0b01b3fbb9`의
`collaboration/MATRIX-SUCCESSOR-HANDOFF.md`를 시작점으로 삼고, 실행 전 각 저장소의 최신
`origin/main`과 `AGENTS.md`를 다시 확인한다.

## 한 문장 교대 지시

```text
너는 Matrix 통합 후임이다. matrix_asset_agent 최신 main의 collaboration/MATRIX-SUCCESSOR-HANDOFF.md를 전부 읽고 [MATRIX-SUCCESSOR-CERT]를 출력한 뒤, 문서에 적힌 전체 Git의 최신 origin/main과 역할 경계를 재검증하고 NEXT-001부터 작은 카드로 실행·검사·commit·push·보고하라.
```

## Clear의 의미

`Clear 가능`은 현재 대화 기억을 폐기해도 위 한 문장과 Git만으로 역할·현황·다음 행동을
복원할 수 있다는 뜻이다. Matrix 제품 완료, 서비스 정상, 품질 우승 또는 미완료 카드의
종결을 뜻하지 않는다.

Clear 전에는 다음이 모두 원격 Git에 있어야 한다.

1. 위 결정과 actor registry의 후임 권한
2. 전체 인수인계 정본과 저장소별 `MATRIX-SUCCESSOR.md`
3. 최신 runtime audit와 알려진 dirty worktree·미배포 상태
4. 다음 카드 `NEXT-001`과 금지 동작
