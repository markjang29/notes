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
| 감사 3차 | 173.9초 | 내용 반환 후 응답 schema 초과 필드로 receipt 거절 | 6,526 tokens |

ZCode 합계는 **9,173 tokens**다. 3차 세부 사용량은 input 4,632, output 1,894,
provider request 1회다. 1·2차는 모델 실행 전에 차단되어 모델 토큰을 사용하지 않았다.

3차 packet 생성은 `2026-07-14T03:57:52.394053Z`, 실패 receipt 생성은
`2026-07-14T04:00:45.303226Z`다. 기록 간 경과는 약 172.9초이고 호출 도구가 측정한
전체 wall time은 173.9초다. 모델은 실제 분석 결과를 반환했지만, 요구된 고정 키 외에
`classifications`와 `experiments`를 추가했다. bridge는 이를
`invalid_receipt_response`로 닫았다. 재호출하지 않고 sanitized log의 기존 결과를
Codex가 회수했다.

## 전체 관측 시간

- 첫 방향 로드맵 커밋: 2026-07-14 12:28:20 KST
- 소형 작업 보드 커밋: 2026-07-14 14:42:50 KST
- 관측 구간: 약 2시간 14분 30초
- 이 중 ZCode 모델 호출: 약 2분 54초

나머지 시간은 Codex의 감사·문서화·도구 조율과 응답 지연이다. 산출물 대비 과도했고,
사용자에게 지속적으로 보이지 않았으므로 운영 실패로 분류한다. Codex 자체 토큰 사용량은
현재 앱에서 이 작업 단위의 수치를 제공하지 않아 기록하지 못했다.

## 응답 운영 실패

긴 외부 작업 중 시작과 중간 상태를 사용자에게 충분히 보이지 못했다. 내부 commentary가
있더라도 사용자가 진행 상황을 확인하지 못하면 무응답으로 취급한다.

## 즉시 적용 규칙

1. 15초가 지나면 시작 시각·현재 단계·경과시간을 기록한다.
2. 이후 30초마다 사용자에게 경과시간과 마지막 관측 단계를 보고한다.
3. 단순 read-only packet은 60초 soft deadline, 180초 hard timeout을 적용한다.
4. hard timeout, usage 부재, receipt schema 실패면 sanitized 결과부터 회수한다.
5. 동일 입력·동일 실패 형태를 다시 모델 호출하지 않는다.
6. 성공 유형이 축적되기 전에는 ZCode를 critical path에 두지 않는다.
7. 계약 초과 필드 때문에 전체 결과를 버리지 않도록 closed `details` schema 또는
   controller-side salvage 규칙을 별도 카드로 설계한다.

## 회수한 결과

- 영구 controller 전용: 로그인/QR/cookie, AWS lease/control, lifecycle, 공유 NDJSON,
  reviewed promotion, 최종 의미 판단, Git push
- 현재도 안전하게 위임 가능: frozen snapshot 분석, advisory validation, exact-file
  mechanical proposal, schema/중복/parser-output 비교
- 제한 확장 후보: controller allowlist check, 여러 exact-file edit의 한 packet 묶음,
  typed evidence details
- full 신규 수집은 권한 토글이 아니라 별도 인증·lease를 가진 controller 역할이다.

## 후속 카드

- ZC-02b: 예시 경로와 실제 credential 경로를 구분하는 최소 fixture
- ZC-03: 모델 shell 대신 controller가 실행하는 allowlisted check
- OPS-01~03: 모든 작업자의 stage event와 wall/active/wait 시간 계측

## ZC-02a 복구 결과

- 실제 sanitized log를 재생해 보니 `classifications`·`experiments` 초과 필드 외에도
  `experiments` 배열의 닫는 괄호가 누락되어 있었다.
- controller는 필수 9개 필드와 각 값이 모두 정상 파싱된 뒤 시작되는 알 수 없는 후반
  확장부만 폐기한다. 필수부 누락·파손·필수 키 중복은 salvage하지 않는다.
- 실제 로그 replay에서 상태 `completed`, provider usage `6,526`을 보존했고 보조 필드는
  신뢰 결과에 포함하지 않았다.
- 전체 skill tests `31/31`, mirror check, quick validation, compile이 통과했다.
- scenario commit `bf29cdb`, skill 정본 동기화 commit `be54957`; 둘 다 push 완료.
- 실제 ZCode를 재호출하지 않아 이 복구 카드의 추가 ZCode 사용량은 `0 tokens`다.
