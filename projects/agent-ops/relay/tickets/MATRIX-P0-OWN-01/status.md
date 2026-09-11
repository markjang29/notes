---
ticket: MATRIX-P0-OWN-01
updated: 2026-09-11T16:05+09:00
by: aws-manager
source: matrix-home@15ce46e9516b015f63955bcd536d5cc257bc186e
---

# MATRIX-P0-OWN-01 상태 (aws-manager)

## 배정 완료 (owner-allocation-v1.json, 총 68/68)

- route 36 + site 27 + internal 5 = 68. 각 항목 정확히 1명의 등록·capable owner.
- owner 분배: aws-manager 31 · aws-audit 12 · aws-asset-agent 10 · aws-novel-col 7 · aws-scenario 5 · aws-rpg 2 · aws-arcade 1.
- blocker 6건(8002·8011·8013·8020·8765·8766): needs_adr — 이사님 선택 안건으로 분리, 추측 결정 없음(work-order done_criteria 3번 준수).
- 배정 기준: actors.json@b7f5233의 capabilities·repo_ids와 disposition 모듈·포트 소유 대조. 매트릭스 HOME 쓰기 권한은 actors.json v10에 미등록이므로
  본 배정은 "조정 책임" 배정이며, 구현 착수는 개별 child mail(권한 포함)의 ACK 이후로 제한.

## 카운터

- allocated: 68/68
- ack: 0 (child mail 미발행·미전달 단계)
- in_progress: 0
- submitted: 0
- verified: 0

## 이슈·결정 안건

1. needs_adr 6포트(8002·8011·8013·8020·8765·8766) — 이사님 선택 대기. 유지·통합·종료 선택지는 disposition JSON note 참조.
2. actors.json에 matrix-home repo_ids 미등록(v10) — 구현 착수 전 최소 권한 변경안을 이사님 승인용으로 별도 제시 예정. 지금은 권한 변경 실행 없음(금지 조항 준수).
3. 신규 공개 웹·포트 생성, AWS 중지·종료, 데이터 삭제: 미실시(전 봇 공지 준수). 본 티켓의 구현은 없음 — 산출물은 notes 티켓 내 JSON·MD뿐.

## Git 근거

- allocation: projects/agent-ops/relay/tickets/MATRIX-P0-OWN-01/owner-allocation-v1.json (본 커밋)
- 정본 고정: work-order-v2.json@b7f5233 / 전환명세 matrix-home@15ce46e
