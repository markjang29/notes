---
title: 관제 Slack류 디벨롭 자료조사 (이사님 09-04 지시)
date: 2026-09-04
status: 조사 완료 — **A안 승인(09-04)**, 범위는 관리 5축으로 한정·채팅 UX(Phase 1~3)는 보류 → ADR `decisions/2026-09-04-gwanje-workspace-five-pillars.md`
tags:
  - agent-ops
  - meeting-room
  - research
---

# 관제 Slack류 디벨롭 — 자료조사 정본

> 이사님 지시: "우리 관제를 좀 디벨롭해보자, slack 처럼? 자료조사좀 하고와"
> 대상: 관제 회의방(8023, ~/projects/meeting-room) + 봇 대시보드(8025, ~/projects/bot-dashboard)
> 결론 한 줄: **우리는 이미 Slack이 2026년에 역으로 따라 만든 "에이전트 네이티브 방" 구조를 갖고 있다.
> 부족한 것은 UX 정보구조(채널·스레드·검색·리액션)다. 자체 발전(A안) 추천.**

## 1. Slack 2026 해부 (조사 결과)

- 기본 축: 채널 / 스레드 / DM / Huddles(음성·화면공유) / Canvas(채널 안 협업 문서) / Clips(비동기 영상) /
  워크플로 자동화. 전부 검색 가능.
- Slack AI: 채널·스레드 요약, 하루 리캡, 회의 노트 자동화 — "AI work platform"으로 재포지셔닝.
- **Slack Code(2026 신설, 핵심 사례)** — 에이전트를 채팅 한 줄(thread)에 넣는 건 좁고, 사적 탭은 팀에서
  분리된다는 진단에서 출발:
  - 실제 작업을 @에이전트에 걸면 **작업 전용 채널(code channel)이 자동 생성** — 팀 전원이 볼 수 있음
  - 코드 diff·라이브 미리보기가 채널에 **카드로** 표시(텍스트 벽이 아니라)
  - 고위험 변경은 **채널 안에서 사람 승인 라우팅**
  - 완료되면 채널 **자동 아카이브**, 검색 가능한 감사 로그로 남음
  - Slack 내부 실측: 코드 채널 70%가 하루 안에 생성→종료(아이디어→머지)
  - Agents & Tools 탭: 에이전트 대화 관리 홈베이스, "에이전트가 아직 일하는 중" 가시화
  - 파트너: Anthropic(Claude Tag)·Cognition(Devin)·GitHub Copilot·Vercel·OpenAI
- 시장 신호: Gartner — 2026년 말까지 엔터프라이즈 앱 40%가 태스크 전용 AI 에이전트 포함(2025년 5% 미만).

## 2. 자체호스팅 3강 비교 (도입 시 참고)

- **Mattermost**: 엔터프라이즈 표준. **Playbooks** = 채널 안 체크리스트(run) 일급 워크플로 — 우리 지라칸반과
  통합 가능한 패턴.
- **Zulip**: **토픽 필수 모델** — 모든 메시지가 라벨 붙은 스레드에 속함. 비동기·회수·검색 최강. "이메일+채트".
- **Rocket.Chat**: 라이브챗·옴니채널 강점, 스레드 가시성 좋음.
- 공통: 자체호스팅 시 데이터 주권 확보. 단, 우리의 커스텀 오케스트레이션(claude -p dispatch, 24건 문맥 주입,
  토큰 0 설계, roster 원장, 활성 공지)을 그들 API/웹훅에 전부 이식해야 함 = 사실상 재구현.

## 3. 우리 관제 현재 vs Slack 갭

이미 갖춘 것 (에이전트 네이티브 코어 — Slack이 따라옴):
- @멘션 → 봇 엔진(claude -p / zcode) 구동·회신 (17기, 원격 폴러 포함)
- 방 로그 문맥 주입(봇끼리 서로 발언 가시), inflight "생각 중" 표시
- 활성 공지 게시판(내리기 전까지 전 봇 주입, 09-04), roster 단일 원장, 요구사항 이중 기록,
  대시보드(8025) 봇카드·지라·토큰·모델·공지 패널, 급정지 킬스위치, systemd 상시성

없는 것 (Slack류 UX 갭):
- 채널 없음 — 전 봇+이사님이 한 평면에 눌려 담김
- 스레드 없음 — 작업 대화가 봇 회신 텍스트 벽 하나로 끝남
- 검색 없음, 리액션 없음, 메시지 수정/삭제 없음, 읽음/미읽음 위치 없음
- 작업 수명주기 없음 — 일이 열리고 닫히고 아카이브되는 개념이 방에 없음(지라는 대시보드에 따로)
- 봇 산출이 카드가 아님 — diff·URL·미리보기 카드 없음(링크는 텍스트로만)
- 승인이 방 밖(대시보드 게시판)에 있음 — 채널 안 승인 카드 없음
- 봇 상태가 "생각 중"뿐 — 온라인/자리비움/작업중 구분 없음, 알림 라우팅 없음

## 4. 방향 3안

**A안 — 자체 디벨롭 (추천)**: 현 구조(에이전트 코어) 유지 + Slack이 증명한 UX 패턴만 흡수.
- 이유 1: 우리 차별점은 이미 에이전트 네이티브라는 것. Slack Code는 우리 모델의 정식 버전 — 같은 결론.
- 이유 2: 토큰 0·기동 0 설계(24건 주입, ACK 폐지, 활성 공지)는 외부 제품에 이식 불가한 자산.
- 이유 3: 조직 로드맵(CLI화→MCP화→agentic)과 직결 — 작업 채널이 agentic의 화면이 됨.

**B안 — 오픈소스 도입(Mattermost/Zulip) + 브리지**: 검증된 UX를 얻지만 커스텀 오케스트레이션 전면 이식,
DB·운영 무게 증가. Zulip 토픽 모델은 우리 작업 단위와 잘 맞으나 "갈아타기" 비용이 이득을 초과.

**C안 — 하이브리드(자체 방 + Mattermost 미러)**: 사람용/봇용 이중 채널 — 복잡도만 상승. 비추천.

## 5. A안 단계별 로드맵 (제안)

- **Phase 1 — 정보구조(채널·스레드)**: 메시지 스키마 v2(channel, thread_id, parent_id) — room.jsonl
  하위호환 마이그레이션. 기본 채널 #일반·#rpg·#autotrader·#scenario·#relay·#ops. @봇 작업 지시 시
  **작업 스레드 자동 생성**(Zulip 토픽 필수 발상 흡수: 모든 작업 대화는 라벨을 가진다). history_text()도
  채널별 주입으로 재설계(토큰 영향 검증 필수).
- **Phase 2 — Slack 필수 UX**: 리액션(=봇 접수 표시를 토큰 0·기동 0으로 해결 — ACK 폐지의 후속 완성),
  검색(SQLite FTS5, room.jsonl 인덱싱), 읽음 위치(이사님 마지막 읽은 곳부터), 관리자 수정/삭제,
  공지는 채널 고정(핀)으로 통합.
- **Phase 3 — 작업 채널(Slack Code 모델)**: @봇 실작업 → 작업 채널 생성, 봇이 중간 진척을 이벤트로 포스팅
  (지금은 최종 회신 한 덩어리), diff·URL·미리보기 카드, **승인 카드 → 이사님 클릭 승인**(MCP화의 도구 인터페이스),
  완료 시 자동 아카이브 + 감사 로그화. Mattermost Playbooks식 체크리스트를 작업 채널에 부착(지라 연동).
- **Phase 4 — 통합·알림**: 대시보드(8025)와 합체해 하나의 관제 워크스페이스로, 에이전트 탭(봇 상태·대화 관리),
  슬래시 커맨드(/보고 /배정), Telegram 브리지(공지·긴급만 — 기존 설계 승인 대기안 연결).

각 Phase는 독립 배포 가능. 1→2→3→4 순서 권장. Phase 1~2는 매니저+zcode 규모, Phase 3는 설계 검수(감사) 거쳐
zcode 구현 배정.

## 6. 리스크

- 스키마 v2 전환 시 room.jsonl 하위호환 깨짐 → 읽기 레이어에서 구버전 메시지 자동 승격 필요.
- 채널별 문맥 주입은 봇이 "다른 채널 소식"을 못 볼 수 있음 → 요약 크로스포스트(채널 간 요약만 공유) 설계.
- 리모트 폴러 봇(N100·gmwin·gmlnx)도 채널/스레드 스키마를 따라야 함 → /api/bot/send에 필드 추가, 구버전 폴러
  호환 유지.
- 대공사 방지: Phase 단위 커밋·실측, 이사님 승인 게이트 유지(자산 사용·창작 컨펌 원칙과 동일).

## 7. 통찰 (매니저 소견)

1. Slack의 2026 결론 = "에이전트에게 한 줄 스레드는 좁고, 사적 탭은 외롭다. **일마다 방을 주어라**" —
   우리는 3개월 전부터 봇마다 워크스페이스와 방을 줘왔다. 따라갈 일이 아니라, 같은 결론에 먼저 서 있고
   UX만 보완하면 된다.
2. 우리가 ACK 폐지로 버린 "접수 확인"을 Slack은 **리액션**으로 푼다 — 이모지는 토큰 0·기동 0.
   Phase 2 리액션은 ACK 문제의 우아한 완결이다.
3. Zulip의 교훈 "모든 대화는 라벨을 가진다"는 우리의 지라·티켓·RELAY 체계와 동형이다. 작업=스레드 필수화는
   검색·회수·감사를 동시에 해결한다.
4. 관제 방은 채팅 도구가 아니라 **조직의 OS**가 되어간다(공지·승인·작업·감사가 한 표면에).
   지금 갭은 기능이 아니라 정보구조다.

## 출처

- Slack 기능: https://slack.com/features · https://slack.com/features/channels · https://slack.com/features/canvas
- Slack Code: https://slack.com/blog/news/slack-code-channels-for-agents · https://slack.com/blog/developers/coding-agents-in-slack
- 에이전트: https://slack.com/ai-agents · https://claude.com/blog/claude-and-slack
- 오픈소스: https://docs.mattermost.com/end-user-guide/workflow-automation/work-with-playbooks.html ·
  https://zulip.com/why-zulip/ · https://zulip.com/help/introduction-to-topics ·
  https://xtom.com/blog/rocketchat-vs-mattermost/
- 커뮤니티: https://www.reddit.com/r/selfhosted/comments/7k471o/ · https://github.com/mpociot/claude-code-slack-bot
