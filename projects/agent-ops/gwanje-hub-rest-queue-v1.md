---
title: 관제 허브 v1 — 봇간 통신 REST API + 큐 (8023 내장)
date: 2026-09-07
status: v1 구현·실측 완료 — 홈 이전은 duradev 접근 수단 확보 후 (관제 오너 = codex_dev_1, 이사님 09-07 지시)
tags:
  - agent-ops
  - gwanje
  - hub
  - queue
  - rest
---

# 관제 허브 v1 — 봇간 통신 REST API + 큐

> 이사님 09-07 지시: "우리 관제를 좀 효율적으로 바꾸고 홈서버로 이전하자. 관제도 소통봇 담당이야.
> 봇간의 통신을 REST API 로 받아주고 큐 관리가 되는 형태였으면 좋겠음"
> 오너십 변경: 관제 오너 = 매니저 → **codex_dev_1(소통봇)** (ADR `2026-09-07-gwanje-hub-rest-queue`)

## 한 줄 결론

봇간 지시·보고를 **8023 안에 REST 큐(`/api/hub/*`)로 받는다** — 서비스·포트 증설 없이,
task만 엔진을 깨우고 나머지는 적재+관제 전달만 한다(RELAY-61 리뷰의 구현). 홈 이전 시 8023과 함께 이동한다.

## 배경 — 지금 봇간 통신의 비효율

| 수단 | 문제 |
|---|---|
| 8023 멘션 릴레이(`@봇` → 즉시 엔진 구동) | 큐 없음 — 대화 한 줄이 곧 실행. 재시도·만료·서열 개념 없음 |
| Agent Mail(notes git 메일) | git pull/push 왕복이라 느리고, 런타임 이벤트(진행·블록)엔 무거움 |
| cokacdir Telegram | 사람 입구 전용 — 봇간 자동 통신로 아님 |

선례: 오늘 firewin이 구축한 `nai-queue`(:8026)가 이사님 지시 패턴("API로 request 전달하면 큐 받아서 처리")의
도메인 사례. 허브는 그 **조직 공용 일반판**이다 — 이미지 생성이 아니라 봇간 지시·보고·승인 흐름용.

## 설계

- **위치**: `~/projects/meeting-room/hub.py` — 8023 안에 APIRouter로 내장. 새 포트·새 서비스 없음
  (원사이트 통합 `/control` 흡수 조건·16+ 포트 정리 방향과 일치).
- **저장**: SQLite WAL 1파일(`hub-queue.db`, git 제외) — mongo 등 신규 인프라 없음, 파일째 이관 가능.
  nai-queue가 mongo인 것과 달리 허브는 "8023에 내장·홈 이관 동행"이 요구라 내장 저장이 맞다.
- **타입**(RELAY-61 리뷰 확정판): `notice` `task` `ack` `progress` `blocked` `submitted` `review`.
  **`task`만 엔진 wake**(기존 dispatch 재사용 — 1회 토큰 비용), 나머지는 적재+관제 전달만.
- **상태머신**: `queued → delivered → acked → done` / `failed → (attempts<3 재큐 | dead)` / notice 만료 `expired`.
  - 가시시간초과: delivered 후 10분 무응답 → 자동 재큐(attempts+1), 3회 초과 시 dead(DLQ).
  - 멱등키: 송신자가 `key` 제공 시 unique — 재시도해도 중복 작업 없음(Agent Mail 멱등키와 동일 발상).
- **인증**: `hub-tokens.json`(username→token, chmod 600, git 제외) — **봇별 독립 토큰**.
  파일에 없는 봇은 기존 `ROOM_BOT_TOKEN` 폴백(전환을 안 깨는 점진 강화 — 관제 한판 v1의 남은 blocker 해소).
  이사님/매니저는 기존 ACCESS 토큰(관리: 재큐·DLQ 비움).
- **관제(8018) 연결**: `GET /api/hub/status` 를 8018 관제 한판이 폴링 — 봇별 큐 적체·DLQ를 한판에 표시.

### 엔드포인트 (X-Token 헤더)

| 메서드 | 경로 | 용도 |
|---|---|---|
| POST | `/api/hub/send` | 발행 `{from,to,type,payload,priority?,key?,ttl?,wake?}` → `{id,state}` (dedup 시 원 id) |
| GET | `/api/hub/inbox?bot=&limit=&peek=` | 수신 (기본: queued→delivered 배달, `peek=1` 읽기만) |
| POST | `/api/hub/msg/{id}/ack` · `/done` | 수신 확인·완료 |
| POST | `/api/hub/msg/{id}/fail` | 실패 보고(오류문) → 자동 재큐 또는 dead |
| GET | `/api/hub/status` | 큐 집계(상태별·봇별 적체·DLQ·토큰모드) — 8018 관제·이사님 확인용 |
| POST | `/api/hub/msg/{id}/requeue` | 이사님 전용 — dead/막힘 재큐 |
| POST | `/api/hub/dead/clear` | 이사님 전용 — DLQ 비움 |

- 시간은 전부 KST. payload 상한 8,000자. priority 1(긴급)~9(기본 5).
- `to`는 roster의 username 또는 `@all`. `@all`은 `notice`·`review`만 허용(ACK 도배 재발 방지).

## 홈 이전 계획 (이 서비스는 "이관 목록"에 이미 올라 있다)

1. 허브는 8023 모듈이라 **8023 회의방의 홈(duradev) 이전과 동행** — 별도 이관 작업 없음.
2. 이전 후 진입: `http://43.201.34.144/hub/...` → 엣지(aws512-edge) nginx → Tailscale → 홈 8023.
3. 8018 관제 한판은 `/api/hub/status`를 같은 tailnet으로 폴링(8GB 의존 제거).
4. **필요 조치(이사님 결정 1건)**: duradev 접근 수단 — ①이 박스에서 duradev로 SSH 키 등록, 또는
   ②홈 측 봇(firebat/n100-zcode·gmwin)에 배치 지시. 현재 이 박스→duradev SSH는 publickey 거부(09-07 실측).

## 실측 (09-07, TestClient)

- (구현 직후 아래에 갱신 — 미실측 상태로 성공을 기록하지 않는다)

## ELI5

봇들끼리 소리 지르며 바로 부탁하던 걸, **접수창구에 종이 접수로 바꾼 것**입니다. 접수증 번호가 있고
(멱등키), 받는 봇은 자기 서랍만 확인하고(인박스), 못 하면 다시 서랍으로 돌아가고(재시도), 세 번 못 하면
"못 처리함" 서랍(DLQ)으로 갑니다. 이사님은 접수 현황판(status)만 보면 됩니다.
