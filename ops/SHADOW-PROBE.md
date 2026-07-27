---
title: 운영체계 v2 무변경 전환 시험
date: 2026-07-27
status: completed-no-write
authority: OPERATING.md
---

# 운영체계 v2 무변경 전환 시험

## 결론

| 환경 | shadow 판정 | 실제 전환 |
|---|---|---|
| Windows Codex | PASS | 차단 |
| Windows ZCode | PASS — `WORK.md`가 없어 의도대로 읽기 전용 | 차단 |
| AWS Cokacdir | 등록 경로 5/5, chat scope 10개 alias 해석 PASS | 차단 |

시험 중 파일·서비스·세션 설정을 수정하지 않았고 서비스 중지·재시작도 하지 않았다.
`ops/registry.json`은 계속 `shadow-only`이며 실제 작업 권한을 만들지 않는다.

## 공통 검증

- 역할 6개, 환경 3개, 실행자 7개, 저장소 7개 JSON 구문·ID 유일성 PASS
- executor 객체에 role, grants, project, capability 같은 직책 의미 필드 없음
- 구형 agent 7개와 transition alias 7개가 중복 없이 대응
- 역할 부여 필드가 `OPERATING.md`, `ops/BOOT.md`, registry에서 일치
- Agent Mail 민감정보 검사기로 registry와 migration manifest 모두 PASS
- 구형 Agent Mail baseline: registry 검사 PASS, 단위 테스트 23/23, boot installer 테스트 7/7 PASS
- 구형 검사기에 새 registry를 직접 넣었을 때 `agent-registry-v1` 불일치로 거부됨. 예상된 결과이며 dual-reader가 필요함

## Windows

### Codex

- 새 registry 파싱과 불변식 검사 PASS
- `role.grants ∩ environment.supports ∩ WORK.allowed`, 금지 우선 규칙 PASS
- 현재 주요 프로젝트에는 `WORK.md`가 없어 새 역할을 추정하지 않고 읽기 전용으로 종결

### ZCode

- `windows-zcode` legacy alias가 동명의 executor로 해석됨
- `OPERATING.md`와 `ops/BOOT.md` 입력 해석 PASS
- 현재 workspace에는 v2 포인터와 `WORK.md`가 없으므로 실제 소비자는 아님
- 기존 진행 작업이 있으므로 workspace나 설정을 건드리지 않음

### Windows 설치기

- `setup/windows/setup-windows.ps1`은 현재 PowerShell AST 오류 5개:
  - 48행: 지원되지 않는 redirection 해석
  - 98, 107, 109, 115행: 예상하지 않은 토큰
- dry-run 옵션도 없으므로 v2 포인터 변경 전에 설치기 자체를 먼저 고쳐야 함
- `setup/windows/setup-wsl.sh`는 shell 구문 PASS지만 구형 `agent-rules.md`만 소비함

## AWS

- Cokacdir 서비스는 시험 전후 active/running
- private settings의 runtime bot 7개 중 구형 registry 등록 대상은 5개, 총 chat scope는 10개
- 미등록 runtime bot 2개가 존재함
- 현 installer의 전체 dry-run은 미등록 bot 때문에 fail-closed
- 등록 5개만 메모리에서 선택한 shadow 시험은 5/5, 10 scope PASS
- settings 직렬화 결과는 시험 전후 동일하며 미등록 2개도 보존됨
- AWS Notes는 로컬 commit 1개와 원격 commit 1개가 갈라져 있고 기존 dirty 로그가 있으므로 reset·checkout·clean 금지
- v2 준비 파일은 `codex/ops-v2-prep` 브랜치의 공유 Git object로 push됐고 AWS의 원격 조회도 성공함
- 다만 기존 소비자는 `origin/main`만 읽고 AWS Notes는 이미 diverged·dirty 상태이므로 fetch·checkout 없이 새 object를 소비할 수 없음

## 실제 포인터 전환 전에 바꿀 소스

### Agent Mail 정본

- `scenario:.agents/skills/agent-mail/SKILL.md`
- `scenario:.agents/skills/agent-mail/references/agent-mail-protocol.md`
- `scenario:.agents/skills/agent-mail/scripts/agent_mail.py`
- `scenario:.agents/skills/agent-mail/scripts/apply_cokacdir_boot.py`
- `scenario:.agents/skills/agent-mail/scripts/test_agent_mail.py`
- `scenario:.agents/skills/agent-mail/scripts/test_apply_cokacdir_boot.py`
- `scenario:agent-skills.lock.json`

정본 변경 후 `.claude`와 사용자 설치 mirror는 공식 sync 도구로만 갱신한다. 설치 mirror를 직접 편집하지 않는다.

### Windows 설치 포인터

- `setup/windows/setup-windows.ps1`
- `setup/windows/setup-wsl.sh`
- `setup/windows/README.md`
- `setup/windows/ONBOARDING-PROMPT.md`

### Scenario 소비자

- `scenario:tools/scenario-generator/backend/director_console/canonical.py`
- `scenario:tools/scenario-generator/backend/director_console/mail-v2.schema.json`
- `scenario:tools/scenario_automation/sync.py`

### AWS runtime

- `runtime:cokacdir/settings`의 등록된 5개 bot, 기존 10개 scope의 instruction만 변경 후보
- `runtime:cokacdir/ops-v2-map`을 private manifest로 신설 후보
- 미등록 2개 bot과 나머지 설정은 byte-for-byte 보존
- systemd unit 자체에는 포인터 변경이 필요 없음

### ZCode runtime

- `runtime:zcode/workspace/AGENTS.md`에는 역할이 없는 얇은 BOOT 포인터만 제안
- 실제 권한은 대상 저장소의 `AGENTS.md`와 `WORK.md`에서만 발생

## dual-reader 필수 동작

```text
private runtime binding
  → legacy actor ID
  → transition.legacy_actor_aliases
  → executor_ref
  → target repository WORK.md role_id
  → role.grants ∩ environment.supports ∩ WORK.allowed
  → deny와 repository gate 적용
```

- bot 이름이나 legacy actor에서 역할을 상속하지 않음
- 등록된 5개 경로만 갱신하고 미등록 2개는 untouched
- 등록 대상 누락·중복은 실패
- dry-run에서 대상 수와 scope 수를 먼저 제시
- 서비스 실행 중에는 실제 설정 저장을 거부
- `WORK.md`가 없으면 항상 읽기 전용으로 종결

## 남은 차단 조건

1. AWS 작업트리를 건드리지 않고 v2 준비 commit을 안전하게 pin·소비할 방식 확정
2. AWS의 갈라진 Notes commit과 dirty 로그를 보존한 채 통합 방법 결정
3. dual-reader와 미등록 runtime bot 보존 테스트 구현
4. 프로젝트별 `WORK.md` 도입안 작성
5. Matrix 정본 결정
6. 기존 Trader hold가 executor·repository 중 어디에 적용되는지 Director 결정

이 차단 조건이 해소되고 별도 승인을 받기 전에는 포인터 저장, 서비스 재시작, 구형 파일 삭제를 하지 않는다.
