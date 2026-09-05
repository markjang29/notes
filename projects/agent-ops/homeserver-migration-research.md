---
title: 홈서버 이관·통합 전략 조사 (이사님 09-04 고민)
date: 2026-09-04
status: 조사 완료 — 인프라·통합 방식 결정 대기
tags:
  - agent-ops
  - infra
  - research
---

# 홈서버 이관·통합 전략 — 자료조사 정본

> 이사님 고민: ①포트 10개+ 사이트 흩어짐 ②지침 유실 ③파이썬 통합 후에도 객체 파편화·"보이게만" 개발
> ④스킬 중구난방 ⑤git·지라 승인 체계가 딥리딩 부담 → 위임했다가 스파게티 ⑥AWS→홈서버(N100 3대: 리눅스1·윈도우2)
> 이관 ⑦테일스케일 vs 기본 호스팅 미결정 ⑧파이썬·몽고 개별포트 → Spring+React 한 포트 ⑨봇 20기 근접, 텔레그램 조작+관제 페이지
> 외부(Gemini) 조언 수신: 테일스케일+CF Tunnel(관제만), Spring Boot 단일 백엔드 모노레포.

## 1. 외부 경험·글 조사 결과

- **Columbia DAP Lab "코딩 에이전트 9대 실패 패턴"(2026-01)**: UI 그라운딩 불일치·상태관리 실패·
  비즈니스 로직 불일치·데이터 관리 오류·외부 연동 오류 — 우리의 "보이게만 개발"은 비즈니스 로직·데이터
  불일치 실패 패턴과 정확히 같은 것.
- **Atlan "에이전트 하네스 13 안티패턴"**: AI 에이전트 프로젝트 88%가 프로덕션 도달 실패 — 아키텍처·실행·
  데이터 3계층으로 원인 분류. 실패의 공통분모 = 중앙 통제(Governance)·SSOT 부재.
- **Simon Willison agentic 안티패턴**: 최상위 안티패턴 = "검증 안 된 코드를 동료에게 떠넘기기" —
  승인 게이트의 필요성 근거.
- **커뮤니티 가드레일**: "에이전트가 멍청한 짓 못 하게 막는 스킬 파일"(규칙 18+안티패턴 30 체크리스트) —
  가벼운 거버넌스로 유행. 우리의 사칙(L0·onboarding)과 동일 발상.
- **이관 패턴 정석**: Strangler Fig(Azure/AWS 정식 문서) — 빅뱅 재작성 금지, 페이스드(진입 레이어) 뒤에서
  기능 단위로 점진 교체, 새 것과 옛 것이 한 진입점을 공유.
- **스킬 생태계**: awesome-claude-skills(travisvn)·claudeskills.info — 인기 스킬: Superpowers,
  code-reviewer, Frontend Design 등. 선별 기준 없이 넣는 게 바로 "중구난방"의 원인 → 원장(skills.json)
  등록+실측 후 채택 절차 필요.

## 2. 인프라 판정 — 테일스케일 vs 호스팅

**판정: 내부망 = 테일스케일, 외부 노출 = 관제 웹만 최소 노출. Gemini 조언에 동의(조건부).**

- 테일스케일: 3대(리눅스1·윈도우2)를 포트포워딩 없이 가상 사설망(100.x)으로 — DB·봇 API·파일 접근은
  외부 노출 금지 자산이라 맞음. 홈랩 커뮤니티 표준 패턴이기도 함. 완전 자체 소유를 원하면 Headscale(오픈소스
  제어서버) 옵션 존재.
- 주의점: **테일스케일은 제어 평면이 외부 SaaS** — 완전한 자주권은 아님. 개인 개발 용도로는 실무적 허용선.
- 외부 노출: 관제 대시보드·회의방만. 방법은 2개 — (a) Cloudflare Tunnel(도메인+인증, CGNAT 무관),
  (b) 기존 방식(공인 IP 직노출+토큰, 현재 8023·8025 방식). 이관 후 집 회선이 공인 IP를 주지 못하면
  (CGNAT) CF Tunnel이 사실상 필수.
- **놓치기 쉬운 결정(중요)**: AWS에서 홈으로 이관하면 **텔레그램 봇 연결(cokacdir)과 LLM 키 게이트웨이를
  어디에 두나**가 최대 쟁점. 봇 20기의 지각·통신 관문이 지금 AWS에 있음. 완전 이관 시 이 두 가지를 홈
  클러스터로 옮기는 절차가 선행돼야 봇들이 끊기지 않음.

## 3. 아키텍처 통합 판정 — Spring+React 한 포트

**판정: 방향 동의, 방법은 빅뱅 금지 — 스트랭글러(페이스드) 단계적. 단, 전부 Spring이 아니라 역할 분리.**

- **비즈니스 사이트**(시나리오·RPG·arcade·수집 등 사용자 대상 서비스): Spring Boot 단일 백엔드 + React
  단일 프론트로 통합 — 한 포트(리버스 프록시 뒤 이름 기반 라우팅). Spring 경험은 이미 matrix-studio-spring
  (zcode 구현)으로 검증됨.
- **에이전트 인프라**(회의방·대시보드·폴러·프록시): 파이썬 유지가 현실적 — claude CLI 연동·빠른 수정이
  생명. 이것들을 굳이 Spring으로 옮기면 속도만 깨진다. 둘은 **같은 진입 뒤에 공존**하면 된다.
- 몽고DB → 통합 시 단일 DB 원장(Postgres 권장) + **원천→가공 단방향 원칙**: 화면은 원천 데이터에서
  파생된 결과만 보여준다("보이게만" 금지 — 데이터 계보가 코드로 드러나야 함).
- 이관 순서(제안): ① 포트 레지스트리(services.json: 사이트·포트·담당·git·상태) → ② 역프록시 단일 진입
  (Caddy 등, 이름 라우팅) → ③ 기존 사이트 그대로 뒤에 붙임 → ④ Spring 코어 신설 후 기능 단위로 앞당겨
  교체 → ⑤ 파이썬 잔여물은 인프라로 남김.

## 4. 이사님 고민 ↔ 구조적 처방 매핑

- 지침 유실 → 사칙 문서 체계(이미 보유) + 봇 기동 시 사칙 필수 섹션 강제 + 관제 5축의 "의사결정" 축으로
  지시 원문 상시 가시(구축 중).
- 객체 파편화·보이게만 개발 → SSOT 원장들(roster·roadmap·skills) + 원천→가공 단방향 + 검수 게이트(감사).
- 스킬 중구난방 → skills.json 원장 등록절차(후보→실측→채택) — 외부 인기 스킬도 절차 없으면 금지.
- 승인 부담 → 2단 승인: 매니저가 1차 게이트(실측·diff 요약·체크리스트) 통과시키고, 이사님은 증명 요약만
  보고 1커맨드 승인. 딥리딩을 이사님께서 안 하도록 만드는 게 매니저의 일.
- 포트 난립 → 포트 레지스트리 + 단일 진입(위 3절).

## 5. 유용한 스킬 후보 (skills.json 등록 전 — 선별 필요)

- react-best-practices: 이미 조직 표준(설치·실측 완료).
- 후보: Superpowers(작업 워크플로 강화) · code-reviewer(검수 게이트 보강) · Frontend Design(UI 품질) ·
  보안·아키텍처 검토 계열. 절차: 후보 등록 → 담당 봇 실측 → 실측 결과로 채택/폐기.
- 우리가 자체 보유한 것도 원장에 등록: 아키텍처 맵, 데이터시각화 가이드, 동시성·컨텍스트 계측 등.

## 6. Gemini 전문 추가분 평가 (09-04 후속 수신 — 2·3단계 상세)

- **모노레포 도구(Nx·Turborepo) + Spring 같은 레포 React**: 방향 채택, 도구는 단순화 — Nx·Turborepo는
  JS 생태계 전용이라 Spring 혼합엔 과투자. 우리 규모는 **단일 repo(gradle 멀티모듈 + /frontend 폴더)** 로
  충분. 기존 에이전트 인프라 repo는 분리 유지(§3 역할 분리 원칙과 동일).
- **JPA Entity/DB 스키마 SSOT + DTO만 사용 제약**: 채택 — "보이게만(Mocking) 개발" 방지의 정석.
  스키마·마이그레이션 파일이 유일 원천, 화면·봇은 스키마에서 파생된 타입만 사용. 파이썬 인프라에도
  동일 원칙(스키마 → 타입 클라이언트).
- **사전 제약(규칙 파일 — CLAUDE.md·AGENTS.md·.cursorrules)**: 이미 3개월째 운영 중(루트 CLAUDE.md ·
  notes 사칙 체계 · L0 부팅 · 온보딩). 보강 1건: **repo 루트 AGENTS.md 표준화** — claude(CLAUDE.md)·
  codex(AGENTS.md)·zcode가 한 파일로 공통 규칙을 읽게 심볼릭 링크/동기화. 신규 Spring 코어 repo는
  처음부터 이 표준으로 발판.
- **자동화된 제약 하네스(사후 검증을 사람·AI 주관 대신 기계에)**: 채택, 이번 조사의 핵심 처방. CI
  (테스트·타입체크·린트)·브랜치 보호·감사봇 실측 검수가 1차 게이트, 이사님은 증명 요약만 보고 최종
  1커맨드 승인 — §4 "2단 승인"과 동일 결론. 이관 시 자체 CI(예: Gitea Actions) 또는 GitHub Actions
  강제까지 포함.

종합: Gemini 조언과 우리 기존 체계는 약 80% 일치 — 사칙·원장·게이트가 정답이었다는 외부 확인.
남은 갭은 ①기계 게이트(CI) 자동화 ②repo 루트 규칙 표준화(AGENTS.md) ③이관 설계.

## 7. 결정 안건 (이사님)

1. 내부망 테일스케일 채택 + 외부 노출은 관제 웹만 — 승인 여부.
2. Spring 통합 = 스트랭글러 단계적(포트 레지스트리·단일 진입 선행) — 승인 여부.
3. AWS 완전 퇴출인지, 아니면 "텔레그램 관문+LLM 키 게이트웨이만 AWS 잔존"인지 — 이것이 이관 설계의
   최대 분기점.

## 출처

- 실패 패턴: https://daplab.cs.columbia.edu/general/2026/01/08/9-critical-failure-patterns-of-coding-agents.html ·
  https://atlan.com/know/agent-harness-failures-anti-patterns/ ·
  https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/
- 이관: https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig ·
  https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html
- 홈랩: https://tailscale.com/use-cases/homelab ·
  https://www.reddit.com/r/homelab/comments/1qw3c43/selfhosting_guide_secure_remote_access_with/
- 스킬: https://github.com/travisvn/awesome-claude-skills · https://claudeskills.info/ ·
  https://www.firecrawl.dev/blog/best-claude-code-skills
