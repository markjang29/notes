---
title: aws-trader 운영 동결
status: active
date: 2026-07-16
authority: director direct instruction
---

# aws-trader 운영 동결

이사님의 직접 지시에 따라 `aws-trader`는 별도 재개 지시가 있을 때까지 작업하지 않는다.

- 야간 아이디어 생성과 아침 브리프 대상에서 제외한다.
- 자동 schedule, manager 위임, controller 자동 배정을 금지한다.
- 기존 작업·후보·감사 기록과 actor identity는 삭제하거나 다른 actor 소유로 바꾸지 않는다.
- 이사님이 과거에 맡긴 독립 작업도 자동 재개하지 않고 현재 상태를 보존한다.
- 재개는 이사님의 명시적인 새 지시와 별도 scoped work order가 있을 때만 허용한다.

이 동결은 actor 삭제나 기존 결과 폐기를 뜻하지 않는다. `aws-manager`, `windows-codex` 및 다른
actor는 Trader의 일을 대신 수행하거나 소유권을 가져가서는 안 된다.
