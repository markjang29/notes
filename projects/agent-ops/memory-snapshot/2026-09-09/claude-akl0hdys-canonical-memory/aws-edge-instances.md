---
name: aws-edge-instances
description: "AWS 인스턴스 2대 구성 — 신규 엣지 512MB(ubuntu 유저, 외부 입구 전용) + 기존 8GB(셧다운 예정)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f2d649c-3598-4170-88fd-57842b5cea87
  modified: 2026-09-06T06:37:15.698Z
---

이사님 2026-09-06 지시. AWS를 **2대 체제**로 정리:

- **신규 엣지 인스턴스** — 메모리 **512MB**, OS 유저명 **ubuntu**, 공인 IP **43.201.34.144**.
  접속 테스트 완료(09-06): Ubuntu 22.04.5 LTS · vCPU 2 · RAM 총 416MB usable(표기 512MB — 커널
  예약분 정상) · 디스크 20G(사용 3G). 키: `~/.ssh/lightsail-512ram.pem`(600, 커밋·채팅 게시 금지).
  역할 = **외부 입구 전용**(봇·게이트웨이 관문 OK, 웹서비스·DB 상주 금지) — 실서빙은 **tailnet으로
  홈 리눅스(N100 #1)에 위임**.
  **tailnet 편입 완료(09-06 이사님 승인)**: 노드명 **aws512-edge**, 조직망 IP **100.102.194.108**.
  조직망 지도(09-06 확정): aws512-edge(엣지) · **duradev=GM 리눅스=홈 N100 1번(100.109.91.0,
  실서빙 예정 — 이사님 확정)** · ip-172-26-2-127=8GB AWS(100.81.50.115) ·
  **nucboxg3=GM 윈도우(100.97.180.0, gmwin claude+zcode 상주 — 본체 직접 검증)** ·
  s23-ultra(폰) · win-tgon9io01tv(윈도우).
  설치: tailscale 1.102.3, `--accept-dns=false`·hostname 고정.
  **봇 heav_aws512 가동(09-06 "go")**: 스왑 1GB + GLM 프록시 이식(`~/scripts/zai-fallback-proxy.js`,
  systemd `zai-proxy.service`, 127.0.0.1:8788) + claude 자격 env를 8GB settings.json에서 ssh 파이프로
  병합. 스모크 성공("ok" 회신). RAM available ~250MB·스왑 사용 66MB 실측 — **봇 1기+claude가 한계선,
  2기째·DB·웹서비스 추가 금지**. claude는 `~/.local/bin/claude`(ssh 비로그인 PATH 밖 — 접속 시
  PATH export 필요).
- **기존 AWS(현재 이 봇·회의방 8023·대시보드 8025 구동 중, 13.125.131.126)** — 메모리 **8GB**,
  **셧다운 예정**. → 봇·관제 서비스의 홈(N100) 이관이 필요하며 이는 설계 v1.1 §6 4단계(이관은 마지막)와
  일치.

**Why:** 설계 v1.1 §1의 "AWS 엣지 축소"가 실물로 확정된 것. 512MB는 게이트웨이 역할만 가능한 초소형 —
서비스 상주 금지, 입구 릴레이만.

**How to apply:** 새 서비스·DB·봇을 신규 엣지(512MB)에 상주시키지 않는다. 이관 작업은 홈 리눅스
대상으로 설계한다. 관련 [[workspace-layout]] · [[relay-site-integration-0824]] · notes 정본
`projects/agent-ops/homeserver-target-design-v1.md`.
