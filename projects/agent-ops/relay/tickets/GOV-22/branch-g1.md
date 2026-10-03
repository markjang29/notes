# GOV#22 [G1] 두 번째 게이트 카드가 영영 안 생김 — 승인게이트 (2026-10-02, 98)

## 재현 (taiga-bridge/bridge.py ensure_card, 운영 무변경)
- `if any(i.get("taiga_ref") == ref for i in d["items"]): return` — taiga_ref 단일키 중복 억제
- 같은 스토리가 설계승인(1차 게이트) 통과 후 이사님승인(배포승인·2차 게이트)에 오면 기존 카드가 있어 **새 카드 미생성 → 판정 불가 정체**
- 실측: 단위시험 ①~④로 재현·해소 이력 남김(아래). 운영 4:82(RELAY-24)·4:89(RELAY-30)이 해당 경로(진단문서)

## 준비 (수정본 bridge.py.G1-patched — 운영 ~/services/taiga-bridge/bridge.py 무변경, 승인 후 교체)
- 중복 키: `(taiga_ref, gate, 진입회차)` — 진행중(pending) 카드 1개만 억제, 판정된 카드는 재진입시 회차+1 새 카드
- `_is_judged`: state.processed에 등록됐으면 판정됨 → 재진입 판단. 반려 재상신도 동일 경로
- 카드 id·round 필드에 게이트·회차 반영(이력 추적)
- 단위시험(가짜 보드, 운영 decisions.json·state.json 미사용):
  ① 진행중 중복 억제 ② 배포승인 2번째 카드 생성(G1 결함 해소) ③ 판정 후 재진입 2회차 ④ 3회차 연속 재진입 — 4/4 통과

## 승인 후 적용 절차
1. `cp ~/notes/projects/agent-ops/relay/tickets/GOV-22/bridge.py.G1-patched ~/services/taiga-bridge/bridge.py`
2. `systemctl --user restart taiga-bridge`(또는 현행 기동 방식) — 20초 폴링 자동 재개
3. 검증: 테스트 스토리를 설계승인→승인→이사님승인으로 이동 → 카드 2개 생성 확인(운영 스토리 금지, 테스트 프로젝트/태그)

## 롤백
- `cp ~/services/taiga-bridge/bridge.py.bak-g1 ~/services/taiga-bridge/bridge.py` + 재시작(state.json·decisions.json 영향 없음 — 키만 확장, 구버전도 읽음)

## 적용·검증 (10-03 04:30, 98 — 이사님 승인 [10-03] 후)
- 절차: 운영본 백업(`bridge.py.bak-g1`) → `bridge.py.G1-patched` 교체 → `py_compile` SYNTAX_OK → `systemctl --user restart taiga-bridge` → active·재폴링 개시("bridge start" 04:30:21).
- 운영본 = 준비본 diff-0 실측. 롤백 1줄: `cp ~/services/taiga-bridge/bridge.py.bak-g1 ~/services/taiga-bridge/bridge.py && systemctl --user restart taiga-bridge`
- 단위시험 4/4 재실측(운영본 기준): ①진행중 중복 억제 ②배포승인 2차 카드 생성(G1 결함 해소) ③판정 후 재진입 round=2 ④3회차 연속 round=3.
- 실측 러너: 가짜보드(운영 decisions.json·state.json 미사용), 운영 파일에서 `ensure_card` 직접 추출 실행 — 환경주입(datetime·roster) 3회 수정 후 4/4.
