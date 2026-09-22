# 메시지 정의서 — 그림(이미지) 생성 플로우 v1 (계획모드, 이사님 09-22 지시)

- 발행: 매니저 2026-09-22 · 상위: `messaging-architecture-v1.md` @ f0636234 (두 평면 — 본 문서는 **시스템간 평면(svc) + 봇 트리거(하이브리드)**)
- 실측 기반: nai-queue 8026 가동 중(status기계: pending→processing→done/failed, retry 구비, GEN_COOLDOWN 레이트제한) · 98봇 RELAY-67 실측("원문저장소→8026 직투"가 이미 실가동 경로)
- 성격: **계획(계획모드) — 98봇 구현 + 이사님 승인 게이트 전까지 미시행. 코드 변경 없음.**

## 0. 한 줄

그림 1장은 6단계 7메시지. 요구(REQ)→큐접수(ACCEPTED)→생성시작(STARTED)→완료/실패(REPLY/DONE|FAILED)→저장고등록(STORED)→알림(NOTIFY)→봇트리거(선택).

## 1. 당사자 (실측)

| 역할 | 주체 | 평면 |
|---|---|---|
| REQ 발신(의뢰) | ① 서비스: 8015 워크벤치·8026외 출판시스템 ② **AI 봇**(heav_lnx_novel_col_bot 등 — 시나리오 읽고 그림 의뢰) | 둘 다 |
| 큐·생성 | nai-queue 8026 (NAI nai-diffusion-3, 832x1216, 개당~3초, cooldown) | svc |
| 저장 | novel_assets 로컬 + gdrive(matrix-upload, rclone) | svc |
| 통보·승인 | 8024 원장 + **봇 트리거**(완료 시 담당 봇이 검수·이사님 전송 판단) | bot |

## 2. 메시지 7종 (SECS식 요구/응답 쌍 — 각 REQ에는 필수 REPLY가 맵핑)

### M1 `PICTURE_CREATE_REQUEST` (REQ)
```
토픽: svc.msg.<의뢰Svc>.nai-queue  (봇 의뢰시: bot.msg.<봇>.nai-queue)
type: task · version: 1
payload: {
  "scene_id": "ep12-s3-001",          // 필수, 멱등키(중복제거 기준)
  "work": "novel-<작품id>",            // 저장경로 루트
  "prompt": "masterpiece, ...",        // 필수, NAI태그 문자열
  "model": "nai-diffusion-3",          // 기본값 고정
  "size": "832x1216",                  // 무료규격 고정(Anlas 0)
  "count": 1,                          // 1~4
  "reply_to": "svc.msg.nai-queue.<의뢰Svc>" | "bot.msg.nai-queue.<봇>",
  "trigger": "bot|none"                // ★봇트리거: 완료시 알림받을 봇 username 또는 none
}
```
### M2 `PICTURE_CREATE_ACCEPTED` (REPLY, 즉시·동기)
```
payload: { "ref_scene_id": ..., "job_id": "8026-queue-<uuid>", "position": 3, "eta_sec": 15 }
```
### M3 `PICTURE_CREATE_STARTED` (큐→구독, 비동기)
```
payload: { "ref_scene_id": ..., "job_id": ..., "worker": "w1", "nai_model": ... }
```
### M4 `PICTURE_CREATE_REPLY` (REPLY, 핵심)
```
성공: payload: { "ref_scene_id":..., "job_id":..., "status":"done", "output":"<절대경로아님: work/scene.png 상대경로>",
                "gen_meta": { "width":832, "height":1216, "took_sec":3.1, "anlas":0 } }
실패: payload: { "status":"failed", "retry_of": n, "error_code": "NAI_TIMEOUT|NAI_AUTH|DISK_FULL|RATE_LIMIT", "error_text":"..." }
```
- 실패시 큐 내부 retry(기존 구현, 무한x — 최대 3회) → 3회 초과 failed 확정 후 M4 failed. **error_code는 계약(문자열 4종 고정)** — 수신측이 분기하는 유일한 키
### M5 `PICTURE_STORED` (저장고 등록 확인)
```
발신: matrix-upload(gdrive)·또는 로컬 확정자
payload: { "ref_scene_id":..., "stored_uri": "gdrive://RPG저장고/NAI_.../<scene_id>.png", "bytes": 1500000, "sha256":"<해시16자>" }
```
### M6 `PICTURE_NOTIFY` (이사님·인계 봇에게 — 봇트리거)
```
토픽: bot.msg.<trigger봇>.<원본의뢰봇>  · type: notice
payload: { "ref_scene_id":..., "stored_uri":..., "review_needed": true|false }
→ ★봇트리거: trigger≠none이면 완료(M4 done)+저장(M5) 후 이 메시지로 지정 봇 깨어남 —
  봇은 검수(이미지 열람·품질 판단)→이사님 텔레그램 전송 여부 판단. **여기서 시스템평면→봇평면으로 승선(bridge)**
```
### M7 `PICTURE_CANCEL` (REQ, 선택)
```
payload: { "ref_scene_id":..., "if_state":"pending|processing" } → REPLY: ACCEPTED|REJECTED(이미 done)
```

## 3. 흐름 (2가지 — 계약 전체지도)

```
[플로우 A: 서비스 의뢰 — 순수 svc 평면]
8015워크벤치 ──M1──▶ 8026큐 ──M2 ACCEPTED(동기)──▶ 8015
                8026 ──M3 STARTED──▶ (원장만)
                8026 ──M4 REPLY done──▶ 8015 + 원장
                matrix-upload ──M5 STORED──▶ 원장
                                    (trigger=none이면 종료)

[플로우 B: 봇 의뢰 — svc→bot 브리지]
novel_col봇 ──M1(trigger=heav_lnx_novel_col_bot)──▶ 8026
        8026 ──M2──▶ 봇 (봇은 즉시 잠들 수 있음 — 비동기)
        ... 8026 처리 ...
        8026/M4+M5 → 8024 원장 ──M6 PICTURE_NOTIFY──▶ 봇 (깨어남)
        봇: 이미지 검수 → 이사님 텔레그램 or 보류판단 → 결과를 type:progress로 8024 원장 (봇평면 복귀)
```

## 4. 계약 규칙 (SECS식 — 어길시 수신거부)

1. **scene_id = 멱등키**: 중복 M1은 기존 job_id로 응답(재생성 아님) — 8026이 보장
2. **REQ 없는 STARTED/REPLY 불가** — 원장 역추적이 항상 가능(사칙: 증적 없는 메시지는 위반)
3. **error_code 4종 고정**: NAI_TIMEOUT·NAI_AUTH·DISK_FULL·RATE_LIMIT — 추가는 정의서 개정만
4. **경로는 상대경로만** (work/scene.png) — 기계 절대경로는 95-1 비밀규칙 준용, 페이로드에서 금지
5. **version 불일치 시 수신측이 거부 + 원장에 "schema_mismatch" 기록** — 조용한 파싱 실패 금지
6. **M6 브리지는 8024가 유일**: svc→bot 직접 연결 없음. 8024가 "봇트리거"필드 보고 깨울 봇 결정(봇이 잠들어도 안전)
7. GEN_COOLDOWN 등 레이트제한은 8026 내부구현 — 메시지 계약에 노출 안 함(캡슐화)

## 5. 미정 (이사님·98 확인 사항 — 계획모드이므로 열어둠)

- ① 봇트리거의 기본값: 신규 의뢰시 무조건 봇 검수 거치는가, 아니면 trigger=none(무검수 즉시 이사님)이 기본인가
- ② M5 저장고 등록: 현재 수동(이사님 승인 후 구드라이브) — 자동화하면 Anlas·용량 관리 규칙 필요
- ③ 실패 3회 초과 후: 자동 재시도 중단+봇 통보(안) / 이사님 즉시 통보(안) — 95-1과 중복 여부
- ④ 8016·8015 등 다른 이미지 소스(NAI외) — 이 정의서 7종으로 커버되는지, 아니면 MESSAGE 종류 추가 필요한지

## 6. ELI5

그림 한 장 주문받기(M1)→"주문접수됐어요 알림"(M2)→"지금 만들고 있어요"(M3)→"완성됐어요/망했어요+이유 4가지 중 하나"(M4)→"창고에 넣었어요+지문번호"(M5)→"OO봇님 확인하세요+이사님께 보낼까요?"(M6)→주문취소(M7). 7단계 전화 규격이고, 마지막에 지정된 봇이 깨어나 그림 확인하고 이사님 폰으로 보낼지 정하는 것.
