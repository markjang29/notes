# 시스템 개선 점검 v1 — NATS·01~04 봇 flow·게이팅·개발환경 (2026-09-30)

- 성격: **진단·제안 문서. 시스템 직접 변경 없음** (읽기 전용 실측만). 조치는 다음 달 저렴 토큰 봇이 티켓 단위로 수행.
- 실측 기준일: 2026-09-30 08:40~09:00 KST, duradev(홈서버). 증거 없는 항목은 "검증필요"로 표시.
- 타이가 등재 계획: 프로젝트 GOV/INFRA/PIPE에 태그 `arch-review-2026-09`, 상태 `접수`(자동발령·게이트 트리거 안 걸림). 등재 완료 여부는 각 티켓 존재로 확인.
- 민감정보 정책: 공인 IP·자격증명 파일 경로는 문서에 쓰지 않음(로컬 운영 문서 참조).

## 0. 저렴 토큰 봇 인수인계 (이 섹션만 읽어도 시작 가능)

**한 문장 지시**: "notes 저장소 `projects/agent-ops/proposals/2026-09-30-system-improvement-review.md` §3 우선순위 표를 위에서부터, 타이가 태그 `arch-review-2026-09` 티켓 1개씩 집어 §4의 '조치·검증'대로 수행하고, P0는 이사님 승인 후에만 운영에 반영한다."

운영 규칙:
1. 한 번에 티켓 1개. 조치 전 해당 티켓의 "검증 명령"으로 현상 재현 → 수정 → 같은 명령으로 해소 확인.
2. **P0 중 NATS 인증·바인딩(N1/N2)과 게이트 로직(G1~G3)은 이사님 승인 게이트** — 코드는 브랜치에 준비하고 배포 전 타이가 `의사결정대기`로 올린다.
3. 타이가 상태는 `접수 → 설계 → 구현`만 사용. 실수로 `구현`+`담당봇(@...)`을 넣으면 dispatcher가 회의방에 자동 발령하니 **담당봇 칸은 마지막에 채운다**.
4. 기밀(토큰·비밀번호)은 문서·커밋·티켓에 값을 쓰지 않고 경로만 적는다.
5. 끝나면 티켓 설명란 꼬리에 `근거 commit`과 검증 출력 1줄, 이 문서 §3 표의 상태칸 갱신.

## 1. 한눈에 (TL;DR)

- **가장 위험**: ① NATS가 `0.0.0.0` 무인증 ② 8024 REST가 토큰 없이 타 봇 사서함 조회 가능 ③ 게이트 로직 3건(두 번째 게이트 카드 미생성·테스터 반려 무시·보드 파일 경합).
- **01~04 봇 flow**: 각성(wake) 경로가 사실상 죽어 있고(스킵 5,217회 vs 성공 149회), 원격 사이트(firewin·gmwin) 봇은 감시 대상에서 빠져 있으며, 01→04를 잇는 **단일 flow 정본이 없다** (조각 문서 3개가 서로 다른 번호 체계 사용).
- **개발환경**: cron 우선순위 버그로 5분마다 에러 기록(6,516줄), notes 사본 2개 중 하나가 8일 stale, 미원격 저장소 3개.

## 2. 실측 증거 요약

| 항목 | 실측 | 출처 |
|---|---|---|
| NATS 바인딩 | `listen: 0.0.0.0:4222`, `http: 0.0.0.0:8222`, auth/tls 설정 없음. 설정 주석은 "로컬 전용: 외부 노출 없음" | `~/.config/nats/nats.conf` |
| NATS 실접속 | 현재 2개 모두 127.0.0.1 (relay98-sidecar, studio-8024-msglog) → 로컬 바인딩해도 기능 영향 없음 | `:8222/connz` |
| 8024 인증 | `inbox?bot=...` 토큰 없이 HTTP 200. whoami도 동일 | curl 실측 |
| 토큰 노출 | 회의방 8023 호출이 `?token=` 쿼리스트링 → `meeting-room/server.log`에 16건 | grep |
| JetStream | 스트림 BOTLOG(7일, 328건), consumer 8개 중 relay98 3개만 실사용. 테스트 잔재 `tc02-durable`·`tc04verify`, `gmlnx-scan-tmp`(filter `>`, pending 77), `gmlnx-claude-*` 2개. 전부 `max_deliver:-1`, inactive_threshold 없음 | `:8222/jsz` |
| 01~04 사서함 | novel_col·firebat_zcode·firebat_claude·asset_agent·gmwin_zcode·arcade 전원 pending 1 (동일 공지 id `…-645`) 미ACK | 8024 whoami |
| 각성 로그 | `comm-relay-awslnx.log` 11,671줄 중 "cron 큐 적체" 스킵 5,217, 성공 149. 리터럴 `\n` 포함 줄 828 | 로그 집계 |
| 각성키 없음 | `heav_gmlnx_zcode_bot`·`heav_gmwin_devpass_bot` 매 60초 "키 파일 미발견" 반복 | 로그 |
| 타이가 상태 | `구현`과 `설계승인대기`의 order가 둘 다 5 | `/userstory-statuses` |
| 게이트증거 필드 | 85건 중 **0건** 기입 | custom-attributes |
| 담당봇 누락 | 3:148(RELAY-66) `구현`인데 담당봇 공란 → 발령 영구 보류, 알림 없음 | 타이가 조회 |
| 승인보드 | pending 3건 중 4:85·4:86은 09-20부터 10일 대기 | decisions.json |
| cron | `pgrep … \|\| cd X && nohup .venv/bin/python …` — `~/server.log`에 동일 에러 6,516줄 | crontab, server.log |
| 포트 8026 | 문서상 주(主)=Spring hub-spring, 실제 점유=Python(pid 804728, `nai-queue-8026.service`와 일치 추정). `Xmx384m` java 프로세스 0개, cron은 5분마다 기동 시도 | ss, ps |
| notes 사본 | `~/notes` 29810f7(09-30) vs `~/.cokacdir/workspace/8jkpubeh/notes` 6fadadd(09-22) | git log |
| 미원격 저장소 | `env-sync`(dirty 23)·`tg-workspace`(dirty 6) 원격 없음, `meeting-room` dirty 7 | git status |
| 디스크 | 76%(54G 여유). `.cokacdir` 11G, `migration-8gb` 2.4G | df/du |

## 3. 우선순위 표 (위에서부터 처리)

| ID | P | 영역 | 한 줄 | 승인 | 상태 |
|---|---|---|---|---|---|
| N1 | P0 | NATS | 4222/8222 로컬 바인딩 + 인증 | 이사님 | 미착수 |
| N2 | P0 | 8024 | REST 봇 토큰 강제 + 쿼리스트링 토큰 제거 | 이사님 | 미착수 |
| G1 | P0 | 게이트 | 카드 중복억제를 (ref,gate)로 — 두 번째 게이트 카드 미생성 | 이사님 | 미착수 |
| G2 | P0 | 게이트 | 테스터 반려/대기를 실제 차단으로 | 이사님 | 미착수 |
| G3 | P0 | 게이트 | decisions.json 무잠금 덮어쓰기 제거 | 이사님 | 미착수 |
| G4 | P1 | 게이트 | 설계승인 후 재발령·에스컬레이션·status order | 매니저 | 미착수 |
| G5 | P1 | 게이트 | 자동발령이 "이사님" 명의로 송신되는 문제 | 이사님 | 미착수 |
| N3 | P1 | flow | 각성 경로 복구 + 원격 사이트 커버리지 | 매니저 | 미착수 |
| F1 | P1 | flow | 01~04 flow 정본 + 번호체계 정리 | 매니저 | 미착수 |
| N5 | P1 | 전송 | 8023/8026/8024 3중 전송계 정리 | 이사님 | 미착수 |
| D1 | P1 | 개발환경 | cron 우선순위 버그·이중 감독자 | 자율 | 미착수 |
| D2 | P1 | 개발환경 | notes 사본 stale·미원격 저장소 | 자율 | 미착수 |
| N6 | P2 | NATS | JetStream consumer 위생·max_deliver | 자율 | 미착수 |
| G6 | P2 | 게이트 | 브리지 공통화·웹훅·agenda hash·하드코딩 | 자율 | 미착수 |
| D3 | P2 | 개발환경 | 비밀 위생·디스크 정리 후보 | 자율 | 미착수 |

## 4. 항목별 상세 (문제 → 증거 → 조치 → 검증)

### N1 (P0) NATS 무인증·전 인터페이스 바인딩
- **문제**: 4222(클라이언트)와 8222(모니터링)가 `0.0.0.0`, 인증 없음. 같은 망(LAN·tailscale) 누구나 `bot.msg.*`를 발행해 봇을 사칭하거나 전체 메시지를 구독 가능. 설정 주석("외부 노출 없음")과 실제가 모순.
- **조치**: 1순위 `listen: 127.0.0.1:4222`, `http: 127.0.0.1:8222` (현 접속이 전부 로컬이라 무영향). 원격 노드가 직접 NATS를 써야 하면 대신 `authorization`(계정/토큰) + tailscale IP만 바인딩. 변경 전 `connz`로 원격 접속 없음 재확인, `systemctl --user restart nats` 후 relay98·8024 재접속 확인.
- **검증**: `ss -ltn | grep -E '4222|8222'`가 127.0.0.1만 표시 / relay98 로그 "JetStream durable 구독 완료" / 8024 whoami 정상.
- **롤백**: 설정 파일 원복 후 재시작 (JetStream 저장소 영향 없음).

### N2 (P0) 8024 REST 인증 미강제·토큰 쿼리스트링
- **문제**: `GET /api/nats/inbox?bot=X`가 토큰 없이 200. 타 봇 사서함·원장 조회 가능. 8023 `api/send?token=`류는 토큰이 URL에 실려 서버 로그(16건)에 남음. (send/ack 인증은 **검증필요** — 운영 메시지 오발송 방지로 미시험)
- **조치**: 봇별 토큰을 `Authorization: Bearer` 헤더로 받고 bot 식별자와 토큰 소유자 불일치면 403. comm_client.py·relay 스크립트 헤더 방식 전환(정본은 notes, 사본 버전주석). 로그 필터에서 `token=` 마스킹. 이미 로그에 남은 토큰은 회전.
- **검증**: 토큰 없는 inbox → 401, 타 봇 토큰 → 403, 정상 토큰 → 200 / `grep -c 'token=' server.log` 신규 증가 0.

### G1 (P0) 두 번째 게이트 카드가 영영 안 생김
- **문제**: `bridge.py ensure_card()`가 `taiga_ref`만 같으면 카드 생성을 건너뜀. 같은 스토리가 `설계승인`을 통과한 뒤 `이사님승인`(배포승인)에 오면 기존 카드가 있어 **새 카드가 안 생기고**, 판정 불가 상태로 정체. 4:82(RELAY-24)·4:89(RELAY-30)이 설계 카드 승인 후 `구현` 상태 → 이 경로 해당. 반려 후 재상신도 동일하게 막힘.
- **조치**: 중복 키를 `(taiga_ref, gate, 진입회차)`로. 스토리가 게이트 상태에 다시 진입하면(상태 이력 기준) 새 카드. `state.processed` 키도 동일 규칙.
- **검증**: 테스트 스토리를 설계승인 → 승인 → 이사님승인으로 이동시켜 카드 2개 생성 확인(테스트 프로젝트/태그로, 운영 스토리 금지).

### G2 (P0) 테스터 게이트가 판정을 무시함
- **문제**: `tester.py`는 verdict가 `반려`·`대기`여도 무조건 `이사님승인`으로 전이. 합격 기준은 "3개 경로 중 2개가 HTTP <500" — 404/401/403도 통과. 포트 필드 없으면 "수동 검증 필요"라고만 쓰고 그대로 전진. 대상은 127.0.0.1 포트뿐이라 원격 사이트 불가. 문서상 테스터(97 `heav_gmwin_codex_bot`)는 역할 미부여.
- **조치**: `반려`→`구현`으로 되돌리고 사유를 설명란에 기록, `대기`→`테스트봇검증` 유지 + 97봇에 8024 task로 인계. 합격은 2xx/3xx만. `게이트증거`(리포트 링크) 기입을 전이 조건으로. 카드에는 판정이 "통과"일 때만 승인 버튼 활성.
- **검증**: 포트 미응답 스토리 → 구현 복귀 / 404만 반환하는 더미 포트 → 반려.

### G3 (P0) 승인보드 파일 경합
- **문제**: 승인보드 앱(`request_store.locked_json/transact_json`)은 파일 잠금을 쓰지만, `bridge.py`·`tester.py`는 잠금 없이 `decisions.json`을 읽고 tmp→replace로 덮어씀. bridge는 루프 초반에 읽은 사본을 **수십 번의 HTTP 호출 뒤** 저장 → 그 사이 이사님이 누른 판정이 소실될 수 있음.
- **조치**: 브리지/테스터가 `request_store.transact_json`을 임포트하거나 승인보드 API를 호출. 근본은 카드 저장소를 한 곳(승인보드)만 쓰기 주체로.
- **검증**: 동시 쓰기 스트레스(브리지 루프 중 판정 POST 100회) 후 판정 유실 0.

### G4 (P1) 설계승인 후 발령 공백·정체·status 순서
- **문제**: dispatcher는 `구현` 진입 시 1회만 발령("설계 먼저 → 설계승인대기로 이동"). 설계 승인으로 `구현`에 다시 오면 state 때문에 **재발령 없음** → 담당 봇이 타이가를 직접 보고 있어야 함(4:82·4:89, 09-21 승인 후 발령 0). 4:85·4:86은 10일째 승인 대기인데 에스컬레이션은 매일 09시 방송뿐. 또한 `구현`과 `설계승인대기`가 같은 order 5라 칸반 순서 모호, `구현` 상태가 설계 작업도 포함하는 의미 중복.
- **조치**: 상태를 `설계`(설계 발령) / `설계승인대기` / `구현`(구현 발령)으로 분리하고 dispatch 키를 (ref, phase). 승인 판정 시 담당봇에 "승인됨" 발령. 대기 N일 초과 시 매니저 에스컬레이션. `설계승인대기` order를 6 이후로 재배열(전체 order 재부여, 프로젝트 4개 모두).
- **검증**: 설계승인 판정 직후 회의방/8024에 구현 발령 1회 / 중복 발령 0.

### G5 (P1) 자동 발령이 "이사님" 명의로 나감
- **문제**: `dispatcher.py`가 회의방에 `sender:"이사님"`으로 송신(agenda는 "매니저"). 대화규칙상 이사님 발언=요구사항이라 자동 메시지가 **승인자 지시로 보임**. 또한 8023은 4단계 폐지 예정 채널이고 8024 원장(증적)에 안 남음 — "모든 계약은 원장" 원칙 위반.
- **조치**: 송신 주체를 서비스 신원(`taiga-bridge`)으로 하고 8024 `/api/nats/send`(type:task, ref=타이가 US)로. payload에 task-contract 7필드(또는 링크) 포함. 이사님 명의 금지.
- **검증**: 원장(`totalLedger`)에 발령 기록, 회의방 메시지 sender가 서비스 신원.

### N3 (P1) 01~04 봇 각성 경로 사실상 불능 + 커버리지 구멍
- **문제**: (a) 각성은 `cokacdir --cron … --at 1m`을 쓰는데 같은 cron 큐가 적체(4건 이상)면 스킵 — 스킵 5,217회. (b) 같은 공지 1건이 01~04 6봇 전원에 미ACK로 남아 스킵/재시도 루프. (c) 사이드카가 `site=awslnx`·`gmlnx`만 감시 → **firewin(01 zcode·02)·gmwin(04 zcode·97·99)은 감시·각성 대상 밖**. (d) 각성키 없는 봇이 60초마다 로그 스팸. (e) 로그 기록 시 `"\\n"`을 써서 리터럴 `\n`이 들어가 줄이 붙음(828줄).
- **조치**: 각성 큐를 본업 cron과 분리(전용 계정/큐) 또는 큐 여유 시 재시도 + 지수 백오프, 스킵 로그는 상태 변화 시 1회만. 키 없는 봇은 roster에 `wake:false`로 표기하고 1회만 알림. 원격 사이트는 그 사이트용 사이드카 배포(INSTALL-sidecar.md) 또는 봇 자체 폴링 주기를 roster에 명시. 로그 `"\n"` 수정. 공지는 봇별 ACK 기한·만료(TTL)로 닫기.
- **검증**: 6봇 pending 0 수렴 / 스킵 로그 일 50줄 미만 / 성공률 지표 로그에 표시.

### F1 (P1) 01~04 flow 정본 부재 + 번호 체계 충돌
- **문제**: roster `seq`가 중복(00×2, 01×2, 04×2)이고 role 라벨의 사이트 표기가 실제 site와 불일치(01 novel_col "[GM윈도]"→site awslnx, 03 "[GM윈도WSL]"→awslnx, 04 arcade "[AWS 8G]"). `hub-payload-schema-v1.md`의 표준 flow는 "01개발봇→03봇"이라 쓰지만 현 roster의 01은 소설수집/Aka자산, 개발봇은 98 dev_1. `handoff-contract-01-04.md`의 "01-04"는 봇이 아니라 **4필드 번호**(이름 충돌). 그림 flow(`arch/picture-flow-messages-v1.md` M1~M7)는 계획 문서(미시행), 자산 파이프라인 8단계(`asset-pipeline-graph-design-v1.md`)는 초안.
- **조치**: `projects/agent-ops/flow-01-04-v1.md` 신설 — 표 한 장: 단계 → 담당 봇(roster username) → 입력/출력 토픽 → 게이트(자동/인가/검수) → 증거(commit·sha256) → 실패 시 경로. roster에서 `seq` 유일성 검증 스크립트 추가(중복이면 `lane` 필드로 분리). hub-payload-schema의 "01/03" 표기를 username으로 교체. 이름 충돌 방지: handoff 4필드 문서 제목에 "(필드 01-04, 봇 번호 아님)" 명기.
- **검증**: flow 표의 모든 봇이 roster에 존재·active, 모든 토픽이 messaging-architecture §토픽 목록에 존재.

### N5 (P1) 전송계 3중 + 문서상 주(主) hub 미가동
- **문제**: 8023 회의방 REST(폐지 예정), 8026 hub(Spring, 문서상 주), 8024 NATS comm이 공존. 타이가 브리지는 8023, 원장은 8024. 8026 포트는 Python이 점유(추정 nai-queue), Spring hub 프로세스 없음인데 cron이 5분마다 재기동 시도 → `hub-payload-schema-v1.md`의 failover 기술이 현실과 다름. (8026 점유 주체는 **검증필요**: `ss -ltnp`·`systemctl --user status nai-queue-8026`)
- **조치**: 이사님 결정 안건으로 상신 — 8024 단일화 일정(4단계) 확정, hub-spring은 폐기 또는 포트 재배정. 결정 후 문서 갱신·죽은 cron 제거.

### D1 (P1) cron 연산자 우선순위 버그 + 이중 감독자
- **문제**: `pgrep -f "uvicorn server:app" >/dev/null || cd $HOME/meeting-room && nohup .venv/bin/python …`은 `(pgrep || cd) && nohup`로 해석됨. 8023이 살아 있으면 cd를 건너뛰고도 `nohup`은 실행 → `$HOME`에 `.venv`가 없어 5분마다 실패, `~/server.log` 6,516줄. 동시에 `meetingroom-8023.service`(systemd)도 있어 감독자가 둘.
- **조치**: cron 두 줄(5분 감시·@reboot) 삭제하고 systemd 단일 감독(`Restart=always`). hub-spring cron 두 줄도 N5 결정 후 정리. `~/server.log` 로그로테이트 또는 삭제.
- **검증**: `tail ~/server.log` 증가 없음 / `systemctl --user is-active meetingroom-8023`.

### D2 (P1) notes 사본 stale·미원격 저장소
- **문제**: 봇 워크스페이스 사본(`~/.cokacdir/workspace/8jkpubeh/notes`)이 8일 stale → 그 사본을 읽는 봇은 구 정책으로 동작. `comm/__pycache__`가 untracked(하위 relay/__pycache__만 ignore). `env-sync`·`tg-workspace`는 원격 없음 + 미커밋 변경.
- **조치**: 사본은 pull-on-boot(부팅 루틴에 `git pull --ff-only`) 또는 심볼릭 링크로 단일화. `.gitignore`에 `__pycache__/` 전역 추가. 미원격 2곳은 private 원격 생성 후 커밋·푸시(이사님 계정 필요 → 상신).

### N6 (P2) JetStream consumer 위생
- **문제**: 테스트 잔재 consumer 4개, `gmlnx-scan-tmp`(filter `>`, pending 77)는 영구 보존. 모두 `max_deliver:-1`이라 독성 메시지가 30초마다 무한 재전달. 본 설계서 "미수신 7일 회수" 보장은 durable consumer가 있는 98봇에만 실제 적용(나머지는 REST inbox). 8024 원장은 core 구독(`studio-8024-msglog`)이라 8024 다운 구간 메시지의 원장 반영 여부 **검증필요**(재기동 시 스트림 재생 여부).
- **조치**: 잔재 consumer 삭제(삭제 전 이사님 공지 불필요한 것만: tc02·tc04·scan-tmp), 운영 consumer에 `max_deliver:5` + `inactive_threshold`. 8024 원장 재생 여부 테스트(8024 재시작 중 메시지 1건 발행 → 원장 확인).

### G6 (P2) 브리지 군집 정리
- `taiga()` 클라이언트가 bridge·dispatcher·agenda·tester 4곳에 복붙, 401 재인증 시 자격증명 파일을 4 프로세스가 동시에 씀. → 공용 모듈 + 파일 잠금.
- 타이가 주소가 공인 IP(엣지 주소)로 하드코딩 — 로컬 `127.0.0.1:8040`이 동작하므로 엣지 장애 시 게이트 전체가 멈춤. → 로컬 우선.
- 프로젝트 ID `{3,4,5,6}`·상태명이 4곳 하드코딩. 폴링(20/30초/10분) 대신 타이가 웹훅 검토.
- `agenda.py` 지문이 Python `hash()`(프로세스별 솔트) → 재시작 때마다 "변경"으로 오인해 중복 방송. → `hashlib.sha1`.
- `보류(deferred)` 판정은 상태 전이도 없고 agenda가 `pending`만 세서 **영구 침묵** → 보류 N일 후 재상신.
- `배포` 상태 전이는 라벨 변경뿐 실제 배포·증거와 연결 없음 → `게이트증거`에 배포 commit/헬스체크 기록을 요구.

### D3 (P2) 비밀 위생·디스크
- 타이가 브리지 자격증명이 평문 파일(권한 600), 회의방 ACCESS_TOKEN URL 전달, git 자격증명 평문 store, 퇴역한 Jira 토큰 파일 잔존(경로는 로컬에서 `find ~ -maxdepth 3 -name '*token*' -o -name 'creds*'`로 확인). → 비밀 디렉터리 + systemd `EnvironmentFile`/`LoadCredential`, 퇴역 토큰 폐기.
- 디스크 76%: `~/.cokacdir` 11G, `migration-8gb` 2.4G, `AWS8gb_bkup`, 설치 파일(`teamviewer_amd64.deb` 115MB, `jre17.tar.gz`) → **삭제는 이사님 확인 후**, 우선 목록화만.

## 5. 이 점검의 한계

- 운영 메시지 오발송을 피하려고 8024 send/ack의 인증 여부는 시험하지 않음(N2 "검증필요").
- NATS 외부 도달성은 공인 IP(엣지)에서만 시험(도달 불가). 홈서버 LAN/tailscale 측 노출은 바인딩 주소와 무인증 설정으로 추론.
- 8026 점유 주체, 8024 원장 재생 여부는 추정. 각 티켓에 검증 명령을 넣어 두었음.
- 타이가 스토리 본문·상태 이력은 전수 열람하지 않음(상태별 건수·게이트 대상 스토리·커스텀필드만).

## 부록 A. 매니저(aws-manager) 보충 실측 — RELAY-68 (2026-09-30)

본문과 겹치지 않는 추가 발견만 기록. 기준: duradev 읽기 전용 실측, 시스템 변경 없음.

- **A1 (N3 보강) 사이드카 각성 계약 공백** — `comm-relay-common.py`의 `wake()`는 `cokacdir --cron … --once` 한 경로뿐이다. 실패 시 재시도·대체 경로·생존 신호가 없고 쿨다운 1시간이 고정이다. 계약 개정 제안: 개정1 각성 이중화(scheduler → `cokacdir --prompt` 직접 호출 → 텔레그램 경보), 개정2 소화 heartbeat, 개정3 만료 메시지 폐기, 개정4 메시지 type 허용목록(`reply`는 8024가 400으로 거부 — 답장 규약이 type과 어긋남).
- **A2 (N3 보강) zcode 폴러는 8023만 본다** — `room-poller-gmlnx-zcode.py`가 `ROOM=:8023` 멘션만 감시하고 8024를 읽지 않는다. gmlnx zcode 사서함 적체의 원인. 8024 사서함 폴링 추가 또는 사이드카 배포 필요.
- **A3 (N1/N2 보강) 공용 토큰 1개** — 8024는 room.token 하나로 어떤 봇의 사서함도 열린다. 봇별 토큰 분리(N2)와 함께 roster 기반 권한표가 필요하다. 이번 전수 테스트에서 매니저가 9개 봇 답장을 대리 송신할 수 있었던 것이 그 증거다(대리 답장 9건, 자기응답 9건).
- **A4 (D3 보강) 봇 기동 스크립트에 토큰 평문** — `run.sh`가 텔레그램 봇 토큰 7개를 명령행 인자로 넘긴다(프로세스 목록·로그에 노출 가능). `--ccserver-token-file` 방식으로 전환하고 기존 토큰 교체 검토. 값은 이 문서에 쓰지 않음.
- **A5 (D3 보강) `~/.cokacdir/debug` 11G** — 일자별 로그 25개, 기존 기록(2.0GB)보다 5배 이상 증가. 보존기간·로테이트 정책 없음. 삭제는 이사님 확인 후, 우선 압축·보존일 설정.
- **A6 (문서) 포트 대장 6개 누락** — `relay/port-registry.json` 등록 22개 대비 실가동 중 미등록 6개(8002 autotrader, 8030 nexus, 8040 taiga, 8100, 8222 NATS 모니터링, 8788 zai 프록시). `pending_registration`은 비어 있다. 등록 또는 폐기 판정 필요.
- **A7 (F1 보강) 파이프라인 순서 정정 반영** — 이사님 09-29 기준 순서는 01 수집 → 02 로드셋·리수 검증 → 03 matrix 자산화. 01A/01B 채굴은 전체 파이프라인 가동 확인 후 시작. 단계 사이 자동 인계가 없고, 02 환경은 Python 부재(설치 vs node 이식 미결). 8018은 AWS·duradev 이중 인스턴스 미해소. F1의 flow 정본에 이 순서와 미결 사항을 그대로 넣을 것.
- **A8 (G 보강) 승인 대기 현황** — 승인보드 대기 3건(5:146, 4:85, 4:86), 4:85·4:86은 09-20부터 대기. 08:40 기준 타이가 게이트 카드와 일치.

정정: 조사 초기에 "포트 대장 0건 등록"으로 읽었으나 `registered` 키를 읽지 못한 오독이었고, 위 A6 수치가 맞다.
