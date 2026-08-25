# 회의록 — 승인 다ossier 제안 v0 전 봇 회의

- 안건: 승인 카드 실체 재설계 (다ossier 구조·순서 수정·임의 스토리 배제)
- 근거: 이사님 08-25 지시, 카드 `req-20260825191347-3cf7b0`
- 정본: `projects/agent-ops/relay/APPROVAL-DOSSIER-PROPOSAL.md` (commit `c09c992`)
- 진행: 매니저 (중립) / 종합: zcode (SE)
- 마감: 2026-08-26 (KST) 각 봇 의견서 1p → 종합본 이사님 보고

## 핵심 논점 (정본 요약)

1. 승인 카드 = 검증 다ossier의 마지막 장 — 7요소(리수셋업·3회 채팅·NAI·GATE·활용도·액션·승인) 완성 후에만 이사님 열람
2. 재료는 실존 자산 source-unit만 — 봇 임의 창작은 승격 불가
3. 파이프라인 단계별 마블 수 홈(8018) 가시화

## 의견서 현황

| 봇 | 역할 | 논점 | 상태 | 산출 |
|---|---|---|---|---|
| scenario | 낙관·창작 가치 | 다ossier가 창작을 막는가 살리는가 | 대기 | `opinions/scenario.md` |
| audit | 비관·통제 | 위조 가능성·GATE 우회 경로 | 대기 | `opinions/audit.md` |
| asset_agent | 실무·비용 | 자산당 생성 비용(NAI·채팅 3회) 감당 가능한가 | 대기 | `opinions/asset_agent.md` |
| rpg | 소비자·활용도 | 활용도 점수가 실제 작품에 쓸만한가 | 대기 | `opinions/rpg.md` |
| codex_dev_1 | 리뷰·구현 | 다ossier 자동 생성 기술 리스크 | 대기 | `opinions/codex_dev_1.md` |
| codex_dev_2 | 리뷰·구현 | 다ossier 자동 생성 기술 리스크 | 대기 | `opinions/codex_dev_2.md` |
| manager | 중립 진행 | 의견 취합·회의록 | 진행 중 | 본 문서 |
| zcode | SE | 종합·설계 확정 | 대기 (의견 취합 후) | 종합본 |

의견서 형식: 1p, `## 낙관 근거` / `## 비관 근거` / `## 수정안`.

## 진행 로그

- 2026-08-25 19:16 — 매니저 접수(claim) → running. 정본 c09c992 origin 푸시·양 클론 동기화.
- 2026-08-25 19:2x — 6봇 웨이크 원샷 등록(개별 비공개 채널). 아래 로그에 발화 확인 기록.
