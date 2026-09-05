---
title: 홈서버 이관·통합 종합 설계 v1 (4차 외부 의견 종합)
date: 2026-09-04
status: 설계 완료 — 이사님 승인 대기
tags:
  - agent-ops
  - infra
  - design
---

# 홈서버 이관·통합 종합 설계 v1

> 근거: 조사 정본 homeserver-migration-research.md(외부 4차 의견: Gemini·GPT·기술상세·엣지설계) +
> 우리 기존 자산(회의방 8023·대시보드 8025·사칙 체계·원장 3종·감사 evaluator).
> 한 줄 요약: **봇 20기는 남긴다(입구·인격), 배관은 하나로(하네스·진입·원장), AWS는 없애지 않고 엣지로 축소.**

## 1. 네트워크 토폴로지 (외부 의견 수용 — 판정 동일)

- Internet → tiny AWS/VPS 엣지(Caddy :443, 공개 서비스만) → Tailscale → 홈 Caddy → Spring/React.
- 원칙: 관리 페이지·DB·SSH·AI 러너·Grafana = **tailnet 전용**(Tailscale Serve). Funnel은
  "URL 아는 누구나" 접근 가능하므로 민감 서비스 금지.
- AWS 역할 소결(결정안 ③의 답): **완전 퇴출이 아니라 엣지 축소** — 텔레그램 관문(cokacdir)·LLM 키
  게이트웨이·공개 게이트웨이/폴백만 잔존. 봇 20기의 통신 지각이 끊기지 않는 가장 안전한 경로.

## 2. N100 3대 역할 (작업=논리, 머신=실행역량)

- **#1 Linux — Control Plane**: Caddy·Tailscale·Spring·React·관제페이지·모니터링·CI runner.
- **#2 Windows — AI Agent Worker**: claude/codex/zcode 러너, worktree 실행, test/build worker.
  (권고: 안정화 후 Linux 전환 시 Docker·CI·ssh 운영이 단순해짐 — 이사님 별도 결정)
- **#3 Windows — 특수 Worker**: 브라우저/UI 테스트, 백업, 실험 환경.
- 핵심 규칙: **서버에 팀을 고정하지 않는다.** #2가 죽어도 "RPG팀이 죽는 것"이 아니라 #3이 task를
  이어받는다. 팀(봇)은 입구·인격일 뿐, 실행은 가용 머신이 받는다.

## 3. 실행 하네스 — Task 중심 (GPT안 확정 반영)

- 봇 = 서로 다른 **입구/프리셋**(persona·context 유지 — 회의방 BOTS 구조 그대로). 뒤에서는
  하나의 Task API → Harness로 수렴.
- Task Contract 7필드 필수: repo·인수조건·허용 모듈·원천(source-of-truth)·예상 테스트·금지 변경·
  산출 형식. 병행 작업은 git worktree 격리.
- 게이트: 빌드·테스트·린트·**아키텍처(Spring Modulith verify())**·**데이터 provenance**·보안·UI.
- Evaluator = 감사봇(모델 분리 유지: codex×claude 교차 검증).

## 4. 정책 버전 관리 — POLICY_SHA (활성 공지의 상위판)

- platform-policy 저장소 = **우리 notes repo 그대로 사용**(사칙·원장·ADR 이미 존재 — 새 repo 불필요).
  POLICY_VERSION + HEAD SHA로 증명.
- 모든 작업 결과·티켓·보고에 `POLICY_SHA=<notes HEAD>` 기록 → 관제 화면에서 봇별 정책 버전 가시.
  "3개월 뒤 누가 읽었는지 모른다" 문제의 기계적 해결. 활성 공지(8023)는 이 버전의 배포 채널이 된다.
- 스킬은 정책과 함께 버전링 — skills.json 등록제(후보→실측→채택)를 VERSION 안에 편입.

## 5. 관제 화면 원칙 — 핵심 객체는 AI가 아니라 Task

- Task 카드 표준: Project·Goal·Status·Planner/Builder/Reviewer·Repo·Worktree·Commit·
  Policy SHA·게이트 결과(Architecture/Tests/Data/UI)·Runtime(노드·CPU·RAM)·Deploy(staging/production).
- 모델이 바뀌어도(예: Opus→Sonnet) **Task history는 그대로 남는다** — 관제 5축의 "담당업무"축이
  이 카드의 뷰가 된다(ADR 2026-09-04 5축과 연결).

## 6. 이관 순서 (Strangler 3단계 + 마일스톤)

1. 선행: 포트 레지스트리(services.json) · repo 규칙 표준(AGENTS.md/CLAUDE.md 헌법) · 티켓 템플릿
   7필드 개정 · provenance 6필드 표준 초안. ← **매니저 즉시 착수 가능**
2. 엣지: AWS 엣지 Caddy + Tailscale 조직망(5거점+홈 3대 편입) · 홈 Caddy 단일 진입.
3. 통합: matrix-studio-spring을 Modulith 코어로 승격(이미 React 동서빙 실측됨) → 기능 단위 어댑터
   이전(Phase A Spring→Python→Mongo) → DB 직결(B) → canonical DB(C) → Python 종료.
4. 상시: 게이트 통과 증명만 이사님께(2단 승인) — 딥리딩 제거.

## 7. 기존 자산 매핑 (버리는 것 없음)

- 회의방 8023 = 봇 입구·프리셋 + 활성 공지(정책 배포 채널로 승격).
- 대시보드 8025 = Task 카드 뷰(5축) · roster/roadmap/skills 원장 그대로 원장.
- 감사 evaluator · 사칙(헌법) · ADR/의사결정 축 · 지라 = 전부 설계 안에 흡수.

## 8. 리스크

- #2 Windows AI 러너의 실행 재현성(세션·토큰·경로) — Linux 전환 전까지 러너 스크립트 표준화로 완화.
- 테일스케일 제어 평면 SaaS 의존 — 개인 개발 허용선, 필요 시 Headscale.
- Strangler 기간 동안 이중 비용(파이썬+Spring 병존) — 기능 단위 티켓으로 분할 상환.
- AWS 엣지 잔존 시 비용 최소 확인(작은 인스턴스 + 스토리지).

## 9. 결정 안건 (간소화 — 이 설계 승인이 곧 4건 소결)

1. **본 종합 설계 v1 승인 여부** (토폴로지·N100 역할·하네스·POLICY_SHA·Task 중심 관제 포함).
   - 승인 시 ③AWS 잔존범위="엣지 축소", ②Spring=스트랭글러, ①테일스케일, ④하네스 표준이 함께 확정됨.
2. N100 #2의 (선택) Linux 전환 — 나중에 결정 가능(보류 가능).
3. 첫 실무 배정 승인: 티켓 템플릿 7필드 개정 + provenance 6필드 표준 초안(매니저 즉시).
