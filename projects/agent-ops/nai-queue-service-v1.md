---
title: NAI 발행 큐 서비스 v1 (nai-queue, :8026) — API→큐→워커
date: 2026-09-07
status: v1 가동 중 — 엔드투엔드 시험 완료 (firewin zcode 구축, 이사님 09-07 지시 "API로 request 전달하면 큐 받아서 처리")
tags:
  - nai
  - queue
  - api
  - service
---

# NAI 발행 큐 서비스 v1 — nai-queue (AWS :8026)

> 이사님 지시: "API로 request 전달하면 그쪽이 큐(db나 카프카 등 메시지 라이브러리) 받아서 처리하도록".
> Kafka 대신 조직 표준 스택인 MongoDB 큐로 구현(대기열·상태·재시도가 DB에 영속 — 재시작에도 유실 없음).

## 아키텍처

```
[아무 봇/사람] --POST /api/jobs--> [nai-queue API :8026] --> [Mongo nai_queue.jobs 큐]
                                                                     |
                                     [워커 스레드] <-- 폴링(10s) --+
                                       |  scene_to_nai.generate (NAI 키는 이 서버 파일에만 상주)
                                       +--> ~/nai_out/queue/<work>/<scene_id>.png
```

- 파일: AWS `~/nai-queue/server.py` (표준 라이브러리+pymongo 단독 — Flask/venv 불필요, workbench_web 선례)
- 토큰: `~/nai-queue/.token` (chmod 600, 값은 서버 파일에만 존재 — 모든 엔드포인트 X-Token 헤더 요구)
- 큐: mongo `nai_queue.jobs` — scene_id unique, 상태 pending→processing→done/error, attempts<3 자동 재시도, error는 retry 엔드포인트로 재큐
- 워커: 10초 폴링 + 생성 후 15초 쿨다운(NAI 레이트 제한 여유), 생성 실패 시 3회까지 자동 재시도

## 엔드포인트 (모두 X-Token 필요)

| 메서드 | 경로 | 용도 |
|---|---|---|
| POST | `/api/jobs` | 발행 요청. 단건 또는 {"jobs":[...]} 배치. 필수: scene_id·work·prompt(prompt_draft 별칭 허용 — scenes.jsonl 직접 투입 가능) |
| GET | `/api/jobs?status=pending&limit=50` | 큐 목록 |
| GET | `/api/jobs/<scene_id>` | 작업 상태·출력 경로·오류 |
| POST | `/api/jobs/<scene_id>/retry` | error → pending 재큐 |
| GET | `/api/status` | 집계(pending/processing/done/error) |

## 운영

```bash
# 기동(ssh -f 필수 — setsid 단독은 세션 종료 시 꺾일 수 있음)
ssh -f aws "python3 ~/nai-queue/server.py >> ~/nai-queue/server.log 2>&1 < /dev/null"
# 확인
ssh aws "ss -tln | grep 8026; pgrep -af 'nai-queue/server.py'"
# 재기동
ssh aws "pkill -f 'nai-queue/server.py'" && 위 기동 재실행
```

## 시험 결과 (09-07)

- POST trial-pd-s01(망나니 PD 1화 편집실 장면) → **12초 만에 done**, `~/nai_out/queue/망나니_PD_아이돌로_살아남기/trial-pd-s01.png` 1,017,610 bytes 발행.
- v1 시험 사례: 망나니 PD scenes.jsonl 5건(커밋 736636b) + nai_out/scene_test 2장(수동).

## 다음 단계

1. **gmwin zcode 연동**(이사님 결정: gmwin 전담 — 요약+NAI 전부): 매니저의 자격 배포(NAI 키 gmwin 복사·law4743 원문 접근) 완료 시, gmwin은 요약 장면을 본 API로 POST하는 방식으로 전환 가능(생성은 큐 워커가 수행 — 키는 AWS에만 상주가 더 안전하나, 이사님이 gmwin 직접 생성을 원하면 키 복사안 유지).
2. scenes.jsonl → POST 자동화 스크립트(배치 투입기).
3. 발행 이미지의 웹 노출(8016 이미지 단계·matrix-home 정적 연결) — 매니저 결정.

## 보안 메모

- 회의방 `/api/bot/config?scope=llm`이 api_key를 평문 반환함(09-07 실측) — 매니저에게 노출 벡터 보고 권장.
- 본 서비스 토큰·NAI 키는 어디에도 기록하지 않음(서버 파일만).
