---
title: 명세서 v4 — 소설 장면 요약→NAI 발행 (gmwin zcode, 관제 허브 경유)
date: 2026-09-08
status: v4 — 관제 허브(8023 /api/hub/*) 경유 확정. 이사님 09-07 허브 배포 + 지시 반영
tags:
  - nai
  - scene
  - gmwin
  - hub
  - queue
---

# 명세서 v4 — 소설 장면 요약 → NAI 발행 (gmwin zcode, 관제 허브 경유)

> 이사님 09-07 결정: gmwin이 요약+NAI 생성 전부 담당. 소스 = 『이것이 법이다』.
> 관제 허브 v1(8023 /api/hub/*)이 가동 중 — gmwin에게는 **hub_client.py로 task 수신 → 요약 → 큐 POST → done 보고**의 흐름.

## 1. 흐름 (관제 허브 경유)

```
firewin(요약 루프) → 배치 노트 commit → hub.send(to:"heav_gmwin_zcode_bot", type:"task", key:"law-batch-NN")
  → gmwin zcode 30초 폴러가 수신(drain→ack)
  → gmwin: 원문 8899 읽기서비스에서 장면 선별 → scenes.jsonl 작성
  → gmwin: POST http://100.109.91.0:8026/api/jobs (NAI 발행 큐)
  → 워커: NAI 이미지 생성 → done
  → gmwin: hub.send(to:"heav_firebat_zcode_bot", type:"submitted", payload:{커밋해시, 이미지 경로})
  → firewin: 갤러리 카드 갱신 + 회의방 보고
```

## 2. 관제 허브 인터페이스 (gmwin 측)

- **수신 폴링**: `python3 hub_client.py poll --base http://43.201.34.144 --bot heav_gmwin_zcode_bot --token <토큰> --cmd "<셸명령>"`
- **송신**: `hub.send(to, type, payload, key)` — 진행=progress, 막힘=blocked, 완료=submitted
- **멱등키**: key 필수(예: `law-batch-003`) — 재전송 중복 방지
- **DLQ**: 3회 실패 시 dead — 이사님 토큰으로 재큐

## 3. NAI 발행 큐 (nai-queue, AWS :8026)

- POST /api/jobs — scene_id·work·prompt·negative 필수
- 워커 자동 발행 → nai_out/queue/<work>/<scene_id>.png
- 상태 확인: GET /api/jobs/<scene_id>
- **갤러리**: `http://100.109.91.0:8027/?key=<뷰키>` — 문장 발췌+프롬프트+이미지 카드 표시

## 4.gmwin 작업 절차

1. hub poll로 task 수신 → ACK
2. `http://100.81.50.115:8899/`(law4743 테일넷 읽기서비스)에서 원문 직독(4~6화)
3. 배치 요약 노트 작성(duradev `_batch_notes/`)
4. scenes.jsonl 작성(문장 발췌+danbooru 태그+프롬프트) → scenario repo 커밋+push
5. nai-queue :8026 POST(NAI 발행 요청)
6. hub.send(type:"submitted", payload:{커밋해시, scene_id 목록, 이미지 경로})
7. 진행 카드 갱신(duradev 8018)

## 5. 금지

- 원문 byte Git 반입 / NAI 키·큐 토큰 Git 기록 / novel_col 영역 침범 / 이미지 외부 배포 / 배치당 10장면 초과
