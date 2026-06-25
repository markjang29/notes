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
  - `~/vault` — Obsidian / 작업노트 Markdown
  - `~/scripts` — 서버 관리 스크립트
- [x] 작업 컨텍스트(메모리)는 cokacdir workspace 하위에 보관
- [x] Node.js / Python 베이스로 개발 시작

## 설치한 것

- [x] **Claude Code CLI** `v2.1.191` — `/home/ubuntu/.local/bin/claude`
- [x] **cokacdir** (Telegram 연동 브리지) — `/usr/local/bin/cokacdir`
- [x] **Node.js** `v22.23.1` + **npm** `10.9.8`
- [x] **Python** `3.12.3` + **pip** `24.0`
- [x] **Git** `2.43.0`

## 다음 할 일

- [ ] Git 전역 사용자 정보 설정 (`user.name`, `user.email`) — 현재 미설정 상태
- [ ] `~/vault` Git 원격 저장소 연결 및 동기화(백업) 전략 수립
- [ ] `~/scripts` 에 서버 관리/운영 스크립트 추가
- [ ] 필요 시 Docker / Go / Rust 설치 검토 (현재 미설치)
- [ ] `~/projects` 첫 프로젝트 세팅
- [ ] 정기 백업 / 스냅샷 스케줄 확인

## 메모

- 현재 이 노트는 `~/vault` 최초 커밋에 포함됨.
- AWS 인스턴스 IMDS 응답 제한으로 instance-id/region은 수동 확인 필요.
