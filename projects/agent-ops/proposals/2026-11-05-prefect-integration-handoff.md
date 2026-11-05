---
title: Prefect 프로젝트 연결도·실행 관리 구현 인수인계
date: 2026-11-05
status: specification-written / awaiting-manager-dispatch
document_id: MATRIX-ORCH-HANDOFF-001
product_repo: markjang29/matrix-home
---

# Prefect 프로젝트 연결도·실행 관리 구현 인수인계

사용자는 Prefect 방식으로 프로젝트 연결구도를 관리하고 싶다고 설명했고, 개발명세를 Git에 남기면 Claude Code 매니저에게 구현을 지시하겠다고 요청했다.

제품 개발명세는 아래 한 파일을 정본으로 사용한다. 이 Notes 문서는 조직 간 인수인계와 진입 링크를 제공한다.

[제품 개발명세 MATRIX-ORCH-001 v1](https://github.com/markjang29/matrix-home/blob/d71c5985f1930f56890a75270fc7952127249745/docs/architecture/prefect-project-orchestration-spec-v1.md)

## 01 근거

- 제품 명세 commit은 `d71c5985f1930f56890a75270fc7952127249745`이며 경로는 `docs/architecture/prefect-project-orchestration-spec-v1.md`다.
- 조사한 제품 기준은 `matrix-home@8eed99425fff2994abe47fac7f47508afaaacd19`다.
- 조사한 조직 기준은 `notes@2f3bc91b7297f9a896e77a574ceaca4e2999b5c4`다.
- 기존 `topology-graph/graph.json`, `topology-graph-v1.md`, `workflow-comm-v1.md`, `asset-pipeline-graph-design-v1.md` 및 원사이트 목표 설계를 읽고 작성했다.
- 연결도는 Notes의 관계 정본, 계보는 제품의 실제 자료와 receipt, 실행 상태는 Prefect를 연결한다.
- 공개된 Git snapshot에 기반한 설계이며 홈서버 runtime은 이번에 실측하지 않았다.

## 02 미완료

Prefect 설치, 제품 코드 구현, 담당 봇 발령, 운영 배포는 아직 수행되지 않았다. 현재 요청의 산출물은 구현 명세다.

구현 첫 범위는 P0 현황 조사, P1 고정 버전 실행 기반, P2 실제 자료 한 건 검증과 원사이트 조회 연결이다. 제작 흐름 확대와 scheduler 운영 전환은 명세의 P3/P4에서 다룬다.

명세에는 15개 검증 항목이 있다. 정의돼 있다는 사실과 시험에 통과했다는 사실을 구분해 보고한다.

## 03 블로커

실제 Spring/React donor의 현재 코드·제품 정본 반영 여부, 홈서버 장비 용량, 실행 중인 scheduler, 첫 validator의 정확한 entrypoint는 매니저가 P0에서 확인해야 한다. 과거 Git 문서의 active/완료 표시를 현재 runtime 상태로 그대로 사용하지 않는다.

첫 flow와 제품 통합에 필요한 저장소부터 조사하고, 기반 기능이 미완료면 그 경로와 선행 작업을 특정한다. 단독 Prefect fixture 실행 검증은 독립해서 진행할 수 있다.

## 04 다음

아래 지시문을 Claude Code 매니저에게 전달할 수 있다.

> `markjang29/matrix-home@d71c5985f1930f56890a75270fc7952127249745`의 `docs/architecture/prefect-project-orchestration-spec-v1.md`를 기준으로 Prefect 연결도·실행 관리 구현을 시작해.
>
> 최신 Git과 실제 환경을 대조해서 첫 flow에 필요한 재사용 모듈·현재 entrypoint·scheduler를 먼저 확인하고, P0~P2를 담당자별 작업으로 나눠. 각 작업에 exact input commit, 변경 경로, 완료 기준과 테스트를 붙여.
>
> 기존 Notes 연결도와 원사이트 Spring/React 구조에 연결하고, 실제 자료 한 건의 검증에서 프로젝트 관계 → 실행 → 입력·출력 근거가 이어지는 데모를 먼저 완성해. sample과 real, 실행 완료와 승인 완료를 구분해.
>
> 결과 보고에는 구현 commit, 실행 receipt, 통과한 AC 번호, 미완료와 다음 작업을 남겨. 운영 배포와 scheduler 전환은 기존 배포 게이트에 맞춰 진행해.

담당 매니저는 최신 정책·정체 확인 후 위 지시를 작업 카드로 정규화한다. 이 문서의 커밋 자체는 봇 발령이나 서버 배포를 의미하지 않는다.
