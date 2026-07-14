---
title: Local-first Scenario Factory 로드맵
status: working-proposal
owner: 이사님
controller: Codex
last_reviewed: 2026-07-14
---

# Local-first Scenario Factory 로드맵

실행은 [소형 작업 보드](tasks/README.md)에서 WIP 1로 관리한다. 이 문서는 방향과 전체
공수를 설명하고, 실제 진행 상태는 작업 보드만 갱신한다.

## 결론

현재 Python 코드를 버리고 새로 만드는 것은 권장하지 않는다. 순수 로컬 Matrix 코어는
이미 동작하므로 이를 중심에 두고, AWS의 요청·설정·봇 제어면만 Windows 미니 PC의
`FastAPI + SQLite + 단일 worker` Hub로 단계적으로 옮긴다. Telegram은 상태 저장소가
아니라 휴대폰 입력·알림 어댑터로 사용한다.

## 1. 레거시 분류

2026-07-14 감사 기준:

- parser-backed 원본 602건
- 동일 SHA 중복 84건
- 최신 후보 213건, superseded 305건
- 최신 후보 중 이미 catalog에 있는 1건을 제외한 staging 212건
- 후보 종류: 캐릭터 43, 모듈 117, 프리셋 53

602건을 전부 수작업 딥다이브하지 않는다. 아래 축으로 기계 분류한 뒤 최신·원본·provenance가
확인된 한 건만 RCC lifecycle에 넣는다.

| 축 | 값 |
|---|---|
| 원본 | present / missing / hash-changed |
| provenance | recovered / pending / blocked |
| 버전 | selected-latest / superseded / ambiguous |
| 종류 | character / module / preset / composite |
| 처리 | primary / auxiliary / reference / rejected |
| Matrix 역할 | world / character / persona / module / narrative |
| 성숙도 | inventory / staged / reviewed / usable / quarantined |

할 일:

1. 현재 parser로 원본 재해시·재파싱하는 legacy preflight — 2~3 인일
2. provenance 복구 join 도구와 `candidate_availability` 생성 — 3~5 인일
3. mtime만으로 고른 99개 family를 명시적 검토 대상으로 재분류 — 1~2 인일
4. dry-run·atomic staging·테스트 추가 — 2~3 인일
5. module 6 / character 4 / preset 4 일일 균형으로 단건 실행

## 2. AWS → Windows 미니 PC

가능하다. Telegram Bot API long polling은 미니 PC가 바깥으로 연결하므로 집 공유기의
인바운드 포트를 열 필요가 없다. 휴대폰 웹은 미니 PC와 휴대폰에 private overlay VPN을
설치해 로컬 FastAPI 화면을 보는 방식이 가장 단순하다. 웹이 필요 없으면 Telegram 명령만으로
운영할 수 있다.

권장 Hub:

```text
Telegram / phone web / CLI
            |
      Scenario Hub API
       |            |
 SQLite state   single worker
       |            |
 lifecycle / Matrix / crawler / Git / LLM adapters
```

단계와 공수(숙련 Python 개발 1명 기준):

| 단계 | 결과 | 공수 |
|---|---|---:|
| A | AWS snapshot, 보안·배포 원천 정리 | 2~3 인일 |
| B | 고정 Python 환경, SQLite request/config/job schema | 3~5 인일 |
| C | 요청·설정 API, 상태 전이, 단일 worker | 8~12 인일 |
| D | Telegram 명령·휴대폰 private web | 4~6 인일 |
| E | Matrix API/UI·replay·catalog 연결 | 4~6 인일 |
| F | 그림자 운영·백업·AWS 종료 | 3~5 인일 |

로컬 control plane + Matrix 동등 기능은 총 21~32 인일이다. 먼저 Telegram 상태/요청만
옮기는 MVP는 약 7~10 인일로 줄일 수 있다. AWS는 7일 이상 read-only fallback으로 남긴 뒤
종료한다.

전환 필수 조건:

- 요청 상태를 JSON 파일이 아니라 SQLite transaction으로 전이
- secret을 프로세스 명령행·Git·URL query에 두지 않음
- 기존 Telegram bot token은 cutover 때 회전
- SQLite 온라인 백업 + 암호화된 외부 백업
- 미니 PC 자동 시작·재시작·UPS 또는 정전 복구

## 3. 신규 수집과 ZCode

현 ZCode bridge에는 브라우저·로그인·shell·shared NDJSON·lifecycle·push 권한이 없으므로
신규 한 건 전체를 일임할 수 없다. 이 제한은 중복 실행과 credential 노출을 막기 위한 것이다.

| ZCode에 맡김 | Codex가 유지 |
|---|---|
| 고정된 본문/파서 JSON 요약 | 로그인·QR·쿠키 |
| 중복·버전·schema 기계 검수 | 게시글 최종 선정 |
| normalized/recipe 초안 | 다운로드·해시·CAS·실제 parser |
| Matrix capsule 후보 분류 | lifecycle·공유 NDJSON·승격 |
| 제한 파일 patch 제안 | 의미 검수·통합·push |

단기 목표는 “Codex가 입력을 확보한 뒤 ZCode가 해석·초안·기계검수를 한 packet으로 처리”다.
ZCode에 전체 일임하려면 별도 secure controller와 lease가 필요하며 5~8 인일 이상의 작업이다.

## 4. 한 건 시간과 효율

현재 기록 하한은 약 54분~5시간 42분이며, Mirka 건은 더 길다. lifecycle에 단계별 event가
없어 정확한 SLA를 계산할 수 없는 것이 먼저 고칠 문제다.

목표:

| 유형 | 현재 계획 범위 | 자동화 후 목표 |
|---|---:|---:|
| not-asset/reference | 10~30분 | 5~15분 |
| direct parser asset | 1.5~3시간 | 30~60분 |
| browser-hosted asset | 3~6시간 | 60~120분 |
| 신규 포맷/실패 | 6시간 이상 가능 | 90분에서 defect checkpoint 후 중단 |

35건/일은 대부분 빠른 terminal 분류일 때만 가능하다. full RCC 자산 35개/일 목표로 해석하지
않는다.

효율화 순서:

1. append-only stage event에 시작/종료/attempt/failure fingerprint 기록
2. 동일 fingerprint는 검증된 복구 recipe를 한 번만 실행
3. 브라우저 warm test와 host별 resolver preflight를 선정 전에 실행
4. `apply-result`를 다중 파일 사전검증·atomic transaction으로 변경
5. AWS 대신 로컬 Matrix를 기본 검증으로 사용
6. 깊은 상태기계/서사 검증은 신규 유형 또는 표본에만 적용
7. ZCode 기계 검수는 여러 작은 호출이 아니라 단일 packet으로 묶기

## 5. Python 표준화와 코드 지도

비용은 크지 않다. 코드 지도는 이 문서와 프로젝트 인덱스로 이미 시작했다. 실제 문제는
Python이 아니라 환경·진입점·상태 저장소가 여러 개인 점이다.

실측:

- Python 74개를 포함한 도구 파일 81개, 약 17.6K줄
- Matrix tests 20/20 통과
- Windows 설치는 Pydantic 1.10/FastAPI 0.94
- generator 요구사항은 Pydantic 2.5+/FastAPI 0.110+라 import 실패
- root lock/고정 venv가 없고 bootstrap이 crawler 의존성만 설치

권장 표준:

```text
pyproject.toml + lock
src/scenario_hub/
  domain/          순수 상태·계약
  application/     command/query/job
  persistence/     SQLite migration/repository
  adapters/        arca, parser, matrix, telegram, git, llm
  api/             FastAPI routes/templates
  worker/          scheduler/outbox/runner
tests/
  unit/ contract/ integration/ e2e/
```

공수:

- 코드 맵·진입점 표: 0.5~1 인일
- `pyproject`·lock·고정 venv·CI: 2~4 인일
- 기존 진입점 shim과 패키지 이동: 5~10 인일
- 전체 서비스 통합은 AWS 이전 공수에 포함

## 6. Matrix 로컬 실행

이미 가능하다. `tools/matrix_factory`는 네트워크·LLM·DB 없이 동작하며 이 PC에서
20개 테스트가 모두 통과했다.

기본 검증:

1. reviewed/active/usable exact component만 admission
2. composition 계약·capability·fusion 검증
3. Git commit·seed·budget 고정 compile
4. 같은 입력으로 두 번 compile해 byte/hash 동일성 확인
5. LLM 창작 품질은 별도 sample playtest

따라서 매 자산마다 AWS 팀장에게 장시간 서사 검증을 요청할 필요가 없다. 신규 parser,
복잡한 interactive state, 고가치 대표 자산, 무작위 10% 표본만 깊은 검증으로 올리는 것이
효율적이다.

## 7. RPG Maker형 도구

처음부터 drag/drop 게임 엔진을 만들지 않는다. JSON 계약과 폼·트리 기반 text-first
Studio를 만들고, reducer와 replay가 안정된 뒤 시각 편집기를 붙인다.

모듈:

1. catalog/component browser
2. world/fusion composer
3. character/persona casting
4. chapter/scene/narrative blueprint
5. typed variable·flag·objective editor
6. trigger → condition → effect event reducer
7. deterministic playtest/replay
8. RISU/JSON export, 후속 Godot adapter

개발 단위마다 `입력 계약 + 출력 계약 + fixture + unit test + 1개 playtest`를 완료조건으로 둔다.

| 스프린트 | 범위 | 공수 |
|---|---|---:|
| 0 | Hub/프로젝트 모델/고정 환경 | 5~8 인일 |
| 1 | catalog + world/character/persona composer | 7~10 인일 |
| 2 | narrative/chapter/scene + event reducer | 8~12 인일 |
| 3 | playtest/replay/feedback | 6~9 인일 |
| 4 | RISU/JSON export + Godot adapter | 6~10 인일 |
| 5 | UI/운영/백업/문서 | 5~8 인일 |

text-first Studio 전체는 37~57 인일, drag/drop graph editor는 추가 8~15 인일이다.

역할:

- 이사님: 제품 우선순위·체감 승인
- Codex: controller, 아키텍처·통합·최종 검수
- ZCode: schema migration, fixture, 반복 테스트, 제한 patch
- 시나리오 역할: 세계/캐릭터/서사 acceptance와 sample playtest
- RPG 역할: event/reducer/export/Godot acceptance

## 8. Notes 관리

기존 자료는 충분하지만 단일 최신 인덱스가 없었다. `work-queue.md` 안에서도 freeze 해제와
FREEZE가 동시에 적혀 있고, 오래 끝난 요청이 현재 작업처럼 남아 있었다.

이번에 `notes/projects/scenario/`를 사람 정본으로 만들었다. 앞으로 Notes에는 질문·결정·
우선순위만 두고, 실행 수치와 lifecycle은 scenario repo의 machine truth를 링크한다.

## 실행 백로그

### Now

- [ ] Mirka 한 건을 비차단 품질 메모와 함께 종결하고 로컬 Matrix replay까지 완료
- [ ] stage event·attempt·duration·failure fingerprint 계약 추가
- [ ] root `pyproject`/lock/전용 venv로 Pydantic drift 제거
- [ ] legacy preflight: 원본 재해시·현 parser 재실행·candidate snapshot
- [x] 질문 인박스·현재 체크포인트·로드맵 정본 생성

### Next

- [ ] Scenario Hub SQLite schema와 request state transition vertical slice
- [ ] Telegram long-polling `/status /request /approve /pause /resume` MVP
- [ ] Matrix validate/compile/replay API와 local UI
- [ ] 기존 AWS를 dual-read하는 그림자 운영

### Later

- [ ] Telegram dispatcher cutover와 phone private web
- [ ] AWS read-only 보존 후 8003/8005/8006 종료
- [ ] RPG Studio text-first vertical slices
- [ ] Godot export adapter와 시각 graph editor

## 다음 결정이 필요한 것

1. AWS를 유지한 채 로컬 Matrix만 먼저 쓸지, 미니 PC Hub MVP까지 바로 시작할지
2. RPG Studio를 수집 효율화보다 먼저 시작할지
3. deep AWS/LLM 검증 표본 비율을 10%로 둘지

권장 기본값은 **로컬 Matrix 즉시 → 수집 계측/표준화 → Hub MVP → RPG Studio**다.
