# RELAY-66 — 테스터 검증 요청: 인사 원장(레거시 라이브) + Spring 이관 커밋 3건

- date: 2026-09-15
- actor: heav_gmwin_claude_bot (GM윈도 인사, 99) — 의뢰: 이사님(09-15 "테스트 역할 봇을 통해 검증받는 게 규칙" 재확인)
- 검증자(담당): heav_gmwin_codex_bot (GM윈도 테스터 코덱스, 97)
- 대상: ① 라이브 레거시 원장 http://43.201.34.144/insa/ ② matrix-studio-spring 인사 이관 커밋 3건(로컬 작업트리: `newux5m2/matrix-studio-spring`, 원격 origin/main)
- 요청 경위: 인사 원장 신규 페이지 설계 승인(A안)→개발 완료. 이사님 규칙에 따라 자체 1차 검증을 마치고 테스터 2차 검증을 정식 요청함. Spring 판 배포(duradev 게이트) 전 코드 리뷰를 포함.

## 01-근거 (evidence)

| kind | ref | 비고 |
|---|---|---|
| artifact | 원장 v2 커밋 `4dce19e` (notes projects/agent-ops/roster.json) + 자동 동기 `dcf89ab`(09-15 표기명 3건) | 유일 변경 경로=git commit |
| measurement | whois 파리티: Java 이식 사양 vs 라이브 8031 — 배터리 17질의 17/17 일치 (09-15 실측) | 키워드 적중도 원장 봇이면 원장 필드로 응답 확인 포함 |
| measurement | 실렌더 검증: `web-react/render-check.cjs` 11항목 11/11 PASS (빌드 산출물 + 라이브 데이터 주입) | 이 검증에서 크래시 버그 1건 발견→수정 커밋 `2596247` |
| artifact | Spring 이관 커밋: `4d5ec14`(base 태그 수정) · `f54a040`(insa 기능) · `2596247`(렌더 크래시 수정) — matrix-studio-spring origin/main | 라이브 검증 항목: /assets 404→/react/assets 200 해소 |

## 02-미완료 (remaining)

| 항목 | 현재 상태 | effort |
|---|---|---|
| ① 라이브 http://43.201.34.144/insa/ 검증 — 정원장 21봇 표·판정 표기·whois 검색·오늘 동기분([홈서버] [개발팀장] Zcode) 노출 | 테스터 검증 대기 | S |
| ② `/insa/api/roster` · `/insa/api/whois?q=` 응답 계약 재현 검증 (파리티 배터리 재실행) | 테스터 검증 대기 | S |
| ③ Spring 이관 3커밋 코드 리뷰 — InsaPageController(60초 캐시·폴백·whois)·React 엔트리(P8·base 태그)·render-check.cjs | 테스터 검증 대기 — GM윈도 로컬 `newux5m2/matrix-studio-spring` | M |
| ④ 8024 `/insa` 라이브 검증 | duradev 배포 후에만 가능(매니저 게이트) — 배포 완료 후 본 티켓에 후속 요청 | 배포 의존 |
| ⑤ 단위테스트 9건(InsaPageControllerTest) 실행 | 로컬 Java/Maven 부재 — duradev 게이트 FULL TEST에서 실행 예정 | 배포 의존 |

## 03-블로커 (blockers)

| 항목 | 해제조건 | 담당 |
|---|---|---|
| ④⑤는 duradev release 게이트(빌드→소나큐브→Release→FULL TEST) 선행 필요 | 매니저(heav_lnx_bot) 게이트 실행 | 매니저 |

## 04-다음 (next)

1. 테스터(97)가 ①②③ 수행 → 결과를 본 티켓에 회신 코멘트(또는 `/tests` 리포트 링크)로 기록
2. ①~③ 통과 시 매니저에게 duradev 게이트 실행 요청(인사봇 경유 보고)
3. 배포 완료 → 인사봇이 ④ 라이브 검증 재요청(본 티켓 후속) → 테스터 최종 확인
