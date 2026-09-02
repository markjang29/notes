# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`) 전관. 활성 작업·대기 결정·다음 스텝만 유지한다.
> 과거 상세는 Git 이력, `work-archive.md`, checkpoints를 본다.
> **2026-08-16 갱신**: 07-12 정지 이후 5주 공백 반영(Windows 종료, Matrix 통합 후임 인계,
> zcode 클라이언트 승계). 07-10~07-12 야간 사이클·승인보드 상세는 `work-archive.md`
> '2026-08-16 아카이브' 섹션으로 이동.

## ★ Matrix 통합 후임 (2026-08-16)

- 담당 actor: `aws-manager`
- 교대 결정: `decisions/2026-08-16-matrix-successor-handoff.md`
- 전체 정본: `matrix_asset_agent` 최신 main의 `collaboration/MATRIX-SUCCESSOR-HANDOFF.md`
- 현재 카드: `NEXT-001` 동일조건 Codex/ZCODE/RISU 품질시험
- Clear는 대화 컨텍스트만 지울 수 있다는 뜻이며, 제품 완료나 서비스 정상 판정이 아니다.
- 아래 한 문장으로 새 세션을 시작한다.

```text
너는 Matrix 통합 후임이다. matrix_asset_agent 최신 main의 collaboration/MATRIX-SUCCESSOR-HANDOFF.md를 전부 읽고 [MATRIX-SUCCESSOR-CERT]를 출력한 뒤, 문서에 적힌 전체 Git의 최신 origin/main과 역할 경계를 재검증하고 NEXT-001부터 작은 카드로 실행·검사·commit·push·보고하라.
```

## 조직 현황 (2026-08-16, actors.json v8)

- Windows Codex·ZCode 구독 종료(08-16). 신규 **zcode 클라이언트**(telegram-zcode-bridge 구동)가
  승계자로 활동 중.
- zcode 클라이언트가 이어받음:
  - Windows 자산 수집 파이프라인(아카 수집/다운로드/디코딩/중복제거 → `matrix_asset_agent` 입고).
    노하우 정본은 Windows 인수인계 문서 `handover-2026-08-16.md`, 이식 착수 예정.
  - 매니저가 직접 실행 금지라 비어있던 '직접 실행 작업자' 역할(예: 8011 ZCODE 서비스 복구).
  - 팀장 봇이 content policy로 blocked 남긴 기계적 처리(성인 픽션 포함 소설 수집·가공·카탈로그) 이관.
    정책 유지: NSFW를 이유로 버리지 않고 동일 provenance/security/quality gate.
- 매니저(`@heav_lnx_bot`): 조율·배정·보고 전관 + **LIVING-DRAMA-OS(Matrix) 통합 작업자 겸직**.
  repo 범위에 matrix 7종(`matrix_asset_agent`/`scenario`/`matrix`/`matrix_zcode`/`matrix_codex`/
  `matrix-engine`/`matrix-living-drama`) + `music_video`(08-08 추가) 포함.
- `aws-trader`: 07-16 이사님 지시로 pause. 재개는 이사님 결정.
- 퇴역 windows-codex/windows-zcode 잔여 권한(크론·approval-board 클라이언트 토큰·시스템 프롬프트)
  감사: 08-16 감사봇 의뢰 진행 중(아래 대기 결정 #3).

## Matrix 다음 카드 (NEXT-001~005; 정본은 handoff 문서)

1. **NEXT-001 동일조건 품질시험** — 같은 모델·요청·온도·출력 예산 고정, 8011/8012/RISU를
   첫 장면·10턴·20턴·재개로 비교. 실행 결과 없이 승자 선언 금지.
2. NEXT-002 사건 코어 흡수 결정 — `matrix-engine` vs `matrix-living-drama` event schema/reducer/
   checkpoint/replay 비교 → 8012 command bus·SQLite 경계 안에서 수렴. donor 재구현 금지.
3. NEXT-003 reviewed 시츄에이션 10개 — 사람 승인 후 같은 release ID로 8011·8012에 공급.
4. NEXT-004 자율 감독·연출 통합 — living-drama 자율 충돌 결정을 8012 사건 원장 앞단에 결합.
5. NEXT-005 제품 영수증·관찰자 UI — 20턴 종료/재개, 동일 checkpoint 두 분기, 사건 누출 0,
   state digest 일치 검증.

## 크론/스케줄 현황 (07-20 이사님 '스케쥴 다 제거' 이후)

- cokacdir 반복 스케줄 3건(감사 09:10 `D6CA2473` / RPG 01:05 `AB3904F8` / scenario 01:00
  `57F08AB6`) 제거 후 **재등록 없음** → 일일 감사·야간 배정·아침 브리프 자동 기동 없음.
- 시스템 crontab 3건은 보존: request_router_poll(매분, approval-board 인바운드 폴백) /
  session-reaper(*/30) / chat-log-backup(매시 :05).
- ★원칙 유지(07-12 사고 반영): 타 봇 key + 그룹 chat recurring cron 금지. 대상 봇 깨우기는
  `--once` 단발만. recurring이 필요하면 매니저 본인 key + 라우터 경유만.

## 인바운드 작업요청 창구 (07-12 신설, approval-board 8005)

외부 Codex/ZCODE → AWS 봇 작업요청. 원장 `requests.json`(Git), 클라이언트 토큰
`clients.json`(gitignore). 이사님 웹 `/requests`. webhook(POST 즉시) + 1분 cron 폴백 +
claim 잠금(멱등). 메일형 작업지시 계약(Agent Mail v2)은 `projects/agent-ops/` 참조.

## 활성 작업

### 1. Matrix 통합 후임 — NEXT-001 (최우선)

- 각 repo 최신 `origin/main`·`AGENTS.md` 재검증 후 `[MATRIX-SUCCESSOR-CERT]` 출력 → NEXT-001 실행.
- 절대 금지(요약): 후보 무작위 prompt 주입, 모델 요약을 사건 정본으로 저장, 미검토 candidate
  runtime 사용, 매 tick LLM 호출, donor 미독 재구현, 근거 없는 완료 보고.

### 2. zcode 클라이언트 이관 조율

- 파이프라인 이식 착수 지원, 팀장 blocked 작업 이관 창구(승인 보드 경유) 운영.
- 매니저는 배정·조율·입고 관점만; 이식 실행은 zcode 클라이언트.

### 3. RPG — Reasoning-Parry / Godot

- 엔진: Godot 확정. 산출은 repo Git 기준. (07-12 감사 실측: ahead 1 + 미추적 다수 — push 보류)

### 4. autotrader — 백테스트/대시보드 (pause)

- 스택: FastAPI + pandas 백테스트 + Oracle 23ai. 대시보드 Streamlit 8002.
- 07-16 이사님 지시로 actor pause. 재개 대기.

### 5. scenario

- 정본: `projects/scenario/README.md`·`roadmap.md`, 실행 상태는 repo `catalog/asset_lifecycle.ndjson`.
- 07-12 freeze는 해제됨(17:23, 리뉴얼 룰 7조 확정).
- 운영 경계(Matrix handoff 지도): 원본 lifecycle=`matrix_asset_agent`, publication=`scenario`,
  의미 정본=`matrix`.

## 대기 결정

1. 야간 배정·일일 감사·아침 브리프 크론 재등록 여부 — 이사님.
2. autotrader 재개 시점 — 이사님.
3. 퇴역 actor(windows-codex/windows-zcode) 잔여 권한 처분 — 감사 결과 수신 후.
4. ~~07-12 감사 실측 push 잔류~~ **처리 완료(08-30 이사님 push 지시)** — notes `b566eb3`·autotrader
   `de7d041`·rpg `6a35f8d`·scenario `f456eac`·matrix-engine `e0ba2ce`·asset_agent `b534c68`·
   approval-board `e56cfa6`(작업 브랜치). 런타임 산물(.runtime/·director_console.sqlite3·save/·
   *.bak)은 의도적 미커밋 보류. **원격 없는 로컬 전용 repo 6건(matrix-nexus·matrix-studio 등)은
   push 불가 — 신규 원격 생성 여부 결정 대기.**
5. `.reviews/session-reaper.log` 커밋/무시 정책 — 08-30 현시점분은 커밋(`b566eb3`). 반영 정책 결정 계류.

6. codex 폴백망 편입 여부(08-31 실측: codex=OpenAI 직통, zai 8788 폴백망 밖) — 편입 시
   프록시에 OpenAI 호환 엔드포인트 추가 작업 필요. 이사님 결정.

## 세션 클리어 전 체크

```bash
git -C ~/notes status --short
git -C ~/projects/scenario status --short
git -C ~/projects/rpg_game status --short
git -C ~/projects/autotrader status --short
git -C ~/projects/matrix_asset_agent status --short
```

필요 시:

```bash
python3 ~/scripts/export-chat-backup.py --latest --out /tmp/chat-backup.md
```

## ★ 관제 회의방 웹챗 개통 (2026-08-31)

- 텔레그램 그룹 한계(봇→봇 차단·그룹 세션 취약·멀티라인 첫 줄만 처리·N100 구버전)로
  이사님 지시 → **AWS 자체 웹챗 개통 완료**. `~/projects/meeting-room` (git `7d6a9ef`).
- 발언 11기 전원 입장(전달 6·zcode 포함, E2E 실측 통과). 대기 5(firebat 3·asus_zai·heav_ai). 포트 8023.
- 잔여: 대기 5기 합류(firebat 3=N100 cokacdir 업데이트 후 원격 API, asus_zai·heav_ai=소재 확인),
  필요시 systemd 승격, 대화 로그 보존 정책. N100 입장 카드 이사님 경유 전달 완료(08-31, 봇 송신 API 개통).
- 홈 사이트맵 18포트 전량 반영(matrix-home `3a307bb`) + /status 봇 모델·API 현황판 개설(토큰0, meeting-room `e78e557`).

## ★ 로컬 서버 마이그레이션 (2026-08-30 수립) — 최상위 신규 트랙

- 정본: `projects/migration/local-server-migration-plan.md` — AWS=IP/게이트웨이 전용,
  N100 윈도우(백지·온보딩 키트 포함) → 터널 → 서비스 이전 → 로컬 리눅스 개발 본거지.
- 이사님 결정 대기: 터널 방식·이전 순서·N100 봇 정체·AWS 봇 처지.
- 봇 공지 완료(08-30). Phase 1 착수는 이사님 지시 후.
- **AWS 서버 실체 안내서 작성 완료(08-30, 이사님 지시)** — 정본
  `projects/migration/aws-server-guide.md` (629f403): 서비스×포트 지도 22건 · 기동법 5계층 ·
  repo/배포 구조 · 데이터 위치(mongo bind·Oracle volume·Works 93G 등) · 운영 스크립트 ·
  보안 경계(키 위치만, 값 미기록) · 재검증 체크리스트.
  주요 발견: 로컬 전용 repo 6건(matrix-nexus·matrix-studio 등, 이전 전 push 필요) · 디스크 87%
  (Works 93G 병목) · 8021 matrix-studio 미등록 운행 · 8022 등록만 미구동 · Tailscale Funnel 8443
  공개 중. 다음: 이사님 검토 후 Phase 2(터널) 설계.

## ★ 사이트 통합 파이프라인 (2026-08-24, RELAY-49) — 현재 활성

- 이사님 지시로 7단계 통합 파이프라인 확립: 1 리수세팅(8013) → 2 검증 → 3 승인(8005) → 4 매트릭스화 → 5 재테스트(8004 아케이드) → 6 이미지(8016) → 7 코어(CLI·AGENT·하네스) → 수익화(RPG 8009·소설)
- SE 정본 = zcode(RELAY-49), 매니저 = 조직화·게이트. 공통 가이드: notes-registry relay/site-integration-guide-2026-08-24.md (a386af2)
- 통합 홈 허브: 8018 (RELAY-50, zcode)
- **방향 결정(이사님 08-24 승인)**: 4단계 매트릭스화=자산 캡슐화 / 7단계 매트릭스 코어=CLI 클로드코드류 하네스(REPL·RAG·MCP·LSP + 노드 9종 스위치형: Triage direct/simple/complex 관문). 뼈대=matrix_codex 재사용. 원문·결정: relay/tickets/RELAY-49/req.md (a294bc0)
- 8봇 위치 인식 공지 완료, ACK: asset_agent·novel_col 수령(2/8) — 잔여 6봇(audit·arcade·rpg·scenario·
  codex_dev_1/2)에 08-24 19:40 관제그룹으로 ACK 재요청 발송, 회신 대기
- RELAY-42(music_video 일상 페이지) 재검토 **반려 유지** 확정(notes 4871304 review.md — 미해결 1~3 +
  추가 5~7: v1→v2 마이그레이션·카드별 출처·KO/EN/VI seed). 08-24 19:40 codex_dev_1에 수정 착수 지시
  전달. 사이트는 운영 중 8020/#daily(99c8796)
- 대기: zcode에 하네스 설계 반영 지시(매니저→zcode 직통 없음, 이사님 채팅 붙여넣기 필요), 페르소나 324개(RELAY-1) 승인 타이밍
- RELAY-51(8018 홈 보고 카테고리·ELI5 보고함, 이사님 08-24 제안) 발행 `1e7b22d` — 구현 codex_dev_2
  배정(19:5x 발송), 리뷰 codex_dev_1 예정. 완료 시 텔레그램=요약+링크·홈=상세 HTML 분리 확립.
- RELAY-52(이사님 사이트 요구사항 정합성·분류) 발행 `da23d5a` — 원문 verbatim 정본화, 1차 분류
  (S 스튜디오 결함/미구현·H 홈 연동·P 파이프라인 구조). 토의 진행 중(audit 정합성 리드·asset_agent
  스튜디오 판정·rpg·scenario 구조 의견, 22:00 KST 기한) → 취합 후 이사님 안건. NSFW(S8·S12)는
  매니저 직접 담당(이사님 지시). 원문 말미 truncated — 재전송 대기.
- RELAY-52 2차 원문 수령 `61201f0` — V(정체성·실측 원칙)·C(카드 실체)·M(실측)·K(채팅·이미지 정합)·
  T(구조: 승인대기 전체 폐기·제로베이스 1건, 하드차단 최소화, RESTful, DB 마스터번호, 용어 개명)
  추가. 낙관(rpg·asset_agent)/비관(audit·scenario)/팩트(codex_dev) 회의 개제(23:00 KST 기한) →
  취합 후 전체 재설계 안 + "카드 1개 실체" 이사님 ELI5 보고. 2차 원문도 말미 truncated.
- RELAY-52 3차 원문 수령 `f9732f2` — K7(프롬프트 추출 근거)·C6(NAI 모듈 명시·교체)·T8(자산 파일
  byte 표기)·M8(RISU 3회 증적 검수)·K1(채팅전문 버그 지속). 이사님 "분업화 뿌려도 좋아" — 조사·
  판정·기획 즉시 분산 착수 지시 완료, 구현은 재설계 승인 후.
