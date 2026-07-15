---
title: 사칙 — Git 정본과 보고 투영
status: active
version: v1
date: 2026-07-16
authority: 이사님 직접 확정
---

# 사칙 — Git 정본과 보고 투영

## 1. 한 줄 원칙

**프로젝트의 아이디어·결정·우선순위·설계·검증된 현황은 commit되고 공유된 Git만 정본이다. Notion은 그 정본을 이사님이 읽기 쉽게 보여 주는 보고 화면일 뿐이다.**

## 2. 정본의 위치

- 프로젝트별 코드·계약·설계·자산·검증 근거는 해당 프로젝트 Git에 둔다.
- 여러 프로젝트에 걸친 사칙·결정·질문·우선순위는 Notes Git에 둔다.
- dirty working tree, 대화 기억, Telegram 메시지, Agent Mail 제출, 작업자 보고, Notion 페이지는 Git commit 전에는 프로젝트 정본이 아니다.
- 다른 agent와 기기에서 재현해야 하는 정본은 commit 후 remote에 push되어야 한다.

## 3. Notion의 허용 역할

Notion은 다음만 할 수 있다.

- Git의 현재 핵심을 짧고 읽기 쉽게 요약한다.
- 여러 Git 문서를 한 화면에 링크한다.
- 이사님이 검토할 후보·결정·진행 상황을 상태 변화 없이 보여 준다.

Notion은 다음을 할 수 없다.

- Git에 없는 아이디어·결정·우선순위·완료 주장을 새로 만든다.
- Git의 `candidate`, `draft`, `pending`을 `핵심`, `확정`, `완료`로 승격한다.
- Git에서 삭제·폐기·supersede된 내용을 최신 사실처럼 유지한다.
- 유일한 사본이 된다.

## 4. 투영 전 필수 게이트

Notion에 프로젝트 내용을 쓰기 전에 controller는 반드시 확인한다.

1. 올바른 `repo_id`와 remote를 확인한다.
2. 근거가 dirty tree가 아니라 commit에 존재하는지 확인한다.
3. full 40-character commit과 exact repo-relative path를 고정한다.
4. 원문의 상태(`candidate`, `draft`, `accepted`, `implemented`, `verified`, `superseded`)를 그대로 보존한다.
5. 다른 agent가 읽어야 하면 push와 remote object 존재를 확인한다.
6. Notion 카드나 페이지에 source repo, full commit, exact refs, projected time을 표시한다.

하나라도 없으면 Notion 쓰기를 중단한다.

## 5. 새 아이디어 처리

대화나 Telegram에서 새 아이디어가 나오면 다음 순서를 지킨다.

```text
사용자 원안
  -> 기존 Git 비전·결정·후보와 대조
  -> Git candidate/draft로 원안과 관계 판정 보존
  -> commit + push + controller 확인
  -> Notion에 같은 상태로 투영
```

- 아이디어 보존은 구현 허가가 아니다.
- 후보 승인은 핵심 비전 승격이나 구현 허가가 아니다.
- 기존 핵심을 전복하거나 우선순위를 바꾸려면 별도 ADR과 이사님 결정이 필요하다.

## 6. 런타임 예외

비밀, token, cookie, session, private payload, mutable lease와 상세 runtime event는 Git에 넣지 않는다. 이들은 승인된 runtime 저장소에 둔다. Notion에는 sanitized 상태만 표시하며, 근거 receipt 또는 검증된 Git milestone을 함께 가리킨다. 이 예외는 제품 아이디어나 결정을 Notion에만 저장할 권한이 아니다.

## 7. 위반 처리

Git 근거가 없는 프로젝트 내용이 Notion에 발견되면 다음을 즉시 수행한다.

1. 해당 Notion 내용을 제거하거나 `INVALID — NO GIT SOURCE`로 숨긴다.
2. 추가 Notion 투영을 중단한다.
3. 원안을 Git candidate로 보존할지 폐기할지 판정한다.
4. 사고 원인과 정정 commit을 기록한다.
5. 위반 agent의 repo/reporting 권한은 이사님이 다시 허가할 때까지 fail-closed로 본다.

Notion 내용을 근거로 Git을 뒤늦게 꾸미거나, Notion의 높은 우선순위를 Git 결정처럼 역수입하지 않는다.
