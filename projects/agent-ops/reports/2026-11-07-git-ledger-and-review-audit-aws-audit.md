---
title: "[3a301711 분담3] Git 저장소 원장 대조·표본검수 (읽기 전용)"
status: submitted
date: 2026-11-07
author: aws-audit (heav_lnx_audit_bot)
linked: 3a301711-bc42-49f3-93dc-99389f29658d (매트릭스 조직 정렬·리모델링 작업지시)
work_order: notes@c3f459e projects/agent-ops/work-orders/2026-11-07-matrix-org-remodeling-mandate.md §5·§4
comm_msg: idem-9d7f4cdf8d4d8d2b1d70fabcb85abee1 (ACK id 1794062819574-49, progress id 1794063113190-51)
constraints: read-only — 운영 변경·배포·삭제·상태 임의변경 없음. 타 저장소 미커밋 작업은 그대로 둠(보존 아닌 비개입).
registry: actors.json @2aa061d (v10) — aws-audit read_only_audit·cross_repo_compare, 금지 state_transition·self_approval
measured_at: 2026-11-07 14:46~15:05 UTC (23:46~00:05 KST)
---

# Git 저장소 원장 대조·표본검수 — 3a301711 분담3 (aws-audit)

## 0. 한 줄 결론

등록·발견 저장소 15종 전수 대조 결과, **정본(Git)과 실운영이 일치하는 곳은 절반뿐**이다 —
8024 comm은 배포=원격=HEAD 완전일치인 반면, 승인 원장 approval-board는 **이사님 11-02 승인
기록 커밋이 미푸시 + 게이트 87줄 미커밋** 상태이고, 8018은 고아 프로세스(09-17 기동)가
systemd 유닛을 크래시 루프시킨 채 실서비스 중이며, 8009·8023·8004는 Git 외 또는
미푸시 HEAD 트리에서 가동 중이다. 분담1(시나리오)·분담2(RPG) 보고서 표본검수는
**주장 전부 실측으로 지지**됐고, 승인보드 정본 공백은 본 검수의 보강 발견이다.

## 1. 조사 범위·커버리지

- 대상: 로컬 발견 Git 저장소 15종(notes + projects 14) 전수 — 원격 URL(소유자), 기본브랜치,
  로컬/원격 브랜치, 미커밋(status), 미푸시(upstream 비교), 실배포 커밋(프로세스·릴리스 디렉터리 실측).
- 표본검수: 분담1(notes@10fc638)·분담2(notes@d995d88) 핵심 주장 각 3건 이상 독립 실측.
- 할일·승인대기: notes work-queue.md·policy-reread-pending.md, approval-board decisions.json, 이전 상신 기록.
- 미확인(제한 기록): GitHub 오픈 PR 상태 전 저장소(gh 미설치·비공개), Jira 백로그(지시 조항에 따라 미수집으로 기록).
- 모든 조회는 읽기 전용(git status/log/show, ls-remote, sqlite mode=ro, journalctl, 프로세스 목록).

## 2. 저장소 원장 대조 (전수)

소유자는 전 저장소 동일 — GitHub `markjang29` 단일 계정(이사님).

| 저장소 | 기본브랜치 | 미커밋 | 미푸시 | 원격 부가브랜치 | 특이 |
|---|---|---|---|---|---|
| notes | main = origin/main | 0 | 0 | agent-ops 3·backup 2·archive 1·n1 1 | clean, HEAD 828b194(11-07) |
| scenario | main = origin/main | 1 (catalog manifest.ndjson) | 0 | backup 6종 | 정상(분담1과 일치) |
| rpg_game | main = origin/main | 0 | 0 | 없음 | 완전 동기(분담2와 일치) |
| autotrader / bot-dashboard / matrix-nexus / matrix-studio / music_video | main = origin/main | 0 | 0 | 없음~소수 | clean |
| **approval-board** | main | **1 (decisions.json ±87줄)** | **1 (c11d13f)** | codex 픽스 1(07-17) | **승인 원장이 로컬 한정** |
| matrix_asset_agent | main | 5 (전부 *.bak-*) | **1 (2752d59 release)** | backup 1종 | **미푸시 HEAD에서 8004 가동** |
| **matrix-home** | main | **21** (*.bak·로그·jira 산출물) | **2 (F-3·F-4/F-11, 09-20)** | 없음 | 8018 서비스 트리, 09-20 이후 정체 |
| matrix-home-orch | orch/p0-p2 = origin | 1 | 0 | — | matrix-home 원격의 2번째 작업본(이중 체크아웃) |
| matrix-studio-spring | bridge/chatgpt-c0c1 | 1 (untracked asset-graph.json) | 0(실측: 원격 헤드=로컬 HEAD c081676) | main·n2-token-bearer | 로컬 upstream 미설정 — 표기 문제만 |
| meeting-room | main = origin/main | 5 | 0 | — | **8023이 이 트리에서 가동** |
| **notes-edge-crumb** | main = origin/main(notes 원격) | 0 | 0 | — | **notes 원격의 구클론, 본체보다 144커밋 뒤짐 — 혼동 리스크** |

## 3. 실배포 대조 (프로세스·릴리스 실측)

| 실행체 | 실배포 | 원장과의 관계 | 판정 |
|---|---|---|---|
| 8024 comm (matrix-studio-spring) | 릴리스 c081676988c3 | = 로컬 HEAD = 원격 브랜치 헤드 | **완전일치 ✓** |
| 8021 matrix-studio (RELAY-58) | 저장소 트리 e3466c0 | clean·pushed | 일치 ✓ |
| 8012 matrix_codex | 릴리스 5559eb2f… 고정 | 입력 5종은 원격 커밋 실재(분담1 §3-2와 동일 실측) | 일치 ✓ |
| 8018 matrix-home (RELAY-57) | **고아 프로세스(09-17 기동)가 점유, systemd 유닛은 "Address already in use" exit 1 반복** | 트리 HEAD 29a7018+미푸시 2+미커밋 21 — 실제 구동 코드는 09-17 스냅샷으로 검증 불가 | **불일치 ✗** |
| 8011 matrix_zcode | 미가동(리슨 0) | — | 다운(분담1과 일치) |
| 8009 rpg 웹 | gunicorn, **repo 외 수동 복사 홈**(apps/rpg-game-01-home/web) | repo web/과 소스 전량 일치(차이는 __pycache__ 1파일뿐)·systemd 미등록 | 비-Git 배포(분담2와 일치) |
| 8017 asset workbench | rpg_game 저장소 트리에서 직접(pid 일치 실측) | rpg_game clean | 일치 ✓ |
| 8004 arcade | matrix_asset_agent 트리 tools/arcade_playable_server.py | **HEAD가 미푸시 커밋(2752d59)인 트리에서 가동** | 원격 부재 운영 ✗ |
| 8023 | meeting-room 트리(28b46ef+미커밋 5) | 미커밋 포함 트리 가동 | 부분일치 |
| 8031 webapp (RELAY-64) | 미가동(리슨 0) | — | 미배포(분담2와 일치) |
| matrix-nexus | 릴리스 530cefe(09-08) | HEAD 9ffd2a1(09-08)의 직전 조상 — 1커밋 지연 | 영향 낮음 |
| dispatcher(taiga-bridge)·comm-relay-98 | 스크립트 직접 가동 | **Git 저장소 아님 — 정본 부재** | ✗ |

문서·세션·배포 불일치 요약: 분담1이 지적한 "matrix-engine 문서가 가리키는 실체가 호스트마다 다름"은
본 대조에서도 동일하게 관찰됨(projects/matrix-engine은 git 아님·실데이터 0 — 분담1 §4와 일치).

## 4. 표본검수 — 분담1·분담2 보고서 (지시: 완료 선언을 그대로 승인하지 않음)

### 분담1 (aws-scenario, notes@10fc638)
1. "출판물 3행 전부 situation_recipe, review_status=reviewed, runtime_status=active,
   availability_verdict=usable" → **실측 일치** — publications ndjson 3행, component_type 전건
   situation_recipe, provenance 3필드(reviewed/active/usable) 확인.
2. "8012 가동·유휴 — works 42, approvals 0, works 전부 동일 scenario_commit 고정" →
   **실측 일치** — 리슨 확인, 런타임 sqlite(읽기 전용) works=42·approvals=0·distinct
   scenario_commit=1. DB 최신 work 시점 필드명 차이로 미재검(보고서의 7/29 주장은 커밋 고정 사실로 간접 지지).
3. "8011 다운" → **실측 일치**(리슨 0). "8018 포트 충돌 크래시 루프" → **독립 재현** —
   고아 프로세스 09-17 기동 확인, journal 11-07 14:48 동일 에러 반복.
   → 분담1의 완료 선언은 근거와 함께 정확. **새 발견 없음(지지)**.

### 분담2 (aws-rpg, notes@d995d88)
1. "rpg_game 완전 동기(단일 main, 미커밋·미푸시 0)" → **실측 일치**.
2. "8009 비-Git 수동 복사 가동, repo web과 전 파일 동일, systemd 미등록" → **실측 일치** —
   gunicorn cwd=repo 외 홈, diff 차이 __pycache__ 1파일뿐, 유닛 부재.
3. "8017 repo 직접 가동·8031 미가동" → **실측 일치**(pid 포함).
4. "rpg-skill-fusion approved(이사님 11-02, approval-board c11d13f)·RELAY-64 설계승인-2 pending,
   1차 게이트 approved 공존" → **실측 일치** — decisions.json에서 세 케이스 모두 확인.
   → 분담2의 완료 선언도 정확. **보강 발견(분담2가 미기술)**: 승인 기록 커밋 c11d13f 자체가
   미푸시이고, decisions.json에 미커밋 ±87줄(신규 게이트 — pending 2·approved 5 추가,
   RELAY-64/RELAY-28 2차 게이트 포함)이 쌓여 있어 **승인 원장 전체가 로컬 한정 상태**다.

### 판정
양 보고서 모두 과장·허위 완료 선언 없음. 단 분담2의 승인현황 서술은 "원격 정본 기준"이 아닌
"로컬 파일 기준"이라는 한계가 있었고, 본 검수가 그 간극을 메운다.

## 5. 불일치·리스크 목록 (영향순)

1. **approval-board 정본 공백** — 이사님 11-02 승인 기록(c11d13f) 미푸시 + 미커밋 게이트 87줄.
   원격 분실·충돌 시 승인 이력 소실. 조치(운영 변경): 매니저 commit+push. 본 감사는 읽기 전용으로 미수행.
2. **8018 이중 운영(RELAY-57 미완)** — 고아 프로세스(09-17~) 점유 + systemd 크래시 루프 + 미푸시 fix 2건
   미반영. 재부팅 시 복구 불명. 조치: 운영(INFRA) — 프로세스 정리 후 유닛 인계(분담1 §7-3·§7-4와 합치).
3. **운영 스크립트·배포의 Git 외 배치** — dispatcher(taiga-bridge), comm-relay-98, 8009 수동 복사 홈.
   정본 부재로 감사·복구 불가. 조치: 저장소 수용 결정 필요.
4. **8004 arcade가 미푸시 HEAD(2752d59) 트리에서 가동** — 원격에 없는 코드로 운영. 조치: push 또는
   배포 기준 확정.
5. **matrix-home 21 미커밋·2 미푸시 정체(09-20~)** — Git-정본 사칙 위반 소지 산물(리포트·pid·로그 포함).
6. **notes-edge-crumb 구클론(본체보다 144커밋 뒤짐)** — 동일 원격의 이중 체크아웃(matrix-home-orch는
   별 브랜치 작업본이라 성격 다름). 오용 시 구판 결정 참조 위험. 조치: 정리 여부 결정.
7. matrix-studio-spring 로컬 upstream 미설정 — 실제 push는 완료(원격 헤드=HEAD)로 표기 문제만.
8. GitHub 오픈 PR 상태 전 저장소 미확인(gh 미설치) — 분담1·2와 동일 제한.
9. matrix-nexus 배포 1커밋 지연(09-08) — 영향 낮음.

## 6. 흩어진 할일·승인 대기 목록 (수집 결과)

- **승인보드 pending 3건**(decisions.json 작업본 기준): ① RELAY-64 8009·8017 재설계 설계승인-2
  (1차 게이트는 approved 공존 — 1차/2차 관계 규칙 명시 필요) ② RELAY-28 P-3 RISU 임포트 기술
  설계승인-2 ③ RELAY-27 P-2 구역 게시판 설계승인(장기 미결).
- **notes work-queue.md**: RELAY-63 firewin·gmwin 스킬 설치 보고 대기(09-04 지시 이후),
  zcode 브리지 수신 409 — 정본 폴러 결정 필요, Matrix 통합 후임 NEXT-001 품질시험 카드.
- **notes policy-reread-pending.md**: 사칙 재독 미완(rpg·scenario), [CERT] 미완료 — asset-agent
  재요청 무응답, windows-zcode·n100-zcode 미도달(전달 경로 부재).
- **이전 상신 잔여**(notes@a7e5535, 10-03): notes 원격 2곳(이사님 계정) 등록, 데몬 토큰 6봇 등록(매니저 권한).
- **Jira**: 지시 조항에 따라 미수집으로 기록함.

## 7. 역할 확인서 (작업지시 §7 — aws-audit 자기 서술)

- **제품 목적과 내 기여**: 매트릭스 조직이 Git 정본 위에서 움직이는지를 독립적으로 검증하는 것.
  나는 다른 팀의 주장과 실제 근거를 분리해 확인하고, 수정은 하지 않고 위험만 보고한다.
- **입력**: actors.json(레지스트리 @2aa061d), 매니저 Agent Mail/comm 발령, 각 저장소 Git·프로세스·저널·
  읽기 전용 DB. **출력**: 본 보고서, 표본검수 판정, 불일치 목록. **의존**: 매니저(발령·회신),
  각 팀 보고서(검수 대상), 8024 comm(회신 채널).
- **권한과 완료 입증**: read_only_audit·cross_repo_compare·repo_read + notes 보고서 commit/push.
  금지 state_transition·self_approval 준수 — 본 검수 중 상태 변경·운영 개입 0건, 타 저장소 미커밋
  파일 비개입. 완료 입증 = 본 보고서의 notes 원격 push 커밋(full sha) + comm submitted 회신.
- **현재 목표와 어긋난 점**: 승인 원장(approval-board)이 정본 요건(push)을 스스로 충족하지 못하는
  상태에서 승인이 계속 발생 중 — 감사 대상 시스템의 뿌리 리스크.
- **다음 한 가지 실행**: 매니저가 approval-board를 commit+push하면 재대조로 정본 회복을 확인
  (운영 변경은 매니저 몫, 나는 검증만).

## 8. 결정 필요 사항 (decisions_needed)

1. approval-board 정본화(commit+push) 승인 — 매니저 실행, 즉시 권장(§5-1).
2. 8018 고아 프로세스 정리·유닛 인계·미푸시 2커밋 반영 — 운영 변경(매니저+운영, 분담1 §9와 중복 지지).
3. dispatcher·comm-relay-98·8009 수동 홈의 Git 수용 여부와 기준.
4. gh(PR 확인 도구) 설치 또는 매니저 일괄 PR 점검 주기.
5. notes-edge-crumb 구클론 정리 여부.

— 이상. 모든 실측은 읽기 전용으로 수행했고 운영 변경·배포·삭제는 없음. 토큰값·세션 ID·
비밀·기계 로컬 절대경로는 본문에 없음(홈 상대 서술만 사용).
