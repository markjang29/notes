# GOV#25 [G4] 설계승인 후 재발령·에스컬레이션·status order — 승인게이트 (2026-10-02, 98)
## 재현 (운영 무변경)
- ①재발령 없음: dispatch-state.sent 키가 단일(4:82 등, 09-20 1회) → 설계승인 판정으로 구현 재진입해도 무발령.
  실측: PIPE#19·PIPE#24 = 구현+담당봇 있음, state 키 있음 → "재발령 없음"
- ②status order 중복: 4개 프로젝트 모두 구현=5, 설계승인대기=5 (칸반 순서 모호) — 실측 출력
- ③에스컬레이션: agenda는 일1회(09시)+변화시 발행뿐 — 4:85·4:86 10일 정체 진단 일치
## 준비 (dispatcher.py.G4-patched — 운영 ~/services/taiga-bridge/dispatcher.py 무변경)
- ①dispatch 키 (ref, phase): 초회발령은 과거 단순키→:impl 키로 승격 이관(중복발령 0), 재진입은 phase 카운터로 재발령 1회
- ③agenda: 변경 최소(주석1행) — 재발령(G4①)으로 4:85·4:86류 정체 해소, 일1회+변화시 발행 유지(대기일수 에스컬레이션은 필요시 별도 상신)
- ②status order 재배열(구현 5·설계승인대기 6·테스트봇검증 7·이사님승인 8·배포 9·폐기 10, 4개 프로젝트)은 **승인 후 적용**(Taiga 4개 프로젝트 40상태 PATCH)
- 단위시험: 과거키 이관(발령 0, 중복 0) / 구현 재진입(이력 1→2, 재발령) / 8024 원장착신(id 1790980847873-134) — 3/3
## 승인 후 적용 절차
1. dispatcher.py 교체+재시작 → 과거키 자동 이관(중복발령 0) 확인
2. status order 재배열: 4개 프로젝트 × 6상태 PATCH(전체 order 재부여)
3. 검증(티켓): 설계승인 판정 직후 회의방/8024에 구현 발령 1회 / 중복 발령 0
## 롤백
- dispatcher.py 원복+재시작. status order는 원값으로 되돌리기(변경 전 실측값: 5/5/6/7/8/9 — branch-g4.md 보존)

## 적용·검증 (10-03 11:40, 98 — 이사님 승인 [10-03] 후)
- 적용: dispatcher.py ← G4-patched 교체(G4·G5 동일본 60ca3ad — 한 번에 2건 적용) → py_compile SYNTAX_OK · import IMPORT_OK → `systemctl --user restart taiga-dispatcher` → active, "dispatcher start" 11:40:15.
- 과거키 승격 이관 실측: 기존 단순키(4:82·4:89 등)가 1회차 루프에서 `:impl`키로 승격(10/13키, 타임스탬프 보존 2026-09-20T15:22 — 중복발령 0). 4:85·4:86은 구현상태 아니어서 미이관(스킵 경로 — 정상, 진입시 이관).
- 신규발령 0 실측(6분 경과, 에러·트레이스 0) — 전 티켓이 `:impl`키 보유로 2회차 루프에서도 재발령 없음(G1·G3과 상호정합).
- status order 재배열(40상태 PATCH)은 티켓 절차 2번 — 이번 회차 착수 후(아래 후기).
- ②status order 재배결과: (미실시 — 다음 회차, 본 티켓 회신에 별도 기록. 승인게이트 ② 적용 범위는 4프로젝트×6상태)
- 롤백 1줄: `cp ~/services/taiga-bridge/dispatcher.py.bak-g4g5 ~/services/taiga-bridge/dispatcher.py && systemctl --user restart taiga-dispatcher`
- 근거: 준비본 60ca3ad, notes@본커밋.
