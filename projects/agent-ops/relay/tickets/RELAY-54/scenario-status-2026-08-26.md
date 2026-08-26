# scenario 팀장 — 담당 사이트·산출물 정합성 표시 (2026-08-26)

기준: 사이트 정합성 장부(2026-08-26) + 이사님 AWS ZCode 대화 100건 지시.
판정자: aws-scenario (@heav_lnx_scenario_bot). 검증은 전부 실측(curl/systemd/git).

## 8003 RISU 자산 실험실 — 부분구현

근거 (2026-08-26 실측):

- 서비스 active: `scenario-generator.service` (system, RELAY_TICKET=RELAY-43 drop-in 주입 확인, 08-24 기동)
- 실험 생성/실행/피드백/히스토리/챕터/장면 API 라우트 존재 (`app.py` @app 라우트 15종)
- `/api/catalog/stats` 응답: character 8 · module 2 · fragments 1,627
- `/api/experiments` 응답: 실험 20건 기록

갭 (부분구현 사유):

- 사이트 가이드상 내 담당은 "리수 세팅 자산 실험·검증 지원(1·2단계)"인데,
  8013 pocketrisu 세팅 산출물을 받아 실험하는 연결 흐름이 아직 없음.
  실험실 카탈로그는 소설/내부 자산 중심(character 8·module 2) — 리수 세팅 자산 반입 전.
- 1·2단계 지원 기능(세팅 검증·audit 연계) 착수에는 매니저 티켓 필요 (티켓 없는 착수 무효).

## 8004 PLAYABLE 계열 (내 산출물, RELAY-44 — arcade 봇 소관 지정) — 항목별 표시

| 산출물 | 판정 | 근거 |
|---|---|---|
| PLAYABLE 웹+파이프라인 (30셋·결합 JSON·GLM 생성) | 구현됨 | E2E: GLM 생성 1,319자 확인, 8004 응답 200, matrix_asset_agent 커밋 249350f·6e8476b·c21049d |
| 승인 영구 저장 (/api/approve → reviews/approvals.jsonl + git commit + 세션 복원) | 구현됨 | E2E: 저장·중복스킵·조회·커밋 확인. 테스트 기록은 삭제 후 재검증 |
| RISU 정본 파서 위임 (risu_canonical) | 구현됨 | 실자산 5개 파싱 통과, S-box 테이블이 RisuAI 업스트림 SHA와 일치 확인 |
| archmap (scenario·fleet·미니맵 드릴다운) | 구현됨 | jsdom E2E: 진입·서브모듈 렌더·복귀 ✓. 8004 /archmap·/archmap-fleet 서빙 중 |

## 갭 (완료 처리하지 않고 남김)

1. **RELAY-44 Jira 404** — 장부 지시에 따라 완료 처리하지 않고 gap 유지.
2. **미승인 자산 재테스트 금지 규칙과 PLAYABLE 30셋 충돌 — 정리필요**.
   30셋은 전부 pending_human_review 상태. 08-24 가이드 이전(08-21) GLM 테스트는
   소급 위반 아니지만, 현재 웹에 GLM 생성 버튼이 살아 있어 향후 클릭 시 규칙 위반이 됨.
   조치: 이사님 승인 완료 셋만 GLM 재테스트 가능하도록 게이트 필요 (arcade 이관 시).
3. **8004 소관 이관 대기** — 가이드상 8004는 arcade 봇 담당. 매니저 회신 대기 중
   (이관 지시 시 서비스·문서 인계 작업 진행).
4. **8005 승인보드와 8004 승인 기록 체계 분리 — 정리필요**.
   reviews/approvals.jsonl(8004)과 8005 승인보드가 별개 체계. 어느 쪽이 정본인지
   매니저 게이트 확정 후 연계 필요. 현재는 8004 JSONL을 8004 내부 정본으로 유지.

## 다음 행동 (티켓 수령 시)

- 8003: 리수 세팅 자산(8013 산출) 반입·실험 흐름 구축 — 매니저 티켓 필요
- 8004: arcade 이관·승인 게이트 — 매니저 판단 대기
