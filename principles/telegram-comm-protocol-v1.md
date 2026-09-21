---
title: 사칙 — 통신 표준 (NATS/comm 채널) — 봇간·공지·ACK
status: active
version: v1
date: 2026-09-21
authority: 이사님 09-21 직접 지시 ("최소한 nats를 보라고 하면서 매뉴얼을 각 .md파일이나 skill에 넣어야겠네")
owner: heav_lnx_codex_dev_1_bot (98 통신, 구축·운영) / 감사(95) 검증
tags:
  - comm
  - nats
  - ack
  - notice
  - 95
---

# 사칙 — 통신 표준 v1 (NATS/comm)

## 0. 한 줄 원칙

봇간 통신·공지·ACK은 **8024 comm 채널 하나로** — 각 봇은 부팅마다 자기 미수신함을 폴링하고,
수신하면 즉시 ACK을 발행한다.

ELI5: 우체국(NATS)은 하나. 봇들은 우체국 앞 자기 우편함(8024 API)만 확인하면 된다.
내용물이 무엇이든 꺼내면 "받았습니다" 도장(ACK)을 찍는다.

## 1. 주소 원장 (95-4-a 연동)

- 화면·원장: http://43.201.34.144:8024/comm
- API 기준: http://43.201.34.144:8024/api/nats/ (아래 §3)
- 이 주소는 95-4-b 규칙대로 URL 단독 한 줄로만 전달한다.

> **구현 현황 (09-21 12:30, 98): §3의 inbox·send·ack·whoami API — 1단계 가동 개시.**
> - 엔드포인트 4종 실측 검증 완료: 발신→수신(꺼내면 자동 done)→ACK→@all fanout 18건(활성 봇 수),
>   가명 발신 400, note 누락 400, 재ACK 멱등. 원장(/comm)에 봇간·notice·bot.ack 3종 모두 기록 확인.
> - 배포: matrix-studio-spring@4fe51a8 → releases/comm-4fe51a8 가동 (8024, 09-21 12:29).
> - 토큰: 공용 1개(`matrix.nats.comm-token`, 8024 서버의 EnvironmentFile) — 미설정 시 1단계는 검사 생략.
>   토큰값은 어디에도 기입 금지(§6) — 위치만.
> - §3의 `type` 7종·§2 토픽 3종·roster 실명 검증은 8024가 서버측 강제. ref 누락은 경고 응답(거부 아님).
> - 아직 미구현(2단계): /comm 화면의 공지 카드 ACK 진척률(확인 N/전체) 실시간 표시, JetStream 직구독
>   푸시(현재는 폴링), comm_client.py의 8023 폴러 완전 은퇴. 8023 신규 발행 금지(§6)는 전환 완료 후 적용.

## 2. 토픽(주소) 규칙 — 3종 고정

| 토픽 | 형식 | 용도 | 누가 듣나 |
|---|---|---|---|
| 봇간 | `bot.msg.<보낸이>.<받는이>` | 1:1 전달 | 8024 (원장) + 받는이 |
| 공지 | `notice.broadcast` | 이사님·매니저 전봇 공지 (fanout) | 8024 + 전 봇 |
| 확인 | `bot.ack.<봇이름>` | 수신 확인영수증 | 8024 (원장) |

- 보낸이·받는이는 **인사 원장(roster.json)의 username** (예: `heav_lnx_novel_col_bot`).
  가명·약칭 발신은 95-4-a 위반 — 원장과 대조 없이는 발신 금지.
- 새 토픽 추가는 본 사칙 개정으로만 (임의 확장 금지).

## 3. 사용법 — 봇 표준 클라이언트 (stdlib 0의존)

### 3-1. 미수신 폴링 (부팅마다 + 30~60초 주기)

```bash
curl -s "http://43.201.34.144:8024/api/nats/inbox?bot=<내_username>&token=<내_토큰값>"
```

- 응답: 미수신 메시지 배열 (꺼내면 자동 done). 빈 배열 `[]` = 새것 없음 (정상).
- **수신 즉시 §3-2 ACK 발행.** 7일간 미ACK인 메시지는 이력에 "미확인" 누적 — 감사(95)가 집계.

### 3-2. 송신 (봇→봇)

```bash
curl -s -X POST "http://43.201.34.144:8024/api/nats/send" \
  -H "Content-Type: application/json" \
  -d '{"from":"<내_username>","token":"<내_토큰값>","to":"<상대_username>","type":"task|notice|ack|progress|blocked|submitted|review","text":"본문","ref":"<근거:티켓ID·커밋·문서경로>"}'
```

- 헤더 7필드는 8024가 부여·검증 (id·ts·subject·from·to·text·payload). 봇은 from·to·type·text·ref만 채운다.
- `ref`(근거) 누락 시 8024가 경고 기록 — 거부는 아니지만 감사 집계 대상.

### 3-3. ACK (수신확인 — 관제 7필드 서명, gwanje-ack-protocol 준용)

```bash
curl -s -X POST "http://43.201.34.144:8024/api/nats/ack" \
  -H "Content-Type: application/json" \
  -d '{"from":"<내_username>","token":"<내_토큰값>","msg_id":"<받은메시지id>","note":"<한줄:무엇을 이해했는지·시작가능여부 acknowledged|blocked>"}'
```

- "봤음"·"오케이" 단독은 ACK 아님 (관제 ACK 사칙 v1 §2 준용).
- 공지(notice.broadcast) 수신 봇은 전부 ACK 의무 — /comm 공지 카드에 명단·진척률 실시간 표시.

### 3-4. 공지 발행 (매니저·이사님 — 전봇 fanout)

```bash
curl -s -X POST "http://43.201.34.144:8024/api/nats/send" \
  -H "Content-Type: application/json" \
  -d '{"from":"aws-manager","token":"<매니저토큰>","to":"@all","type":"notice","text":"공지본문","ref":"<정본커밋·티켓>"}'
```

- 발행 즉시 `notice.broadcast` 기록 + /comm 공지 카드 생성 + 각 봇 inbox에 1건씩 적재.
- 수령한 봇이 §3-3 ACK → /comm에서 "확인 봇 수 / 전체 봇 수" 진척 실시간.

## 4. 클라이언트 스크립트 (comm_client.py — hub_client.py 후계)

- 정본 위치: notes `projects/agent-ops/comm/comm_client.py` (원본 1개, 각 봇은 복사본·버전주석 필수)
- 동등 기능: `poll` (미수신→handler→자동ACK) · `send` · `ack` · `whoami`
- 사용 예:

```python
from comm_client import CommClient
c = CommClient("http://43.201.34.144:8024", "<내_username>", "<내_토큰값>")
c.poll_forever()          # 수신 → handler → 자동 ACK
c.send("<상대>", "task", {"prompt": "리밸런스 리포트"}, key="rpt-0921")
```

## 5. 부팅 체크리스트 (L0 부팅 절차에 추가 — 각 봇)

1. L0-agent-boot로 정체 확인 (기존)
2. **comm: `GET /api/nats/whoami` 1회 — 내 미수신건 확인·ACK** (신규)
3. 미수신에 공지가 있으면 정독 → 95-4-b 형식으로 답장 하단에 담당 주소 병기

## 6. 금지 (전 actor 공통)

- 8023 허브로의 신규 task·notice 발행 금지 (v1 전환 완료 후) — 기존 큐 소진까지만 예외
- 텔레그램 `;` 전체지시를 업무지시로 사용 금지 (중복실행·비용) — 공지는 comm 채널로
- 가명·약칭 발신, ref(근거) 누락, 미ACK 방치
- 토큰값을 채팅·커밋·본문에 기입 금지 — 위치(파일경로)만 기재

## 7. 장애 규칙 (95-1 연동 + 자동감지)

- comm 채널 장애(브로커 다운·8024 무응답·폴링 침묵 10분+)는 **8024가 자동 감지 → 이사님 텔레그램 통보**
- 봇이 통신 실패 시 95-1: 먼저 통신담당(98)에게 "무엇을 시도했고 어디서 막혔는지" 문의 — 이사님 직접 호출은 마지막 수단
- 8024가 죽어도 각 봇 본업은 지속(큐 비의존) — 재접속 후 미수신 자동 회수(JetStream 보존 7일)

## 8. ELI5

우체국(8024+NATS)이 하나 있고, 봇마다 자기 우편함이 있다. 봇은 부팅 때마다 우편함을 열어보고
(폴링), 편지가 오면 "받았다+무엇을 이해했다" 도장(ACK)을 찍는다. 공지는 우체국이 전 봇
우편함에 복사해 넣어주고, 화면(/comm)에서 누가 도장 찍었는지 실시간으로 보인다. 우체국이
불나면(장애) 우체국이 직접 아버지(이사님) 폰(텔레그램)으로 알린다.
