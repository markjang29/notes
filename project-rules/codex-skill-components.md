# Codex skill 구성요소와 실패 피드백 규칙

작성일: 2026-07-13 KST

## 목적

노트북을 교체하거나 Codex 세션이 새로 시작돼도 같은 작업을 같은 안전 기준으로 복원한다.
skill은 질문 답변용 설명서가 아니라, 요청이 trigger되었을 때 Codex가 실제로 따라야 하는
재현 가능한 작업 계약이다.

## 필수 구성요소

1. `SKILL.md` frontmatter
   - 짧은 skill 이름
   - 어떤 요청에서 자동 사용해야 하는지 모두 포함한 description
2. 완결 조건
   - 설치나 중간 산출물이 아니라 사용자가 원하는 terminal outcome을 명시
3. 단계별 gate
   - 선행 검증, 허용 조건, 중단 조건, 다음 단계 진입 조건
4. 결정적 helper script
   - 반복되는 설치, 진단, 상태 기록, API 호출은 script로 고정
5. 외부 상태 경계
   - Git/AWS/로컬/비밀 저장소 각각의 책임과 금지 데이터
6. 재개 상태
   - 실패 단계, 입력 ID, 증거, 마지막 명령, retry 조건, 사용자 행동 필요 여부
7. 검증
   - skill validator, script 구문 검사, dry-run/fixture, 실제 최소 실행 순서
8. UI metadata
   - `agents/openai.yaml`의 표시명, 설명, `$skill-name` 기본 prompt

## arca-collection 적용

`$arca-collection`의 terminal 범위:

```text
새 노트북 bootstrap
-> AWS 설정 sync / 장치 등록
-> 실제 Arca 로그인 검증 / QR 복구
-> lifecycle gate / 단일 장치 lease
-> 게시글 한 건 선정
-> 본문·직접 후속글 딥다이브
-> Proton/GDrive/Risu Realm 실제 브라우저 다운로드
-> bytes/SHA-256 / 승인 parser / 직접 검토
-> extracted/normalized/fragments/RPG 자산 승격
-> AWS 시나리오 가용성 검증
-> usable 또는 not_usable terminal 판정
-> lifecycle closure
-> 제한 staging / commit / push
-> lease release / 결과 보고
```

중간 단계만 성공한 상태를 skill 성공으로 보고하지 않는다.

## 실패 피드백의 장점

skill 실패는 일반 작업 실패보다 다음 피드백이 쉽다.

- 실패 위치가 단계명으로 고정된다.
- 동일 입력(post id, config version, request id)을 보존한다.
- 관찰 증거와 추측을 분리한다.
- 사용자만 할 수 있는 행동과 자동 재시도를 구분한다.
- 다음 Codex가 전체 문맥을 재구성하지 않고 실패 단계부터 재개한다.
- 반복 실패를 stage/error_class별로 집계해 skill 자체의 결함을 찾을 수 있다.

필수 실패 record:

```json
{
  "stage": "browser_download",
  "post_id": "...",
  "error_class": "host_password_required",
  "evidence": "...",
  "last_command": "...",
  "retry_condition": "...",
  "user_action_required": false,
  "resume_from_stage": "browser_download"
}
```

토큰, 쿠키, 세션, 비밀번호, 원본 응답 본문, 로컬 비밀 경로는 실패 record에 넣지 않는다.

## Codex/Claude 공용 skill 동기화

agent별 skill 본문을 따로 관리하지 않는다.

```text
.agents/skills/<skill>          단일 정본
.claude/skills/<skill>          Claude용 생성 mirror
~/.codex/skills/<skill>         Codex 전역 설치
~/.claude/skills/<skill>        Claude 전역 설치
agent-skills.lock.json          파일별 SHA-256 계약
```

수정자는 `.agents` 정본만 편집한다. 동기화 프로그램이 Claude repo mirror와 두 전역
설치를 갱신한다. pre-commit은 mirror와 lock을 재생성·stage하고, CI는 정본과 mirror가
다르면 실패한다. Claude와 Codex는 같은 완료 조건과 `arca-collection-failure-v1`을 사용해
서로의 실패 지점부터 재개한다.

공용 skill 명세에 반드시 포함할 것:

- 양쪽 agent에서 같은 trigger 의미
- 동일한 terminal outcome과 gate
- 도구 이름이 달라도 유지되는 행위 수준의 절차
- 공통 helper와 failure record schema
- 정본·mirror·전역 설치 위치
- sync/check 명령과 drift 차단 방식
- 제품별로 완화할 수 없는 보안·provenance 규칙

## 테스트 원칙

1. 구문·schema·skill validator를 먼저 통과한다.
2. 외부 변경 없는 fixture로 gate와 실패 record를 시험한다.
3. 실제 테스트는 한 게시글·한 장치·한 lease로 제한한다.
4. browser pending, AWS open request, Git push 전 단계는 terminal 성공이 아니다.
5. 실패 테스트 결과가 다음 실행에서 실제 resume 입력으로 사용되는지 확인한다.
