# [req] 8018 홈 보고 카테고리 페이지 (ELI5 보고함)
- jira: RELAY-51
- 출처(원문 그대로 인용): 이사님 2026-08-24 매니저(aws-manager) Telegram:
  "스킬이 html 로 만드는거면 우리 홈에 보고용 카드테고리 페이지 설계해서 하나 따던지?"
- 발화자/채널/일시: 이사님(director) → 매니저 Telegram, 2026-08-24 수령
- 배경: `eli5@claude-community` 플러그인 설치(전 봇 공유) → HTML 시각 설명 생성. 동시에 이사님
  보고 형식 4규칙("맨날 .txt 나 .md 파일 열어서 보는거 불편함") 확립. 텔레그램=요약+링크,
  8018 홈=상세 HTML 보고판으로 분리.

## 설계 초안 (매니저)

- 대상: `~/projects/matrix-home/main.py` (8018, RELAY-50 zcode 소관 — 이사님 직접 제안으로 진행,
  완료 후 zcode 통보)
- 라우트: `GET /reports` — 카테고리별 카드 목록(최신 상단), `GET /reports/{category}/{slug}` —
  개별 HTML 렌더(샌드박스: 외부 스크립트/링크 차단, 로컬 파일만).
- 저장: `~/projects/matrix-home/reports/<category>/<slug>.html` + 동봉 `index.json`
  (title, bot, created_at KST, ticket). 게시 = 해당 repo 커밋(shared-git 정책, 배정받은 등록 actor).
- 카테고리 초기값: `operations`(운영보고) / `decisions`(결정·ADR) / `explain`(ELI5 설명).
  추가는 이사님 결정.
- 홈(`/`)에 "📊 보고함" 카드 1개 추가, 포트 8018 불변.
- 텔레그램 규약: 봇 보고 시 본문 요약(4규칙) + `/reports` 해당 카드 링크 동봉.

## 담당
- 구현: `codex_dev_2` (aws-codex-dev, 구현 지원 역할, 현재 재검토 대기로 유휴)
- 리뷰: `codex_dev_1` (self-review 회피 — RELAY-42과 역방향)
- 완료 기준: /reports 카테고리 3개 렌더 + 샘플 1개 게시 + 홈 카드 추가 + 커밋·non-force push
  + 8018 실측 스크린샷/링크 + 관제그룹 완료 보고.
