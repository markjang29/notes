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
