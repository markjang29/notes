---
title: 전사 토폴로지 그래프 v1 — git·티켓·자산·사이트 전수 (누락 방지 원장)
date: 2026-09-08
status: 수집 진행 중 — 사이트별 분배 완료
tags: [agent-ops, topology, graph]
---

# 전사 토폴로지 그래프 v1

> 이사님 09-08: "git·jira·로컬자산·사이트 전체 다 확인해서 노드·엣지로 누락 없이. 나중에
> 홈서버 동기화·인수인계도 할 것." — 자산 파이프라인 그래프(asset-pipeline-graph-design-v1)의
> 데이터 기반이 되는 전사 원장.

## 1. 노드 타입 (6종)

- `site` — 컴퓨터/위치(AWS 8GB·AWS 엣지 512·홈 리눅스 duradev·GM 윈도우 nucboxg3·firewin PC·폰)
- `service` — 사이트 위에서 돌아가는 것(포트 보유: 8018·8023·8024·8788…)
- `git` — 저장소(notes·matrix-*·scenario·relay…) — 원격 유무·위치(사이트) 포함
- `ticket` — 요구사항/작업(RELAY-*·대기결정·20장 카드) — JIRA 상당
- `asset_store` — 자산 창고(Works/arcalive 87G·novel 5.7G·risu·asset_ledger·novel_queue·Drive 콜드)
- `bot` — 봇(사이트 소속·엔진·모델·폴러 상태)

## 2. 엣지 타입 (5종)

- `runs_on` (service/bot → site) · `hosts` (site → asset_store/git)
- `owns` (bot → service/git/asset_store/단계)
- `flows` (asset_store → asset_store: 수집→원장→미러→콜드)
- `tracks` (ticket → 대상 node: 요구사항이 가리키는 것)
- `commits_to` (bot → git)

## 3. 데이터 규격

- 단일 JSON: `topology-graph/graph.json` — `{nodes:[{id,type,label,site?,owner?,status?,survey}], edges:[{from,to,type,label?}]}`
- **모든 노드에 `survey` 필드**: `done|pending` — 누락 방지의 핵심(미수집은 빈칸이 아니라 pending으로 남긴다).
- React Flow는 이 JSON을 직접 읽는다(라이브 뷰). 편집·deploy는 asset-pipeline-graph-design-v1의 2단 구조를 따른다.

## 4. 수집 분배 (사이트별 — 누락 방지 책임자)

- AWS(매니저·자기 기계): 로컬 봇 10·서비스 포트 지도·notes/관제 git·RELAY 티켓 — **done(1차)**
- nucboxg3 — **gmwin claude**: 기기 봇 4기(firebat claude·gmwin claude/zcode)·git clone 현황·폴러 상태 + firebat 폴러 기동 협조 — pending
- firewin PC(WIN-TGON9IO01TV) — **firewin zcode**: 자산창고 트리·ledger·동기화 상태·보유 git — pending(폴러 상태 불명, 도달 시점 대기)
- duradev(홈 리눅스) — **gmlnx claude**: 8018/8021/8022 서비스·소설 큐·홈 git — pending(폴러 미구동 — gmwin 경로로 릴레이 시도)
- AWS 엣지 512 — 매니저가 직접(자기가 구축): aws512-edge·zai 프록시·heav_aws512 — done

## 5. 홈서버 동기화·인수인계 대비

- graph.json은 **git 원장(notes)으로만 관리** — 사이트 로컬 사본 금지(단일 원장선행이동 원칙).
- 홈 이관 시: ①graph.json 그대로 이관(경로 불변) ②각 노드 `site` 필드만 갱신 ③deploy 게이트로
  반영 — 인수인계자는 graph.json + ORG-RULES + 관제 허브 정본 3개로 전체 복원 가능하도록 유지.
