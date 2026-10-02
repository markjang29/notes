# GOV#28 [G6] 브리지 군집 정리 (2026-10-02, 98)

## 재현 (조치 전 — ~/services/taiga-bridge: bridge·agenda·dispatcher·tester 4파일)
- ①def taiga 4곳 복붙(bridge:24-38·agenda:25-43·dispatcher:23-41·tester:20-38행), 401 재인증시 creds.json을 4 프로세스가 각각 json.dump 덮어쓰기(잠금 0) — 최근 7일 "token refreshed" 7회 실측(동시쓰기 위험의 실증)
- ②타이가 주소 4곳 모두 공인IP 하드코딩(TAIGA="http://43.201.34.144:8040/api/v1") — 로컬 127.0.0.1:8040은 200(실측, 2ms)인데 미사용
- ③프로젝트ID·상태명 4곳 흩어짐(PROJECTS·GATES·REAL_SLUGS 등)
- ④agenda hash — 이미 수정됨(확인만): agenda.py:57 `hashlib.sha1(...)` — 프로세스솔트 hash() 아님. 추가 조치 없음

## 조치
1. **공통 모듈 신설** `taiga_common.py`: taiga() 1곳 단일화 + 401 재인증(잠금내 중복검사 — 남이 갱신했으면 그 토큰 재사용) + creds.json 쓰기 fcntl 잠금(tmp+replace) + 로컬우선(127.0.0.1:8040 → 공인IP 폴백, 300초 재판정) + PROJECTS·SLUGS·STATUS 상수 집결
2. **4파일 전환**: def taiga 블록 제거 → `from taiga_common import taiga` 1행. 사용 0인 TAIGA 상수 3곳·bridge.reauth는 공통모듈 래퍼로. 남은 "8040" 문자열 3행은 표시용 링크뿐 — API 주소 하드코딩 0(1곳화)
3. 백업: ~/.local/share/taiga-bridge-backup-20261002/

## 시험중 발견·수정 (taiga_common 개발 실측)
- /auth는 Content-Type 헤더 없으면 400
- _save_creds 이중 open 제거
- 401 except 내 잠금+재인증 동시 수행시 같은 프로세스 fd2개 LOCK_EX 데드락 → "잠금내 열람만, 재인증·저장은 잠금 밖"으로 분리(faulthandler로 지점 실측: 70행 flock)

## 검증 (같은 명령)
- 3서비스(bridge·agenda·dispatcher) 재기동 후 active, 오류 로그 0
- 실사용: bridge.taiga→공통모듈로 by_ref INFRA#11 읽기 성공(id 161), 로컬우선 base=127.0.0.1:8040 확인
- 401→재인증→재시도 단위시험: 강제 401 후 by_ref 161 복구, token 갱신+잠금 저장
- creds.lock 신설(0byte — 잠금 전용)
- tester는 타이머(다음 실행시 신규 경로) — 별도 검증 불필요(동일 import)

## 범위 밖 (미접촉)
- 웹훅 검토·폴링주기·배포상태 증거연결·보류 재상신: G6의 '검토' 안건/타 티켓(GOV#24 등) — 티켓 지시 범위 밖
