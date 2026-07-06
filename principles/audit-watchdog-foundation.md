---
title: 감사모드 저토큰 와치독 원칙
date: 2026-07-04
status: v1
tags:
  - audit
  - watchdog
  - agent
  - git
  - context
---

# 감사모드 저토큰 와치독 원칙

## 목적

Claude 매니저와 각 팀장이 기능과 역할을 제대로 수행하는지 저토큰으로 감시한다.

Codex 쪽은 별도 팀장 체계가 아니라 **이 감사 봇 하나만** 보조 감사/검증 역할을 맡는다.

## 감시 대상

- 매니저: `heav_lnx_bot`
- RPG 팀장: `heav_lnx_rpg_bot`
- 시나리오 팀장: `heav_lnx_scenario_bot`
- trader 팀장: `heav_lnx_trader_bot`
- Codex: 이 감사 봇 1개만 보조 감사/검증 역할

## 최우선 감사 기준

### 역할 이탈

- 팀장이 매니저 역할을 떠맡는가?
- 매니저 전관인 `work-queue`, 우선순위, 통합보고, ops를 팀장이 침범하는가?
- 자기 정체를 확인하지 않고 역할을 주장하는가?
- 이전 합의사항이나 사용자 지시와 반대로 행동하는가?

### 기능 실패

- 사용자가 요청한 핵심 작업을 완료했는가?
- 실패했는데 성공한 것처럼 보고하는가?
- "완료", "push", "commit", "모델 전환" 보고가 실제 상태와 일치하는가?
- 필요한 파일/링크/결과물을 전달하지 않았는가?

### 세션/모델/컨텍스트 리스크

- 세션이 끊겼는데 이어서 처리하는 척하는가?
- 모델을 바꾸기로 했는데 실제로 바꾸지 못했거나 확인 없이 진행하는가?
- recovery gate disabled, context lost, compact 실패, timeout을 숨기는가?
- 컨텍스트가 과도하게 커졌는데 세션 클리어/요약/보존을 권장하지 않는가?

### Git 로컬-only 누락

- Git에 없고 로컬에만 남은 산출물, WIP, 로그, 의사결정 문서가 있는가?
- 중요한 정보가 `.md` 파일에는 적혔지만 commit/push 되지 않아 세션 클리어 시 유실될 위험이 있는가?
- Markdown 산출물, ADR, notes, deliverables가 로컬에만 있는데 완료 보고를 하는가?

### Git 문서 정합성

- 이미 Git에 commit된 문서들 사이에 현재 운영 기준이 충돌하는가?
- 운영 repo 개수, clone 스크립트, onboarding, L0, org-structure, work-queue, audit-watchdog의 기준이 서로 맞는가?
- `key → bot → role → project` 매핑이 `bot_settings.json`, L0, onboarding, org 문서에서 일치하는가?
- 포트 정책, ADR, work-queue, checkpoint가 서로 다른 현재값을 말하지 않는가?
- 과거 날짜의 역사 기록을 현재 기준처럼 오해할 위험이 있는가?

처리 원칙:

- 명백한 최신 기준 불일치는 감사봇이 직접 문서 수정 후 commit/push한다.
- 과거 기록 자체는 함부로 덮어쓰지 말고, 현재 기준 주석·최신 문서 보강으로 해결한다.
- 의미가 애매하거나 정책 판단이 필요한 정합성 문제는 이사님께 질문한다.

## 저토큰 감시 방식

전체 로그를 매번 읽지 않는다.

우선순위:

1. `git status --short`
2. 최근 24시간 commit log
3. 최근 수정된 Claude 세션 파일
4. 위험 키워드 주변 20~50줄
5. 필요 시에만 상세 로그 확대

위험 키워드:

- `push`, `commit`, `merge`, `deploy`, `release`
- `완료`, `푸시`, `커밋`, `배포`
- `model`, `모델`, `switch`, `fallback`
- `context`, `세션`, `compact`, `clear`, `클리어`
- `timeout`, `429`, `529`, `recovery gate disabled`
- `untracked`, `modified`, `not staged`, `미추적`, `미커밋`, `로컬`

## 대상 repo

- `/home/ubuntu/notes`
- `/home/ubuntu/projects/rpg_game`
- `/home/ubuntu/projects/scenario`
- `/home/ubuntu/projects/autotrader`

기본 확인:

```bash
git -C <repo> status --short
git -C <repo> log --since='24 hours ago' --pretty='%h %ad %s' --date=iso
```

## 세션 클리어 점검

이사님이 "세션 클리어 가능?"이라고 물으면 즉시 상세 점검한다.

판정:

- **클리어 가능**: 중요한 변경이 모두 Git/notes/전달 파일에 보존됨
- **클리어 보류**: 미추적 산출물, 미커밋 변경, 미전달 파일, 미기록 결정이 남음
- **즉시 보존 필요**: 세션이 터지면 잃을 수 있는 로컬-only 결과가 있음

### 메신저 대화 백업 의무

이사님이 특정 봇/세션에 대해 "대화 백업", "터진 세션 백업", "읽기 쉬운 백업"을 요청하면, 현재 감사봇 세션이 `/clear` 된 이후라도 반드시 수행한다.

기본 백업 소스:

- AI 세션 history: `~/.cokacdir/ai_sessions/<session_id>.json`
- Telegram 입력 로그: `~/.cokacdir/logs/telegram_YYYY-MM-DD.jsonl`
- 그룹 shared log: `~/.cokacdir/group_chat/<chat_id>.jsonl`
- Claude transcript: `~/.claude/projects/*/<session_id>.jsonl`

기본 출력:

- 사람이 읽기 쉬운 Markdown `.md`
- `User / Assistant` 턴 번호 구분

도구:

```bash
python3 ~/scripts/export-chat-backup.py --session-id <SESSION_ID> --out <OUT.md>
python3 ~/scripts/export-chat-backup.py --latest --out <OUT.md>
```

크기 제한:

- 백업이 너무 커서 1M 토큰을 넘길 것 같으면 그대로 전달하지 않는다.
- 기본 `--max-chars 2000000`로 자르고, 기본은 `--keep tail`이다.
- 즉, 최근/뒤쪽 대화를 보존하고 앞쪽을 절단한다.
- 필요 시 `--keep head` 또는 `--keep middle` 사용.

보고 양식:

```markdown
## 세션 클리어 점검

- 판정: 클리어 가능 / 클리어 보류 / 즉시 보존 필요
- 이유:
- Git 미반영:
- 로컬-only 산출물:
- notes/ADR 기록 필요:
- 권장 조치:
```

## 정기 감시 스케줄

### 매일 아침 종합 브리프

- schedule id: `B7C51FA3`
- cron: `10 9 * * *`
- 최근 24시간 역할 위반, 세션/모델 이상, Git 로컬-only 누락, Git 문서 정합성, 완료보고 불일치, 클리어 가능 여부 요약
- 실행 주기: 하루 1회. 상시/매시간 감시는 하지 않는다.

## 운영 원칙

- 보안/도구사용 자체 감사가 아니라 **역할·기능·세션·Git 보존 상태**를 감시한다.
- `.md` 파일은 세션 기억이 아니라 Git/notes에 보존되어야 한다.
- "완료"보다 "보존 완료"가 우선이다.
- 클리어 권장은 Git/notes 보존 확인 후에만 한다.

## 권장조치 전달 원칙

- **중요정보 Git 누락**은 발견 즉시 보존 지시한다. 단, 추상적으로 "즉시보존"이라고만 쓰지 않는다.
  - 예: `.md` 산출물, ADR, notes, deliverables, 인수인계, 결정 근거가 로컬-only 상태.
  - 지시 내용: "세션 클리어 보류. 해당 파일을 Git/notes에 보존하고 commit/push 또는 보존 완료 보고 전까지 완료 처리 금지."
- 감사봇은 기계적으로 "미반영 파일 있음"만 보고하지 않는다. 내용을 읽고 판단한다.
- 직접 처리 가능한 보존 조치는 직접 수행한다.
  - 예: notes repo의 운영 문서·ADR·work-queue·checkpoint가 로컬-only이고 내용상 보존이 명백하면 감사봇이 commit/push까지 처리한다.
  - 단, 자동 로그(`.reviews/*.log`)·불명확한 임시 산출물·폐기 가능성이 큰 WIP는 이사님께 묻는다.
- 매니저/팀장에게 시정 지시가 필요한 경우, 가능한 전달 경로가 있으면 간결한 지시문으로 전달하고, 불가능하면 이사님께 전달문을 제시한다.
- 보고에는 반드시 아래를 포함한다.
  - **무슨 내용인지:** 어떤 파일의 어떤 결정/운영 정보인지 1~3줄 요약
  - **책임 주체:** 매니저 / RPG 팀장 / 시나리오 팀장 / trader 팀장 중 누구 영역인지
  - **누구에게 지시했는지:** 예) 매니저에게 Git 보존 지시
  - **처리 상태:** 미처리 / 처리 중 / 처리 완료 / 이사님 확인 필요
  - **다음 문장:** "제가 처리할까요?" 또는 "처리했습니다." 중 하나로 끝낸다.
- 그 외 문제는 이사님께 먼저 묻는다.
  - 예: 역할 경계 위반 의심, 모델 전환 실패 의심, 품질 판단, 우선순위 조정, 팀장에게 시정 요구 여부.
- 직접 수정/개조/삭제/재배정은 이사님 명시 지시 전에는 하지 않는다.
