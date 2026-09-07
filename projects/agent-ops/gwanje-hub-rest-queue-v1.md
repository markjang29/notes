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
| GET | `/api/hub/history` | **메시지 이력**(최신순·봇/타입/상태 필터) — 이사님 전체, 봇은 자기 관련만. `/hub` 화면 이력 섹션에서 조회 |
| POST | `/api/hub/msg/{id}/requeue` | 이사님 전용 — dead/막힘 재큐 |
| POST | `/api/hub/dead/clear` | 이사님 전용 — DLQ 비움 |

- 시간은 전부 KST. payload 상한 8,000자. priority 1(긴급)~9(기본 5).
- `to`는 roster의 username 또는 `@all`. `@all`은 `notice`·`review`만 허용(ACK 도배 재발 방지).

## 홈 이전 계획 (이 서비스는 "이관 목록"에 이미 올라 있다)

1. 허브는 8023 모듈이라 **8023 회의방의 홈(duradev) 이전과 동행** — 별도 이관 작업 없음.
2. 진입: `http://43.201.34.144/hub` → 엣지(aws512-edge) nginx → Tailscale → **duradev 8023**.
   - 09-07 UTC 14:25(=KST 23:25) gmwin claude가 요청에 따라 라우트 개설 — 당시 임시로 13.125.131.126:8023
     프록시(GET 전용). 백업: 엣지 `~/nginx-backups/edge.conf.bak-hub-09071425`.
   - 09-07 23:40 **이사님 지시("13.은 이제 없다 — 43.으로 해결, 시도·기록·안내 전면 금지")로 재정리 완료
     (codex_dev_1, 엣지 키 `~/.ssh/lightsail-512ram.pem` 확보 후 직접 수정)**: edge.conf에서 8GB 참조
     (13.125.131.126·100.81.50.115) **전면 제거**, `/hub`·`/api/hub`를 `duradev_hub`(100.109.91.0:8023)로
     고정, GET 전용 제한 제거(이사님 재큐·DLQ 비움 POST 필요). 실측: nginx -t OK·reload, 회귀
     /·/healthz·/governance·/policies 200, /hub 502(duradev 8023 배치 대기 — 배치 즉시 200).
     이후 엣지 재실측으로 13.·8GB 참조 0건 유지 확인. 수행 경로·상세: `edge-routing-2026-09-07.md`.
3. 8018 관제 한판은 `/api/hub/status`를 같은 tailnet으로 폴링(8GB 의존 제거).
4. **필요 조치(이사님 결정 1건)**: duradev 접근 수단 — ①이 박스에서 duradev로 SSH 키 등록, 또는
   ②홈 측 봇(firebat/n100-zcode·gmwin)에 배치 지시. 현재 이 박스→duradev SSH는 publickey 거부(09-07 실측).

## 실측 (09-07, 스크래치 포트 실측 — 라이브 8023 무영향)

- 14항목 전부 통과: task 발행+wake 콜백 1회 호출, 멱등키 중복 수렴(deduped·동일 id),
  인증 실패 401, 봇별 토큰 발행, peek 상태 불변, drain→delivered, ack→acked, done→done,
  fail→재큐(attempts 증가)→재배달→fail→dead 전이, `@all` notice 단일행·배달 안 됨,
  ttl 만료→expired, requeue, DLQ clear, status 토큰모드(per-bot) 표시.
- 시험 방식: hub_router를 별도 앱(:8099)에 장착해 실측 — 라이브 8023은 건드리지 않음.
  운영 반영은 meeting-room.service 재시작으로 활성화.

## ELI5

봇들끼리 소리 지르며 바로 부탁하던 걸, **접수창구에 종이 접수로 바꾼 것**입니다. 접수증 번호가 있고
(멱등키), 받는 봇은 자기 서랍만 확인하고(인박스), 못 하면 다시 서랍으로 돌아가고(재시도), 세 번 못 하면
"못 처리함" 서랍(DLQ)으로 갑니다. 이사님은 접수 현황판(status)만 보면 됩니다.

## v1.1 — 메시지 서버 완성 (09-07 2차, 이사님 지시 "근본은 메시지 서버인샘 치고")

### ① 기술 선택 — 왜 이 조합인가

| 후보 | 판정 |
|---|---|
| **FastAPI + SQLite(8023 내장) — 채택** | 서비스·포트 증설 0, 봇 20기 규모엔 SQLite WAL 충분, 파일째 홈 이관 |
| Kafka/Redis/Mongo 전용 브로커 | 봇 간 메시지 분당 수 건 규모에 과잉 — 운영 인프라만 늘어남. 도메인 대량 큐(nai-queue)만 해당 |
| Mattermost/Zulip 도입 | A안 승인(09-04)으로 자체 발전 확정 — 커스텀 오케스트레이션 이식 비용이 이득 초과 |
| Spring Modulith 흡수 | 원사이트 2차 단계에서 기능 단위 흡수(스트랭글러) — 지금 스키마가 그대로 계약이 됨 |

### ② 관제 페이지 — `/hub` 현황판 (8023)

- 상단 집계 카드 6장: 대기·배달·수신확인·완료·못처리함(DLQ)·만료
- 봇별 큐 표(대기/배달/못처리함), DLQ 최근 10건 + **재큐·DLQ 비움 버튼(이사님 토큰 전용)**
- 10초 자동 갱신, 모바일 퍼스트 카드형, CDN 0, 토큰은 입력 1회 → 브라우저 저장
- 홈 이전 후 8018 관제 한판이 같은 `/api/hub/status`를 읽어 한 판에 합침

### ③ 사칙 등 배포 방식

```
매니저/이사님 POST /api/hub/send {to:"@all", type:"notice", payload:{text:"[사칙 개정] ..."}}
  → 큐 적재(감사 보존) + 방 공지 기록 + 활성 공지 등록(notices-active.jsonl)
  → 전 봇이 다음 구동 시 무조건 문맥 주입 (ACK 요구 없음 — 토큰 0 원칙)
```
- notice는 개인 수신함으로 흐르지 않는다(도배 방지) — 배포는 주입으로, 작업은 큐로 역할 분리
- 내리는 법: 기존 `/api/notices` DELETE 그대로

### ④ 각 봇의 메시지 폴링 방식 — 표준 클라이언트 `hub_client.py` 제공

```
GET /api/hub/inbox?bot=<나>&limit=5   ← 30초 권장 주기 (queued→delivered 자동 배달)
  → 메시지 처리 → POST /msg/{id}/ack → 완료 시 /done, 실패 시 /fail {error}
     (fail 3회 → DLQ. 10분 무응답도 자동 재큐 — 죽은 봇의 일이 큐에 남아 회수됨)
```
- 로컬 봇: `from hub_client import HubClient` 후 `poll_forever(handler)`
- 원격 봇(N100·gmwin): `python3 hub_client.py poll --base http://43.201.34.144 --bot <이름> --token <토큰> --cmd <셸명령>`
- peek 모드로 훔쳐보기 가능(배달 상태 불변)

### ⑤ A 봇 → B 봇 전달 방법

```
A: hub.send("B봇", "task", {"prompt": "..."}, key="작업-001")
     → 큐 접수(멱등) → B 엔진 1회 wake(dispatch) → B가 drain으로 수신 → ack → 작업 → done
B의 중간 보고: hub.send("A봇", "progress", {...}) / 막히면 "blocked" / 끝나면 "submitted"
검수: 제3봇이 "review" — @all로 공개 검수요청도 가능(각 봇 수신함에 표시)
```
- 같은 큐 원장을 쓰므로 A→B 전달이 곧 관제 기록 — 별도 보고 체계 불필요

### 실측 v1.1 (09-07)

- 스크래치 20항목 전부 통과(v1 14항목 + notice 본문 필수 400·브로드캐스트 훅 호출·수신함 배제·
  review @all 수신함 표시·hub_client drain/ack)
- 라이브 반영: meeting-room.service 재시작, `/hub` 페이지 200, status API 200/401 확인
- 커밋: meeting-room `b1c7040` (**주의: meeting-room repo는 원격 없음 — 로컬 커밋만. 원격 생성은 별도 결정**)
  · notes 본 문서 커밋은 아래 배포 문장과 함께

## 배포 문장 (09-07, 회의방 공지용)

> [배포·이사님 09-07 지시] 관제 허브(메시지 서버) v1 가동 — 봇간 통신이 REST 큐로 바뀌었습니다.
> ① 지시·보고·질문은 이제 8023 `/api/hub/*`로 접수합니다. A봇→B봇 전달:
> `POST /api/hub/send {from, to, type, payload}` — task만 상대 엔진을 깨우고, notice(@all 한정)는
> 활성 공지로 전 봇 문맥 주입됩니다(ACK 불필요). ② 각 봇은 `hub_client.py`(8023 repo) 표준 폴러로
> 30초 주기 수신: drain → ack → done/fail. 실패 3회면 못 처리함(DLQ) — 재큐는 이사님 토큰으로.
> ③ 작업에는 멱등키(key)를 붙여 재전송 중복을 막습니다. 진행=progress, 막힘=blocked, 완료=submitted.
> ④ 현황판: `http://43.201.34.144/hub`(홈 이전 후 동일 경로). 정본: notes
> `projects/agent-ops/gwanje-hub-rest-queue-v1.md` + ADR `2026-09-07-gwanje-hub-rest-queue`.
> 폴링 봇 전환은 단계적으로 — 기존 @멘션 방도 당분간 병행됩니다.
