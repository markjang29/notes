---
title: ADR — Godot 4.7 엔진 + 모듈식 프로토타입 아키텍처 (rpg_game)
date: 2026-07-01
tags:
  - adr
  - rpg_game
  - engine
  - architecture
---

# ADR — Godot 4.7 엔진 + 모듈식 프로토타입 아키타입 (rpg_game)

## 상태
accepted (2026-07-01, 이사님 확정)

## 날짜
2026-07-01

## 프로젝트 / 적용 범위
rpg_game (걷기×전술 RPG) — 엔진·빌드 체인·데모 아키텍처 전반.

## 결정
1. **엔진: Godot 4.7** (GDScript, GL Compatibility 렌더러), 타겟 **모바일 Android 우선**.
2. **아키텍처: 모듈식 프로토타입 개발.** 각 메커니즘을 독립 실행 가능한 모듈(`demo/modules/<이름>/`)로 프로토타입 → 폰 검증 → 모듈 라이브러리 적립 → 본편 조립. 공통 헬퍼는 `demo/shared/`.

## 맥락
- 2026-06-26 컨셉 수렴(걷기=입장재화 + 전술PvP/PvE + 로맨스 + 진영 분기) 후 엔진 ADR이 미결정으로 남아 있었음(`memory/concept-convergence` "How to apply").
- "손맛/체감은 폰에서 만져봐야 안다" — 큰 단위로 한 번에 짜면 실패 비용이 크고, 재미 검증이 늦음.
- 서버 헤드리스 빌드 체인(Linux EC2)에서 폰까지의 루프를 빠르게 돌려야 함.

## 제약
- 서버: Ubuntu 24.04 EC2, 화면 없음(헤드리스), 메모리 6.7G/디스크 150G.
- 이사님 환경: Android 폰, Telegram 비대화형(cokacdir).
- 외부 그래픽 에셋 파이프라인 부재 → Godot 내장 primitive/셰이더/절차 합성 사운드로 자급.
- 다중 에이전트 협업(Windows 머신과 repo 공유) → pull→push 규칙.

## 선택한 이유 / 버린 대안
- **선택: Godot 4.7**
  - 경량·오픈소스, GDScript = 빠른 프로토타이핑, 헤드리스 CLI 빌드 지원, 모바일(GL Compat) 안정.
  - 절차적 에셋(draw API, 셰이더, AudioStream)으로 외부 의존 없이 폰 손맛 구현 가능.
- 버린 **Unity(C#)** — 무거움, 헤드리스 CLI 빌드 번거로움, 라이선스/의존 비대. 프로토타입 속도에서 불리.
- 버린 **웹(Phaser/PixiJS/TS)** — 모바일 네이티브 감각(진동·히트스톱·셰이크) 한계, 오프라인 배포 번거로움.
- **선택: 모듈식 아키텍처**
  - 작은 루프를 빨리 폰에 올려 검증 → 재사용 가능한 자산(FX/사운드/판정) 축적.
  - 이미 1→2 모듈에서 `shared/` 재사용 성공(parry → grid_parry).
- 버린 **monolithic 데모** — 한 메커니즘 실패 시 전체 날림, 재사용 어려움.

## 트레이드오프
- 얻은 것: 빠른 검증 루프 / 모듈 재사용 / 실패 비용 분산.
- 잃은 것: 모듈 간 결합 없음(본편 조립 시 통합 씬 설계 별도 필요) / 중복 가능성(공통 헬퍼 승격 판단 부담).
- 레거시 APK 빌드(`use_gradle_build=false`) 채택 — 헤드리스에서 가장 간편, 단 Gradle 전용 기능(커스텀 안드로이드 코드) 사용 불가.

## 검증 기준
- [x] 빌드 체인: Godot 4.7 헤드리스 → Android 디버그 APK 서명·검증 통과.
- [x] 모듈 1(parry): 폰 작동 확인(이사님 "실행 잘 되는거 같고").
- [x] 모듈 2(grid_parry): APK 빌드·폰 전송 완료(체감 피드백 대기).
- [x] 모듈 재사용: shared/ FX·SFX 가 grid_parry에 그대로 적용됨.
- [ ] 이사님 폰 체감 피드백(telegraph/비행/판정) — 통과 시 grid_parry 검증 완료.

## 실패 / 복구 과정
- **Godot 헤드리스 빌드 함정 4종** (DEVELOPMENT.md "빌드 노하우"에 정리):
  1. export template 위치 — `4.7.stable/` 바로 아래에 둬야 인식(templates/ 서브디렉토리 아님).
  2. SDK/JDK 경로 — 환경변수가 아니라 `~/.config/godot/editor_settings-4.7.tres`의 `export/android/*` 키.
  3. Gradle 빌드 대신 레거시(`use_gradle_build=false`) — android build template 별도 설치 불필요.
  4. `compress_native_libraries=false` + ETC2/ASTC 텍스처 압축 on.
- APK 50MB 초과 시 Telegram 전솝 불가 → arm64만 넣어 55→27MB 절감, 또는 서버 HTTP(80포트) 링크.

## 후속 재검토 조건
- 본편 조립 시점: 모듈 통합 씬 구조 재설계(모듈 간 통신·씬 전환·메뉴).
- 그래픽 에셋 파이프라인 도입 시: 절차적 에셀 의존 축소, 빌드 크기 재평가.
- 모듈 5개+ 적립 시: shared/ 승격 기준 명문화(재사용 2회 임계 — persona §3).
- 튜닝값(판정 윈도우·속도·이펙트)은 본편 조립 시점에 일괄 확정(지금은 _TUNE 상수에 모아둠).

## 관련 링크
- commit `99ddf9c` (parry 모듈 + DEVELOPMENT.md), `cc713b8` (grid_parry 모듈).
- repo: `rpg_game/DEVELOPMENT.md` (개발 원칙·컨벤션), `rpg_game/demo/` (Godot 프로젝트).
- 회의록: `notes/meetings/2026-07-01-rpg-parry-demo-and-module-architecture.md`.
- 선행: `memory/concept-convergence-walking-rpg.md` (컨셉 수렴 — 본 ADR이 "엔진 ADR" 빈칸 메움).
