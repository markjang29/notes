# codex_dev_1 상태 표시 (RELAY-54, 2026-08-26~27)

기준: 이사님 AWS Zcode 대화 100건 · 정합성 장부 지시 · 매니저 23:30 재독촉.
Jira 전면 404(프로젝트 API `[]`)는 gap으로 남김 — 완료 처리에 Jira 근거 사용 안 함.
담당 사이트: 8005 승인보드 · 8020 music_video.

## 담당 사이트·산출물 상태

| 대상 | 상태 | 비고 |
|---|---|---|
| 8020 music_video 여행 플래너(일정·촬영·기념품) | 구현됨 | `main` = `560f69a`. 기념품 구글맵 길찾기 `a273c47`, 캐시 우회 `c8acb66` 포함. /·/api/health 실측 정상, POST 0건 |
| 8020 일상(혼인·TOPIK·F-6) RELAY-42 | 부분구현→수정 제출 | 반려 1~3·5~7 수정 완료 `b23cb3a` — enum 검증·원자성·v1 마이그레이션·서류별 출처·KO/EN/VI seed, 테스트 22/22·분기 92.16%. 6-코드리뷰 재검토 대기 |
| 8005 승인보드 서비스 | 부분구현 | uvicorn 라이브 200(게이트 인증 401 정상 동작). RELAY-19/20/52 반영. 작업 브랜치 `codex/board-linux-release-fix-20260717`가 배포 실체 |
| 8005 승인 이력 정본 | 부분구현 | decisions.json/requests.json + git 백업(RELAY-19). Jira 404 중이라 Notes/Git이 실효 정본 — 장부 지적과 동일 |
| RELAY-57 P/C 디버그모드 8005·8020 | 구현됨 | 8020 `560f69a`(P1~P3·C1~C16), 8005 `252b247`(P1·P2, 섹션 안정 id). 부여 목록 `RELAY-57/pc-registry-codex-dev-1.md` |

## 장부 검증 항목 응답 (8005)

- 승인 카드 쉬운 말 설명: 구현됨 — "승인하면:" 두괄식 한 줄 + 요구사항/결과 요약 접힘(RELAY-16·52).
- 승인 전 근거 연결: 구현됨 — 원문/검증결과/전문/Git 자산 링크를 카드 내 패널로 제공.
- 승인 이력 Jira/Notes 정본: 부분구현 — Jira 자동기록(RELAY-19)은 현재 Jira 전면 404로 기록 불능,
  서버 로컬 decisions/requests + GitHub 백업은 유지. Jira 복구 시 재검증 필요.
- Jira 404 상태 참조 정본: Notes tickets + 각 repo git. port-registry의 "Jira 확인" 주석은 근거 불충분(매니저 정리 C안과 동일 결론).

## 정리필요 (매니저 건의)

- **8005 미커밋 변경분**: 작업 디렉토리에 `main.py`(VALID_TARGETS 확장: audit/asset_agent/arcade/novel_col/codex_dev_1·2),
  `decisions.json`·`requests.json` 변경, `tools/bot_mail_daemon.py`(추적 안 됨)가 커밋 없이 존재.
  제3자 작업 가능성으로 미삭제·미커밋 유지. 소유자 확인 후 커밋 또는 정리 필요.
- **8005 배포 브랜치 이원화**: `origin/main`(12c0a78)이 작업 브랜치(abcd791→252b247)보다 크게 뒤짐.
  병합 주기·담당 확정 건의.

## RELAY 진행 요약

- RELAY-42: 수정 제출 완료(재검토 요청) · RELAY-54: 본 파일 제출 · RELAY-57: 담당분 구현+부여 목록 커밋.
