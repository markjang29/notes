---
title: Codex·ZCode 토큰 예산 및 작업 라우팅 v1
status: active
updated: 2026-07-17
owner: windows-codex
---

# Codex·ZCode 토큰 예산 및 작업 라우팅 v1

## 문제 진단

- 2026-07-15~17 로컬 Codex 세션은 각각 18, 69, 56개였다.
- 세션별 마지막 `token_count`를 합산한 로컬 계측에서 입력의 약 97.5%가 캐시 입력이었다. 이 값은 계정 한도 차감량이 아니라, 긴 컨텍스트가 여러 세션과 반복 턴에 재투입된 정도를 보는 진단 지표다.
- Director Console 반복 수정, Matrix 아키텍처 다회 보강, Windows/Linux 패키징, 작은 변경마다 전체 회귀, 10분 단위 무변경 관제, 긴 worker receipt의 메인 대화 재삽입이 주된 낭비였다.
- 현재 Windows Codex 설정은 `gpt-5.6-sol`/`ultra`이며 Fast mode는 켜져 있지 않다. 따라서 Fast mode 배수보다 깊은 추론과 반복 컨텍스트가 핵심 원인이다.

## 즉시 적용 예산 규칙

1. 메인 관제 보고는 변화·산출물·막힘·다음 행동을 합쳐 8줄 이내로 쓴다. 원문 로그는 파일과 commit으로 참조한다.
2. worker에게 전체 대화를 복제하지 않는다. 필요한 파일과 2,000토큰 이내 frozen packet만 전달한다.
3. 구현 중에는 관련 테스트만 실행하고, 전체 회귀는 release candidate마다 정확히 한 번 실행한다.
4. 독립 검수자는 기본 1명이다. 운영 배포·보안·비가역 변경만 최대 2명까지 허용한다.
5. 상태 변화가 없으면 재조회하지 않는다. 무변경 관제는 최소 30분 간격으로 하고 event receipt가 있으면 즉시 갱신한다.
6. 각 5시간 구간의 최소 30%는 사용자 대화·아이디어·의사결정 대응용으로 남긴다.
7. 사용자에게 보이는 MVP와 일일 Arca terminal 수집을 아키텍처 심화·다중 플랫폼 재현보다 먼저 끝낸다.

## 역할 분담

| 작업 | windows-codex | windows-zcode | AWS Claude/Z.AI 팀장 |
|---|---|---|---|
| 사용자 대화·우선순위·의미 판단 | 소유 | 금지 | 제안만 |
| 로그인·쿠키·브라우저·lease·lifecycle | 소유 | 금지 | 금지 |
| AWS 제어·배포·rollback | 소유 및 최종 승인 | 금지 | 명시된 bounded 작업만 |
| Git 통합·commit·push·완료 판정 | 소유 | 금지 | 금지 |
| frozen 저장소 인벤토리·스키마·lint | 검수 | 수행 | 필요 시 보조 |
| 중복·누락·참조 정합성·로그 분류 | 검수 | 수행 | 프로젝트별 후보 제안 |
| exact-file 수정안 | 최종 판단·적용 | 제안 | 제안 |
| 시나리오·RPG 아이디어 | 방향 결정 | 구조 점검만 | bounded 후보 생성 |

## ZCode 배치 정책

- ZCode는 간단한 일마다 호출하지 않는다. 하루 1회 또는 입력이 5개 이상 쌓였을 때 `daily-pipeline-health`로 묶는다.
- 묶음 범위는 schema/lint, ID·digest·source reference 중복, parser 필수 필드, candidate/promotion/dashboard projection drift, exact-file patch 제안이다.
- 결과에는 점검 항목별 이름·판정·근거·수정 대상 파일이 반드시 있어야 한다. 개수 요약만 있으면 controller가 반려한다.
- 반려된 동일 packet은 자동 재호출하지 않는다. done criteria를 좁혀 다음 배치에 포함한다.
- `windows-zcode`는 live login, controller secret, AWS control, shared state write, Git push를 하지 않는다.

## 확인된 구조 갭

현재 actor registry의 정식 ID는 `windows-zcode`지만 로컬 bridge packet은 `zcode`를 사용한다. bridge가 정식 actor ID와 packet digest를 Agent Mail v2에 직접 연결하기 전까지 bridge receipt는 transient evidence이며 durable Agent Mail 완료로 세지 않는다.

