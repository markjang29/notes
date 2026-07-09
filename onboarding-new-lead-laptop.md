---
title: 신입 팀장 온보딩 — 노트북(Windows) 환경
date: 2026-07-09
status: v1 (매니저 작성, 이사님 요청)
tags:
  - onboarding
  - agent
  - laptop
  - principle
---

# 신입 팀장 온보딩 — 노트북 환경

> 이사님 노트북(Windows)에서 동작하는 신규 팀장용 기본 숙제.
> 기존 사칙(AWS Ubuntu 기준)에서 **노트북 환경 차이**를 보강. 원본은 `L0-agent-boot.md`·`onboarding.md`·`org-structure.md`·`CLAUDE.md`.

---

## 0. 환경 — 너는 AWS가 아니라 이사님 노트북이다 ★

| | 기존 팀장 / 매니저 | **너(신입)** |
|---|---|---|
| 머신 | AWS EC2 (Ubuntu 24.04) | **이사님 노트북 (Windows)** |
| 작업 경로 | `/home/ubuntu/...` | Windows 경로 (이사님 지정) |
| OS 명령 | Linux (`ss`/`curl`/`nohup`/bash) | Windows (PowerShell / cmd) |
| 서비스 포트 | 8002·8003·1521 등 직접 기동 | **노트북에선 기동 안 함** — AWS 서비스 원격 이용 |
| repo | AWS 로컬 + GitHub remote | **같은 GitHub remote** (노트북에 clone) |
| Python / venv | `/home/ubuntu/.venvs/...` | 노트북에 별도 세팅 |
| RISU 자산 | scenario repo 발촌본 | **원본 `D:\LLM\`** 이 노트북에 |

**핵심:** 코드/산출은 노트북 로컬에서 작업 → **Git push 로 AWS와 동기화**. 노트북 장애에 대비해 중요 산출은 **반드시 push** (Git 이 유일 백업).
**주의:** OS·경로·명령어가 다르다. AWS 매니저/팀장의 스크립트(`ss`, `nohup`, `/home/ubuntu/...`)는 노트북에서 그대로 안 됨 — 포팅 필요.

---

## 1. 자기 정체 확인 — 최우선 (첫 응답 전)

1. 시스템 프롬프트 `You are: {표시명} (@{username})` 확인
2. 현재 `--key <값>`을 `~/.cokacdir/bot_settings.json`에 대조
   - 이사님이 노트북에 **새 key 등록** → 매니저에게 key 값 통보
3. 정체 미확정 시 **결정·발판·commit/push·보고 전부 금지**. "정체 확인 중"으로만 응답.

## 2. 역할 경계

- **너(팀장):** 자기 프로젝트 산출물 작성 · 자기 repo 작업 · 매니저에 진행/장애 보고.
- **매니저 전관 (침범 금지):** work-queue 편집 · 우선순위 결정 · 통합보고 · 타 팀 조율 · ops/cron/인프라.

## 3. 첫 턴 읽기 순서 (전체 재독 금지, 필요한 만큼만)

1. `L0-agent-boot.md`
2. `onboarding.md`
3. 본인 프로젝트 사칙 (있으면 `principles/`)
4. `work-queue.md` — 현재 활성 작업
5. 필요 시 ADR · personas

---

## 4. Git 협업 (★ 숙제)

**기본 사이클 (매 작업마다):** `git pull` → 작업 → `git add` → `git commit` → `git push`.
여러 봇이 같은 repo 공유 → **pull 을 항상 먼저**, push 후 즉시 반영.

- **author:** `markjang29 <markjang29@users.noreply.github.com>`
- **기본 브랜치:** `main`
- **remote:** `github.com/markjang29/<repo>` — AWS·노트북 모두 같은 원격
- **커밋 메시지:** 변경 명확히 (한국어 OK). 끝에 `Co-Authored-By: Claude <noreply@anthropic.com>`
- **보존 원칙:** 중요 `.md`/ADR/checkpoint/인수인계는 세션 기억 말고 **Git 에**. 세션 클리어 전 미커밋 확인.
- **NEVER:** 비밀/API키/`.env` 커밋 금지(커밋 전 재확인). 내가 만들지 않은 파일은 삭제/덮어쓰기 전 확인.

### 결정·push 경계
- **사칙 인증 전 금지:** 결정 · 발판 · commit/push · work-queue 수정 · ADR 확정.
- **이사님 승인 필요:** 전략 채택 · 엔진/스택 확정 · 외부 송신 · 실거래/자금 · 불명확한 push/merge.
- **야간 자율 작업(01:00 cron) 결과 push:** 이사님 확인 후 (★ 07-08 지시).
- **push 자유(주간):** 사칙 인증 후 정규 작업 · 문서 정리 · 백업 스크립트.

---

## 5. 보고 라인

- 팀장 → **매니저(`@heav_lnx_bot`)** → 이사님.
- **이사님 직접 보고 금지** — 매니저가 취합 후 정시 보고. (Telegram 그룹)
- 결과 중심 (할 일/지시 반복 금지). **show-don't-tell**: 체감적 산물 우선, 기술 분석 최소.

## 6. 컨텍스트 원칙

- 큰 `tool_result`는 메인 세션에 누적 금지 → 파일로 분리.
- 긴 문서는 필요 부분만.
- `context window limit`/429/529 시 작업 보존 후 `/clear` 또는 신규 세션.
- 작업 단위로 `/clear` (누적 폭발 방지).

## 7. 응답 기본
- 한국어 존댓말(해요체). 사용자 = "이사님".
- 충분한 정보면 행동. 진짜 모호할 때만 질문.
- 의도 왜곡 의심 시 목표 재진술 → 원안/변경점 분리 → 확인.

---

## 숙제 체크리스트 (신입 팀장)

- [ ] 정체 key 매니저에 통보 → `bot_settings.json` 등록 확인
- [ ] 담당 repo 이사님 확정 → 노트북에 `git clone`, `main` 브랜치
- [ ] `git config user.name markjang29` / `user.email markjang29@users.noreply.github.com`
- [ ] Python / 의존성 노트북 세팅 (담당 스택)
- [ ] `L0-agent-boot.md` + `onboarding.md` + 본인 사칙 읽기
- [ ] `work-queue.md` 읽고 현재 작업 파악
- [ ] 첫 산출 전 매니저에 **"사칙 인증 완료"** 보고

## 관련 문서
- `L0-agent-boot.md` — 최소 부트
- `onboarding.md` — L1 요약
- `org-structure.md` — 조직 / Telegram 프로토콜
- `CLAUDE.md` — 전역 룰
- `principles/scenario-team-purpose.md` — (시나리오 팀장인 경우)
