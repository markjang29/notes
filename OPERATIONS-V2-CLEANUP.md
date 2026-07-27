---
title: 운영체계 v2 볼륨 다이어트 조사표
date: 2026-07-27
status: approved-no-delete-preparation
authority: director
approved_at: 2026-07-27
---

# 운영체계 v2 볼륨 다이어트 조사표

> Director는 v2 공통 원칙과 무삭제 준비 단계만 승인했다. 이 문서는 정확한 전환·삭제안을 만들기 위한 분류표이며, 기존 파일 삭제·자격정보 교체·Git 이력 재작성은 아직 허용하지 않는다.

## 1. 조사 기준

- 조사 대상: Notes Git의 운영·조직·온보딩·Agent Mail·작업큐·체크포인트·보고·백업 문서
- 현재 규모: tracked 150개, 약 1.1MB
- 핵심 문제:
  - Telegram 봇·호스트·역할이 한 객체로 묶임
  - 여러 세대의 운영 규칙이 서로 다른 권한과 조직 구조를 주장
  - 프로젝트 상태가 Notes와 프로젝트 Git에 중복
  - 검증용 스키마와 rollout 문서가 실제 사용량보다 큼
  - 체크포인트·채팅 백업·리뷰 원문이 현재 트리에 누적
  - 사용자가 읽을 결정 카드와 직접 테스트 인벤토리가 없음

## 2. 보호 중인 기존 변경

아래는 조사 시작 전부터 있던 사용자 측 변경으로 간주하며 이번 작업에서 수정·삭제·스테이징하지 않는다.

| 경로 | 상태 | 처리 |
|---|---|---|
| `decisions/2026-07-12-scenario-repo-freeze.md` | modified | 사용자 변경 보존 |
| `projects/agent-ops/scheduled-codex-guardrails-2026-07-17.md` | untracked | 사용자 변경 보존 |

## 3. 목표 구조

승인 후 Notes의 운영 정본은 다음처럼 줄인다.

```text
OPERATING.md              공통 운영방침
ops/BOOT.md               세션이 읽는 최소 부팅 진입점
ops/registry.json         역할·실행자·저장소를 서로 분리한 레지스트리
ops/WORK-TEMPLATE.md      전환 중 사용할 프로젝트 발령장 형식
persona.md                Director의 현재 소통·판단 기준 한 개
decisions/                프로젝트 간 살아 있는 결정만
```

프로젝트 전문 규칙·현황·작업·테스트는 각 프로젝트 Git의 `README.md`, `STATUS.md`, `WORK.md`에 둔다.
전환 중에만 `ops/migration-v2-manifest.json`, `ops/SHADOW-PROBE.md`, `ops/WORK-TEMPLATE.md`를 두고, 프로젝트별 `WORK.md` 도입과 전환 검수 뒤 최소 운영방침에 병합하거나 삭제한다.

## 4. 우선순위별 분류

### P0 — 민감정보 대응 후 제거

| 대상 | 이유 | 제안 |
|---|---|---|
| `L0-agent-boot.md` | 실행자와 역할을 고정 연결하며 런타임 식별 정보 포함 | 현재 트리 제거, 관련 자격정보 교체 검토 |
| `onboarding.md` | 동일한 런타임 식별 정보와 구형 매니저 전관 규칙 포함 | `OPERATING.md`로 대체 후 제거 |
| `policy-reread-pending.md` | 구형 런타임 식별 정보·모델 규칙을 임시 메모로 보존 | 즉시 삭제 후보, 자격정보 교체 검토 |
| `chat-backups/` | 대화 원문·세션 맥락을 Git에 장기 보존 | 현재 트리 삭제, 필요 시 Git 밖의 제한된 백업으로 전환 |
| `memory/user-access-context.md` | 사용자 접근환경·런타임 정보의 장기 Git 보존 위험 | 필요한 비밀 교체 후 제거 |
| `setup/server/chat-log-backup.py` | route key·사용자명·경로·역할이 한 코드에 고정 | 런타임 설정으로 분리하고 권한성 key이면 교체 |

주의: 현재 파일 삭제만으로 Git 과거 이력의 민감정보는 사라지지 않는다. 먼저 해당 자격정보를 교체하고, 이력 재작성은 별도 승인 작업으로 분리한다.

이번 정규식 감사에서는 알려진 API 토큰·개인키 형식이 발견되지 않았다. 다만 Cokacdir route key 원문이 현행 트리 43곳에 중복된다. 호출 권한을 가진 값이면 먼저 재발급하고, 단순 경로 식별자여도 Git 밖 런타임 설정으로 옮긴다. Telegram chat ID·세션 UUID·머신 식별자·절대경로는 비밀로 단정할 수 없지만 장기 보존과 이식성에 불필요하므로 일반화하거나 제거한다.

### P1 — `OPERATING.md` 승인 후 통합 삭제

| 대상 | 흡수할 핵심 | 삭제 이유 |
|---|---|---|
| `agent-rules.md` | Git 안전, 범위 최소, 비밀 금지, 검증 | AWS 경로와 구형 다중 에이전트 규칙에 고정 |
| `org-structure.md` | Director 최종권한, 역할 분업 | Telegram 한 그룹·영구 봇 직책 전제 |
| `onboarding-new-lead-laptop.md` | 세션 시작 시 환경·저장소 확인 | Windows 실행기와 역할을 결합 |
| `principles/git-first-project-truth.md` | Git 정본, 보고는 투영 | `OPERATING.md` 1·6절로 통합 가능 |
| `principles/context-budget.md` | 큰 원문 반복 금지, 변화 기반 보고 | 운영방침의 WIP·보고 규칙으로 통합 |
| `principles/audit-watchdog-foundation.md` | 완료 주장 실측, dirty tree 점검 | 특정 봇·스케줄·고정 경로에 묶임 |
| `project-rules/notion-reporting.md` | 보고가 정본을 승격하지 않음 | 보고 채널 일반 규칙으로 통합 |
| `work-queue.md` | 활성 작업·결정 대기만 표시 | 구형 매니저 전관과 프로젝트 상태 중복 |
| `work-archive.md` | 필요한 과거는 Git 이력 | archive 자체가 볼륨 다이어트와 충돌 |
| `change-deployment-checklist-template.md` | 고위험 변경 검수 | 과도한 고정 체크리스트를 작업 계약으로 대체 |

### P1 — Agent Mail 복잡성 제거

`projects/agent-ops/`의 현재 17개 파일은 역할과 실행자를 다시 결합하고, 실제 운영보다 복잡한 메일·후보·rollout 상태를 유지한다.

| 대상 | 판정 |
|---|---|
| `projects/agent-ops/README.md` | `OPERATING.md`로 대체 후 삭제 |
| `projects/agent-ops/actors.json` | 역할·실행자·저장소를 분리한 `ops/registry.json`으로 재작성 후 삭제 |
| `projects/agent-ops/mail-v1.schema.json` | 삭제 후보 |
| `projects/agent-ops/mail-v2.schema.json` | 최소 작업 계약으로 대체 후 삭제 |
| `projects/agent-ops/telegram-intake-v1.schema.json` | Telegram 전용 정본화를 일반 의도 기록으로 대체 후 삭제 |
| `projects/agent-ops/idea-candidate-v1.schema.json` | 프로젝트별 후보 상태로 대체 후 삭제 |
| `projects/agent-ops/cokacdir-boot-v1.md` | 구형, 삭제 후보 |
| `projects/agent-ops/cokacdir-boot-v2.md` | 새 단일 부팅 요약으로 대체 후 삭제 |
| `projects/agent-ops/identity-probe.md` | 영구 actor 검증 모델 폐기와 함께 삭제 |
| `projects/agent-ops/legacy-relay-v1.md` | legacy bridge 폐기 시 삭제 |
| `projects/agent-ops/overnight-ideation-v1.md` | 자동 야간 작업 기본 중지, 필요 시 작업별 허가로 대체 |
| `projects/agent-ops/shared-git-access.md` | 역할 기반 범위 권한으로 대체 |
| `projects/agent-ops/token-budget-routing-v1.md` | 핵심 예산 원칙만 `OPERATING.md`에 통합 |
| `projects/agent-ops/deployments/` | 당시 배포 증거, Git 이력만 남기고 삭제 |
| `projects/agent-ops/holds/` | Director의 중지 명령은 임의 삭제하지 않고 대상 프로젝트에 이관한 뒤 삭제 |
| `projects/agent-ops/scheduled-codex-guardrails-2026-07-17.md` | 기존 untracked 사용자 파일. 자동 스케줄 정책 결정 후 별도 처리 |

### P2 — 프로젝트 저장소로 이동 후 Notes에서 삭제

| 대상 | 이동 목적지 |
|---|---|
| `principles/scenario-team-purpose.md` | scenario 프로젝트의 현행 원칙 |
| `principles/scenario-resources.md` | scenario 프로젝트의 수집·출처 안내 |
| `project-rules/scenario-autopoietic-narrative-system.md` | scenario에서 현행 여부 판정 후 통합 또는 폐기 |
| `projects/scenario/` | scenario Git의 README·STATUS·decisions로 통합 |
| `memory/arca-collector-handoff.md` | scenario/Arca 파이프라인 인계 |
| `memory/scenario-asset-pipeline*.md` | scenario의 provenance·파이프라인 문서 |
| RPG 관련 `meetings/` | rpg_game 결정의 근거로 필요한 부분만 이동 |
| RPG 관련 `decisions/` | rpg_game 정본에 없는 현행 결정만 이동 |
| autotrader 관련 `decisions/` | autotrader 정본에 없는 현행 결정만 이동 |
| `project-rules/codex-skill-components.md` | 실제 skill/plugin 정본으로 이동하거나 삭제 |
| `setup/server/`, `setup/windows/` | 실행 중 스케줄·출력 위치를 먼저 확인하고, 살아 있는 배포·복구 도구만 비밀 없는 별도 ops 위치로 이동 |

복사하지 않는다. 목적지에 이미 같은 결정이 있으면 Notes 파일은 삭제하고 기존 정본을 가리킨다.

### P2 — 하나로 합친 뒤 중복 삭제

| 대상 | 처리 |
|---|---|
| `persona.md` + `personas/markjang29.md` | 현재 사용자 판단·소통 기준 한 파일로 통합 |
| `principles/ai-dev-신념.md` | 핵심인 의도부채·검증 대기·재사용 원칙만 `OPERATING.md` 또는 `persona.md`에 축약 |
| `principles/README.md`, `principles/references.md` | 실제 남은 파일 기준으로 삭제 또는 최소 인덱스화 |
| `decisions/README.md`, `ADR-template.md` | 프로젝트 간 결정이 실제 남을 때만 최소형 유지 |

### P3 — 현재 트리에서 삭제하고 Git 이력으로만 보존

| 대상 | 이유 |
|---|---|
| `checkpoints/` | RPG의 열린 Git 정본 공백만 RPG `STATUS.md`로 옮긴 뒤 삭제. 나머지는 2026년 7월 세션·장애 복구 당시 상태 |
| `.reviews/` | 과거 병렬 검토 원문, 현재 프로젝트 정본과 중복 |
| `.tool-results/` | 일회성 도구 출력 |
| `emergency-manager.md` | 종료된 장애 기록 |
| `manager-survival-fixes-applied.md` | 당시 완료 보고 |
| `manager-survival-implementation-8d.md` | 구형 매니저 중심 인프라 보고 |
| `healthcheck-deployment-checklist.md` | 완료·중단된 도입 체크리스트 |
| 루트의 2026-06-25 서버·샌드박스 세팅 문서 | 현행 환경 검증 없이 사용하기 위험한 역사 기록 |

## 5. 삭제 전 확인해야 할 의존성

- AWS Cokacdir 부팅 지시가 `L0-agent-boot.md`, `onboarding.md`, `org-structure.md`, `actors.json`을 참조한다.
- Windows 설치 스크립트와 온보딩 프롬프트가 `agent-rules.md`를 참조한다.
- Scenario 자동운영 문서가 Agent Mail README와 구형 상태명을 참조한다.
- 현재 Agent Mail 스킬과 Scenario 자동화가 `actors.json`과 Mail 스키마를 실제 입력으로 사용한다.
- 체크포인트·결정 문서의 역사적 링크는 삭제 후 Git 현재 트리에서는 깨진다. 이는 허용하되, 현행 문서에서는 삭제 대상 링크를 남기지 않는다.
- 실제 런타임 지시를 v2로 교체하기 전에는 구형 부팅 문서를 먼저 삭제하지 않는다.
- AWS·Windows·ZCode에서 새 레지스트리를 읽는 무변경 시험이 모두 통과하기 전에는 기존 스키마를 삭제하지 않는다.
- 표준 Markdown 내부 링크 6개는 현재 정상이나 대부분의 참조는 검사하기 어려운 일반 텍스트 경로다. 이미 없는 `tool-inventory.md`, `autotrader.md`, `rpg_game.md`, `CLAUDE.md`와 구형 healthcheck 경로가 있으므로 전환 뒤 전체 텍스트 참조를 다시 검사한다.

### Matrix 정본 미결

- `matrix-work`는 `matrix.git`을 가리키며 로컬 `main`이 원격보다 15커밋 뒤다.
- `matrix-candidate`는 별도 `matrix-living-drama.git`을 가리키며 runtime 미추적 디렉터리가 있다.
- Notes 정리와 별개로 두 저장소의 목적·이력·산출물을 비교해 정본 하나를 먼저 정한다. 결정 전에는 병합·삭제·미추적 파일 정리를 하지 않는다.

## 6. 권장 실행 단계

### A. 현재 단계 — 초안

- `OPERATING.md`와 이 조사표 작성
- 기존 dirty 파일 보호
- 링크·민감정보·중복 검증
- 삭제 없음

### B. 이번 Director 결정

- v2 공통 원칙 승인·수정
- 무삭제 준비 단계 승인 여부

### C. 무삭제 준비

- 모든 관련 저장소 원격 상태와 dirty tree 재확인
- 보호 태그는 dirty·untracked 변경을 담지 못하므로, 기존 사용자 변경은 대상과 diff를 확인한 뒤 승인된 브랜치·커밋·patch 중 하나로 별도 보존
- 정리 전 remote tag 또는 보호 브랜치 생성
- `ops/registry.json` 초안과 최소 부팅 규칙 작성
- AWS·Windows·ZCode의 포인터 전환 무변경 시험
- 실제 이동·삭제 대상의 정확한 diff와 복구 방법 작성
- 삭제·자격정보 교체 없음

현재 준비 증거:

- `pre-ops-v2-head-20260727`: 정리 전 clean `HEAD` 보호 태그
- `pre-ops-v2-working-20260727`: 기존 사용자 변경과 승인된 v2 초안을 담은 별도 synthetic commit 보호 태그
- 검증된 로컬 Git bundle: 두 태그와 전체 도달 이력을 포함하며 Notes 작업트리 밖에 보존
- `codex/ops-v2-prep`: v2 준비 파일만 담은 원격 공유 브랜치. 기존 사용자 dirty 변경은 포함하지 않음
- `ops/migration-v2-manifest.json`: 기준 커밋의 tracked 150개를 중복·누락 없이 분류
- `ops/SHADOW-PROBE.md`: Windows·ZCode·AWS 무변경 시험과 실제 포인터 차단 조건

### D. 후속 Director 결정

- Matrix 정본
- 권한성 자격정보 교체와 Git 이력 재작성 범위
- 프로젝트별 이관안과 P0→P3 실제 삭제

### E. 승인 후 전환

- `ops/registry.json`과 최소 부팅 규칙 반영
- 필요한 프로젝트 전문 내용을 각 프로젝트 Git으로 이동
- 승인된 자격정보 교체
- P0→P1→P2→P3 순서로 작은 커밋에 나눠 삭제
- 각 단계마다 링크, 부팅, Git 상태 검증
- 사용자용 STATUS·결정 카드·테스트 패키지 형식 적용
- archive 폴더를 만들지 않음

### F. 시험 운영

- RPG 한 프로젝트에서 작업 1건을 v2 방식으로 수행
- 역할 부여→구현→검수→사용자 테스트→정본 반영 전 과정을 확인
- 통과 후 Matrix·Scenario에 확대

## 7. 이번 검토에서 Director가 정할 것

지금은 두 가지만 정한다.

1. `OPERATING.md`의 작업별 역할 임명, 영구 봇 직책 폐지, 무허가 야간 작업 기본 중지, 쉬운 4상태 보고를 회사 공통 원칙으로 승인할지
2. 무삭제 준비 단계만 승인할지: 기존 변경 보호, 보호 snapshot·tag, `ops/registry.json` 초안, AWS·Windows·ZCode 포인터 전환 무변경 시험, 정확한 삭제 diff 작성

아래 사항은 별도 조사 결과를 쉬운 결정 카드로 받은 뒤 정한다.

- `matrix.git`과 `matrix-living-drama.git` 중 Matrix 정본
- 실제 권한성 key의 교체 범위와 Git 이력 재작성 여부
- P0→P3 실제 삭제와 프로젝트 문서 이관
- 프로젝트별 살아 있는 hold·결정·WIP의 구체적 이관안
