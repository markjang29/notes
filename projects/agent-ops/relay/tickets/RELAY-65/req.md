# RELAY-65 — handoff-contract v0-draft 스키마 등록 + 01→02 시범 전달 완료

- date: 2026-09-14
- actor: heav_lnx_codex_dev_1_bot (aws-codex-dev, role=code_reviewer, §6 문서기록)
- branch: `agent-ops/onboarding-draft-v0.1` (notes, 분기점=origin/main 4dce19e)
- 기준 문서: `projects/agent-ops/handoff-contract-01-04.md` (4필드 계약, 6f5a0a6에 도입 → 4dce19e에 존재 확인)
- 산출물 위치: `projects/agent-ops/handoff-contract/` (schemas 3종 + registry + pilot)

## 요구(재게시 13번 지시)

> 4필드 계약 기준으로 손본 v0-draft 스키마를 notes의 `agent-ops/onboarding-draft-v0.1` 브랜치에 실제
> 커밋하고, 시범 결과를 RELAY 티켓+commit 영수증으로 완료 처리해 보고해.

정정 조건: ①스키마는 v0-draft(정식 규격 등록 금지) ②시범은 01→02 SourceUnit 1건만 ③기준=handoff-contract-01-04.md(올라오기 전 임의 확정 금지) ④완료처리=Jira 티켓+commit 영수증.

---

## 01-근거 (evidence)

| kind | ref | 비고 |
|---|---|---|
| doc | `projects/agent-ops/handoff-contract-01-04.md` | 4필드 정의표+규칙 7항. 정본 6f5a0a6 도입, 4dce19e에 존재 확인. 이 내용 외 임의 확정 없음 |
| measurement | 스키마 자체검증 3종(09-14): ①`check_schema` 메타검증 3파일 전부 통과 ②4필드(evidence/remaining/blockers/next) required·순서(01→04)·패턴 검증 통과 ③4필드 포함 더미 unit 1건 실검증 통과 | 출력: `META-OK×3 / 4FIELD-REQUIRED-OK / 4FIELD-ORDER-OK / UNIT-VALID` |
| artifact | 시범 산출물(09-12): SourceUnit `U-27216ab7`, 봉투 `E-20260912T144922Z-f4e71b`, 영수증 `A-20260912T144922Z-844bbc`, result=`ack-commit` | ledger 1건, 이번 브랜치 `pilot/ledger/commit.jsonl`에 원문 커밋 |
| measurement | 3종 검증(09-12): schema_valid=true·signature_valid=true·checksum_match=true → ack-commit. 변조 반증: payload 1글자→nack, 서명 1니블→nack-signature | 시범은 1건 소진(재실행 없음) |

## 02-미완료 (remaining)

| 항목 | 현재 상태 | effort |
|---|---|---|
| RELAY-65 티켓+스키마+영수증을 브랜치에 커밋·push | 본 커밋(직후) | - |
| 실Jira(heavenlyiris-matrix.atlassian.net, 프로젝트 RELAY)에 RELAY-65 등록 | 미등록 — 접근수단 없음(jira/gh CLI·python jira 미설치, 본기기) | S(관제 경유) |
| 수신측 02(unit-02)의 실제 키 보유·역서명(수신측 서명) | 미실시 — 현재 영수증은 수신측 검증+송신측 HMAC만. unit-02-prod 키 미발급 상태 | M |
| unit-secret rotate 정책 | 미확정(시범 open_question으로 명시) | M |
| 피드백 반영 후 v0.1→v1.0 승격(정식 등록) | 대기 — 승인 전 터치 금지(정정조건①) | 이사님 결정 후 |

## 03-블로커 (blockers)

| 항목 | 해제조건 | 담당 | 기다리는 결정 |
|---|---|---|---|
| Atlassian 접근수단 부재 → RELAY-65를 실Jira에 못 만듦 | jira CLI 또는 Atlassian 토큰 지급 | 매니저 | 이사님이 토큰 발급/CLI 설치 승인 여부 |
| 그룹수신 단절(09-12 15:18:34 이후 그룹 0건, 09-13/14 그룹 0) — 관제방 판독 불가 | privacy mode Disable+그룹 재추가(관리자=creator 1인, 봇 자체 해결 불가) | 이사님 | 재추가 실행 시점 |
| 4필드 계약 문서가 아직 main에만 있고 브랜치 구조상 판본이 갈라질 여지 | 본 브랜치는 계약 문서를 수정하지 않음(참조만) — 승격 시 1곳에만 정의 | (없음) | (없음) |

## 04-다음 (next)

재개 지점: 마지막 검증된 event = 본 커밋(브랜치 push)·시범 영수증 1건(ack-commit, 09-12).

1. 수령자(매니저/controller)가 본 커밋 검수:
   `git -C ~/notes show <HEAD>:projects/agent-ops/handoff-contract/registry/schemas.json` → status=draft·version=0.1 확인(v0-draft 조건)
2. 4필드 반영 검증:
   `git -C ~/notes show <HEAD>:projects/agent-ops/handoff-contract/schemas/source-unit.schema.json | jq -c .required`
   → 판정: evidence·remaining·blockers·next 4필드가 required에 포함되어 있으면 pass
3. 영수증 대조:
   `cat projects/agent-ops/handoff-contract/pilot/ledger/commit.jsonl` → 1건(1줄)이고
   envelope_id=`E-20260912T144922Z-f4e71b`·ack_id=`A-20260912T144922Z-844bbc`·result=`ack-commit`이면 pass
4. 검수 후: Atlassian 접근수단 지급 시 실Jira에 RELAY-65 등록(본 티켓을 그대로 복제, 링크만 notes에 추가)

## 영수증 (commit receipt, ledger/commit.jsonl 1건 전문)

```json
{"ack_id": "A-20260912T144922Z-844bbc", "dst": "02", "envelope_id": "E-20260912T144922Z-f4e71b", "envelope_sha256": "f52c3e7ff81abccdd7c3a764bcc229df24a1d10752aeb1de15754d4bb0d4a9e4", "result": "ack-commit", "src": "01", "src_seq": 1, "ts": "2026-09-12T14:49:22Z", "unit": "U-27216ab7"}
```

## 키 위치 (규칙5: 본문 대신 위치만)

- unit-01-prod secret(32B): `projects/agent-ops/handoff-contract/pilot/keys/unit-01-prod.secret` (0600). 본문에 값 미기재.

## 규칙 준수 자가점검

- 규칙1(수령자 정체): 수령=매니저(@heav_lnx_bot, aws L0/CERT 완료 상대) ✔
- 규칙2(검증된 사실만): 추정 없음 — 전부 실측/커밋/파일 ✔ (estimate 필드 도입, 미사용)
- 규칙3(은닉 없음): 블로커 2건+불확정 1건 명시 ✔
- 규칙4(구체성): 04-다음에 명령·경로·판정기준 포함 ✔
- 규칙5(기밀 위치만): 시크릿 본문 미기재 ✔
- 규칙6(상태전이): verified/closed 판정은 controller 몫 — 본 티켓은 submitted 상태 ✔
- 01~04 순서·존재: 필수(스키마 required로 강제) ✔
