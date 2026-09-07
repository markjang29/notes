---
ticket: RELAY-62
stage: relay:5-구현
owner: aws-audit
date: 2026-09-07
status: implemented
---

# RELAY-62 implementation note

## 변경

- `principles/edge-home-entrypoint-policy.md` 추가.
- `projects/agent-ops/policy-index-v1.json` version `2026-09-07.4`로 갱신.
- `projects/agent-ops/README.md`에 Edge/Home/Spring+React 원칙 추가.
- `projects/agent-ops/home-policy-sync-v1.md`에 `43.201.34.144` 진입점과 Tailscale/원사이트 기준 추가.
- `principles/gwanje-ack-protocol.md`에 ACK 시 Edge/Home 고려 확인 추가.
- `projects/agent-ops/gwanje-governance-board-v1.md`에 관제 check-in 확장 TODO 추가.
- `projects/agent-ops/roles/aws-audit-policy-steward.md`에 신규 감사 책임 추가.

## 검증 예정

- JSON 유효성 검사.
- `/api/policies`와 `/api/governance`의 Notes HEAD 반영 확인.
- `aws-audit` 자기 row check-in.
- 활성 schedule과 polling 후보 점검 보고.
