# GOV#24 [G3] 승인보드 파일 경합(무잠금 덮어쓰기) — 승인게이트 (2026-10-02, 98)

## 재현 (운영 무변경)
- 보드 앱(approval-board/main.py → request_store)은 `locked_json/transact_json`(flock+원자교체) 쓰지만,
  `bridge.py`·`tester.py`는 잠금 없이 `read_text` → 사본을 20초 루프+수십 회 HTTP 호출(Taiga PATCH 2회/카드) 뒤 `tmp→replace` 전체 덮어쓰기
- 그 사이 이사님이 보드에서 누른 판정(status=approved 등)이 소실될 수 있음 — 단위시험 ①로 재현(옛 방식이면 소실)

## 준비 (수정본 2개 — 운영 ~/services/taiga-bridge/{bridge,tester}.py 무변경, 승인 후 교체)
- 승인보드의 `request_store.transact_json`(파일잠금+원자교체, decisions.json.lock)을 빌려 쓰도록 교체 — sys.path.insert 1행+import 1행(의존성 0, 보드와 동일 모듈)
- `board_save`/tester 저장부: 무잠금 전체 덮어쓰기 → **add-only 병합저장**(같은 id면 보드 측 최신본 존중, bridge·tester는 신규카드 추가만)
- 스키마 변경 0(기존 decisions.json·state.json 그대로), 락파일은 보드와 동일(.json.lock)
- 단위시험(사본 경로, 운영 파일 미사용):
  ① 사본-저장 병합: 이사님 판정 유실 0 + 신규카드 추가(옛 방식이면 소실) ✓
  ② 동시쓰기 스트레스 4스레드×20회(bridge 2+보드 2): 에러 0, 초기 판정·카드 유실 0 ✓

## 승인 후 적용 절차
1. `cp ~/notes/.../GOV-24/{bridge,tester}.py.G3-patched ~/services/taiga-bridge/` (각각 원본 백업 후)
2. 재시작(bridge 20초 폴링 자동 재개)
3. 검증(티켓): 동시쓰기 스트레스(브리지 루프 중 판정 POST 100회) 후 판정 유실 0 — 위 단위시험 ②를 운영 경로로 1회 재실행

## 롤백
- 원본 복원+재시작(decisions.json·state.json·lock 스키마 변경 없음)

## 적용·검증 (10-03 11:38, 98 — 이사님 승인 [10-03] 후)
- **준비본은 G1·G2 이전판** — 그대로 교체 시 선행 개정 소실(회귀)이므로 **병합 이식** 수행: 운영본(G1·G2 반영)에 G3 변경 2부분만 이식(bridge·tester 각: import 2행+저장부 교체). G1(_is_judged·round_no)·G2(2xx/3xx 합격) 유지 확인. 백업: `bridge.py.bak-g3`·`tester.py.bak-g3`.
- py_compile SYNTAX_OK · import both IMPORT_OK.
- 단위시험 ② 재실행(사본 경로, 운영 파일 미사용): 4스레드×20회(보드 2+브리지 2) — 에러 0, 이사님 판정(seed) 유지(approved), 신규카드 유실 0, .json.lock 생성 실측. 참고: transact_json 계약은 mutator의 data 직접변형(반환값 무관) — 운영 코드는 fresh 직접변형이라 적합.
- 재기동+회귀(이사님 지시): `systemctl --user restart taiga-bridge` → active, "bridge start" 11:38:12, 에러·트레이스 0, 운영 decisions.json 28카드 무손상(28→28), tester·dispatcher·agenda 타이머·서비스 전부 active.
- 롤백 1줄: `cp ~/services/taiga-bridge/{bridge,tester}.py.bak-g3 ~/services/taiga-bridge/ && systemctl --user restart taiga-bridge` — 스키마 변경 없음.
- 근거: 준비본 d11de27(병합분), 8024@불간, notes@본커밋.
