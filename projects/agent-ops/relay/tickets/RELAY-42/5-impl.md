# [impl] 구현 기록
- jira: RELAY-42
- 구현 담당: codex_dev_1 (이사님 직접 지정: “너야 담당자”)
- 배포일: 2026-08-23 KST

## 커밋 목록(해시 + 한 줄)

- `music_video` `2fe9000e09d1dd0d0f37a314fbd85a88e26e3ac5` — `RELAY-42 여행·일상 분리와 혼인 준비 페이지 추가`
- 설계 근거 `notes-registry` `14f8bf7` — `RELAY-42 여행·일상 분리 설계 및 승인 기록`

## 구현 요약

- `/` 첫 화면에 `여행` / `일상` 선택 추가.
- 기존 여행 DOM/API를 보존하고 `#travel` hash로 진입·새로고침 가능.
- `#daily`에 혼인·TOPIK·F-6 일정/서류 CRUD, 상태·비용 요약, JSON export 추가.
- 신규 데이터는 `aloha-daily-marriage-v1` localStorage에만 저장하고 `/api` POST를 사용하지 않음.
- KO/EN/VI 일상 UI 전환과 공식 출처·기준일 카드 추가.
- 2026-09-11 베트남 Apostille 발효, 한국 선혼인신고 관할기관 확인, TOPIK 비유일성, D-4→F-6 비단정 표현 반영.
- 외부 `unpkg` 실행 스크립트 제거.
- `daily-core.js` 순수 검증/집계/백업 로직과 Node 단위 테스트, 최상위 `check.sh` 추가.

## 테스트 결과(명령과 출력 요약)

- `./check.sh`
  - `node --test tests/daily-core.test.js`: **4/4 pass**
  - `node --check daily-core.js daily.js app.js`: pass
  - `python3 -m py_compile server.py`: pass
  - `git diff --check`: pass
- Playwright 임시 서버 `http://127.0.0.1:18021`: **2/2 pass**
- Playwright 공개 서비스 `http://13.125.131.126:8020`: **2/2 pass**
  - viewport 390x844, 1440x1000
  - 홈→여행→일상, hash 직접 진입, KO/EN/VI, 여행 촬영 5필드 dialog
  - 일상 CRUD·새로고침 localStorage 유지
  - 일상 작업 중 POST 요청 0건
  - 가로 overflow 없음
- 배포 후:
  - systemd `music-video.service`: active
  - `/`: 200
  - `/#daily`: 200
  - `/api/health`: `ok=true`, `git=true`, `translation=true`, model `glm-4.7`
  - `/.git/config`, `/.env`: 404
  - 배포 전후 `content.json` 사용자 데이터 변경 없음(SHA-256 `db0df0add5e86de30f233f608320f44b636934ed3135b666820bed5ef7fad406`)

## spec 대비 이탈 및 사유

- JSON **가져오기(import)**는 구현하지 않았다. spec에서 import는 선택사항이며, 개인정보·스키마 위험을 줄이기 위해 export만 제공한다.
- 사용자 입력 자동 번역은 하지 않는다. spec대로 원문을 보존한다.
- 첨부 HTML의 모든 seed 날짜·서류를 그대로 복제하지 않았다. 확인되지 않은 TOPIK 회차 날짜와 단정적 인증 요구를 제거하고, 공식 확인 중심의 최소 seed만 제공한다.
- 구현 담당자가 원래 6-코드리뷰 전관이므로 자기리뷰를 하지 않는다. 6단계는 codex_dev_2 또는 독립 리뷰어 재배정이 필요하다.
