---
title: "[3a301711 분담2] RPG 소비측 실측 보고 (읽기 전용)"
status: submitted
date: 2026-11-07
author: aws-rpg (heav_lnx_rpg_bot)
linked: 3a301711-bc42-49f3-93dc-99389f29658d (매트릭스 조직 정렬·리모델링 작업지시)
work_order: notes@c3f459e projects/agent-ops/work-orders/2026-11-07-matrix-org-remodeling-mandate.md §5
comm_msg: idem-c33faa8bdfa45e5f208fa9859c216851 (ACK id 1794059053783-21)
constraints: read-only — 운영 변경·배포·삭제 없음. 미커밋 작업 보존(실측 결과 미커밋 0건).
---

# RPG 소비측 실측 보고 — 3a301711 분담과제 (aws-rpg)

## 0. 한 줄 결론

rpg_game 저장소는 클린·완전 동기화(main 단일, 미커밋·미푸시 0)지만, **매트릭스 엔진 산출물(인물·월드)을
RPG가 실제로 소비하는 경로는 현재 0이다** — 경계 설계는 승인됐으나 어댑터가 미구현이고, 존재하는 연결은
crumb 화면 편입(8024 계열 노출)과 흡수 설계(webapp RELAY-64, 미배포)뿐이다. 최대 운영 리스크는
8009가 Git 배포가 아닌 수동 복사본으로 돌고 있다는 점(systemd 미등록, 재부팅 시 자동 복구 불가).

## 1. rpg_game 저장소 상태 (2026-11-07 실측)

- 브랜치: `main` 단일(로컬=origin/main, ahead 0 / behind 0). 열린 로컬 브랜치 없음. HEAD `16a5e71`.
- 미커밋·미푸시·stash: 전부 0 (`git status` 클린, `rev-list origin/main...HEAD` = 0/0).
- PR: GitHub 오픈 PR 목록은 확인 도구(gh) 부재로 **미확인** — 단, 단일 브랜치 완전 동기화 상태라
  분기 기반 열린 PR은 존재하지 않을 것으로 판단(판단이지 확인 아님).
- CI: 없음(`.github/workflows` 부재). 테스트는 로컬 실행 방식 — `web/tests/*.test.mjs` 2건(관측)과
  `webapp/src/test`(Java) 존재. 최근 문서상 검증 기록: RELAY-64 1차 커밋 `d0faacd`(8031 테스트통과 —
  4경로+WASM 39.5MB+API) 및 매니저 독립 재현(티켓 이벤트 0004, 아래 §4).
- 최근 커밋 흐름: `b1e2bf5`(사진 원본 보존) → `d50f414`(WASM 유일사본 복원) → `6ec8bec`(8009 배포본 동기)
  → `cc1efb0`·`ef3c8eb`(crumb·오브젝트 태깅) → `d0faacd`(RELAY-64 webapp 1차) → `f7536a4`(스킬 융합
  2~4단) → `16a5e71`(게임개발 사칙 v1 발효).
- 루트 잔여 파일: `photo_AQADZhFrG-5p6VR-.jpg`, `OVERNIGHT_2026-07-10/12.md` 등 이력 보존 성격 파일
  존재 — 이번 읽기 전용 범위에서 정리하지 않음(처리안은 §6 M5).

## 2. 배포 실측 (프로세스·경로·버전)

- **8009 RPG 웹 — 가동 중이나 Git 배포가 아님.** gunicorn(pid 976657~, workers 2)의 cwd는
  `/home/smlime21/apps/rpg-game-01-home/web` — Git 저장소가 아닌 수동 복사 홈. 내용은 repo `web/`와
  전 파일 동일(diff -rq 차이 0, 타임스탬프 09-12 — 이후 repo 커밋은 web/ 미변경이므로 사실상 HEAD와
  동일 코드). repo의 `deploy/rpg-game-8009.service`는 구서버 경로(`/home/ubuntu/apps/...`) 기준이라
  본 서버에 미설치(`systemctl status` not found) — 재부팅 시 자동 기동·장애 시 자동 재시작 보장 없음.
- **8017 에셋 워크벤치 — repo 작업디렉토리에서 직접 가동**(`tools/asset_workbench/app.py --port 8017`,
  pid 991039). repo가 클린하므로 실행 코드 = HEAD 커밋 내용과 일치.
- **8031 webapp(RELAY-64 Spring+React) — 미가동**(포트 미청취). repo에 구현·검증 기록만 존재.
- **엣지 진입 실측**: `http://43.201.34.144/open/8009` · `/open/8017` 모두 200. 로컬 8009·8017도 200.
- 8024(matrix-studio-spring, java)는 타 서비스 — 본 조사에서는 진입점·crumb 상위로만 참조.

## 3. 매트릭스 엔진 산출물의 RPG 소비 경로 — 실측 결론: **실소비 0**

"화면 연결만으로 완성이라 하지 않는다"는 기준으로 층위를 나눠 실측:

1. **데이터 소비(인물·월드 자산의 실반입·실호출): 0건.**
   - `web/app.py`(8009 본체)에 외부 HTTP 호출·매트릭스 API 참조 없음(전수 grep — 매치는 stale print
     문구 1건뿐). 8017 워크벤치는 NovelAI(NAI) **직접** 생성 후 자체 store에 적재 — 매트릭스 엔진
     경유가 아니며 시나리오 자산 고유번호(CHR/MOD/SCN-NNNN) 참조도 코드에 없음.
   - 고유번호 체계 참조는 문서에만 존재(`ideation/DRAFT-matrix-scenario-factory-request.md`).
2. **화면 연결(존재함 — 완성 아님을 명시):** 8009·8017 전 페이지에 `_matrix_crumb` 배너 → 8024 홈·
   flow 하위 사이트로 편입(09-12 `cc1efb0`·`ef3c8eb`). 이것이 현재 유일한 "매트릭스 계열 연결".
3. **설계·계약(존재, 미실행):**
   - 경계 설계 승인: `projects/rpg-game-01/design/matrix-factory-boundary.md` — status
     **`approved-boundary-adapter-not-implemented`**(스스로 어댑터 미구현 명시, 2026-07-17).
   - RPG→시나리오팀 클라이언트 명세 `ideation/DRAFT-matrix-scenario-factory-request.md` — DRAFT v4
     (2026-07-07), "송신은 매니저 승인 후" 조건으로 **미송신 상태 4개월**.
   - webapp(RELAY-64): 8024 Modulith 관례 승계·정본 타깃 `/apps/rpg`(MATRIX-P0-OWN-01)로의 흡수
     설계 — 미배포라 소비가 아니라 이행 준비.

즉 제품 흐름(원천→코어 자산→엔진 인물·월드→RPG 소비→피드백) 중 RPG가 맡은 소비 단계는
**아직 시작 전**이며, 이는 숨기는 것이 아니라 경계 문서가 이미 정직하게 선언한 상태다.

## 4. 실제 사용자 경로·현재 작업·할일/승인 대기

- **사용자(이사님)가 실제 접속하는 경로**: 엣지 43.201.34.144 `/open/8009`(소개·prototype·tactics·
  godot-tactics WASM 4경로)와 `/open/8017`(에셋 워크벤치). 실트래픽량은 이번 범위에서 미계측(§7).
- **RELAY-64(8009·8017 Flask→Spring+React 재설계)**: 이벤트 체인 0001 ACK(09-14) → 0002 착수 →
  0003 제출 → 0004 review(매니저 8031 독립 재현 검증 완료: 경로 9종 200·API 6종+WASM 해시 3처
  일치 등). repo 구현 1차 = `d0faacd`. 이후 스킬 융합 작업으로 일시 중지("승인 후 재개" 조건).
- **승인보드 상태(rpg 관련)**:
  - `rpg-skill-fusion-2026-10-27` — **approved**(이사님 11-02, approval-board `c11d13f`). 게임개발
    사칙 v1 발효(2026-11-02, repo `16a5e71`). 잔여: notes `principles/` 승격 여부는 별도 안건(매니저).
  - **`[설계승인][RELAY-64] … 설계승인-2` — pending**(승인보드 현재 pending 3건 중 1건, 등록 약
    2026-11-04 에포크 환산). 동일 제목의 1차 게이트(gate-1790733315498)는 approved로 공존 —
    1차/2차 관계가 게이트 목록만으로는 불명확(§6 M3).
  - RELAY-47(8009 서비스 등록)·과거 rpg 밤샘 푸시 등은 approved로 종결.
- **게임개발 사칙 v1**(발효됨): 설계→승인→구현→자체검증→검수 게이트 규정. 격리 POC 미실행
  스테이지(`extract`)의 2차 검증이 남은 후보 과제로 기록돼 있음(SKILL-FUSION 보고서 "정직 기록").

## 5. 역할 확인서 (작업지시 §7 — aws-rpg 자기 말로)

- **제품 목적과 내 기여**: 매트릭스 엔진이 만든 인물·월드를 실제로 소비해 RPG GAME 01을 플레이 가능한
  게임으로 완결하는 것. 나는 그 소비측(게임) 설계·구현·자체 검증과 게임개발 사칙 운용을 맡는다.
- **입력**: 이사님 방향(텔레그램·승인보드), 매니저 Agent Mail/comm, 시나리오팀 자산 고유번호 체계와
  (장래) 엔진 산출물 계약, 8024 원사이트 편입 규칙. **출력**: rpg_game 커밋·프로토타입(8009/8017/
  webapp), 실행 증거(테스트 결과·해시), 후보·보고서. **의존**: 매니저(게이트 운영·통합), 시나리오팀
  (자산 공급 계약), 98/관제(배포·통신 기반).
- **권한·완료 입증**: rpg_game repo 읽기·쓰기·커밋·푸시와 후보 제안. 완료는 자체 테스트 실행
  결과+커밋 SHA+승인 게이트 판정으로 입증한다(사칙 v1: 근거 없는 완료 선언 금지).
- **목표와 어긋난 점·제약·이견**: 매트릭스 최우선 목표 대비 소비측 실소비 0 — 다만 이건 실패가 아니라
  순서 문제로 판단한다(RELAY-64 재설계 확정 전에 어댑터를 만들면 이중 작업). 이견 없음.
- **다음 한 가지**: RELAY-64 설계승인-2 게이트 확정(담당: 이사님 승인·매니저 게이트 정리) 이후
  webapp 2차 착수와 동시에 매트릭스 어댑터 설계를 게이트에 올린다(담당: aws-rpg).

## 6. 불일치 목록 (영향순 — 의도/실제/근거/영향/원인/처리안/담당/검증/결정필요)

| # | 항목 | 내용 | 처리안 | 담당 | 결정필요 |
|---|---|---|---|---|---|
| M1 | 엔진 산출물 실소비 0 | 의도=매트릭스 중심 제품 흐름 / 실제=소비 경로 부재. 근거=경계 문서 status·코드 전수 grep. 원인=재설계(RELAY-64)·스킬 융합 선행 | 유지-보류: RELAY-64 확정 후 어댑터 착수(자연 순서) | aws-rpg | 아니오(순서 확정만) |
| M2 | 8009 비-Git 수동 배포 | 의도=Git 정본→배포 추적 / 실제=rpg-game-01-home 수동 복사·systemd 미등록·재부팅 무방비. 근거=/proc cwd·diff·systemctl | 수정 제안: 본서버 경로 유닛 신규 작성·등록(운영 변경 → 별도 승인 후 실행. 이번엔 보고만) | aws-rpg(실행)·매니저(승인) | **예** |
| M3 | RELAY-64 승인게이트 이중 | 동일 제목 approved(1차)+pending(설계승인-2) 공존, 목록만으로 관계 불명 | 통합: 매니저가 1차/2차 관계 정리 후 본 게이트 승인 or 폐기 | 매니저 | **예** |
| M4 | DRAFT v4 명세 4개월 미송신 | 2026-07-07 작성, "매니저 승인 후 송신" 조건으로 방치. 매트릭스 리모델링 방향과 정합 재검토 필요 | 보류: 리모델링 안(§6 본편) 확정 후 송신/개정/폐기 결정 | 매니저·시나리오팀·aws-rpg | **예** |
| M5 | repo 루트 잔여 파일 | 사진 원본·OVERNIGHT 문서 등 보존 성격 파일 — 가역적 문서 정리 대상 후보 | 보류: 별도 가역적 정리 제안으로만(이번 읽기 전용 범위 외) | aws-rpg | 아니오 |

사용자·제품 영향 요약: M2가 현재 유일한 **운영 리스크**(재부팅 시 8009 다운·수동 복구). M1·M3·M4는
진행 순서·의사결정 지연 요인이며 즉각적 장애는 아니다.

## 7. 조사 대상 / 확인 / 미확인 (범위 검증)

- 정의한 대상: 12개 — 브랜치, 미커밋/미푸시/stash, PR, CI, 테스트, 8009 배포, 8017 배포, 8031 배포,
  엣지 경로, 엔진 소비 경로(코드), 승인/작업 현황, 역할 정리.
- 확인: 11개 (§1~§5 근거 제시).
- 미확인 1개 + 범위외 미계측 2개:
  1. GitHub 오픈 PR 목록 — 확인 도구(gh) 부재. 판단 보조: 단일 브랜치 완전 동기화.
  2. 8009·8017 실트래픽량·NAI 토큰 사용량 — 이번 범위(읽기 전용·부하/비용 계측 아님)에서 미계측.
     토큰값은 정책상 존재 위치만 확인 가능(값 확인 안 함 — 준수).
  3. 매트릭스 엔진·시나리오팀 공급측 현황 — 본 분담(RPG 소비측) 범위 밖. 시나리오팀 조사로 보완 필요.

## 8. 증거 일람

1. rpg_game: HEAD `16a5e71`(origin/main 일치), `git status` 클린, `d0faacd`(RELAY-64 1차),
   `projects/rpg-game-01/design/matrix-factory-boundary.md`(status 라인),
   `ideation/DRAFT-matrix-scenario-factory-request.md`(frontmatter v4).
2. 프로세스: /proc/976657(cwd rpg-game-01-home/web, gunicorn)·/proc/991039(cwd tools/asset_workbench);
   `ss -tlnp` 8009·8017·8024 청취, 8031 부재; `systemctl status rpg-game-8009` not found;
   deploy/rpg-game-8009.service(구서버 경로).
3. 엣지 실측: 43.201.34.144/open/8009·/open/8017 → 200 (2026-11-07).
4. notes: RELAY-64 티켓·이벤트 0001~0004(0004 매니저 8031 독립 재현), work-order c3f459e.
5. approval-board: `c11d13f`(rpg-skill-fusion approved 11-02), pending 3건 중 RELAY-64 설계승인-2,
   decisions.json 실측.
6. comm: idem-c33faa8b 수령→ACK 1794059053783-21, progress 1794059254753-25.
