# 95(감사봇) 지시 — Taiga INFRA#14 [D3], INFRA#17 [A6] (매니저, 2026-10-01)
근거: projects/agent-ops/proposals/2026-09-30-system-improvement-review.md §4 D3, 부록 A6
## 1. INFRA#17 [A6] 포트 대장 6개 누락 등록
- relay/port-registry.json 의 registered 22개 대비 실가동 미등록 6개: 8002(autotrader), 8030(nexus), 8040(taiga), 8100, 8222(NATS 모니터링), 8788(zai 프록시).
- 각 포트의 서비스명·소유 봇·외부 노출 여부를 ss -ltnp, systemctl --user 로 실측해 등록하거나 폐기 판정안을 적는다. 8100은 소유 불명이므로 프로세스 확인 후 판정.
- 검증: 실가동 포트 중 미등록 0. 포트 대장 변경은 커밋하고 해시를 적는다.
## 2. INFRA#14 [D3] 비밀 위생·디스크 정리 후보 목록화 (목록만, 삭제 금지)
- 평문 자격증명 위치(경로만, 값 금지), 퇴역 토큰 파일 잔존, git 자격증명 store 현황을 경로 목록으로 정리한다.
- 디스크 정리 후보(~/.cokacdir/debug 11G, migration-8gb, 설치 파일 등)는 크기와 최종 수정일만 목록화한다. 삭제·이동·압축 금지.
## 규칙
- 수정 범위: port-registry.json 과 결과 문서만. 토큰 값은 어디에도 쓰지 않는다.
- 완료 시 Taiga 티켓 설명 꼬리에 근거 commit + 검증 1줄, 8024로 매니저(heav_lnx_bot)에 type=task, ref=INFRA#17 또는 INFRA#14 로 회신. Taiga 상태는 옮기지 않는다.
