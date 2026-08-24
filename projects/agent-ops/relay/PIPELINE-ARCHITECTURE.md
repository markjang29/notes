# 통합 자산 파이프라인 아키텍처 v1 (RELAY-49 정본)

> 이사님 2026-08-24 지시. 설계 담당: zcode (SE 롤). 변경은 이사님 결정 + 본 문서 수정로만.

## 0. 한 줄 그림

**식재료 창고(수집) → 테스트 주방(리수 검증) → 품질검수대(승인보드) → 정규 레시피 등록(매트릭스화) → 매장 진열(아케이드) → 음식 사진(이미지 스튜디오) → 프랜차이즈 매뉴얼(코어 디벨롭) → 출점(수익화 작품)**

## 1. 파악 결과 — 사이트 7개 실측 (08-24)

| 포트 | 이름 | 목적 | 상태 |
|---|---|---|---|
| 8013 | PocketRisu | 리수 실행 환경 (검증 소요) | 가동 |
| 8015 | Matrix Workbench | 리수 프리셋 세팅·검증 (플랜→자산→3회 채팅 전문) | 가동 (TRACK-1) |
| 8005 | 승인보드 | 검증 확인·승인 (⭐통합 대기열) | 가동 |
| — | materializer | 승인 판정 → matrix-human-approval-v1 레코드 | 구현됨, releases 연결 미완 (releases=0) |
| 8004 | 아케이드 | 매트릭스화 자산 선택·재테스트 (PLAYABLE) | 가동 |
| 8016 | 이미지 스튜디오 | 검증 자산 이미지 생성 (SFW/NSFW 분리) | 가동 (RELAY-41) |
| 8010/8011/8012 | 매트릭스 엔진·ZCODE·Codex | 사건 원장·코어 | 8011 복구 대기 (RELAY-12 보류) |

## 2. 파이프라인 7단계 (입출력 계약)

```
[S0 수집]      원본 byte + sha256 대장 (COLD CAS)          ← novel_col / 수집기
     ↓ source-unit JSON (matrix-source-unit-v1)
[S1 리수 검증] 8015 프리셋(카드+모듈+로어+모델+NAI) → 3회 채팅 실사
     ↓ 검증 리포트 (플랜 id + 전문 + 판정 데이터)
[S2 승인]      8005 승인보드 — 이사님 전문 열람 → O/X/보류
     ↓ approval 레코드 (matrix-human-approval-v1, 서명)
[S3 매트릭스화] ★구상 필요★ materializer → release publication
     ↓ matrix_components.ndjson + provenance(실사 SHA) — release ID
[S4 아케이드]  8004 — release ID 단위 선택·재테스트(PLAY 배지)
     ↓ 아케이드 실사 기록 → 정오회수(리콜) 조건
[S5 이미지]    8016 — 검증 자산에 이미지 자동 제안(core→NAI)
     ↓ 이미지 매니페스트 (category·policy_gate)
[S6 코어 디벨롭] CLI → AGENT → 하네스화 (렌즈·감독개입·월드스모크)
     ↓ 수익화 작품: RPG · 신규 소설 (자동 납품 구조)
```

**연결 열쇠 = 자산 ID 체계** (이미 존재): sha256(원본) → source-unit → workbench plan → approval → release ID. 지금 각 사이트가 이 ID를 제각각 부르는 게 유일한 단절점.

## 3. 구멍 — S3 매트릭스화 (유일한 미구축 단계)

재료는 다 있다: 계약(삼중보관 ADR-0005)·materializer·스키마(matrix-asset-release-v1)·소비자(8011/8012).
빠진 것: 승인 레코드 → release publication 자동화 + 아케이드가 release ID를 읽는 어댑터.

## 4. 로드맵 — 트랙 토폴로지 (병렬 가능)

```
TRACK-1 (사용성)  ──────────────► 이사님 체험승인 ──┐
TRACK-A (연결)    S3 매트릭스화 구축 ─► 아케이드 release 연결 ──┤합류
TRACK-B (이미지)  스튜디오×자산 자동제안 (RELAY-13/14) ─────────┤
TRACK-2 (대량)    페르소나 324 파싱 (체험승인 해제 후 개시) ◄─┘
TRACK-3 (코어)    8011복구 → 월드스모크·렌즈·감독개입 → CLI-AGENT-하네스
TRACK-4 (작품)    RPG · 신규 소설 (TRACK-3 산출 소비)
```
병렬 규칙: TRACK-1·A·B 동시 가능(다른 repo·다른 담당). TRACK-2는 TRACK-1 완료 후, TRACK-4는 TRACK-3 완료 후.

## 5. 담당 배분

| 트랙 | 담당 | 산출 |
|---|---|---|
| TRACK-1 | asset_agent + zcode(NSFW) | 프리셋·체험 승인 |
| TRACK-A | zcode | S3 publication 자동화 + 아케이드 어댑터 |
| TRACK-B | asset_agent(SFW)/zcode(NSFW) | 이미지 자동 제안 |
| TRACK-2 | asset_agent | 324 파싱·태깅 |
| TRACK-3 | zcode(계약) + scenario(월드스모크) | 코어·하네스 |
| TRACK-4 | rpg 팀장 + scenario 팀장 | 작품 |
| 게이트 운영 | 매니저·감사(audit) | 승인보드·포트단속 |

## 6. 기존 티켓 재배치
- TRACK-1: RELAY-1·8·13·14 + RELAY-49(본 설계)
- TRACK-A: 신규 2건 (S3 자동화, 아케이드 연결)
- TRACK-2: RELAY-24(페르소나)·2(로어북)
- TRACK-3: RELAY-12(8011)·10(월드스모크)·11(감독개입)·23(렌즈)
- 유지: 15(포트단속)·19·20(승인보드)
