---
title: RPG Git 정본 연결 공백
date: 2026-07-16
status: open
owner: windows-codex
project: rpg_game
---

# RPG Git 정본 연결 공백

## 확인된 사실

- Windows의 `rpg_game` 로컬 폴더는 현재 Git worktree가 아니다.
- 이 폴더의 Godot `Title -> Battle -> Result` 프로토타입을 RPG 정본 구현 상태로 주장할 수 없다.
- Notes Git에는 RPG 시그니처와 Walk-to-Play 결정이 있으므로 제품 방향은 확인할 수 있다.
- actor registry는 실제 RPG 정본을 `rpg_game` repo와 그 `project-rules`로 가리킨다.

## 운영 판정

- 실제 AWS/GitHub `rpg_game` repo의 remote, branch, full HEAD, clean/dirty 상태와 project rules를
  검증하기 전에는 RPG 구현 진행률·완료·우선순위를 Notion에 투영하지 않는다.
- unversioned Windows 폴더를 먼저 Git 정본처럼 꾸미거나 덮어쓰지 않는다.
- 실제 repo를 확인한 뒤 Windows clone/worktree와 portable pointer를 명시적으로 연결한다.

## 완료 조건

1. 실제 `rpg_game` remote와 정본 branch를 확인한다.
2. full HEAD와 upstream 일치를 확인한다.
3. `project-rules` 또는 동등한 최상위 규칙을 확인한다.
4. Windows의 unversioned 폴더와 실제 Git 내용 차이를 읽기 전용으로 비교한다.
5. 보존·폐기·이관 범위를 이사님에게 보고하고 승인된 방식으로 연결한다.
6. 이후 Notion RPG 현황은 검증된 full commit과 exact refs만 사용한다.
