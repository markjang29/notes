# 아케이드 → 홈서버(duradev) 이관 명세 v1

- 작성: 아케이드 봇 (heav_lnx_arcade_bot)
- 일자: 2026-09-07
- 근거: 이사님 직접 지시 "니가 맡았던 페이지나 개발건 홈서버 쪽으로 옮기고
  프론트 타고 넘어갈 수 있게 이관 후 접속정보 수정" (티켓 매니저 발행 병행 대기)
- 목적: AWS 매니저 박스(13.125.131.126) 개별 포트 → 홈서버(duradev) +
  엣지(43.201.34.144) 경로 통합. 원사이트 통합·포트 정리 방향 준수.

## 1. 이관 대상

### 1-A. 8004 arcade-playable (본 명세로 이관 진행)

- 소스: matrix_asset_agent `tools/arcade_playable_server.py` +
  `arcade_playable_web/` (matrix_asset_agent cdf24c1)
- 기능: PLAYABLE 자산화 보고서 + 30셋 카드 + 최신 카탈로그(1,066) 라이브 +
  GLM 승인 게이트(미승인 403) + /api/approve·releases
- 준비 완료 (cdf24c1 push): `ARCADE_BASE_PATH=/arcade` prefix 지원,
  `ARCADE_PORT` 포트 지정. 미설정 시 기존 루트 서빙과 100% 동일(회귀 없음
  — 양 모드 실측 검증 완료: 301 리다이렉트, fetch 치환 4경로, API/data.js
  200, 게이트 403 유지).

### 1-B. 8010 arcade (matrix-engine v0.3.0, 1,116 카드)

- 별도 이관 건 — 서비스 규모가 커서 8004 완료 후 매니저 조율로 진행.
  본 명세 범위 밖 (RELAY-54 gap "8010 파이프라인상 위치"와 병행 검토).

## 2. duradev 배치 절차 (공개키 등록 후 실행)

```bash
# 0) 접속: ssh duradev (키 등록 선행 — 허브 m1a07c46f427f4e9f7로 요청)
# 1) 소스 확보
git clone https://github.com/markjang29/matrix_asset_agent.git ~/matrix_asset_agent
# 2) 30셋 카드 데이터 재생성 (data.js는 .gitignore *.js 규칙으로 미추적 — 생성물)
cd ~/matrix_asset_agent && python3 tools/arcade_playable_web.py
# 3) 최신 카탈로그 원본 (scenario repo clone 경로를 env로 지정)
git clone https://github.com/markjang29/scenario.git ~/projects/scenario
#    → systemd 유닛에 SCENARIO_REPO=$HOME/projects/scenario 환경변수 필수
# 4) systemd 유저 서비스 (기존 AWS 쪽 유닛과 동일 + 환경변수 2개 추가)
#    ARCADE_BASE_PATH=/arcade  ARCADE_PORT=8004  RELAY_TICKET=<티켓발행后 갱신>
# 5) 헬스체크
curl -s localhost:8004/arcade/api/catalog   # total 1,066 기대
curl -s -o /dev/null -w '%{http_code}' localhost:8004/arcade/  # 200
```

## 3. 프론트 연결 (엣지)

- 엣지(aws512-edge) nginx에 라우트 등록: `/arcade/` → `duradev:8004`
  (`/arcade`, `/arcade/api/*` 전부 — 요청은 gmwin claude에 허브로 전달 완료)
- 등록 후 실측: `http://43.201.34.144/arcade/` 200 + 카탈로그 API 1,066

## 4. 접속정보 정리

| 구분 | 이전 | 이관 후 |
|---|---|---|
| 매장(8004) | http://13.125.131.126:8004/ | http://43.201.34.144/arcade/ |
| 홈 카드 링크 | http://13.125.131.126:8004/ | `/arcade/` 경로로 수정 필요 |

- 홈(8018, duradev 이전 완료 상태)의 "🎮 매장 — 아케이드" 카드 링크를
  `/arcade/`로 바꾸는 작업이 접속정보 수정의 핵심. 엣지 라우트가 열린 뒤
  홈 소스에서 수정 (duradev 접근 확보 후 아케이드 봇이 수행 예정).
- 구 주소(13.125.131.126:8004)는 8010 등 미이관 서비스와의 전환 기간 동안
  유지하고, 8010 이관 완료 시 함께 폐쇄하는 것을 권장 (전환 기간 병행 서빙).

## 5. 의존·gap (이관 후에도 남는 것)

1. GLM 재테스트 원본 자산: `~/Works/arcalive` (대용량 zip) — duradev 미보유.
   재테스트(/api/generate)는 승인 게이트 뒤에 있어 미승인 상태로는 미사용.
   원본 복사 또는 공유 마운트 결정이 필요하면 이사님 결정 사항.
2. approvals.jsonl(승인 장부)·releases.ndjson은 Git에 있어 clone 시 따라옴.
3. SCENARIO_REPO가 없으면 /api/catalog만 비활성(빈 카탈로그) — 나머지 기능
   정상. 절차 3)을 빼먹지 말 것.
4. RELAY_TICKET: 재연결·이관 작업의 정식 티켓이 매니저 미발행 상태 —
   발행되면 systemd 환경변수 갱신.

## 6. 검증 체크리스트 (이관 완료 판정 기준)

- [ ] duradev 로컬: /arcade/ 200, /arcade/api/catalog 1,066, 게이트 403
- [ ] 엣지: http://43.201.34.144/arcade/ 200 (이사님 네트워크 기준)
- [ ] 홈 8018 카드 링크가 /arcade/로 바뀌었고 클릭 시 도달
- [ ] 구 주소 병행 서빙 확인 (전환 기간)
- [ ] systemd 유닛 등록·부팅 자동기동·RELAY_TICKET 기입

## 7. 진행 상태 (2026-09-07)

- [x] 앱 코드 BASE_PATH/PORT 지원 (cdf24c1 push)
- [x] data.js 재생성 절차 검증 (클론에서 `tools/arcade_playable_web.py` 성공)
- [x] 엣지 라우트·duradev 공개키 등록 요청 (허브 m1a07c46f427f4e9f7)
- [ ] duradev 키 등록 회신 → 배치 실행 (블로킹: 아케이드 봇의 duradev 접속 권한)
- [ ] 엣지 /arcade/ 라우트 등록 (블로킹: gmwin claude)
- [ ] 홈 카드 링크 수정 + 전 구간 실측
