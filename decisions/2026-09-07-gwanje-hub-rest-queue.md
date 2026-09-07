# ADR — 봇간 통신 REST 큐를 8023 회의방에 내장, 관제 오너십 codex_dev_1 이관

- 날짜: 2026-09-07
- 상태: **accepted** (이사님 09-07 직접 지시: "관제도 소통봇 담당이야. 봇간의 통신을 REST API로 받아주고
  큐 관리가 되는 형태였으면 좋겠음" + "홈서버로 이전하자")
- 근거: `projects/agent-ops/gwanje-hub-rest-queue-v1.md` · RELAY-61 리뷰(gwanje-governance-board-v1.md)
  · 선례 `nai-queue-service-v1.md`(도메인 큐의 일반화)

## 맥락

봇간 통신이 ①8023 멘션 릴레이(즉시 엔진 구동, 큐 없음) ②Agent Mail(git 왕복, 런타임엔 과중) ③Telegram
(사람 전용)로 분산돼 있어 재시도·서열·적체 가시성이 없다. 이사님이 관제 오너십을 소통봇(codex_dev_1)에게
넘기고, 통신을 "REST API 수신 + 큐 관리" 형태로 바꾸라고 지시.

## 결정

1. **큐는 8023 안에 내장**(`/api/hub/*`, `hub.py`) — 새 서비스·새 포트를 만들지 않는다.
   원사이트 통합(8GB 셧다운 전제)에서 포트 정리 방향과 일치하고, 홈 이전은 8023 이관과 동행한다.
2. **저장은 SQLite WAL 1파일** — mongo 등 신규 인프라 도입하지 않는다(nai-queue와 다른 선택이유:
   허브는 8023 내장·파일째 이관이 요구). 런타임 원장이며, 완료의 정본은 여전히 Git commit이다.
3. **타입 7종**(notice·task·ack·progress·blocked·submitted·review), **task만 엔진 wake**,
   `@all`은 notice·review 한정 — ACK 도배·토큰 낭비 원칙(09-03)을 큐에서도 강제한다.
4. **봇별 독립 토큰**(`hub-tokens.json`, git 제외) — 관제 한판 v1의 남은 blocker(토큰 발급·보관 위치)를
   "8023 런타임 파일, 오너=관제 오너"로 소결. 미등록 봇은 기존 공유 토큰 폴백으로 점진 전환.
5. 상태머신 queued→delivered→acked→done / failed→재큐(3회)→dead, 가시시간초과 10분, 멱등키 지원.
6. 관제 오너십: 매니저 → **codex_dev_1(소통봇)**. `/control` 페이지 매칭(원사이트 문서의 "매니저" 표기)도
   여기로 갱신한다. work-queue·roadmap 반영은 매니저 몫.

## 결과

- meeting-room에 `/api/hub/*` 추가(구현 커밋 별도), 8018 관제 한판은 `/api/hub/status` 폴링로 연결 예정.
- 홈 이전: duradev 접근 수단(SSH 키 또는 홈 측 배치 지시)은 이사님 결정 사항으로 보고.
- 보류(후속 결정): Agent Mail과의 역할 재조정(영속 작업지시 vs 런타임 큐), 봇 폴러의 hub 전환 일정.
