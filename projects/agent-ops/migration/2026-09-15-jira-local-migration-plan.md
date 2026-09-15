# JIRA 로컬 이관 계획 v1 (2026-09-15, 개발팀장 Zcode)

**배경**: Atlassian JIRA 무료 분 종료 임박. 조직 운영-core가 JIRA REST에 결합되어 있어
종료 전 이관 필수. 이사님 승인 후 실행.

## 1. 현재 JIRA 사용 실태 (실측 2026-09-15)

- 인스턴스: `heavenlyiris-matrix.atlassian.net` (cloud, REST v3, Basic auth)
- 소비자 3종:
  1. **봇들** — `.jira-token` + curl로 RELAY 티켓 조회 (status/labels/components) — `~/.cokacdir/values`에 명령 패턴 다수
  2. **matrix-home 8018** — `/api/jira` (main.py 1322) + 홈 대시보드 `jira_pending` 카운트
  3. **이사님(휴먼 뷰)** — 에픽/로드맵 용도 (homeserver-target-design v1: "Jira는 인간용 에픽/로드맵만")
- 이중 보관: notes repo에 RELAY 티켓 markdown 미러 25개 디렉터리 (`relay/tickets/`) — **단, 최신 티켓 상태·댓글은 JIRA에만 존재**
- ⚠️ **API 토큰이 홈에 없음** (AWS 폐기 서버에 있던 `.jira-token` 접근 불가, 세션 아카이브 내 후보 3개 모두 401)

## 2. 대안 비교 (홈서버 예산: RAM 가용 4.3G, 디스크 76G 여유)

| 후보 | RAM | REST API | 에픽/로드맵 UI | 비고 |
|---|---|---|---|---|
| **Taiga** (추천) | ~1G | ✓ 완비 | ✓ (스크럼·칸반·에픽·로드맵) | 도커 6컨테이너, 라이트, JIRA JSON/CSV 임포터 내장 |
| Redmine | ~0.4G | ✓ 완비 | △ (에픽 약함, Gantt는 강함) | 가장 가볍지만 UI 구식 |
| Plane | ~2G+ | ✓ | ✓ 최신식 | 컨테이너 8개+ — 현재 부하에 과함 |
| OpenProject | ~1.5G+ | ✓ | ✓ | 무거움, 관공서 스타일 |
| 자체 확장 (approval-board+notes) | 0 | 자유 | ✗ | 인프라 0이나 휴먼 로드맵 뷰 없음 — 탈락 |

**선정: Taiga** — 이사님 휴먼 뷰(에픽/로드맵) 요구 충족 + 봇 어댑터 가능한 완전한 REST API + RAM 예산 내.

## 3. 이관 절차 (승인 후 실행)

### 0단계 — 토큰 재발급·전수 백업 (⚠️ 무료 종료 전, 최우선)
1. 이사님: https://id.atlassian.com/manage-profile/security/api-tokens 에서 신규 API 토큰 생성 → `~/.jira-token`(0600)으로 전달
2. 전수 익스포트: RELAY(+기타 프로젝트) 이슈·댓글·첨부 전부 JSON으로 `~/backups/jira-export-$(date)/` (스크립트 준비 완료 가능)
3. notes repo에 최종 스냅샷 markdown 동기화

### 1단계 — Taiga 구축
- `~/services/taiga/` docker-compose (taiga-front/back/gateway/db/rabbit/redis, 포트 8040)
- 엣지 nginx에 8040 라우트 추가, tailscale 직접 접속 우선(방화벽 이슈 회피)
- 이사님 계정 + 봇 API 계정(bot) 생성, 프로젝트 RELAY 생성

### 2단계 — 데이터 이관
- 익스포트 JSON → Taiga 임포터(JIRA 호환) 또는 REST 일괄 생성 스크립트
- 검증: 이슈 수·상태·코멘트 수 대조표 (notes 미러와 3중 대조)

### 3단계 — 소비자 전환
- matrix-home `/api/jira` → Taiga REST 어댑터 (응답 스키마 유지해 프론트 무변경)
- 봇 명령 패턴: `.jira-token` curl → Taiga 토큰 curl로 values/스크립트 일괄 치환
- 관제 공지 후 1주 병행 운영(JIRA 읽기 전용) → 컷오버

### 4단계 — 종결
- JIRA 데이터 최종 익스포트 보관(아카이브 gdive 3차)
- Atlassian 구독 종료

## 4. 롤백
- 3단계까지는 JIRA 원본 유지되므로 어댑터 되돌리기만으로 즉시 롤백
- 4단계(종료)는 이사님 최종 확인 후에만

## 5. 공수
- 0단계: 0.5일 (토큰 대기 제외) · 1단계: 0.5일 · 2단계: 1일 · 3단계: 1일 · 총 ~3일

## 승인
- [ ] 이사님: 계획 승인 + API 토큰 재발급 (0단계 잠금 해제)
