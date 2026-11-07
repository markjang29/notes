---
title: ChatGPT HTTP 관제 브리지 C0·C1 검증 보고서
status: verified-c0c1
date: 2026-11-06
spec: projects/agent-ops/proposals/2026-11-05-chatgpt-http-control-bridge-spec-v1.md
author: aws-manager (이사님 지시 11-05 "우선 C0·C1을 구현해")
---

# ChatGPT HTTP 관제 브리지 C0·C1 검증 보고서

## 1. 결과 한 줄

C0(연결·인증)·C1(작업 왕복) 구현 완료. 읽기 전용 status 작업 1건이
ChatGPT 자격 제출 → 매니저 각성·수신 → 결과 제출 → ChatGPT 결과 조회까지 실증되었다(AC-10).

## 2. 인계 항목 (명세 §9)

1. HTTPS base URL: `https://acting-carpet-ripe-level.trycloudflare.com/api/agent-bridge/v1`
   - quick tunnel 특성: 터널 재시작 시 하위도메인 변경됨. 변경 시 `agent-bridge-urlwatch` 크론(10분 주기)이
     이사님 채팅(heav_lnx_bot)으로 자동 통보. 인증키는 그대로 유효.
   - 터널은 8024 전체를 노출하지 않는다. 경로 필터 프록시(127.0.0.1:8126 → 8024)가
     `/api/agent-bridge/v1/*`만 통과시키고 나머지는 404 차단(실측).
2. 구현 커밋(전체 SHA): `markjang29/matrix-studio-spring` 브랜치 `bridge/chatgpt-c0c1`
   - 5911e9a5f1af517b8beaf7a1f45220a82b0f1188 최초 구현(컨트롤러·서비스·send 확장)
   - 29404d5… 발송 payload reply_contract 안내
   - 2d0be5f… 신원·토큰 캐시 폐기 즉시 반영(AC-11)
   - 515bf3c… 이벤트 수집기 command_id 추출 강화(payload.data·payload·텍스트 관례)
   - d7b8331bae17b616000a9cb1eabcf9f177459c21 상태조회 result 평탄화(최종)
3. 배포: releases/d7b8331bae17 → `current` 심볼릭 링크 → 유저 systemd 유닛
   `matrix-studio-spring-8024.service`. service version: agent-bridge v1.
   배포 원본은 기존 2e19147 릴리스 디렉토리에 그대로 보존(롤백 대상).
4. 등록 신원: `chatgpt_architect`(transport=http, wake=false, status=active,
   허용 수신자 heav_lnx_bot·heav_lnx_codex_dev_1_bot) — service-actors.json(notes d5d1ee6).
5. 자격증명 보관·전달(값은 본 보고서·Git·텔레그램 어디에도 없음):
   - 보관: `~/.config/matrix-studio-spring/service-actor-tokens.json`(0600, 소유자 전용)
   - ChatGPT 호출 환경 제공 방법: 서버 콘솔에서 위 파일을 직접 확인해 OpenAI 쪽 비밀 보관소
     (예: GPT Actions의 인증 설정·환경변수)에 등록. 텔레그램·Git·URL query·채팅 전송 금지.
   - 회전(rotate): 같은 파일의 값을 교체하면 최대 60초(캐시) 뒤 새 토큰만 승인.
   - 폐기(revoke): 파일에서 해당 항목을 삭제하면 최대 60초 뒤 401(실측: 65초 내 401).
6. 테스트 command_id: `a00e493a-f2a8-4aa0-9277-fc975af0db0c` (kind=status, 읽기 전용)
   - 이벤트 5개: blocked(초기 수신 세션 보류) → ack → progress → submitted → 늦은 progress(역행 방지 시험)
   - 부속 시나리오 작업: `d79059fa-1109-4ff9-9326-a4a3408e67e5`(NATS 중단),
     `0215e036-1789-4610-b3a0-a818c5e9a9a8`(접수 직후 재시작)
7. 읽기 전용 조회 예시:
   `GET /commands/{id}` — 상태·dispatch_msg_id·awaiting_recipient_since·result(Git 증거 포함)
   `GET /commands/{id}/events?after=0` — 순번 이벤트 전체. 둘 다 배달 상태 불변(AC-2 실측).

## 3. 수용 기준별 판정 (명세 §8)

1. pass — 무토큰 401·잘못된 토큰 401·타인/없는 작업 404 (실측).
2. pass — 상태 GET 5회 반복 후에도 미수신 1건 유지(whoami 비소진 확인).
3. pass — 동일 키 동시 POST 10건 전부 동일 command_id 수렴(1 신규+9 duplicate), 원장 발송 1건.
   응답 유실 가정 재시도도 동일 command_id 회수.
4. pass — 동일 키·다른 내용 409, 기존 작업 불변.
5. not-run(실측 불가) — 공용 운영 DB(PostgreSQL unified)를 강제로 죽일 수 없어 미실시.
   구조상 접수는 단일 INSERT 트랜잭션이므로 DB 실패 시 202가 나올 경로가 없음(Spring 기본 500).
   전용 스테이징 DB에서의 장애 주입은 C2에서 보강 예정.
6. pass — NATS 정지 상태에서 접수·원장 저장·배달장부 기록(brokered=false 정직 표기),
   NATS 복구 후 동작 지속. 접수 직후 서버 재시작에도 발송 정확히 1회(고정 msg_id+원장 dedup).
7. not-run — sidecar 수신 직후 종료·ACK 유실 시나리오. claim/lease 설계는 명세 §6이 C2로 지정.
   현행 보호: 매니저 command_id 중복 실행 방지 + sidecar 미수신 재각성. C2에서 lease 테이블로 보강.
8. pass — 매니저 부재 약 20분(02:42~03:02) 동안 dispatched 유지, `awaiting_recipient_since` 표기.
   실행 중으로 꾸미지 않음.
9. pass — submitted 후 늦은 progress 이벤트는 기록(seq 5)되나 상태 submitted 유지(역행 금지).
   submitted와 verified는 별도(verified 승격 경로는 미구현 — 아래 제한 참조).
10. pass — ChatGPT 자격으로 외부 HTTPS에서 제출·결과 조회 완료. result에 repository·branch·
    full commit 2개·테스트(7 passed)·실자료 데모 증거·미완료 4건 포함 확인.
11. pass — 서버 재시작 5회에도 작업·이벤트·권한 유지(PostgreSQL 영속). 폐기 65초 내 401, 복구 즉시 200.
12. pass — 토큰값 노출 전수 검사: 터널 로그·소스·응답 캡처·systemd 저널·git 히스토리(-S 검색)·notes 전부 0건.

## 4. 왕복 경로에서 발견·수정한 사항 (정직 기록)

1. 최초 각성 매니저 세션이 chatgpt_architect를 "미등록 발신자"로 보고 본작업을 blocked 처리했다.
   원인은 service-actors.json을 작성만 하고 notes에 커밋하지 않은 매니저(aws-manager) 실수.
   커밋(notes d5d1ee6) 후 매니저가 직접 실행해 submitted 완료. 이 경위는 result_note에도 기록.
2. 각성 세션의 회신이 텍스트 관례(command_id=…, [bridge-…])로 와서 수집기가 놓친 사실을 발견,
   수집기가 payload.data·payload·텍스트 관례를 모두 수용하도록 수정(515bf3c).

## 5. 남은 제한 (C2 범위)

1. verified 상태 승격 경로 미구현 — 별도 허가 검수 주체·절차가 명세에 없어 자동화하지 않았다.
   현재 최종 상태는 submitted이며, 검수 결과는 review 이벤트로 기록만 가능.
2. sidecar bridge 작업용 claim/lease(AC-7)·타임아웃·재시도 정책·제한된 implement 미실시.
3. quick tunnel URL 불안정 — 고정 도메인 필요 시 명명 터널+도메인 확보가 필요(이사님 결정 사항).
4. AC-5 DB 장애 주입 실측 — 전용 스테이징 DB 필요.
5. kind=implement는 접수만 가능(검증 안 함). C1 검증은 읽기 전용 status 1건이 전부.

## 6. 기존 comm 사용자 영향·롤백

1. 영향: 기존 4개 API(/api/nats/inbox·send·ack·whoami) 계약 불변. 원장 624건 보존(재시작 후 동일 수 확인).
   신규 테이블 4종(agent_bridge_*)은 별도 네임스페이스로 기존 테이블과 무관.
   /api/nats/send는 선택적 Idempotency-Key 헤더만 추가(미제출 시 기존 동작 그대로).
2. 롤백: `ln -sfn ~/services/matrix-studio-spring/releases/2e1914751341 ~/services/matrix-studio-spring/current
   && systemctl --user restart matrix-studio-spring-8024` — 접수된 작업 원장(agent_bridge_*)은
   PostgreSQL에 남아 롤백 중에도 보존(명세 §9 요건). 엣지 프록시·터널은 별도 유닛이라 무관.

## 7. 11-07 추가 — 호출환경 403 대응: HTTPS 경로 전환 + 부트스트랩 전달

사건: 이사님 보고 "ChatGPT 호출환경에서 trycloudflare 주소가 403 'Your request was blocked.'"
(서버 측 동일 주소 200 — Cloudflare WAF의 데이터센터 IP·비브라우저 차단으로 판단).

1. 경로 탐색: LE IP 인증서(엣지 443) 시도 → certbot 5.9.0이 IP 주소 발급 자체를 거부(불가 확인).
   대안 확정: aws512-edge에 이미 켜져 있던 Tailscale Funnel(443, ts.net 인증서는 Tailscale이
   자동 발급·갱신) 재사용. Funnel 루트가 엣지 nginx :80으로 전달되는 구조라
   nginx에 `location ^~ /api/agent-bridge/v1/ → duradev_spring(8024)` 1행만 추가(edge.conf 49행).
   Funnel 설정·타 서비스 경로 무변경.
2. **새 base URL(주소 고정 — 터널 재시작 무관, 인증키 동일):**
   `https://aws512-edge.tail1cf879.ts.net/api/agent-bridge/v1`
3. 서버 측 실측(11-07, 전부 통과):
   - tailnet 내부 경로: health 200(0.11s), 무토큰 whoami 401, 타 경로(/api/nats/*) 404 — 경로 필터 유지.
   - **공용 인그레스 경로**: 공용 DNS(1.1.1.1)가 알려준 공인 IP(103.84.155.153)로 강제 접속 —
     health 200(0.47s), 무토큰 401, TLS 유효(시스템 CA 검증 통과). 진짜 인터넷 왕복 실증.
   - POST 계약: Idempotency-Key 누락 400, 잘못된 kind 400(헤더·본문 정상 도달, 원장 미삽입).
   - quick tunnel·8126 경로프록시·urlwatch 크론 폐기(disable --now·crontab 제거, 파일 보존).
     롤백: `systemctl --user enable --now agent-bridge-tunnel agent-bridge-edge` + urlwatch 재등록.
4. 부트스트랩 일회용 URL(커밋 `c081676…`, 배포 releases/c081676…):
   - POST /bootstrap(Bearer 필수) → 코드 40자 hex·10분 만료. 재발급 시 그 신원의 이전 코드 폐기.
   - GET /bootstrap/{code} — 공개·단 1회. 응답 {actor_id, token, usage}. 환급은
     `DELETE … RETURNING` 원자 처리로 동시 조회 시 1명만 성공. 토큰값은 서버 전용 파일(0600,
     또는 60초 캐시)에서 즉시 읽어 반환 — 채팅·Git·로그 미경유, 저장도 안 함.
   - 실측 7항목 통과: 무토큰 발급 401 · 발급 형식(40hex) · 공개 URL 1회 환급 값 일치(MATCH) ·
     재환급 404 · 미지수 코드 404 · 재발급 시 이전 폐기(404) · whoami 정상.
5. **ChatGPT 실제 접속 검증: 미실시(이사님 확인 몫)** — 체크리스트:
   ① `GET <base>/health` → 200 ② 부트스트랩 URL 1회 환급으로 토큰 수령→안전 보관
   ③ `GET /whoami`(Bearer) → 200 ④ status 작업 1건 제출·조회 왕복.
6. 남은 제한 갱신: "고정 도메인 필요" 항목은 해소(기계명 고정 주소). 단 tailnet Funnel 정책이
   바뀌면 경로 상실 가능(감시 방법은 C2 과제). C2 나머지(verified 승격·lease·타임아웃·implement) 동일.
