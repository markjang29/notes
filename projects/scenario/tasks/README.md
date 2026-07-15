---
title: Scenario 소형 작업 보드
status: active
last_reviewed: 2026-07-16
---

# Scenario 소형 작업 보드

## 업무 목표와 현재 판정

이 문서가 Windows Codex의 단일 실행 큐다. 새 질문이나 기술 문제가 생겨도 아래 `현재 WIP`를
임의로 바꾸지 않는다. 새 일은 큐에 넣고, 사용자가 우선순위를 바꾸거나 현재 WIP가 terminal로
닫힌 뒤에만 다음 카드로 이동한다.

| KPI | 2026-07-16 현재 | 통과 기준 |
|---|---|---|
| Arca 일일 수집 | terminal `0/1`; 설정값 35와 실제 처리량 사이에 큰 간극 | 우선 오늘 1건 terminal, 이후 warm-path 3건 계측으로 일일 목표 재산정 |
| ZCode 실제 배정 | 성공 `0건`; live probe HTTP 429 | quota 복구 뒤 frozen read-only packet 1건 ACK·RESULT·Codex 검수 |
| 예약 실행 | 일일 task 활성, sync task 비활성; 최근 자동 완결 증거 없음 | `AUTO-01` 재실행 receipt 또는 exact blocker |
| 단건 소요시간 | 단계별 계측 없음 | `OPS-01`~`OPS-05`로 실제·대기·LLM 시간 분리 |
| Matrix↔RISU 연속성 | C0 설계만 완료; 구현·benchmark 증거 없음 | C1 usage recipes 뒤 8개 continuity gate 측정 |
| 관리 화면 | Git 업무판은 이 문서; Notion은 commit 기반 투영 | Git commit/path가 있는 상태만 Notion에 표시 |

제품의 장기 목표는 검증된 Arca 자산을 Matrix 코어에 넣어 세계·캐릭터·페르소나·서사를
재현 가능하게 조립하고, 같은 캐릭터의 여러 세계선 경험을 본 캐릭터로 합성할 수 있는 공장을
만드는 것이다. Notion과 웹은 이 Git 정본을 사람이 읽고 결정하기 쉽게 보여주는 화면이지
별도 아이디어 저장소가 아니다.

## 운영 규칙

- WIP는 항상 1개다.
- 한 카드는 0.5~2 인일 안에 검증 가능한 결과를 만든다.
- 구현 전 입력·완료조건·rollback을 적고, 완료 후 증거와 소요시간을 기록한다.
- ZCode는 먼저 작은 read-only 패킷으로 통과한 작업 유형에만 사용한다.
- 실패한 ZCode 패킷을 같은 형태로 반복 호출하지 않는다.
- 단순 ZCode 작업은 60초 soft deadline, 180초 hard timeout, 30초 사용자 heartbeat를 적용한다.
- 모든 작업은 10분에 체크포인트를 만들고, 15분 초과 예상 시 이사님 동의 전에는 계속하지 않는다.
- 카드가 끝날 때마다 이사님께 결과·다음 카드·막힘을 중간보고한다.
- `autonomous-operations.md`의 `safe_auto` 카드는 별도 task/예약 worker가 사용자 재지시 없이
  착수할 수 있다. 제품 결정 gate와 승격은 계속 사용자 판단을 요구한다.

상태: `queued / in_progress / review / done / deferred / blocked`

## 0. 자율 실행 인프라

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| AUTO-01 | Arca sync 비활성·예약 CLI 모델/버전 실패 복구 | queued | disabled 원인, 지원 모델/runner, 재실행 receipt 또는 exact blocker |

## 현재 WIP

| ID | 작업 | 상태 | 담당 | 완료조건 |
|---|---|---|---|---|
| ARCA-DAY-01 | 오늘 Arca 게시글 한 건 완결 | in_progress | 별도 Codex task `Arca 오늘 1건` | fresh login/gate/lease부터 Git push까지 terminal receipt, 또는 정확한 gate blocker |

첫 체크포인트는 시작 후 10분이다. 메인 대화는 사용자 창구와 우선순위 controller로 남고,
수집 실행은 별도 task가 맡는다. 일반 시간당 `factory-steward`는 우선순위 복구가 끝날 때까지
일시정지했다.

## 다음 실행 순서

| 순서 | ID | 이유 | 시작 조건 |
|---|---|---|---|
| 1 | AUTO-01 | 하루 0건 재발을 막는 예약·sync 복구 | `ARCA-DAY-01` terminal 뒤 |
| 2 | OPS-01→OPS-05 | 같은 시행착오와 장시간 무응답을 시간·실패 fingerprint로 차단 | AUTO-01 receipt 뒤 |
| 3 | LEG-01→LEG-06 | 레거시 분류와 신규/레거시 균형을 실제 terminal pilot로 검증 | 계측 최소 계약 뒤 |
| 4 | ZC-02b 검수→ZC-02c | ZCode가 아닌 Codex 제출물을 먼저 검수하고, 429 복구 뒤 실제 ZCode packet 실행 | bridge 단일 probe 성공 뒤 |
| 5 | PY-01→PY-06 | 새 노트북에서도 같은 실행 구조가 돌도록 표준화 | 수집 warm path를 깨지 않는 범위 |
| 6 | MX-01→MX-08 | RISU-like 연속성, Genome, 멀티버스 코어를 증거 기반으로 개발 | reviewed 수집 recipe 확보 뒤 |
| 7 | RPG-01→RPG-08 | Matrix 코어를 사용하는 RPG Maker형 Studio 구성 | Matrix 최소 schema/replay 뒤 |
| 8 | NOTE-03→NOTE-05 | handoff·주간 KPI·Notion 투영 유지 | Git 변경과 함께 계속 |
| 주말 | AWS-01 | AWS→미니PC/Telegram 운영 비용·구조 결정 | 2026-07-18 리마인드 뒤 사용자 결정 |

승인보드·Director Console 추가 기능, AWS actor ACK 경로의 추가 드릴다운, 멀티버스 후보의
즉시 구현은 위 큐를 밀어내지 않는다. 별도 blocker/idea 카드로 보존하고 해당 순서가 왔을 때
다룬다.

## ZCode 권한·분업

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| ZC-01 | 현 bridge 권한 제한 근거 감사 | done | 단일 writer·secret 경계와 실패 재현 기록 |
| ZC-02a | receipt 핵심 결과·usage salvage | done | 알 수 없는 후반 필드는 폐기하고 신뢰 필드·usage 보존 |
| ZC-02b | 입력 절대경로 오탐 최소 fixture | review | 별도 Codex 제출 `52d9f1f`의 diff·tests를 controller가 독립 검수; local ZCode 작업으로 계산 금지 |
| ZC-02c | bridge 단계·heartbeat 표시 | queued | 30초 heartbeat와 stage/elapsed/timeout 가시화 |
| ZC-03 | raw shell 대신 controller allowlist check 설계 | queued | 명령 문자열 없이 check ID만 허용하는 계약 |
| ZC-04 | 격리 폴더 read/grep 실험 | queued | repo·환경변수·절대경로 탈출이 불가능함을 테스트 |
| ZC-05 | exact-file edit 왕복 재검증 | queued | isolated commit + Codex diff review 통과 |
| ZC-06 | 신규 수집 controller 승격 조건 ADR | queued | worker 권한 확대와 별도 controller를 명확히 분리 |

### ZC-01 결과

- 모든 ZCode 도구는 bridge의 deny list로 명시적으로 꺼져 있다.
- 이유는 모델 성능 문제가 아니라 로그인·AWS lease·lifecycle·공유 NDJSON·push의
  단일 소유권과 credential 격리를 보장하기 위해서다.
- exact snapshot 분석과 exact-file 제안은 이미 허용된다.
- 문서/코드 4개 감사 패킷은 예시 절대경로 과잉 탐지로 2회 차단됐다.
- 문서 1개 패킷은 173.9초 뒤 6,526-token 결과를 반환했지만 초과 필드 때문에 receipt가 거절됐다.
- 이번 감사 ZCode 합계는 probe 포함 9,173 tokens다.
- 상세 시간과 운영 실패는 `../reviews/2026-07-14-zcode-permission-audit.md`에 기록했다.
- 결론: 당장은 권한을 넓히지 않는다. 입력 정제(ZC-02)와 controller 실행 check(ZC-03)를
  먼저 만들고, 통과한 유형만 ZCode에 배정한다.

### ZC-02a 결과

- 실제 응답은 초과 필드뿐 아니라 닫히지 않은 후반 배열도 포함했다.
- bridge는 완전한 필수 9개 필드가 먼저 확인될 때만 후반 확장부를 폐기한다.
- 실제 실패 로그에서 `completed`와 `6,526 tokens` usage를 추가 호출 없이 회수했다.
- 필수 필드 누락·중복·파손은 계속 차단하며 전체 보안 gate는 유지한다.
- 스킬 전체 31 tests, mirror/quick validation/compile 통과; `bf29cdb`, `be54957` push.
- 카드 소요 약 8분, 추가 ZCode 호출·토큰 0.

## 1. 레거시 분류

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| LEG-01 | 213 최신 후보 snapshot 재생성 | queued | 종류·SHA·선정근거가 결정적으로 재현 |
| LEG-02 | 원본 재해시 dry-run | queued | 원본 변경/누락/일치 분류 보고서 |
| LEG-03 | 현 parser 재실행 pilot 3종 | queued | character/module/preset 각 1개 비교 |
| LEG-04 | mtime 선정 99 family 재분류 | queued | 자동승격/명시검토 근거 분리 |
| LEG-05 | provenance join 최소 구현 | queued | 한 후보의 post/source 근거 연결 |
| LEG-06 | 레거시 한 건 RCC 종결 pilot | queued | lifecycle→Matrix→Git terminal |

## 4. 시간·시행착오 효율화

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| OPS-01 | stage event 계약 | queued (다음) | schema·fixture·validator |
| OPS-02 | append-only event writer | queued | atomic append와 secret/path 차단 테스트 |
| OPS-03 | 단건 주요 단계 계측 | queued | preflight/resolve/parse/review/Matrix/commit 시간 |
| OPS-04 | 실패 fingerprint | queued | 동일 실패의 중복 retry 감지 |
| OPS-05 | 단건 복기 리포트 | queued | 실제/대기/LLM 시간을 분리해 출력 |
| OPS-06 | warm-path SLA 3건 측정 | queued | 유형별 목표시간 현실성 검증 |

## 5. Python 표준화

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| PY-01 | import·entrypoint·dependency inventory | queued | 실행 파일과 요구 패키지 지도 |
| PY-02 | root pyproject 초안 | queued | 기존 도구를 깨지 않는 package/test 설정 |
| PY-03 | lock·전용 venv bootstrap | queued | 새 PC에서 동일 버전 설치 |
| PY-04 | Pydantic/FastAPI drift 제거 | queued | automation-settings import/test 통과 |
| PY-05 | 통합 test 명령 | queued | Matrix/crawler/parser/lifecycle 핵심 suite 1회 실행 |
| PY-06 | 기존 entrypoint compatibility shim | queued | 문서화된 기존 명령 유지 |

## 6. 로컬 Matrix·RISU 이후

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| MX-01 | Mirka local compile/replay | queued | 동일 입력 2회 byte/hash 일치 |
| MX-02 | component/composition 정본 경로 ADR | queued | Git 입력과 runtime 산출 분리 |
| MX-03 | one-command local runner | queued | validate→compile→replay→report |
| MX-04 | 시간·자산 사용 ledger | queued | 단계시간·component refs·budget·hash 기록 |
| MX-05 | RISU-like adapter spike | queued | lore trigger/persona/memory를 Matrix 계약으로 투영 |
| MX-06 | Scenario Genome spike | queued | 세계·인물·관계·갈등을 capability graph로 조립 |
| MX-07 | 두 방향 비교 playtest | queued | 같은 자산으로 RISU-like/Genome 체감 비교 |
| MX-08 | 선택 방향 v1 계약 | queued | 이사님 선택을 ADR·schema·fixture로 고정 |

## 7. RPG Maker형 Studio

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| RPG-01 | project-v1 최소 schema | queued | world/cast/state/chapter/scene exact refs |
| RPG-02 | Mirka 예제 project fixture | queued | schema 검증 통과 |
| RPG-03 | trigger-condition-effect reducer | queued | 순수 함수와 unit tests |
| RPG-04 | CLI 3턴 playtest/replay | queued | 같은 선택으로 같은 state/result |
| RPG-05 | catalog/component browser API | queued | read-only 검색·선택 |
| RPG-06 | text-first chapter/scene editor | queued | 폼/트리 저장·검증 |
| RPG-07 | RISU/JSON export | queued | provenance 포함 export fixture |
| RPG-08 | Godot adapter spike | queued | 한 project를 Godot 입력 JSON으로 변환 |

## 8. Notes 관리

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| NOTE-01 | 프로젝트 인덱스·inbox·roadmap | done | Notes Git push |
| NOTE-02 | 소형 작업 보드 | done | WIP 1·담당·완료조건 기록 |
| NOTE-03 | 현재 handoff 자동 갱신 후보 | queued | machine truth를 복제하지 않는 링크/요약 |
| NOTE-04 | 오래된 scenario 문서 stale 표식 | queued | 삭제 없이 최신 정본 포인터 추가 |
| NOTE-05 | 주간 완료/소요시간 review | queued | done 카드와 실제 시간 집계 |

## 2. AWS→미니PC

| ID | 작은 작업 | 상태 | 완료조건 |
|---|---|---|---|
| AWS-01 | 주말 방향 재검토 | deferred | 2026-07-18 10:00 KST 알림 후 MVP 착수 여부 결정 |
| AWS-02 | 현 AWS read-only snapshot 명세 | queued | 서비스·DB·request·secret 위치 목록 |
| AWS-03 | Telegram-only local MVP ADR | queued | 범위·rollback·7일 shadow 기준 |
