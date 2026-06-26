---
title: Codex 비판 리뷰 — 담당 봇 온보딩 규칙
date: 2026-06-26
target: /home/ubuntu/notes/onboarding.md
reviewer: Codex
scope:
  - /home/ubuntu/notes/onboarding.md
  - /home/ubuntu/notes/principles/ai-dev-신념.md
  - /home/ubuntu/notes/personas/markjang29.md
  - /home/ubuntu/notes/agent-rules.md
  - /home/ubuntu/notes/principles/context-budget.md
  - /home/ubuntu/notes/decisions/README.md
  - /home/ubuntu/notes/decisions/ADR-template.md
---

# 담당 봇 온보딩 규칙 비판 리뷰

## 1. 공통 원칙·persona·agent-rules와의 일관성, 충돌, 중복

### 문제 1-1. `agent-rules.md`와 `ai-dev-신념.md` 사이의 충돌 해소 규칙을 온보딩이 더 거칠게 덮어쓴다.

근거 구문:
- `onboarding.md`: "`project-rules/<프로젝트>.md` 또는 프로젝트 repo 내 CLAUDE.md. 공통 원칙(이 문서 + `principles/`) 위에 덮어쓰되, **충돌 시 공통 원칙이 상위**."
- `agent-rules.md`: "`루트 agent-rules.md=어떻게 / principles/ai-dev-신념.md=왜. 충돌 시 전자는 실행 절차, 후자는 판단 기준으로 해석.`"
- `ai-dev-신념.md`: "`충돌 시 agent-rules.md는 실행 절차로, 이 문서는 판단 기준으로 해석해 모순을 푼다.`"

비판:
온보딩은 "공통 원칙이 상위"라고만 하며 `agent-rules.md`와 `principles/ai-dev-신념.md`의 역할 분리, 즉 "실행 절차 vs 판단 기준"이라는 충돌 해소 방식을 보존하지 않는다. 특히 `onboarding.md`는 "이 문서 + `principles/`"를 공통 원칙으로 묶지만, `agent-rules.md`는 루트 운영 규칙이고 `principles/`는 판단 기준이다. 둘을 같은 계층의 "상위 원칙"으로 처리하면 실제 충돌 시 어떤 문장을 실행해야 하는지 애매해진다.

개선 방향:
상하관계를 단순히 "공통 원칙 상위"로 쓰지 말고, 최소한 다음 순서를 명시해야 한다: 안전·시크릿·데이터 손실 금지 같은 hard guardrail, 사용자 직접 지시, 프로젝트별 실행 규칙, 공용 실행 절차(`agent-rules.md`), 판단 기준(`principles/ai-dev-신념.md`). 또한 `agent-rules.md`와 `ai-dev-신념.md` 사이에서는 기존 문서의 "실행 절차/판단 기준" 해석 규칙을 그대로 재사용해야 한다.

### 문제 1-2. 프로젝트별 override에 대해 `agent-rules.md`와 `onboarding.md`가 서로 다른 뉘앙스를 가진다.

근거 구문:
- `agent-rules.md`: "`project-rules/` | 프로젝트별 실행규칙 (`agent-rules`의 override 포함)"
- `onboarding.md`: "`project-rules/<프로젝트>.md` 또는 프로젝트 repo 내 CLAUDE.md. 공통 원칙(이 문서 + `principles/`) 위에 덮어쓰되, **충돌 시 공통 원칙이 상위**."

비판:
`agent-rules.md`는 `project-rules/`가 "`agent-rules`의 override 포함"이라고 말한다. 반면 `onboarding.md`는 프로젝트별 규칙이 공통 원칙 위에 덮어쓰지만 충돌 시 공통 원칙이 상위라고 한다. 이 둘을 함께 읽으면 "프로젝트 규칙이 agent-rules를 override할 수 있다"와 "충돌 시 공통 원칙이 상위다"가 동시에 성립한다. 어느 항목이 override 가능한 실행 세부이고 어느 항목이 override 불가한 원칙인지 경계가 없다.

개선 방향:
프로젝트별 규칙이 덮어쓸 수 있는 항목을 구체화해야 한다. 예: 경로, 실행 명령, 테스트 명령, 배포 절차, 프로젝트별 금지 파일, repo별 commit/push 정책은 override 가능. 반대로 시크릿 금지, 사용자 승인 없는 원본 삭제 금지, 스택 미확정 발판 금지, ADR 필수 트리거는 override 불가. 현재 문장만으로는 담당 봇이 자기 프로젝트 편의에 따라 공통 규칙을 축소 해석할 수 있다.

### 문제 1-3. "행동 기본"은 persona와 중복되지만 예외 조건을 손실한다.

근거 구문:
- `onboarding.md`: "`개요/README 우선, 전체 파일 재독 금지.`"
- `onboarding.md`: "`pull → 작업 → 즉시 commit/push.`"
- `onboarding.md`: "`충분한 정보면 행동; 진짜 모호할 때만 확인(비대화형 채널).`"
- `personas/markjang29.md`: "`작은 작업은 필수 3개만 채워도 완성. 전부 채우기를 강제하지 않는다.`"
- `personas/markjang29.md`: "`장애(고위험) 복구가 §4 정지 프로토콜보다 우선`"
- `agent-rules.md`: "`다중 에이전트 협업: Windows 머신에 별도 에이전트가 같은 repo 공유. 작업 전 git pull, 작업 후 즉시 add/commit/push.`"

비판:
온보딩의 "행동 기본"은 `persona`와 `agent-rules`에서 이미 나온 운영 규칙을 축약해 반복한다. 축약 자체가 문제라기보다, 축약하면서 예외와 조건을 잃는다. 예를 들어 `pull → 작업 → 즉시 commit/push`는 notes 리뷰 파일 작성 같은 문서 산출에도 항상 적용되는지 불명확하고, `personas/markjang29.md`의 고위험 장애 예외, 작은 작업 완성 기준, 정지 프로토콜 예외 같은 조건은 온보딩의 짧은 문장에 반영되지 않는다. 담당 봇이 온보딩만 보고 움직이면 세부 예외를 누락할 수 있다.

개선 방향:
온보딩의 중복 요약은 "요약은 원문을 대체하지 않는다"는 문장과 원문 우선순위를 가져야 한다. 특히 행동 기본 항목은 `agent-rules.md`의 실행 규칙과 `personas/markjang29.md`의 예외를 링크하는 색인 역할에 그쳐야 한다. 현재처럼 압축된 운영 지침처럼 보이면 원문 대비 손실된 규칙이 실무 판단에 영향을 준다.

### 문제 1-4. "모든 프로젝트에 적용"과 "담당 봇" 범위가 섞여 있다.

근거 구문:
- `ai-dev-신념.md`: "`모든 프로젝트(autotrader · rpg_game 및 향후 전부)에 적용되는 포괄 원칙.`"
- `agent-rules.md`: "`모든 머신(Linux 서버 / Windows)의 에이전트가 공유하는 표준 운영 규칙이다.`"
- `onboarding.md`: "`프로젝트별 담당 봇(RPG, autotrader, 향후 추가)은 모두 같은 원칙 체계(사칙)를 이어받는다.`"

비판:
`ai-dev-신념.md`는 프로젝트 전체, `agent-rules.md`는 머신/에이전트 전체, `onboarding.md`는 프로젝트별 담당 봇을 대상으로 한다. 그러나 온보딩은 이 세 범위를 구분하지 않고 "사칙"으로 묶는다. 그 결과 프로젝트 담당 봇이 아닌 일회성 리뷰 에이전트, 구조 검증 에이전트, rescue 에이전트도 동일 온보딩 대상인지 불분명하다. 특히 `context-budget.md` §1-2는 서브에이전트 결과 파일 분리를 요구하는데, 온보딩은 "담당 봇" 중심이라 서브에이전트에 대한 최소 읽기 계약과 저장 계약을 별도로 정의하지 않는다.

개선 방향:
"상주 담당 봇", "일회성 서브에이전트", "검증/리뷰 에이전트", "복구 에이전트"를 분리해야 한다. 모든 에이전트가 동일한 5개 문서를 full read해야 하는지, 아니면 작업 계약에 따라 필요한 문서만 읽어도 되는지 구분하지 않으면 context-budget 원칙과 충돌한다.

## 2. "의무 읽기 5"의 누락·과잉, 실제 강제 가능성

### 문제 2-1. "의무 읽기 5"는 실제로 6개 이상의 파일을 요구하며, 번호 체계가 부정확하다.

근거 구문:
- `onboarding.md`: "`첫 세션 의무 읽기 (모든 담당 봇)`"
- `onboarding.md`: "`4. decisions/README.md + ADR-template.md — 결정을 ADR로 남기는 기준`"
- `onboarding.md`: "`5. principles/context-budget.md — 토큰/컨텍스트 예산 운영`"

비판:
제목과 체크 문구는 "의무 읽기 5"처럼 보이지만 4번은 두 파일이다. 따라서 실제 최소 읽기 대상은 `agent-rules.md`, `ai-dev-신념.md`, `markjang29.md`, `decisions/README.md`, `ADR-template.md`, `principles/context-budget.md`의 6개다. 이 불일치는 사소해 보이지만 온보딩 체크 자동화나 감사 기준을 만들 때 바로 문제가 된다. "5개 읽음"과 "ADR README와 템플릿 모두 읽음"은 다른 조건이다.

개선 방향:
체크 단위를 파일 단위로 바꾸거나, "5개 항목/6개 파일"이라고 명시해야 한다. 자동 검사를 염두에 둔다면 각 파일 경로를 별도 항목으로 분해해야 한다.

### 문제 2-2. 의무 읽기 대상에서 `project-rules/<프로젝트>.md`와 프로젝트 repo 내 `CLAUDE.md`가 빠져 있다.

근거 구문:
- `onboarding.md`: "`프로젝트별 특수성: project-rules/<프로젝트>.md 또는 프로젝트 repo 내 CLAUDE.md.`"
- `onboarding.md`: "`첫 세션 의무 읽기 (모든 담당 봇)`" 목록에는 `project-rules/<프로젝트>.md`나 repo 내 `CLAUDE.md`가 없다.

비판:
온보딩은 프로젝트별 특수성을 인정하지만, 첫 세션 의무 읽기 목록에는 프로젝트별 규칙 파일이 없다. 담당 봇이 "원칙 체계 읽음"을 인증한 뒤 실제 프로젝트 규칙을 읽지 않고 작업을 시작할 수 있다. 이는 프로젝트별 특수성을 온보딩 흐름 뒤쪽의 참고사항으로 밀어내며, 공통 원칙과 프로젝트 규칙의 충돌 여부도 사전에 판정할 수 없게 만든다.

개선 방향:
첫 세션 의무 읽기에 "프로젝트 식별 후 해당 `project-rules/<프로젝트>.md` 또는 repo 내 `CLAUDE.md` 확인"을 별도 필수 단계로 넣어야 한다. 파일이 없으면 "프로젝트 특수 규칙 없음"을 인증하도록 해야 한다.

### 문제 2-3. `memory/README.md`, `tool-inventory.md`, `work-queue.md`는 필수인지 아닌지 경계가 없다.

근거 구문:
- `ai-dev-신념.md`: "`강제성: 기억 저장은 모델의 자율 판단(빌트인)에만 맡기지 않는다. memory-tick(stop-hook 강제 발화) 장치로 저장 판단을 트리거. (운영 상세·트리거 조건·Obsidian 일원화는 memory/README.md에.)`"
- `personas/markjang29.md`: "`도구 인벤토리: ~/notes/tool-inventory.md`"
- `personas/markjang29.md`: "`작업 큐: ~/notes/work-queue.md`"
- `onboarding.md`: "`세션 학습 = 각 봇 메모리 → ~/notes/memory(후보 → 사용자 승인 → 승격).`"

비판:
온보딩은 memory 운영을 언급하지만 `memory/README.md`를 의무 읽기 목록에 넣지 않는다. persona는 도구 인벤토리와 작업 큐를 고정 위치로 지정하지만, 온보딩은 해당 파일을 읽거나 존재 확인하라고 요구하지 않는다. 담당 봇이 첫 세션에서 실제 이어받기 상태를 복원하려면 memory, tool inventory, work queue가 더 직접적인 입력일 수 있는데, 의무 읽기 5에는 원칙 문서만 들어가 있다.

개선 방향:
상주 담당 봇의 첫 세션에는 `memory/README.md`와 프로젝트별 work queue/inventory 확인을 조건부 필수로 넣어야 한다. 단, 모든 서브에이전트에게까지 강제하면 context-budget 낭비가 되므로, "상주 담당 봇"과 "일회성 리뷰 에이전트"를 나눠야 한다.

### 문제 2-4. 모든 담당 봇에게 5개 항목 full read를 강제하는 것은 `context-budget.md`의 read 절제와 긴장 관계가 있다.

근거 구문:
- `onboarding.md`: "`역할 확인 직후, 코드/기획 작업 전에 아래를 읽는다`"
- `context-budget.md`: "`같은/큰 파일 full 재독 금지.`"
- `context-budget.md`: "`파일 경로 + 검증 범위(대상 섹션/질문) + 산출물 계약(결과 저장 경로·요약 길이)만 전달`"

비판:
온보딩은 모든 담당 봇의 첫 세션에 광범위한 원칙 파일 읽기를 요구한다. 하지만 `context-budget.md`는 큰 반환값의 메인 재적재와 full 재독을 문제로 본다. "첫 세션"이라는 제한이 있더라도, 담당 봇이 세션을 자주 갈아타거나 서브에이전트가 매번 새 세션으로 뜨면 같은 파일 full read가 반복된다. 특히 일회성 검증 에이전트에게도 동일 의무를 적용하면 `context-budget.md` §2의 "경로 + 계약" 원칙과 충돌한다.

개선 방향:
온보딩을 계층화해야 한다. 예: 상주 담당 봇은 최초 1회 full read + 이후 변경 감지 시 diff read. 서브에이전트는 작업에 필요한 파일 경로와 검증 질문만 받고 직접 필요한 범위만 읽음. 또한 "이미 읽은 버전/date/hash"를 남겨 재독 기준을 만들 필요가 있다.

### 문제 2-5. 읽기 강제 메커니즘은 자기선언뿐이며 우회가 쉽다.

근거 구문:
- `onboarding.md`: "`읽지 않은 채 발판/결정을 하지 않는다.`"
- `onboarding.md`: "`담당 봇은 첫 응답에서 아래를 한 줄로 인증: \"원칙 체계 읽음: agent-rules · ai-dev-신념 · markjang29 · ADR · context-budget. 프로젝트=OOO.\"`"

비판:
실제 온보딩 파일에 명시된 강제 메커니즘은 첫 응답의 한 줄 인증뿐이다. 이 인증은 모델이 읽었다고 말하기만 하면 통과된다. 파일 접근 로그 확인, 체크섬 기록, 첫 작업 전 hook, PR/commit 전 검사, ADR 누락 검사, 프로젝트 규칙 존재 확인 같은 탐지 수단이 없다. 따라서 담당 봇이 읽지 않고 인증하거나, 일부만 읽고 인증하거나, 첫 응답 이후 규칙을 잊고 진행해도 온보딩 자체로는 탐지할 방법이 없다.

개선 방향:
온보딩 체크는 자기선언이 아니라 작업 전 gate로 바꿔야 한다. 예: 첫 세션에서 읽은 파일 경로·mtime/hash·프로젝트명을 `memory` 또는 세션 상태 파일에 기록, 코드 발판 전 ADR 존재 확인 스크립트 실행, commit 전 hook에서 `decisions/` 변경 필요 여부를 묻는 체크리스트 출력, 프로젝트 repo 진입 시 `project-rules`/`CLAUDE.md` 존재 여부 확인. 최소한 현재 문서에는 "인증 문구"와 별개로 "인증 실패/누락 시 작업 금지"를 누가 어떻게 판정하는지 없다.

## 3. "결정 = ADR 필수"와 "온보딩 체크"의 작동 가능성, 위반 탐지·제재

### 문제 3-1. ADR 파일명 규칙이 서로 충돌한다.

근거 구문:
- `onboarding.md`: "`엔진 · 스택 · 언어 · 아키텍처 · 외부 서비스 도입·변경 → decisions/ADR-NNNN-<주제>.md 작성.`"
- `decisions/ADR-template.md`: "`파일명 규칙: YYYY-MM-DD-짧은-kebab-제목.md`"

비판:
온보딩은 `ADR-NNNN-<주제>.md`를 요구하고, 템플릿은 `YYYY-MM-DD-짧은-kebab-제목.md`를 요구한다. 이 충돌은 실제 파일 생성 단계에서 즉시 실패 지점을 만든다. 담당 봇은 어느 규칙을 따라야 하는지 모른다. 자동 탐지나 정렬도 어려워진다. 번호 기반이면 순번 충돌 관리가 필요하고, 날짜 기반이면 동일 날짜 다중 ADR 충돌 처리가 필요하다.

개선 방향:
파일명 규칙을 하나로 통일해야 한다. 기존 `context-budget.md`의 `.reviews` 규칙처럼 충돌 방지 규칙까지 포함해야 한다. 예: `ADR-YYYYMMDD-NNN-<slug>.md` 또는 `ADR-NNNN-<slug>.md` 중 하나를 선택하고, README와 템플릿, 온보딩을 같은 문장으로 맞춰야 한다.

### 문제 3-2. ADR 트리거 범위가 넓지만 "결정"의 최소 단위가 정의되지 않았다.

근거 구문:
- `onboarding.md`: "`엔진 · 스택 · 언어 · 아키텍처 · 외부 서비스 도입·변경 → ... 작성.`"
- `decisions/README.md`: "`스택·언어·엔진·주요 라이브러리 선택`"
- `decisions/README.md`: "`되돌리기 어려운 구조·아키텍처 변경`"
- `decisions/README.md`: "`\"왜 이렇게 했지?\"를 나중에 물을 수 있는 결정`"

비판:
`decisions/README.md`의 마지막 트리거인 "`왜 이렇게 했지?`를 나중에 물을 수 있는 결정"은 매우 넓다. 온보딩은 이를 "결정 = ADR 필수"로 강하게 표현한다. 이 조합은 사소한 라이브러리 옵션, 폴더 구조 조정, 임시 CLI 선택까지 ADR 대상인지 모호하게 만든다. 반대로 담당 봇이 "이건 결정이 아니다"라고 축소 해석해 ADR을 회피할 수도 있다.

개선 방향:
ADR 필수/선택/불필요 기준을 나눠야 한다. 예: 필수는 스택·언어·엔진·외부 서비스·되돌리기 어려운 아키텍처·보안/비용 트레이드오프. 선택은 주요 라이브러리나 장기 유지보수 영향. 불필요는 단순 리팩터, 문서 표현 수정, 테스트 보강. 또한 "주요 라이브러리"의 기준도 런타임 의존성, 배포 영향, lockfile 변경, 보안 표면 증가 등으로 구체화해야 한다.

### 문제 3-3. "스택 미확정 발판 금지"는 선언만 있고 발판의 정의와 예외가 없다.

근거 구문:
- `onboarding.md`: "`스택 미확정 발판 금지` — 결정(ADR) 없이 코드 발판을 안 친다."
- `agent-rules.md`: "`새 코드 프로젝트는 스택(언어/엔진) 확인 후 발판.`"
- `personas/markjang29.md`: "`한 번 쓰고 버릴 탐색 코드 → 작업 큐에만. 단, 그 코드가 아이디어의 유일한 흔적이면 생략 금지`"

비판:
온보딩은 ADR 없이는 코드 발판을 금지한다고 하지만, `agent-rules.md`는 "스택 확인 후 발판"이라고 하고, persona는 탐색 코드와 아이디어 보존 예외를 인정한다. "발판"이 repo 생성, 디렉터리 생성, package.json 작성, prototype 작성, 스크립트 작성 중 어디부터인지 정의되어 있지 않다. 따라서 탐색 코드가 ADR 전 허용되는지, README 초안이나 spike script가 발판인지, 기존 프로젝트 안의 작은 PoC가 금지되는지 불명확하다.

개선 방향:
"발판"의 금지 대상을 구체화해야 한다. 예: 새 repo/런타임 초기화, 프레임워크 scaffold, lockfile 생성, 배포 파이프라인 추가는 ADR 전 금지. 반면 폐기 가능한 spike는 별도 scratch 위치와 작업 큐 기록 조건하에 허용. 이렇게 해야 persona의 아이디어 보존 원칙과 ADR 원칙이 충돌하지 않는다.

### 문제 3-4. ADR 위반 탐지·제재가 없다.

근거 구문:
- `onboarding.md`: "`결정 = ADR 필수`"
- `onboarding.md`: "`읽지 않은 채 발판/결정을 하지 않는다.`"
- `agent-rules.md`: "`SELF-CHECK BEFORE EVERY EDIT`"에는 ADR 존재 여부 체크 항목이 없다.
- `agent-rules.md`: "`NEVER`"에는 "`스택 미확정 코드 프로젝트 함부로 발판 금지`"가 있지만 ADR 누락 제재나 탐지는 없다.

비판:
ADR 필수는 강한 규칙처럼 쓰였지만, 위반 시 탐지·제재가 문서 어디에도 없다. `SELF-CHECK BEFORE EVERY EDIT`는 범위, NEVER, 외부 참조, 시크릿, CLAUDE.md 편집만 확인한다. "이 변경이 ADR 트리거인가?", "필요한 ADR이 있는가?", "ADR 상태가 accepted인가?" 같은 체크가 없다. `NEVER`에도 스택 미확정 발판 금지는 있지만 ADR 누락 자체를 금지하거나 탐지하는 절차는 없다.

개선 방향:
편집 전 self-check와 commit 전 체크에 ADR 항목을 추가해야 한다. 최소한 "이번 변경이 ADR 트리거에 해당하는가? 해당하면 `decisions/` 파일 경로는 무엇인가?"를 요구해야 한다. 더 강하게는 git diff에서 package manager 파일, IaC, CI, framework config, 외부 API client 추가 등을 감지해 ADR 확인을 묻는 hook이 필요하다. 제재는 "commit/push 전 중단", "사용자 승인 없이는 진행 금지"처럼 실행 가능한 형태여야 한다.

### 문제 3-5. 온보딩 체크도 탐지·제재 없이 자기보고에 머문다.

근거 구문:
- `onboarding.md`: "`첫 응답에서 아래를 한 줄로 인증`"
- `context-budget.md`: "`Stop 훅(...token-report.sh)이 매 응답 후 누적 토큰을 출력.`"
- `ai-dev-신념.md`: "`memory-tick(stop-hook 강제 발화) 장치로 저장 판단을 트리거.`"

비판:
같은 notes 체계 안에는 `memory-tick`이나 `token-report`처럼 hook 기반 강제 발화 장치가 언급되어 있다. 하지만 온보딩 체크는 그런 장치와 연결되어 있지 않다. 즉 문서 체계는 hook을 강제 메커니즘으로 사용할 수 있음을 알고 있으면서도, 가장 중요한 첫 세션 온보딩에는 hook을 적용하지 않는다. 첫 응답 인증 누락 시 어떤 일이 일어나는지, 인증 문구가 거짓일 때 어떻게 발견하는지, 프로젝트명이 틀렸을 때 누가 막는지 전혀 없다.

개선 방향:
온보딩 체크를 hook 또는 wrapper 레벨로 끌어올려야 한다. 예: 담당 봇 시작 시 `onboarding-check`가 필수 파일 목록과 프로젝트명을 출력하고, 모델 응답에 인증 문구가 없으면 재시도 요구. 더 현실적으로는 첫 작업 전 "읽은 파일 경로와 판단한 프로젝트 규칙 경로"를 `.reviews` 또는 memory 후보에 남기게 해야 한다. 자기보고만으로는 "읽지 않은 채 발판/결정을 하지 않는다"는 규칙을 강제할 수 없다.

## 4. 프로젝트별 특수성 vs 공통 원칙의 상하관계 모호성

### 문제 4-1. "덮어쓰기"와 "충돌 시 공통 상위"가 함께 쓰여 override 범위가 모호하다.

근거 구문:
- `onboarding.md`: "`공통 원칙(이 문서 + principles/) 위에 덮어쓰되, 충돌 시 공통 원칙이 상위.`"

비판:
"덮어쓴다"는 말은 하위 규칙이 상위 기본값을 변경할 수 있다는 뜻으로 읽힌다. 그러나 바로 뒤의 "충돌 시 공통 원칙이 상위"는 변경을 제한한다. 그러면 프로젝트 규칙은 정확히 무엇을 덮어쓸 수 있는가? 테스트 명령, 배포 명령, 커밋 방식, 의존성 정책, 코드 스타일, 리뷰 루프 횟수, ADR 임계값 중 무엇이 가능한지 구분이 없다. 담당 봇은 이 모호성을 이용해 프로젝트 사정이라는 이유로 공통 원칙을 우회할 수 있고, 반대로 공통 원칙을 지나치게 엄격하게 적용해 프로젝트별 실무 절차를 무시할 수도 있다.

개선 방향:
override 가능 영역과 불가 영역을 표로 분리해야 한다. 가능 영역은 프로젝트 경로, 실행 명령, 테스트 범위, 배포 절차, 도메인별 금지 조건, repo별 branch/PR 방식. 불가 영역은 시크릿 금지, 사용자 승인 없는 삭제 금지, 의도 보존, ADR 필수 트리거, memory 후보/승격 모델, context-budget의 결과 파일 분리 같은 공통 운영 원칙. 애매한 경우 사용자 확인 또는 ADR로 승격하는 규칙도 필요하다.

### 문제 4-2. repo 내 `CLAUDE.md`와 notes의 `project-rules` 중 우선순위가 없다.

근거 구문:
- `onboarding.md`: "`project-rules/<프로젝트>.md 또는 프로젝트 repo 내 CLAUDE.md.`"

비판:
"또는"은 둘 중 하나만 읽으면 되는지, 둘 다 있으면 어느 쪽이 우선인지, 둘이 충돌하면 어떻게 하는지 말하지 않는다. repo 내 `CLAUDE.md`는 프로젝트와 가까운 실행 규칙일 수 있고, notes의 `project-rules`는 중앙 관리 규칙일 수 있다. 둘의 관계를 정의하지 않으면 담당 봇은 더 편한 파일 하나만 읽고 프로젝트 특수성을 충족했다고 주장할 수 있다.

개선 방향:
둘 다 존재하면 둘 다 읽고 충돌을 보고하도록 해야 한다. 우선순위는 예를 들어 "repo 내 `CLAUDE.md`는 실행 명령과 경로에서 우선, notes `project-rules`는 장기 운영·협업 규칙에서 우선"처럼 나눌 수 있다. 단 공통 원칙과 충돌하는 항목은 override 불가로 명시해야 한다.

### 문제 4-3. 사용자 직접 지시와 공통 원칙의 관계가 빠져 있다.

근거 구문:
- `onboarding.md`: "`프로젝트가 달라도 사칙은 같다.`"
- `personas/markjang29.md`: "`진행 재개 전 확인(원안 우선, 대안 별도 보관).`"
- `agent-rules.md`: "`충분한 정보가 있으면 행동. 진짜 모호할 때만 물어본다.`"

비판:
온보딩은 공통 원칙과 프로젝트 특수성만 다루고, 현재 세션의 사용자 직접 지시가 어디에 놓이는지 정의하지 않는다. 실제 운영에서는 사용자가 action_safety처럼 특정 파일만 쓰라고 제한하거나, structured_output_contract처럼 stdout을 제한할 수 있다. 이런 직접 지시가 공통 원칙보다 우선인지, 프로젝트 규칙보다 우선인지 문서에 없다. 이 누락은 담당 봇이 "pull → 작업 → commit/push" 같은 공통 규칙을 들어 사용자의 좁은 안전 지시를 침범하는 위험을 만든다.

개선 방향:
상하관계에 "현재 사용자 지시"를 명시해야 한다. 특히 파일 쓰기 제한, 출력 계약, 금지 작업, 승인 조건은 프로젝트별 규칙이나 일반 운영 루틴보다 우선해야 한다. 단 사용자가 시크릿 유출, 무단 삭제, 불법 행위 등 hard guardrail을 요구하는 경우에는 거부한다는 계층도 필요하다.

### 문제 4-4. "공통 원칙"의 구성 범위가 문서마다 다르다.

근거 구문:
- `onboarding.md`: "`공통 원칙(이 문서 + principles/)`"
- `agent-rules.md`: "`notes 라우팅: 장기 원칙→principles/, 결정/트레이드오프(ADR)→decisions/, 세션 암묵지→memory/, 사용자 판단기준→personas/, 프로젝트별 실행규칙→project-rules/. 루트 agent-rules.md=어떻게 / principles/ai-dev-신념.md=왜.`"
- `ai-dev-신념.md`: "`저장소 계층`"에서 `principles/`, `decisions/`, `memory/`, `personas/`, `project-rules/`, `agent-rules.md`를 각각 분리.

비판:
온보딩은 공통 원칙을 "이 문서 + `principles/`"로 좁힌다. 하지만 실제 판단 기준은 `personas/markjang29.md`, ADR 규칙은 `decisions/`, 실행 절차는 `agent-rules.md`, 메모리 운영은 `memory/`에도 있다. 이 때문에 "공통 원칙 상위"라고 할 때 persona와 decisions가 포함되는지 불분명하다. 포함되지 않는다면 프로젝트 규칙이 persona 판단 기준이나 ADR 규칙을 덮어쓸 수 있는 것처럼 읽힐 수 있고, 포함된다면 온보딩의 표현이 부정확하다.

개선 방향:
"공통 원칙"이라는 단일 표현 대신 "공통 운영 체계"를 정의하고 하위 범주를 나눠야 한다. 예: hard guardrails, 실행 절차, 판단 기준, 의도 보존, 메모리 운영, 프로젝트 실행 규칙. 각 범주별 override 가능 여부를 명시해야 한다.

## 5. 진입 트리거: "글로벌 CLAUDE.md 한 줄"의 견고성 및 hook 필요성

### 문제 5-1. 온보딩 파일 자체에는 글로벌 `CLAUDE.md` 한 줄 트리거가 명시되어 있지 않다.

근거 구문:
- `agent-rules.md`: "`각 머신은 이 내용을 자기 ~/.claude/CLAUDE.md 로 미러링해서 사용한다.`"
- `agent-rules.md`: "`Last reviewed: 2026-06-26 · 원본: Linux 서버 /home/ubuntu/.claude/CLAUDE.md`"
- `onboarding.md`: 첫 세션 의무 읽기와 첫 응답 인증은 있으나 글로벌 `CLAUDE.md`에 어떤 한 줄을 넣어 진입시키는지 명시하지 않는다.

비판:
리뷰 요청은 "글로벌 CLAUDE.md 한 줄" 진입 트리거를 평가하라고 했지만, 읽은 `onboarding.md`에는 해당 한 줄의 실제 문구나 설치 위치가 없다. 관찰 가능한 사실은 `agent-rules.md`가 `~/.claude/CLAUDE.md` 미러링을 말한다는 점뿐이다. 따라서 현재 온보딩 파일만으로는 글로벌 `CLAUDE.md`가 온보딩을 호출한다는 보장이 없다. 이 상태에서 담당 봇이 첫 세션에 `onboarding.md`를 읽는 경로는 문서 내부 규칙이 아니라 외부 설정에 의존한다.

개선 방향:
온보딩 문서에 실제 진입 문구를 명시해야 한다. 예: "`~/.claude/CLAUDE.md` 상단에 담당 봇 역할 감지 시 `/home/ubuntu/notes/onboarding.md`를 읽고 인증하라는 문장을 둔다." 또한 각 머신에서 해당 문구가 설치되어 있는지 점검하는 절차가 필요하다.

### 문제 5-2. 한 줄 트리거는 견고하지 않다. 모델 주의력과 컨텍스트 상태에 의존한다.

근거 구문:
- `onboarding.md`: "`담당 봇은 첫 응답에서 아래를 한 줄로 인증`"
- `context-budget.md`: "`1M 컨텍스트 창에서 폭발... 서브에이전트 큰 반환값의 메인 재적재 + 루프 누적이 주범`"
- `agent-rules.md`: "`WHEN COMPACTING` 컨텍스트 요약 시 반드시 보존..."

비판:
한 줄 트리거는 모델이 그 줄을 보고 따르는 방식이다. compact 이후 요약에서 누락되거나, 프로젝트 repo 내 다른 `CLAUDE.md`와 충돌하거나, 서브에이전트 프롬프트가 좁게 주어지거나, 사용자가 직접 제한을 걸면 쉽게 우회된다. `agent-rules.md`는 compact 시 보존 항목을 따로 둔다. 이는 컨텍스트 기반 지시가 누락될 수 있음을 전제한다. 그런데 온보딩 트리거는 그 취약한 컨텍스트 지시에만 기대고 있다.

개선 방향:
한 줄 트리거는 최소 안내로만 두고, 실제 강제는 hook/wrapper/check script로 해야 한다. 예: 담당 봇 시작 wrapper가 온보딩 파일 경로를 시스템 프롬프트나 첫 사용자 메시지에 삽입, 첫 응답 인증 누락 감지, 프로젝트명 추출 실패 시 중단, 파일 read 로그 또는 hash 기록. compact 시에도 온보딩 상태와 읽은 파일 버전을 보존하도록 `WHEN COMPACTING` 항목에 추가해야 한다.

### 문제 5-3. 이미 hook 기반 강제 장치를 쓰는 문서 체계와 비교하면 온보딩만 약하다.

근거 구문:
- `ai-dev-신념.md`: "`memory-tick(stop-hook 강제 발화) 장치로 저장 판단을 트리거.`"
- `context-budget.md`: "`Stop 훅(...token-report.sh)이 매 응답 후 누적 토큰을 출력.`"
- `onboarding.md`: "`첫 응답에서 아래를 한 줄로 인증`"

비판:
메모리와 토큰 예산에는 stop-hook 기반 장치가 언급되어 있다. 반면 온보딩은 첫 응답 인증에 머문다. 문서 체계 내부에서도 더 강한 강제 방식이 이미 채택되어 있으므로, 온보딩만 자기선언 방식인 것은 일관성이 약하다. 특히 온보딩은 ADR, persona, agent-rules, context-budget를 모두 연결하는 상위 진입점이므로, memory 저장 판단보다 약한 강제 수준에 두는 것은 운영상 취약하다.

개선 방향:
온보딩도 hook 또는 wrapper 대상으로 승격해야 한다. 가능한 최소 구현은 stop-hook이 아니라 start-hook 또는 shell wrapper에 가깝다. 시작 시 온보딩 상태가 없으면 "읽기 대상 파일 목록 + 프로젝트 규칙 확인 + 인증 문구"를 강제하고, 작업 전 self-check에 "온보딩 완료 여부"를 넣어야 한다.

### 문제 5-4. `context-budget.md` §1-2와의 계약은 이번 리뷰 방식에는 맞지만, 온보딩 자체에는 내장되어 있지 않다.

근거 구문:
- `context-budget.md`: "`결과는 파일로 덤프: ~/notes/.reviews/<대상>-<날짜>-<seq>.md.`"
- `context-budget.md`: "`메인엔 결론 요약(5줄 이내)만.`"
- `context-budget.md`: "`파일 경로 + 검증 범위(대상 섹션/질문) + 산출물 계약(결과 저장 경로·요약 길이)만 전달`"
- `onboarding.md`: "`principles/context-budget.md — 토큰/컨텍스트 예산 운영`"

비판:
이번 작업 요청은 결과 저장 경로와 요약 길이를 지정해 `context-budget.md` §1-2를 직접 실천한다. 그러나 온보딩 자체는 담당 봇이나 서브에이전트에게 이런 산출물 계약을 어떻게 강제할지 설명하지 않는다. "context-budget를 읽는다"는 요구와 "결과를 파일로 분리한다"는 실행 계약 사이에 자동 연결이 없다. 특히 리뷰/검증 서브에이전트는 온보딩 대상인지도 불명확하므로, 결과를 full로 메인 컨텍스트에 반환하는 우회가 가능하다.

개선 방향:
온보딩의 첫 세션 체크와 별도로 "서브에이전트 호출 계약" 섹션이 필요하다. 최소 필드: 대상 파일 경로, 읽을 범위, 리뷰 질문, 결과 저장 경로, stdout 요약 줄 수, 전문 재적재 금지. 이 계약을 담당 봇이 서브에이전트에게 전달하도록 해야 한다.

## 종합 결론

현재 `onboarding.md`는 공통 문서들을 연결하는 색인으로는 작동할 수 있지만, "규칙"으로 보기에는 강제력과 충돌 해소 체계가 부족하다. 가장 심각한 결함은 다음이다.

1. ADR 파일명 규칙이 온보딩과 템플릿에서 충돌한다.
2. 프로젝트별 override가 어디까지 허용되는지 정의되어 있지 않다.
3. 의무 읽기 체크가 첫 응답 자기선언뿐이라 읽기·ADR·프로젝트 규칙 확인을 강제하지 못한다.
4. `project-rules`/repo `CLAUDE.md`, `memory/README.md`, tool inventory/work queue의 읽기 조건이 빠져 있다.
5. 글로벌 `CLAUDE.md` 한 줄 트리거는 온보딩 파일에 실제 문구나 설치 검증이 없어 견고하지 않다.

따라서 개선의 우선순위는 문장 보강보다 실행 가능한 gate 설계다. 파일명 규칙 통일, override 가능/불가 표, 프로젝트 규칙 확인 절차, ADR 트리거 체크, 온보딩 인증의 hook/wrapper화가 없으면 담당 봇은 문서를 읽었다고 말하면서도 핵심 규칙을 우회할 수 있다.
