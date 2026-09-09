---
name: topology-map-first
description: 항상 전체 봇·전체 사이트(컴퓨터·AWS·구성도)를 머릿속에 두고 일한다 (이사님 09-08)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6f2d649c-3598-4170-88fd-57842b5cea87
  modified: 2026-09-09T02:47:07.466Z
---

이사님 2026-09-08 지시. 모든 판단·배정·보고는 **전체 구성도 기준**으로 한다:

- **사이트(컴퓨터)**: AWS 8GB(13.125.131.126, 셧다운 예정) · AWS 엣지 512MB(43.201.34.144,
  aws512-edge, 외부 진입점) · 홈 리눅스 duradev(100.109.91.0, 본진) · GM 윈도우 nucboxg3
  (100.97.180.0, gmwin+firebat) · 윈도우 WIN-TGON9IO01TV(100.122.67.122, firewin) · 이사님 폰.
- **연결**: 엣지 → tailscale(가족 복도) → 홈 리눅스 실서빙. 관제 서버 8023(AWS, 홈 이관 진행 중),
  원사이트 스프링 8024.
- 배정 시 "이 일은 어느 사이트의 어느 봇 몫인가"를 항상 구성도로 확인. 보고에도 위치를 붙인다.

**Why:** 봇·서비스가 흩어져 있어 위치 없이 판단하면 배정 실수·중복이 생김. 이사님 명시 지시.

**How to apply:** 작업 접수 → 구성도에서 대상 사이트·봇 특정 → Task Contract repo 필드에 위치 명기.
정본 지도: notes `projects/agent-ops/aws-edge-instances` 관련 + ORG-RULES §1 + tailnet 6노드.
관련 [[manager-window-principle]] · [[aws-edge-instances]].
