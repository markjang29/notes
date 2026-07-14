---
title: ZCode 권한 감사 실행 복기
date: 2026-07-14
status: failed-with-action
related_task: ZC-01
---

# ZCode 권한 감사 실행 복기

## 목적

권한 계약 문서를 ZCode가 읽고, 영구 controller 경계와 제한적으로 열 수 있는 권한을
분류할 수 있는지 확인했다. repository 변경 권한은 주지 않았다.

## 실행 시간

| 실행 | wall time | 결과 | 사용량 |
|---|---:|---|---|
| live probe | 7.8초 | 성공 | 2,647 tokens |
| 감사 1차 | 1.3초 | 코드의 절대경로 검증 예시를 입력 필터가 차단 | 모델 호출 전 |
| 감사 2차 | 1.8초 | 문서의 절대경로 예시를 입력 필터가 차단 | 모델 호출 전 |
| 감사 3차 | 173.9초 | 유효 receipt 없이 실패 | provider 사용량 미반환 |

3차 packet 생성은 `2026-07-14T03:57:52.394053Z`, 실패 receipt 생성은
`2026-07-14T04:00:45.303226Z`다. 기록 간 경과는 약 172.9초이고 호출 도구가 측정한
전체 wall time은 173.9초다.

## 응답 운영 실패

긴 외부 작업 중 시작과 중간 상태를 사용자에게 충분히 보이지 못했다. 내부 commentary가
있더라도 사용자가 진행 상황을 확인하지 못하면 무응답으로 취급한다.

## 즉시 적용 규칙

1. 단순 ZCode packet의 기본 hard timeout은 60초다.
2. 15초가 지나면 시작 시각·현재 단계·경과시간을 기록한다.
3. 이후 30초마다 사용자에게 경과시간과 마지막 관측 단계를 보고한다.
4. 60초 초과 또는 usage/receipt 부재면 실패로 닫고 Codex가 회수한다.
5. 동일 입력·동일 실패 형태를 다시 모델 호출하지 않는다.
6. 성공 유형이 축적되기 전에는 ZCode를 critical path에 두지 않는다.

## 후속 카드

- ZC-02: 예시 경로와 실제 credential 경로를 구분하는 최소 fixture
- ZC-03: 모델 shell 대신 controller가 실행하는 allowlisted check
- OPS-01~03: 모든 작업자의 stage event와 wall/active/wait 시간 계측

