# GOV#23 [G2] 테스터 게이트가 판정을 무시함 — 승인게이트 (2026-10-02, 98)

## 재현 (taiga-bridge/tester.py, 운영 무변경)
- ①verdict가 `반려`·`대기`여도 무조건 이사님승인으로 전이(`"status": st2[STATUS_BOSS]` 단일 경로)
- ②합격기준 `c < 500` — 404/401/403도 통과(실측: 404 3종 → 옛 기준 통과, 개정안 반려)
- ③포트 필드 없으면 "수동 검증 필요"만 쓰고 그대로 이사님승인 전진
- 대상 127.0.0.1 포트뿐 — 원격 사이트 불가(현행 유지, 본 티켓 범위 밖)
- 테스터(97 heav_gmwin_codex_bot) 역할 미부여 — 문서상 존재, 코드에 인계 경로 없음

## 준비 (수정본 tester.py.G2-patched — 운영 ~/services/taiga-bridge/tester.py 무변경, 승인 후 교체)
- 합격: 2xx/3xx만(`200 <= c < 400`) — 404·401·403·5xx는 반려
- 전이 3분기: 통과→이사님승인(+게이트증거: 포트·판정·일시 설명란 기입=전이조건) / 반려→구현 복귀(사유=헬스체크 실패내역 기록) / 대기→테스트봇검증 상태 유지+97봇(heav_gmwin_codex_bot)에게 8024 task 인계(ref=test-97:pid:sid)
- 단위시험(로컬 더미 포트 3종, 운영 Taiga·decisions.json 미사용): 200→통과 / 404→반려 / 500→반려 — 3/3. 옛 기준(c<500)과 달리 404가 반려가 됨을 실측
- 보드 카드 1건(재호출 억제)·decisions.json 저장 방식: 기존 유지(변경 최소)

## 승인 후 적용 절차
1. `cp ~/notes/projects/agent-ops/relay/tickets/GOV-23/tester.py.G2-patched ~/services/taiga-bridge/tester.py`
2. 재시작(20초 폴링 자동 재개)
3. 검증: 포트 미응답 스토리 → 구현 복귀 확인 / 404만 반환하는 더미 포트 → 반려 확인(테스트 프로젝트·태그, 운영 스토리 금지)

## 롤백
- tester.py 원복+재시작(decisions.json·state.json 스키마 변경 없음)

## 적용·검증 (10-03 11:37, 98 — 이사님 승인 [10-03] 후)
- 적용: 운영 `~/services/taiga-bridge/tester.py` ← tester.py.G2-patched 교체(diff-0 실측) → `py_compile` SYNTAX_OK → `import tester` IMPORT_OK → taiga-tester.timer는 유지(다음 회차 11:39:45부터 새 판정).
- 더미검증(운영 Taiga·decisions.json 미사용, 운영본 `probe()` 직접 추출): 더미200 통과(3/3) · 더미404 반려(0/3) · 더미500 반려(0/3) — 3/3. 옛 기준(c<500)이면 404가 통과되나, 판은 404·500 반려로 실측 확인(2xx/3xx만 합격, 2/3 이상).
- 97봇(heav_gmwin_codex_bot) 인계: 대기 판정 시 8024 task(ref=test-97:pid:sid) — N2 토큰 강제 이행으로 97봇은 토큰표 등록 필요(잔여, 자동해소).
- 롤백 1줄: `cp ~/services/taiga-bridge/tester.py.bak-g2 ~/services/taiga-bridge/tester.py`(없으면 notes 티켓 준비본 역복사)+taiga-tester 재실행 — 스키마 변경 없음.
- 근거: 8024@n2-token-bearer(불간), notes@본커밋, 준비본 a188cee.
