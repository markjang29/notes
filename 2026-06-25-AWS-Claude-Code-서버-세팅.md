---
title: AWS Claude Code 서버 세팅
date: 2026-06-25
tags:
  - aws
  - claude-code
  - dev-server
---

# AWS Claude Code 서버 세팅

> 2026-06-25 기준 개발 서버 초기 세팅 정리.
> Ubuntu 24.04 (AWS EC2) + Claude Code CLI + Telegram(cokacdir) 연동 환경.

## 서버 스펙 요약

| 항목 | 값 |
|---|---|
| OS | Ubuntu 24.04 LTS (Linux 6.17.0-1010-aws) |
| 플랫폼 | AWS EC2, x86_64 |
| CPU / 메모리 | 2 vCPU / 7.6 GiB |
| 디스크 | 154 GB (사용량 2%) |
| 사용자 | `ubuntu` (홈: `/home/ubuntu`) |

## 결정사항

- [x] OS: Ubuntu 24.04 LTS (AWS 관리 이미지) 채택
- [x] Claude Code를 Telegram에서 구동 — `cokacdir` 브리지로 연동
- [x] 홈 디렉토리 용도 분리
  - `~/projects` — 개발 프로젝트
    - `autotrader` → `github.com/markjang29/autotrader` (자동매매 시스템)
    - `rpg_game` → `github.com/markjang29/rpg_game` (파랜드 택틱스풍 전술 RPG)
    - `scenario` → `github.com/markjang29/scenario` (시나리오/RISU 자산·자생 서사, 2026-06-30 추가)
  - `~/notes` → `github.com/markjang29/notes` (Obsidian / 작업노트)
  - `~/scripts` — 서버 관리 스크립트
- [x] 작업 컨텍스트(메모리)는 cokacdir workspace 하위에 보관
- [x] Node.js / Python 베이스로 개발 시작
- [x] **다중 에이전트 협업 구성**: Linux 서버(본 머신) + Windows 머신(별도 에이전트) — 모든 작업은 git/notes로 상세 공유

## 설치한 것

- [x] **Claude Code CLI** `v2.1.191` — `/home/ubuntu/.local/bin/claude`
- [x] **cokacdir** (Telegram 연동 브리지) — `/usr/local/bin/cokacdir`
- [x] **Node.js** `v22.23.1` + **npm** `10.9.8`
- [x] **Python** `3.12.3` + **pip** `24.0`
- [x] **Git** `2.43.0`

## 다음 할 일

- [x] Git 전역 사용자 정보 설정 — `markjang29` / GitHub noreply 이메일
- [x] `~/notes` 원격 저장소 연결 (`github.com/markjang29/notes`)
- [x] 프로젝트 저장소 초기 세팅 (`autotrader`, `rpg_game`)
- [x] **GitHub 인증 완료** — classic PAT 저장(credential helper), 3개 저장소 push 성공 (2026-06-25)
- [x] 현재 운영 repo 기준 갱신 — `notes`, `autotrader`, `rpg_game`, `scenario` 총 4개 (2026-07-06)
- [ ] Android Obsidian 에서 `notes` 동기화 세팅
- [ ] 프로젝트별 기술스택 확정 (autotrader: Python? / rpg_game: 엔진?)
- [ ] `~/scripts` 에 서버 관리/운영 스크립트 추가
- [ ] 필요 시 Docker / Go / Rust 설치 검토 (현재 미설치)
- [ ] 정기 백업 / 스냅샷 스케줄 확인

## 메모

- 이 노트는 `~/notes` 저장소에 있으며 `github.com/markjang29/notes` 로 push 됨.
- AWS 인스턴스 IMDS 응답 제한으로 instance-id/region은 수동 확인 필요.
- **협업 규칙**: Windows 머신의 다른 에이전트와 저장소를 공유하므로, 모든 변경/결정/진행상황은 커밋 + 노트로 상세 기록.
