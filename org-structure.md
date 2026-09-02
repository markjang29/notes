---
title: 조직 구조 — Telegram 그룹 매니저-팀장 협업
date: 2026-06-26
status: 확정 v1 (2026-06-26, Telegram 그룹 세팅 완료)
tags:
  - org
  - telegram
  - collaboration
---

# 조직 구조 — Telegram 그룹 중심 협업

> 모든 봇을 **Telegram 한 그룹 채팅**으로 모은다. 총 매니저가 중심이 되어 보고·조율·아이디어 회의·의사결정 support. 실시간은 그룹, 영구 기록은 `~/notes`.

## 그룹 구성 (Telegram) — 확정
- **사용자(준희)** — 최종 의사결정자, 아이디어/방향.
- **총 매니저 봇 `@heav_lnx_bot`** (이 봇) — 조율·보고·회의 정리·ADR support·쿼터 감시.
- **RPG 팀장 봇 `@heav_lnx_rpg_bot`** — 프로젝트 실행 + subagent 직원.
- **trader 팀장 봇 `@heav_lnx_trader_bot`** — 프로젝트 실행 + subagent 직원.
- **시나리오 팀장 봇 `@heav_lnx_scenario_bot`** — **RISU 자산 기반 창작 스튜디오**. repo `~/projects/scenario`. 2026-06-30 신설. 2026-07-04 이후 최신 기준은 `principles/scenario-team-purpose.md`가 우선한다: 자의적 자생서사는 금지, RISU 기반 draft 창작은 본업, 디벨롭은 이사님 컨펌 후, RPG 의뢰 시 RPG=클라이언트/시나리오팀=창작 서포터로 협업한다.
- (향후 팀장 추가 시 동일 패턴)

## 운영 사이클 (매니저 주도)
1. **진행 보고** — 매니저가 각 팀장 진행상황 수집·정리 → 사용자에게 요약 보고 (정기 cron 또는 사용자 호출 `@heav_lnx_bot 보고`).
2. **팀장 요청 라우팅** — 팀장이 리소스/결정/승인 요청 → 매니저가 정리 → 사용자 전달.
3. **아이디어 회의** — 사용자↔매니저(필요시 팀장 참여) 논의 → 매니저가 정리(옵션+트레이드오프).
4. **의사결정 support** — 매니저가 정리안 → 사용자 결정 → **ADR화**·팀장에 배포(`@팀장`).

## 조직 발전 로드맵 (이사님 09-02 확정)

4단계 북극성 — 각 단계 완료 후 다음 단계:

1. **사이트 정합성 구축** (현재 진행) — 모든 봇이 맡은 사이트·서비스를 데이터·카드·
   프롬프트 정합(실측 원칙)으로 완성. RELAY-52 요구사항 정합성 → 분업 구축.
2. **CLI화** — 각 기능을 명령줄/API로 조작 가능하게(웹 UI 의존 제거). 관제 회의방(8023)이
   그 자체로 CLI/API 기반 인프라의 원형.
3. **MCP화** — 기능을 MCP 도구로 노출 → 봇들이 표준 프로토콜로 서로의 서비스를
   도구 호출(승인보드·자산뱅크·회의방 도구화).
4. **Agentic 자율 운영** — 봇이 스스로 계획→MCP 도구 호출→검증 루프. 매니저 배정만으로
   자율 실행·보고.

RELAY-49 7단계(CLI 클로드코드류 하네스: REPL·RAG·MCP·LSP)가 2~3단계 코어에 해당 —
동일 방향의 구현체.

## 메시지 프로토콜 (cokacdir 그룹)
- `@heav_lnx_bot <...>` — 사용자→매니저 지시/질문.
- `@heav_lnx_rpg_bot <...>` / `@heav_lnx_trader_bot <...>` / `@heav_lnx_scenario_bot <...>` — 매니저→팀장 task 배정 (또는 사용자 직접).
- `;<...>` — 전체 브로드캐스트 (사칙 변경 등 공지).
- `/query@봇 <...>` — 특정 봇 쿼리.

## 토큰/쿼터 관리 (context-budget 연계)
- **컨텍스트 자동 압축 정책(이사님 09-02 확정)** — 전 봇 기본. claude 계열은
  `~/.claude/settings.json` env(`CLAUDE_CODE_AUTO_COMPACT_WINDOW=300000`,
  `CONTEXT_LIMIT_TOKENS=1000000`)이 모든 기동(봇·회의방·인터랙티브 공통)에 상속되어
  이미 활성. zcode는 CLI 자체 압축, N100 폴러도 동일 정책 준용. 컨텍스트 이유로
  새 세션을 권장하지 않는다 — 압축 이어가기 기본, 압축 직후 중요 디테일만 재확인.
- **mention 기반** — 필요한 봇만 깨움, 비활성 봇은 토큰 0.
- **/contextlevel 확정값:** 매니저 `8` (팀장 활동 가시) / 팀장 `0` (mention 수신만). 그룹에서 `@봇 /contextlevel N` 설정. 운용하며 조정.
- **수면 batch** — 매니저가 cokacdir cron으로 팀장 task 예약 (5h 쿼터 윈도우 활용).
- token-report 훅으로 그룹 소비 감시 → 임계 시 인계(context-budget §3).

## 역할 분담
- **사용자:** 결정·방향·아이디어 추가. (작업 기획·배분은 **매니저 영역** — 이사님이 일일이 지시할 필요 없음. 이사님 피드백 06-30.)
- **매니저:** **작업 기획·배분 주도** — 매니저가 판단해 팀장에게 배정. **실행(실제 작업)은 팀장이 하고, 매니저는 직접 작업 금지**(보고·조율만 — 팀장 둔 의미 살리기). 이사님께는 정해진 시간에 **결과 + 결정 안건** 보고 (할 일/지시 내용 반복 금지 — **결과 중심**). 시간 보고는 항상 **KST**. work-queue 조율, 회의 정리, ADR support, 쿼터 감시, 팀장 온보딩 감독(사칙 인증 확인).
- **팀장:** 프로젝트 실행, subagent 직원 소환, Codex 검증 루프, 진행 보고.
- **직원:** 팀장이 subagent로 task 단위 소환. 영구 봇 아님.

## 통신 계층 분담
- **실시간 조율·보고·회의** → Telegram 그룹.
- **영구 기록·인계·결정(ADR)·큐** → `~/notes` (`work-queue.md`, `decisions/`, `.reviews/`).

## 체크리스트
- [x] 봇 ID: 매니저 `@heav_lnx_bot`, RPG `@heav_lnx_rpg_bot`, trader `@heav_lnx_trader_bot`, 시나리오 `@heav_lnx_scenario_bot`
- [x] 그룹 채팅 생성 + 봇 초대
- [ ] BotFather 프라이버시모드 off (각 봇 `/setprivacy` → Disable) — 2026-08-30 회의 단체방
      신설로 **전 봇(N100 포함) 대상 재필요**, 변경 후 재초대 (아래 §회의 단체방 규칙 1)
- [ ] 그룹에서 `/contextlevel` 설정 — 회의 단체방 규칙(발언 8 / 전달 0)으로 적용
- [x] 본 구조 → ADR `decisions/2026-06-26-org-telegram-group.md`

## 회의 단체방 (2026-08-30 이사님 신설 — 전 봇 초대)

- 하드웨어 전체(AWS·N100) 봇이 한 방에서 회의·조율. cokacdir 그룹챗 운용 규칙 정본은
  `~/.cokacdir/docs/how-to-use-group-chat.md`.
- **방 정체(08-31 확정)**: 기존 **관제그룹을 재활용** — 이사님이 전 봇 추가 초대로 회의방
  편성 완료. 신규 방이 아니므로 방 ID 재확보 불필요.

### 하드웨어별 발언/전달 분류

**전체 봇 16기 (BotFather 실측, 이사님 08-31 확인)**

**AWS — cokacdir 10기**

- **발언**: 매니저 `@heav_lnx_bot`(진행·통합보고) · rpg `@heav_lnx_rpg_bot` · scenario
  `@heav_lnx_scenario_bot`(각 현황 보고) · audit `@heav_lnx_audit_bot`(감사 소견)
- **전달만**: trader `@heav_lnx_trader_bot`(pause — 재개 안건 시에만 발언) · asset_agent ·
  arcade · novel_col · codex_dev_1/2 (지시 수신용)

**AWS — 자체 브리지 1기**: `@heav_lnx_zcode_bot` (zcode 클라이언트 다리, cokacdir 밖 —
`/contextlevel` 없음). 08-31 매니저 조치 완료: 그룹방에서 @멘션/자기 답장에만 반응하는
가드 추가(비허용 방 ⛔ 도배 방지) · 재시작 KillMode=process 드롭인으로 8018·8021 생존
검증 · 소스 내 폐기 토큰 하드코딩 제거 · **회의방(관제그룹) 허용 목록 추가·재시작 완료**.
그룹 사용법: `@heav_lnx_zcode_bot <지시>` (1:1은 종래대로 아무 텍스트).

**AWS 10봇 /contextlevel 서버 직접 세팅 완료(08-31)** — 발언(매니저·rpg·scenario·audit)=8,
전달(trader·asset_agent·arcade·novel_col·codex_dev_1/2)=0. 매니저가 bot_settings.json에서
직접 반영(붙여넣기 블록이 첫 줄 봇만 처리되는 문제의 우회). firebat 3기는 N100 쪽 설정.

**N100 firebat — 3기**: `@heav_firebat_claude_bot`(**발언** — n100-zcode, actors.json v9 등록,
온보딩·Phase 2/3 이전 주체. **담당 프로젝트: matrix-studio-spring(8024, RELAY-58) —
이사님 09-02 지정. LLM=llmgateway 오푸스(claude-opus-4-8), 회의방 /api/bot/config 창구**) ·
`@heav_firebat_zcode_bot`·`@heav_firebat_codex_bot`(텔레그램 배당 미등록 — 3기 모두
**관제 회의방에는 09-02 입장 완료**, 원격 폴러로 발언)

**신규 3기 (09-02 이사님 추가 — 온보딩 전)**: `@heav_gmwin_claude_bot` ·
`@heav_gmwin_zcode_bot` · `@heav_gmlnx_claude_bot`. 회의방 명부 ⏳ 대기 등록 완료.
**온보딩 정본: `projects/agent-ops/new-bot-onboarding.md`** (git 제로→관제 합류→합류 시험).
합류 절차: 폴러 연결(§3) → 매니저가 명부 갱신.

**기타 1기**: `@heav_asus_zai_bot`(소재·용도 확인 중, 미등록) — `@heav_ai_bot`은
**삭제됨(이사님 09-02)**, 명부에서 제거.

### 위치별 봇 배치 (09-02 이사님 명명 확정)

- **awslnx**(구 lnx, AWS 리눅스 — 관제 본점): `heav_lnx_bot`(매니저·총괄) · `heav_lnx_rpg_bot` ·
  `heav_lnx_scenario_bot` · `heav_lnx_trader_bot` · `heav_lnx_audit_bot` · `heav_lnx_asset_agent_bot` ·
  `heav_lnx_arcade_bot` · `heav_lnx_novel_col_bot` · `heav_lnx_codex_dev_1_bot` ·
  `heav_lnx_codex_dev_2_bot` · `heav_lnx_zcode_bot`(브리지) — **11기**
- **firewin**(파이어뱃, N100 윈도우): `heav_firebat_claude_bot`(RELAY-58 담당) ·
  `heav_firebat_zcode_bot` · `heav_firebat_codex_bot` — **3기**
- **gmwin**(지앰택 윈도우): `heav_gmwin_claude_bot` · `heav_gmwin_zcode_bot` — **2기 신규**
- **gmlnx**(구 지앰텍, 리눅스): `heav_gmlnx_claude_bot` — **1기 신규**
- **asus**(노트북): `heav_asus_zai_bot` — **1기**(소재 확인 중)
- 총 **18봇 · 5거점** (`heav_ai_bot` 삭제 반영 — 이사님 09-02). 사람 계정: 이사님 · 노트북_Zcode 수집기 · 노트북(asus).

**배당표 미등재 6기** (firebat_zcode·firebat_codex·asus_zai·heav_ai·lnx_zcode브리지 등) —
actors.json v10 등재는 이사님 승인 후 진행.

**사람 계정(봇 아님)**: 한 준희 이사님 · 노트북_Zcode 수집기 · 노트북

### 관제 회의방 웹챗 — 08-31 신설, 조직 소통 본거지

텔레그램 그룹의 구조적 제약(봇→봇 송신 차단·그룹 세션 취약·N100 구버전)을 우회하기
이사님 지시로 AWS 자체 웹챗을 열었다. **정본 `~/projects/meeting-room/README.md`**.

- 접속: `http://13.125.131.126:8023/` + 액세스 토큰(토큰 값은 `.env`에만, 채팅·Git 금지)
- 사용: `@봇 지시` 또는 칩 선택(기본 매니저). 방 로그 최근 24건이 매 봇 구동마다
  주입되어 **봇끼리 서로의 발언이 가시** — 텔레그램에서 불가능하던 부분의 해결.
- 참여: **14기 입장(08-31 11기 + 09-02 firebat 3기)** — 매니저·RPG·시나리오·감사·trader·
  자산에이전트·아케이드·소설수집·dev1·dev2·zcode(z.ai 엔진, `zcode.cjs -c -p`)·
  firebat claude/zcode/codex(N100 원격 폴러). **대기 2기**: asus_zai·heav_ai(소재 미확인).
- **★단일 채널 정책(이사님 09-02)**: 봇 간 통신·작업지시·보고는 **모두 이 회의방으로 통일**.
  텔레그램 그룹 중계·이사님 수동 붙여넣기 배달 폐지. 봇→봇 호출은 방 안 @멘션
  (maybe_relay), 지시·보고도 방 안에서. 텔레그램은 긴급 1:1만.
- 세션: 봇별 전용 워크스페이스(`workspaces/<bot>/`). 꼬이면 `.session_id` 삭제로 리셋.
- 텔레그램은 **긴급 1:1 채널로 유지** (그쪽은 이미 정상).

### 운용 규칙 (그룹챗 문서 기준)

1. **전제 — BotFather 프라이버시모드 off**: 각 봇 `/setprivacy` → Disable. 변경 후 해당 방에서
   **재초대**해야 적용. off가 아니면 `;` 프롬프트·일반 메시지를 아예 못 받는다.
2. **지시는 `@봇이름 내용` 타겟팅이 기본**. `;`는 방 안 전 봇에 동일 지시가 각각 실행되는
   브로드캐스트(중복 작업·토큰 비용·응답 홍수) — 전체 공지 등 의도적 경우만.
3. **/contextlevel**: 발언 봇 8(공유 로그 가시 — 다른 봇 발언 인지), 전달 봇 0(토큰 절약).
   봇별 개별 설정: `@봇이름 /contextlevel N`. 기본값 12.
4. **/public off 유지**(기본 owner-only) — 이사님 주관 회의 방침.
5. 봇은 봇별 큐로 **순차 처리** — 동시 즉답 아님.
6. 공동 작업 규칙 커스터마이즈 가능: `~/.cokacdir/prompt/cowork.md`.
7. 새 방 ID는 봇이 그 방에서 첫 응답을 해야 bot_settings에 등록된다 — 초대 직후 각 봇을
   `@봇이름 /contextlevel N` 한 번으로 기상·등록·세팅을 겸한다.
8. **여러 봇 멘션은 봇별로 메시지를 분리**해서 보낸다. 한 메시지에 여러 줄의 @멘션을
   붙여넣으면 **맨 첫 줄 봇만 처리**되고 나머지는 무시된다(08-31 실측 — 이사님 3회
   시도 전부 첫 줄 매니저만 적용). 봇→봇 송신은 텔레그램이 차단하므로 기상·설정 명령은
   반드시 사람 계정이 보내거나, 매니저가 서버(bot_settings)에서 직접 세팅한다.
