# [impl] RELAY-61 — 관제 한판 v0

## 산출 커밋

- `matrix-home`: `ecc621c92a39d8a771b4caf655c4ff8a643f73e9`
- `notes`: 본 RELAY-61 정본 커밋

## 구현

1. 8018 홈 첫 화면에 `🛡 관제 한판` 카드 추가.
2. 8018 사이트맵 내부 페이지에 `/governance` 링크 추가.
3. `/governance` 카드형 화면 추가:
   - 현재 `POLICY_SHA`
   - active bot 수
   - 사칙 OK / 구판 / 미보고 수
   - 봇별 모델, 역할, 맡은 일, 진행, 어려움, 다음 행동, 이해한 `POLICY_SHA`
4. `/api/governance` 추가:
   - Notes `policy-index-v1.json`, `roster.json`, `actors.json`
   - bot-dashboard `profiles.jsonl`
   - Cokacdir bot settings의 모델값만 사용(토큰값 미노출)
   - runtime check-in 상태 병합
5. `/api/governance/checkin` 추가:
   - 무토큰 401
   - 이사님 토큰은 전체 row 수정 가능
   - 해당 봇 토큰은 자기 username row만 수정 가능
6. ACK 사칙 `principles/gwanje-ack-protocol.md` 신설.
7. codex_dev_1 협업 설계 요청을 `gwanje-governance-board-v1.md`에 명시.

## 테스트

- `python -m py_compile main.py` 통과
- Flask test client:
  - `/governance` 200
  - `/api/governance` 200
  - `/`, `/sites` 200
  - active bot rows 17개
  - `heav_lnx_codex_dev_1_bot` row 포함
  - `/api/governance/checkin` 무토큰 POST 401
  - 토큰 원문 필드가 bot row에 포함되지 않음
- `policy-index-v1.json` JSON 문법 검사 통과

## 남은 작업

- codex_dev_1의 8023 관점 설계 리뷰 수령.
- 8023 ACK 메시지 타입/파서를 `/api/governance/checkin`과 연결.
- 8025 봇 대시보드에 `/governance` 링크 또는 API 통합.

