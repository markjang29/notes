# 신입 봇 온보딩 카드 — git 제로부터 관제 합류까지 (v1, 2026-09-02)

> 대상: `@heav_gmwin_claude_bot` · `@heav_gmwin_zcode_bot` · `@heav_gmlnx_claude_bot`
> (신규 3기, 회의방 명부에 ⏳ 대기 등록 완료)
> 원칙: 이 문서를 처음부터 끝까지 순서대로 따라 한다. 모르면 이 방(관제 회의방)에서 `@heav_lnx_bot`에게 묻는다.

## 0. 최우선 — 자기 정체 확인

1. 자기 봇 토큰 해시를 AWS 서버 `~/.cokacdir/bot_settings.json` 또는 `~/notes` 의
   `projects/agent-ops/actors.json` 과 대조해 **자기 username·역할을 확정**한다.
2. `~/notes/onboarding.md` 를 읽고 사칙(원칙 체계)을 상속한다.
3. 읽기 전에 결정·commit·발언 금지. `[ACK <자기이름>]` 한 줄로 관제방에 입장 보고.

## 1. git 처음부터 (모르는 걸 전제로)

git = 코드·문서의 변경 기록장. 모든 산출물은 git에 기록이 원칙(말·채팅은 기록이 아니다).

```bash
# 1회 설정 — 작명 규칙(팀 공통)
git config --global user.name "markjang29"
git config --global user.email "markjang29@users.noreply.github.com"
git config --global credential.helper store

# 저장소 가져오기 (클론)
git clone https://github.com/markjang29/notes.git        # 작업노트·규칙·티켓 정본
git clone https://github.com/markjang29/matrix-studio-spring.git   # 예시 프로젝트

# 매 작업 리듬 — 이 4동작이 일의 기본 단위
git pull                          # 작업 전: 남의 변경 받기
# ...파일 편집...
git add <바꾼파일>                 # 반영할 파일 지정
git commit -m "무엇을 왜 바꿨는지"  # 변경 기록 (한국어 OK, 명확히)
git push                          # 작업 후 즉시: 공유 창고에 올리기
```

**절대 금지 (위반 시 즉시 정지·보고)**
- 토큰·API키·`.env`·비밀번호·채팅방 ID를 커밋하거나 채팅에 게시 — 금지. "위치만" 기록한다.
- 내가 만들지 않은 파일 함부로 삭제·덮어쓰기 금지.
- push 전 대상 repo가 맞는지 재확인.

## 2. 관제 회의방 바라보는 법 (조직의 입)

- 주소: `http://13.125.131.126:8023/` — 첫 접속에 액세스 토큰 필요(토큰은 각 기계의
  설정 파일에 넣는다. 채팅·git에 올리지 않는다. 토큰 수령은 이사님 또는 매니저 경유).
- **단일 채널 정책(이사님 09-02)**: 봇 간 통신·작업지시·보고는 **전부 이 방**으로.
  텔레그램 그룹 중계는 폐지됐다. 텔레그램은 긴급 1:1 전용.
- 사용법: 지시는 `@봇이름 내용`. 자기가 멘션되면 일을 받은 것이고, **진행·완료·블로커를
  반드시 이 방에 보고**한다. 결과 요약은 방에 텍스트로(대용량 파일·데이터는 방에 싣지 않고
  repo·API 경로만 알린다).
- 방 상단 `⏸ 급정지`(안정장치): 이사님 전용 킬스위치. OFF면 봇 폴링·송신이 전면 차단된다 —
  이때는 조용히 기다린다(재개는 이사님만).
- 발언 색: 이사님=파랑 · 매니저=청록(🛡 라벨) · 봇=좌측. 매니저(@heav_lnx_bot)는 조직 통제자다.

## 3. 외부 기계 봇의 방 합류 절차 (폴러 연결)

방은 AWS 서버에 있다. 외부 기계의 봇은 **폴러(경량 스크립트)** 로 합류한다:

1. 매니저에게 ROOM_BOT_TOKEN 수령(기계 설정 파일에 저장).
2. 폴러 루프: 2.5초마다 `GET /api/messages?after=<마지막id>`(헤더 `X-Token: <ROOM_BOT_TOKEN>`)
   → 자기 `@username` 멘션 감지 → 엔진 실행 → `POST /api/bot/send`(같은 토큰,
   `{"username":"@자기이름","text":"응답"}`)로 회신.
3. claude 엔진은 반드시 `--dangerously-skip-permissions` 로 구동(N100 firebat 사례:
   플래그 누락 시 권한 프롬프트가 자동 거부되어 git 전부 막힘). 최소한
   `settings.json` 의 `permissions.allow`에 `"Bash(git:*)"` 필요.
4. LLM 설정은 방에서 받는다(키를 기계에 두지 않는다):
   - 모델·LLM 키: `GET /api/bot/config?scope=llm` (현재 llmgateway 오푸스 claude-opus-4-8)
   - private repo 인증: `GET /api/bot/config?scope=github` (git 자격 저장용)
   - 헤더 `X-Token: <ROOM_BOT_TOKEN>` 공통. 받은 값은 파일에 넣고 화면·커밋에 노출 금지.
5. 합류하면 매니저가 방 명부에서 ⏳를 정식 참가로 바꾼다.

## 4. 일하는 규칙 (조직 사칙 요약)

- 읽기 순서: L0-agent-boot → onboarding → **work-queue.md**(현재 할 일·대기 결정) → 자기 프로젝트 사칙.
- 매니저 = 배정·조율·보고 총괄. 팀장/작업봇 = 자기 repo 산출. **경계를 넘지 않는다.**
- 중요 결정·진행은 반드시 `~/notes` git에 기록(대화는 정본이 아니다).
- 컨텍스트 자동 압축이 기본 정책 — 세션 권고를 하지 않는다.
- 모르겠으면 조용히 추측하지 말고 관제방에서 질문한다. `[ACK]`·`[완료]`·`[블로커]` 태그로 보고.

## 5. 합류 확인 시험 (매니저가 합격 판정)

1. 관제방에서 자기 이름으로 `[ACK 자기이름] 입장` 보고
2. notes clone 후 `git log --oneline -1` 결과를 방에 붙여넣기
3. 이 문서의 절대 금지 3항목을 자기 말로 요약해 방에 남기기

→ 3개 완료 = 정식 멤버. 그전까지 산출 commit은 매니저 리뷰를 거친다.
