---
title: matrix-home 원사이트 전환과 AWS 8GB 종료 결정
date: 2026-09-11
status: accepted-decision / implementation-unverified / shutdown-blocked
authority: director direct instruction
tags: [agent-ops, matrix-home, spring, react, homeserver, aws8, migration]
---

# matrix-home 원사이트 전환과 AWS 8GB 종료 결정

## 0. 결론

- 조직의 **제품 통합 저장소는 `markjang29/matrix-home`**이다.
- 공개 루트 `/`와 `/sites`, H8를 포함한 사용자 화면은 이 저장소 안의
  **Spring Boot + React 원사이트**가 소유한다.
- `matrix-studio-spring`, `matrix-nexus`, 기존 `matrix-home` Flask 및 각 Python 웹은
  기능과 데이터를 옮겨 오는 **기증 소스(donor)**다. 별도 제품 정본으로 계속 키우지 않는다.
- Python, Node, Risu, NAI, CUA처럼 언어·실행 환경이 중요한 기능은 억지로 Java로 다시 쓰지
  않는다. 공개 포트와 화면만 없애고 Spring 뒤의 내부 작업자로 둔다.
- `43.201.34.144`의 작은 AWS 엣지는 공개 현관으로 유지하고, Tailscale을 통해 홈서버로
  연결한다. **종료 대상 AWS 8GB와 엣지는 서로 다른 컴퓨터**다.
- AWS 8GB 종료는 확정 목표지만, 현재 종료 게이트는 통과하지 못했다. 데이터·봇·스케줄·복구
  증거를 먼저 만들고 `stop + disable` 관찰 후 종료한다. 이 문서는 미완료 항목을 완료로
  바꾸는 승인이 아니다.

## 1. 이 결정이 정리하는 충돌

기존 `one-site-consolidation-v1.md`는 `matrix-studio-spring`을 통합 뼈대로 적었다. 반면 최신
조직 헌장과 이사님 지시는 `markjang29/matrix-home`을 통합 저장소로 지정했다.

이제 다음처럼 해석한다.

- **저장소·제품 이름:** `markjang29/matrix-home`
- **가져올 구현:** `matrix-studio-spring`의 Spring/React/React Flow 코드와 운영 산출물
- **가져올 기능:** Nexus, H8, 사이트맵, 기존 Flask 33개 경로, 승인·자산·Matrix 기능
- **전환 뒤 상태:** 기증 저장소는 보존·읽기 전용 또는 archive 처리

따라서 `one-site-consolidation-v1.md`의 “matrix-studio-spring이 제품 정본”이라는 부분은 이
결정으로 대체한다. 그 문서의 모바일 우선, 경로 통합, 검증 후 종료 원칙은 계속 유효하다.

## 2. 공개 주소 계약

최종 사용자는 다음 세 주소에서 시작한다.

- 홈: `http://43.201.34.144/`
- H8: `http://43.201.34.144/nexus/system/h8`
- 사이트·기능 목록: `http://43.201.34.144/sites`

기존 주소는 전환 기간에 호환한다.

- `/nexus/`는 새 React 화면으로 연결한다.
- `/nexus/?view=system`은 새 H8로 보낸다.
- `/?debug=1`과 기존 Spring 보고서 주소는 새 H8의 읽기 화면으로 연결한다.
- 폐기한 화면은 조용히 502가 되게 두지 않는다. 대체 주소가 있으면 301, 의도적으로 폐기하면
  이유와 보관 위치를 포함한 410 화면을 반환한다.

## 3. 현재 사실과 목표를 분리한다

2026-09-11 실측 현재:

- `/`, `/sites`, `/nexus/`, `/nexus/?view=system`은 HTTP 200이다.
- 그러나 `/`와 `/sites`는 아직 Flask다.
- Spring + React는 별도 `:8024`에서 동작한다.
- 공개 Spring 진단은 `cutoverReady=false`다.
- 세부 게이트는 route parity, data, bot/cron, secret rotation, rollback이 모두 `false`다.
- AWS runtime 의존 16개, Python 사용자 화면 22개, 엣지 미연결 15개가 보고된다.

즉, **접속 가능**은 확인됐지만 **원사이트 통합**과 **AWS 8GB 종료 준비**는 완료되지 않았다.

## 4. 구현 정본과 조직 정본

- 조직 사칙, actor, Telegram 큐 규칙, 여러 프로젝트에 걸친 결정은 `markjang29/notes`가
  정본이다.
- 제품 코드, API 계약, DB migration, 제품 아키텍처, 테스트·release 증거는
  `markjang29/matrix-home`가 정본이다.
- 대용량 원본과 이미지의 실제 바이트는 Git에 넣지 않는다. Git에는 식별자, 출처, SHA-256,
  크기, 타입, 생성 조건, 저장 위치, 검증·승인 영수증을 둔다.
- 대화, Telegram, JIRA, 대시보드는 정본을 보여 주는 창구다. Git commit과 검증 증거 없이
  완료 상태를 만들지 않는다.

제품의 상세 설계와 P0~P5 실행 순서는 다음 경로가 소유한다.

- repo: `markjang29/matrix-home`
- ref: `docs/architecture/one-site-palantir-blueprint-v1.md`

## 5. AWS 8GB 종료 원칙

현재 판정은 `SHUTDOWN_BLOCKED`다. 종료 목표를 취소한다는 뜻이 아니라, 복구 불가능한 종료를
막는 안전 표시다.

종료 전 최소 조건:

- 쓰기 주체, bot, cron, timer를 한쪽만 실행하도록 fence한다.
- queue를 drain하거나 격리하고 마지막 차이를 기록한다.
- Mongo, Oracle, 파일 자산을 논리 백업하고 count/hash와 복원 시험을 남긴다.
- AWS에만 큰 차이가 남은 `matrix-candidate`, `matrix_codex`, `matrix_asset_agent`를 분류·이관한다.
- bot별 Telegram 왕복, identity ACK, mail 재개, 중복 방지를 홈에서 확인한다.
- 토큰·비밀값을 회전해 AWS 복사본으로 더는 접근할 수 없게 한다.
- nginx root를 Spring으로 전환하고 실제 rollback을 한 번 성공시킨다.
- release digest, DB/object manifest, systemd 자동 기동, 외부 cold backup을 남긴다.

그 뒤 정확한 AWS 8GB 서비스만 `stop + disable`하고 관찰한다. 복구 기간 동안 snapshot과
volume을 보존한 뒤 별도 최종 승인으로 terminate/delete한다.

## 6. 소통 적용

- `큐시작`을 받으면 한 요청 버퍼를 열고, 정확한 `큐끝`이 올 때까지 답변·실행을 시작하지 않는다.
- `큐끝`에서 원문을 하나의 요구사항으로 봉인하고 중복 제거·질문·작업지시 생성을 수행한다.
- Telegram에는 표 대신 짧은 목록과 링크를 사용하고, 긴 답변은 나눈 뒤 마지막에 ELI5를 붙인다.
- 작업 상태는 `queued -> claimed -> acknowledged -> in_progress -> submitted -> verified -> closed`
  순서로 보며, ACK나 worker 보고만으로 완료라고 하지 않는다.

## 7. 복구 한 문장

> 관제, `markjang29/notes`의 이 결정과 `markjang29/matrix-home`의
> `docs/architecture/one-site-palantir-blueprint-v1.md`에 고정된 commit·release·백업 manifest를
> 정본으로 읽고, duradev의 Tailscale → systemd → Spring readiness → DB·object restore →
> Cokacdir actor별 ACK → 엣지 `/`·`/sites`·`/nexus` 순으로 복구하되 검증 전 레거시 write나
> 중복 scheduler를 켜지 마.

## ELI5

지금은 여러 가게가 따로 있고 작은 안내소가 링크만 연결한다. 앞으로는 `matrix-home`이라는
한 건물 안에 가게들을 옮긴다. Spring은 건물 관리자, React는 손님이 보는 매장, Python과
Risu·NAI는 뒤쪽 작업실이다. 오래된 AWS 창고는 물건과 열쇠가 모두 새 창고에 있는지 직접
복구 시험한 뒤 문을 잠그고, 며칠 지켜본 다음 없앤다.
