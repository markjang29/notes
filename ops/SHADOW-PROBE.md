---
title: 운영체계 v2 무변경 검증과 전환 준비
date: 2026-07-27
status: trust-anchor-prepared-final-aws-reprobe-pending
authority: OPERATING.md
---

# 운영체계 v2 무변경 검증과 전환 준비

## 한눈에 보는 결론

| 대상 | 현재 판정 | 실제 전환 |
|---|---|---|
| Windows Codex | 실제 `WORK.md` 없음, 역할·권한 없이 읽기 전용 | 차단 |
| Windows ZCode | 실제 `WORK.md` 없음, 역할·권한 없이 읽기 전용 | 차단 |
| AWS Cokacdir | 5+2 private baseline 캡처 완료, 고정 Git anchor 재검증 대기 | 차단 |
| 구형 파일·worktree | 삭제 전 목록과 보호 규칙만 준비 | 삭제 안 함 |

이번 단계는 코드·테스트·증거와 삭제 전 목록만 준비한다. 사용자 설치 skill, Cokacdir 설정,
서비스, 세션, 기존 dirty 작업, `main` 포인터는 변경하지 않는다.
`ops/registry.json`은 계속 `shadow-only`이며 실제 작업 권한을 만들지 않는다.

## 준비한 안전장치

### 역할과 WORK

- 역할과 실행기를 분리했다. 세션은 고정 직책을 갖지 않고 Director가 발령한 `WORK.md`로만
  역할을 얻는다.
- 실제 production CLI는 임의 로컬 registry 파일을 받지 않는다. 코드에 미리 고정한 Notes
  원격 ref와 full commit을 확인하고, 임시 bare Git 저장소에서 exact
  `100644 ops/registry.json` blob만 읽는다.
- 대상 저장소의 정확한 Git 최상위 `WORK.md`만 인정한다. 외부 파일, 하위 경로, symlink,
  Windows reparse와 비정규 파일은 차단한다.
- `base_commit`은 대상 저장소에 존재하는 것만으로 부족하다. canonical remote의 실제
  default-branch tip과 정확히 일치해야 한다.
- 8MiB 초과, 깊이 64 초과, duplicate JSON key, `NaN`·`Infinity`, 형식 손상,
  필드 누락, `task_id` 중복, 만료·충돌, 잘못된 reviewer와 self-review를 차단한다.
- 문서 앞 설명과 JSON 전체에서 알려진 credential 형식을 검사하고, 오류 출력에 원문 값을
  반사하지 않는다.
- shadow 상태에서는 계산 가능한 교집합을 증거로만 남긴다. 실제 `allowed`, read scope,
  write scope와 production authority는 모두 빈 값이다.

### AWS runtime

- private settings의 runtime bot은 7개다. 구형 registry 등록 대상 5개와 보존 대상 2개로
  분리하며, 등록 대상 chat scope 분포는 `3/2/2/2/1`, 총 10개다.
- actor→executor→route 대응과 actor별 chat scope fingerprint를 exact 비교한다.
- 검증기는 caller가 넘긴 settings 객체나 before/after hash를 믿지 않는다. 고정된 실제
  settings 파일을 regular file·owner·mode·inode/device에 결속해 직접 두 번 읽는다.
- private baseline에는 256-bit salt, scope fingerprint와 settings 원본 hash를 둔다.
  Windows private 파일은 `<user>/.codex/ops-v2-runtime-baseline.private.json`에 두고,
  현재 사용자·SYSTEM·Administrators만 접근하도록 상속 없는 ACL을 적용했다.
- Git에는 private baseline 대신 `ops/runtime-baseline-anchor.json`의 salted commitment만
  둔다. salt, settings hash, chat ID, username과 private fingerprint는 Git·일반 로그·공개
  receipt에 쓰지 않는다.
- mutation plan은 항상 비어 있다. 공개 판정은 baseline commitment, 파일 경로 결속,
  시험 중 무변경, `5/10/2`, mutation 0만 보고한다.

### skill 설치와 mirror

- `.agents/skills`가 정본이고 `.claude/skills`와 lock은 생성물이다.
- user target이 기존 관리 manifest가 없거나 설치 뒤 로컬에서 바뀌었으면 자동 교체를
  거부한다.
- 사용자 설치는 모든 target을 먼저 검사·stage한 뒤 한 transaction으로 교체한다.
  일부 실패 시 이미 바꾼 target과 manifest를 원상복구한다.
- symlink·junction·Windows reparse와 non-regular entry를 따라가지 않는다.
  `__pycache__`, `.DS_Store`처럼 보이는 추가 파일도 사용자 변경으로 감지한다.
- lock은 같은 디렉터리의 임시 파일을 원자 교체해 외부 hardlink·symlink inode를
  덮어쓰지 않는다.
- 실제 사용자 설치는 하지 않았다. 현재 Codex·Claude user target은 unmanaged이므로
  읽기 전용 preflight가 의도대로 교체를 거부한다.

## 실제 관측

### Windows

- Scenario의 Codex와 ZCode를 각각 실제 판정했다.
- 두 실행기 모두 exact `WORK.md`가 없어 `read-only / work-missing`으로 끝났다.
- 기존 dirty Scenario 작업 폴더는 수정하지 않았다.

### AWS

- SSH 읽기 전용 연결과 Cokacdir user service `active` 상태를 확인했다.
- 기존 settings 원본 hash가 앞선 같은 세션의 읽기 전용 관측과 일치하는 경우에만 private
  baseline을 캡처했다.
- settings 원문과 private baseline은 화면·Git·일반 로그에 출력하지 않았다.
- public anchor를 고정한 Notes Git object와 Scenario 실행 commit이 아직 확정 전이므로,
  이 문서에서는 최종 `shadow-valid` receipt를 주장하지 않는다.
- 최종 단계는 immutable Notes tag를 만든 뒤 AWS 임시 디렉터리에서 그 exact object와
  committed Scenario reader를 사용해 다시 검사하고, 서비스·settings 무변경 receipt를
  남기는 것이다.

## Git 보호 대상

- AWS Notes: 원격과 서로 다른 로컬 commit 1개, 기존 dirty log 1개
- AWS Autotrader: 원격 `main`보다 앞선 로컬 commit 2개, dirty 항목 7개
- AWS RPG: 원격 `main`과 commit은 같지만 미추적 아이디어·WIP 6개
- AWS Scenario: runtime DB 1개가 미추적이고 checkout의 remote ref가 실제 GitHub
  `main`보다 뒤에 있음
- AWS Matrix: working tree는 clean이지만 checkout의 remote ref가 실제 GitHub
  `main`보다 뒤에 있음
- AWS approval-board: 비정본 전환 branch에 dirty 항목 3개

전부 reset·checkout·clean·자동 삭제 금지다. 대상 프로젝트 정본과 대조해
보존·통합·폐기를 결정하기 전에는 cleanup에 포함하지 않는다.

## 볼륨 다이어트 준비

- Scenario worktree 49개, cache 제외 약 1.62GB
- clean이고 원격에 보존된 정리 후보 33개, 약 1.02GB
- dirty, local-only 또는 현재 작업 중인 보호 대상 16개, 약 0.60GB

정확한 증거는 `ops/worktree-cleanup-manifest.json`에 있다. 이 파일은 삭제 허가가 아니다.
실행 직전에 fetch, exact HEAD, dirty 상태, remote reachability, 사용 중인 process와 경로
결속을 다시 확인한 worktree만 `git worktree remove <resolved-path>`로 제거한다.
`--force`, branch 삭제와 raw recursive filesystem 삭제는 금지한다.

## rollback 증거

전환 전 Notes 상태는 `<user>/notes-snapshots/pre-ops-v2-20260727.bundle`에 보존했다.
`ops/evidence/pre-ops-v2-bundle-receipt.json`에는 파일 크기, SHA-256, 각 annotated
tag object·peeled commit과 `git bundle verify`의 complete-history 결과가 있다.
이 bundle과 receipt 검증이 실패하면 cutover를 시작하지 않는다.

## 최종 전환 전 남은 조건

1. public anchor를 포함한 Notes commit에 immutable 원격 tag를 만들고 Scenario reader가
   그 tag·commit을 코드로 고정하기
2. committed reader와 Git 밖 private baseline으로 AWS 최종 무변경 probe를 다시 실행하고
   비밀 없는 receipt 남기기
3. 기존 user skill을 유지할지, 백업 후 managed target으로 adoption할지 Director 결정
4. 프로젝트별 `WORK.md`를 실제 배치하기 전 현재 WIP·hold와 대조하고 Director 발령 받기
5. Matrix 정본 결정
6. Trader hold가 executor와 repository 중 어디에 적용되는지 Director 결정
7. worktree 33개 실제 삭제 여부를 별도 승인받기

이 조건과 별도 승인이 끝나기 전에는 runtime 포인터 저장, 서비스 재시작, `main` 병합,
구형 파일 또는 worktree 삭제를 하지 않는다.
