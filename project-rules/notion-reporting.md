---
title: Notion 보고 투영 규칙
status: active
date: 2026-07-16
authority: principles/git-first-project-truth.md
---

# Notion 보고 투영 규칙

이 문서는 사칙 `principles/git-first-project-truth.md`를 Notion 작업에 적용하는 절차다. 사칙과 충돌하면 사칙이 우선한다.

## 보고 단위

모든 프로젝트 카드나 섹션은 최소한 다음 근거를 가진다.

- `source_repo`
- `source_commit` — full 40-character commit
- `source_refs` — exact repo-relative paths
- `source_status`
- `projected_at`

## 순서

1. 기존 Notion 페이지를 읽는다.
2. 대상 Git repo·branch·remote·clean/dirty 상태를 확인한다.
3. Git 원문의 상태와 위계를 확인한다.
4. commit과 push를 확인한다.
5. Git에서 읽은 사실만 쉬운 한국어로 투영한다.
6. 다시 fetch하여 source block, 상태, 핵심 숫자를 확인한다.

## 동기화

- Git 변경·폐기·supersede를 발견하면 같은 보고 작업에서 Notion을 갱신한다.
- 정본을 재검증하지 못하면 오래된 내용을 최신으로 단정하지 않고 투영을 중단한다.
- Notion에서 직접 받은 사용자 입력은 원문을 잃지 않게 Git candidate로 먼저 보존한 뒤 투영한다.
- Notion 페이지의 버튼·상태 변경은 Git 결정이나 구현 허가가 아니다.
