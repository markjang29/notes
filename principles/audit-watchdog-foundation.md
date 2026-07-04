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

### 매시간 저토큰 와치독

- cron: `45 * * * *`
- 정상이고 변화가 작으면 한 줄 보고
- 문제 있으면 판정, 근거, 책임 주체, 권장 조치, 클리어 가능/보류 여부 보고

### 매일 아침 종합 브리프

- cron: `10 9 * * *`
- 최근 24시간 역할 위반, 세션/모델 이상, Git 로컬-only 누락, 완료보고 불일치, 클리어 가능 여부 요약

## 운영 원칙

- 보안/도구사용 자체 감사가 아니라 **역할·기능·세션·Git 보존 상태**를 감시한다.
- `.md` 파일은 세션 기억이 아니라 Git/notes에 보존되어야 한다.
- "완료"보다 "보존 완료"가 우선이다.
- 클리어 권장은 Git/notes 보존 확인 후에만 한다.

