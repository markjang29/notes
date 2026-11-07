---
title: 봇 간 통신망 실가동 점검 보고서 (command 3b9d4da5)
status: submitted
date: 2026-11-07
command_id: 3b9d4da5-e79e-40d9-a8ae-d11be6169e1d
author: aws-manager (heav_lnx_bot)
linked: 3a301711-bc42-49f3-93dc-99389f29658d (조직 리모델링, 진행 누락 해소 포함)
constraints: diagnostics_only — 서비스 중단·재시작·설정변경·배포 없음. probe 봇당 1건·동시 2·봇당 120초 준수.
---

# 봇 간 통신망 실가동 점검 (3b9d4da5)

## 1. 결과 한 줄

통신 본체(8024 comm·원장·NATS·브리지)는 정상이나, **각성 체인의 쿨다운 결함이 신규 지시를 삼켜**
이번 "GPT 지시 무응답" 사건을 만들었다. 폐기 ACK와 pending 정의 불일치로 인한 재ACK 무한루프도 실측됐다.

## 2. 사건 재구성 (이번 미응답의 인과 — 전부 실측)

1. 13:05:25 ChatGPT가 연결시험 ba939cc7 제출 → 13:05:27 배달. 릴레이(comm-relay-awslnx)가
   13:05:58 heav_lnx_bot 각성 예약 → 각성 실행(스케줄 이력 977819DD, 13:10:14 ok).
   각성 세션이 ba939cc7 처리 → 13:09:22 submitted 회신. 이 시점 봇은 **1시간 각성 쿨다운 진입**.
2. 13:09:16 두 번째 지시 3b9d4da5, 13:18:38 세 번째 3a301711 도착 — 릴레이 상태
   `last_note=cooldown`로 재각성 생략(원장·배달은 정상 기록). 두 메시지는 미수신 대기.
3. 13:23:35 이사님 지시로 aws-manager가 직접 수신(수동 소진)·ACK하고 본 점검을 수행.
   근거: 릴레이 상태 파일 waked_at=13:05:58/pend=1, 스케줄 이력 977819DD, 브리지
   awaiting_recipient_since 13:09:19/13:18:38.

## 3. 봇별·서버별 판정

**awslnx 사이트(duradev 서버, 릴레이 실측) — roster active 9봇**

1. heav_lnx_bot(매니저) — 활성. 각성체인 정상 작동 실증(사건 재구성 1). 다만 쿨다운 중 신규
   미수신 메시지에 재각성 안 됨 → 부분정상(결함 F1의 직접 피해자).
2. heav_lnx_codex_dev_1_bot — relay98 전담(NATS durable consume + inbox drain). 진단 probe
   (msg idem-799a8e39, 13:29:56)가 NATS 수령·대리 ACK까지 같은 초 완료(로그 실측).
   세션 각성·pong은 설계상 없음(98 수신안정화) → 정상(대리 ACK 설계).
3. heav_lnx_audit_bot — probe(msg idem-43283ee5, 13:29:56) → 릴레이 각성 발사 실측
   (상태 waked_at 13:32:22, last_note=ok). pong 회신은 probe 예산 120초 내 미도착 → 부분정상
   (각성됨·회신 지연; 세션 진행 여부는 후속 확인).
4. heav_lnx_scenario_bot — 각성 가능(쿨다운 경과, 11-03 각성 이력). 미소진 2건(11-03~) 보유.
   본 점검 probe 미실시(예산) → 미확인. 조직 리모델링 과제로 실측 예정.
5. heav_lnx_rpg_bot — 4와 동일(미소진 2건). 미확인. 과제 발송 예정.
6. heav_lnx_novel_col_bot — 미소진 8건(09-22~), 이전 각성 실패 기록(fails=1) → 실패 의심·미확인.
7. heav_lnx_asset_agent_bot — 미소진 6건(09-22~), fails=1 → 실패 의심·미확인.
8. heav_lnx_arcade_bot — 미소진 1건, 09-26 이후 무각성 → 미확인.
9. heav_gmwin_devpass_bot — 각성키 없음(릴레이 nokey) → 각성 불가(실패). 이름 접두사(gmwin)와
   소속(awslnx) 불일치 — 신원·사이트 매핑 정리 필요.

**gmlnx 사이트(같은 서버, comm-relay-common.py watch)**
10. heav_gmlnx_claude_bot — 감시 중. 미소진 1건 + 890~1115h 경과 노후 메시지들이 폐기 ACK 후에도
    pending에 남아 매분 재ACK 루프(46,060회, 로그 9.0MB) → 부분정상(F2 당사자).
11. heav_gmlnx_zcode_bot — roster wake=false + nokey → 의도적 비각성, 등록 정상.

**aws512 사이트(SSH 실측)**
12. heav_aws512_bot — rel레이 프로세스·유닛·상태파일 전부 없음 → 통신 자동각성 불가(부분정상,
    수동 운영 추정). roster active와 실제 감시 부재 불일치.

**firewin(4봇)·gmwin(4봇)** — 서버 접근 수단 없어 미실측 → 미확인. 필요시 해당 서버 점검 지시 필요.

**서비스 신원** — chatgpt_architect: 활성, 이번 왕복 3건(ba939cc7·3b9d4da5·3a301711) + 기존
a00e493a(11-06)로 원장·배달·이벤트 수집·상태 전이 정상 실증. 토큰은 값 확인 없이 설정 여부만 확인(준수).

## 4. 발견(영향순) — 실측/추론/미검증 구분

1. **F1 각성 쿨다운이 신규 지시를 차단(실측)** — 쿨다운(1h)이 '메시지 재각성 방지'가 아니라
   '봇 단위 전면 차단'으로 작동. 새 지시가 와도 1시간 동안 무시됨. 이번 사건의 직접 원인이고
   조직 리모델링 분담 발송에도 같은 영향.
2. **F2 pending 정의와 폐기 ACK 불일치(코드+로그 실증)** — ACK는 ackedAt만 설정(NatsLogController
   ack, deliveredAt 미변경)하는데 whoami pending은 deliveredAt IS NULL 기준 → 릴레이가 만료
   폐기 목적으로 ACK해도 목록에 영원히 남아 매분 재ACK. 46,060회 반복, 로그 9MB 낭비.
3. **F3 ba939cc7 result=null(실측)** — submitted 이벤트는 존재하나 회신 payload에 result 객체가
   없어 GET command result가 null. 브리지 결함 아님(회신 계약 미준수). 향후 회신엔 result 필수.
4. **F4 aws512 사이드카 부재(실측)** — 12번 참조. roster-active 봇의 감시 공백.
5. **F5 nokey·매핑 불일치(실측)** — gmwin_devpass(키 없음+사이트 의심), gmlnx_zcode(wake=false+nokey).
6. **F6 노후 미소진 백로그(실측)** — 6·7·8·10번 참조. 수신 세션 부재로 쌓인 메시지들.
7. **F7 릴레이 로그·상태 경로 겹침 의심(추론, 미확정)** — gmlnx 유닛의 watch 로그가
   comm-relay-awslnx.log에 섞여 기록. 유닛별 경로 분리 확인 필요.

## 5. 우선 수정 제안 3개 (실행은 별결 — 이번 범위 밖)

1. 쿨다운 정책 변경: 미소진 '새 msg_id' 도착 시 쿨다운 예외(스팸가드로 봇당 최소 간격 5분 정도
   이중 장치) — F1. 릴레이 수정 수 줄, 이번 사건 재발 방지의 핵심.
2. pending 정의 통일: whoami pending에서 ackedAt NOT NULL 행 제외(8024 코드 1줄) 또는 릴레이
   폐기를 inbox 소진 방식으로 전환 — F2. 즉시 로그 폭증 종결.
3. 회신 계약 result 필드: 각성 프롬프트 템플릿에 "submitted 회신 payload에 result 객체 필수"
   명시(브리지 reply_contract에는 이미 있음) — F3.

## 6. 미검증 항목 (지시 제약 준수)

1. 장애 주입(NATS·DB 중단, 서비스 재시작) — 금지 준수. 대신 기존 실측 증거 재사용:
   NATS 중단 d79059fa, 재시작 경쟁 0215e036, 재시작 5회·폐기 반영 AC-11(11-06 검증 보고서).
2. firewin·gmwin 서버의 릴레이·봇 실가동 — 접근 수단 없음.
3. pong 전이(각성→회신) 완결 — audit pong이 예산 내 미도착. 후속 확인으로 남김.
4. 토큰값 검증 — 값 확인 금지 준수, 파일 존재·키 존재 여부만 확인.

## 7. 증거 일람

1. 원장·메시지 ID: bridge-ba939cc7(13:05:27 배달→13:09:22 submitted), bridge-3b9d4da5(13:09:19),
   bridge-3a301711(13:18:38), probe idem-799a8e39(→98), idem-43283ee5(→audit),
   ACK idem-204fa83c·idem-c6e9e8ed, progress idem-d52c25b5.
2. 각성 이력: schedule_history/977819DD.log(13:10:14 ok). 릴레이 상태 파일 waked_at/pend/fails.
3. 로그: comm-relay-98.log(13:29:56 수령·ACK), comm-relay-awslnx.log(TTL 재ACK 46,060회).
4. 코드: NatsLogController.ack(ackedAt만 설정)·whoami(deliveredAt 기준 pending) — 정의 불일치.
5. 원장 총수 644건(13:23 whoami). NATS 로컬 프로세스 정상(nats-server, nats.conf).
