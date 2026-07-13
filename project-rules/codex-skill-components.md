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
-> lifecycle availability_testing 잠금 / AWS gate=false 보고
-> usable 또는 not_usable terminal 판정
-> lifecycle closure
-> 제한 staging / commit / push
-> lease release / 결과 보고
```

중간 단계만 성공한 상태를 skill 성공으로 보고하지 않는다.
가용성 요청을 등록했는데 해당 asset의 lifecycle 행이 없으면 열린 게이트로 간주하지
않고, `availability_testing` 행을 생성해 다음 게시글을 차단한 뒤 판정을 기다린다.

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

## Windows 브라우저 런타임 복구 구성요소

브라우저가 페이지를 열기 전 `failed to write kernel assets`와 Windows `os error 3`으로
실패하면 대상 사이트 장애가 아니라 `node_repl` sandbox 초기화 장애로 분류한다.

- 정본 skill의 `repair_node_repl_sandbox.ps1`가 `~/.codex/config.toml`의
  `[mcp_servers.node_repl]`에 `args = ["--disable-sandbox"]`를 멱등 적용한다.
- 설정 적용 뒤 공식 browser transport를 다시 시도한다. transport만 닫혔고 Codex 앱의
  computer-use pipe가 살아 있으면 `browser_rpc_client.py`가 현재 runtime/plugin/pipe와
  rollout의 session/turn을 매번 동적으로 찾아 smoke를 수행한다.
- 공식 transport와 동적 복구가 모두 실패할 때만 Codex task/app을 재시작하고 같은
  게시글의 browser documentation/navigation부터 재개한다.
- 임시 복구 코드에 session id, turn id, runtime hash, cookie, token을 저장하지 않는다.
- 복구 뒤에도 실제 브라우저 클릭과 로컬 파일 존재 확인이라는 download gate는 유지한다.

## live 링크 재대조와 Proton 저장 복구

외부 host를 열기 직전에 Arca 루트 본문을 live로 다시 받아 캐시 링크와 비교한다. 캐시된
Proton 주소가 422/폐기 상태이고 live 본문에 다른 주소가 있으면 브라우저 장애가 아니라
`stale_source_link`다. 새 주소로 resolution evidence를 교체하고 같은 게시글을 계속한다.

Proton 단일 파일은 첫 다운로드 버튼 뒤의 `다운로드` 또는 `스캔 및 다운로드`까지 눌러야
한다. 대용량 공개 폴더는 행 클릭이 시각적 focus에 그치면서 폴더 전체 ZIP을 내려줄 수 있고,
브라우저 Blob을 다시 읽으면 임시 파일 핸들이 먼저 사라질 수 있다. 그러므로 브라우저의 실제
다운로드 경로를 격리된 staging으로 지정하고 `.crdownload`가 사라진 안정 파일을 기다린다.
결과가 폴더 ZIP이면 중앙 디렉터리와 CRC를 검증한 뒤 요청한 정확한 파일명 한 개만 추출한다.
최종 bytes와 SHA-256 검증은 생략하지 않는다.

2026-07-13 post `176729619` 실측:

- stale Proton `S5H9QGGA3C` → live `4V1MPJKKK0` 교체 감지
- `무직전생Alternate V1.6 (1).charx`, 308,166,666 bytes 회수
- 동적 browser smoke와 Proton inspect-only 스크립트 통과
- CHARX parser v1의 혼합 엔트리 과삭제 발견: 이미지 태그 한 줄 때문에 긴 캐릭터 설정
  전체를 버리던 조건을 v2에서 전용/짧은 이미지 명령만 제외하도록 수정
- RCC-110558063 회귀 결과 유지: lorebook 49 retained / 12 omitted

2026-07-13 post `176735321` 추가 실측:

- Proton 폴더 ZIP 2,753,561,421 bytes 완결 후 정확한 v2.1 CHARX 304,012,947 bytes 추출
- 메모리 Blob 재복사는 1,935,671,296 bytes에서 임시 핸들 소실로 손상됨을 CRC로 식별
- Risu Realm의 고정 `png-v3` 추정은 type 30 카드에서 403; character page가 명시한
  `charx-v3` 엔드포인트를 재해석해 1,872,605 bytes 원본 회수
- Realm resolver는 포맷 거부 시 character page의 현재 v3 엔드포인트를 읽고 같은 ID만 재시도
- 봇 114개 프래그먼트 승격, 4,966개 미디어 모듈은 parser-backed companion으로만 보존

## AWS accepted 정체 복구 구성요소

approval-board의 `accepted`는 claim 잠금만 획득한 상태이며 실행 성공이 아니다. scenario
요청에 result가 없으면 라우터가 휴면 팀장 프로세스를 실제로 시작했는지 확인한다.

- scenario freeze는 2026-07-12 해제 상태이므로 과거 freeze 프롬프트를 재사용하지 않는다.
- 휴면 세션에 `--message`만 보내지 않고 scenario bot 설정 key로 one-shot을 예약한다.
- 프로세스 또는 schedule history 생성만으로 성공 처리하지 않는다. 요청 API가 `running`
  또는 terminal result를 반환해야 실제 진행으로 인정한다.
- absolute one-shot이 예정 시각을 넘기면 `--cron-list`와 기존 scenario 프로세스의 자식
  generator를 함께 본다. generator가 살아 있을 때는 중단하지 않는다. 자식 종료와 결과
  커밋 영속화를 확인한 뒤에만 stale 세션을 종료하고 overdue one-shot 기동을 확인한다.
- 교정 요청이 여러 개 생기면 최종 요청은 terminal 결과로, 중간 요청은 superseded로
  manager 권한 API에서 정리해 `accepted` 잔류를 없앤다.
- 실행을 시작할 수 없으면 `accepted`에 방치하지 않고 `failed`와 재시도 근거를 쓴다.
- 원 요청 result가 terminal 판정을 갖기 전까지 lifecycle/AWS gate를 닫아 둔다.

post `176729619`에서 시나리오 완결 판정의 양방향 오검출도 확인했다. 플롯 요약의 `결말`
단어만 보고 본문 중간 절단을 usable로 판정하면 안 되고, 반대로 자연스러운 마지막 문장 뒤에
`◆`/`★` 런타임 마커가 있거나 `결말` 단어가 없다는 이유로 not_usable 처리해서도 안 된다.
실제 이야기 본문의 마지막 산문 문장과 종결부호를 hard gate로 쓰고, 결말 키워드는 진단값으로만
사용한다.

## 단건 선정 즉시 lifecycle 잠금

가용성 요청 시점까지 기다리지 않고 root post를 고른 직후 `start-post`로 gate를 닫는다.
다운로드·브라우저·파서 단계에서 막혀도 다음 스케줄이 다른 게시글을 고를 수 없어야 한다.
승격 asset id와 AWS request id가 정해지면 `bind-asset`으로 같은 행을
`availability_testing`에 전환하고, terminal 판정에서만 gate를 다시 연다.
