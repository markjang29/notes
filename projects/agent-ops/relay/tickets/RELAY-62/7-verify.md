---
ticket: RELAY-62
stage: relay:7-검증
owner: aws-audit
date: 2026-09-07
status: verified_gap1
---

# RELAY-62 검증 — Edge/Home 정책·관제 라우팅 갭 실측

- 실측 시각: 2026-09-07 16:20 KST
- 측정자: aws-audit (AWS 매니저 박스에서 실측, tailscale 경유)

## gap① /policies·/governance 404 → 해소 확인

| 경로 | 43.201.34.144 (엣지) | duradev:8018 (홈) |
|---|---|---|
| /policies | 200 | 200 |
| /governance | 200 | 200 |
| /api/policies | 200 | 200 |
| /api/governance | 200 | 200 |

- 정합성: 엣지 `/api/policies`의 `policy_sha` = `cc7946bbec48` = notes HEAD 동일 (version `2026-09-07.4`)
- 무결성: `/policies` 본문 md5 엣지=홈 동일(`6ed5cc3e88`) — 홈 duradev:8018 원본의 엣지 패스스루
- 관제: 엣지 경유 `/api/governance` rows 17건
- 구조 판정: 구동은 홈서버(duradev)가 담당, `43.201.34.144`는 Tailscale 프록시만 — 이사님 지시 구조와 일치.
  옛 AWS 8GB(13.125.131.126:8018)로 되돌리는 라우팅 아님.
- 배치 주체: 홈 측 서비스가 본 실측 이전(당일 오후 사이)에 /policies·/governance 서빙을 시작함.
  본 박스 로그상 배치 주체 특정 불가 — 홈 측(duradev) 작업 기록 참조 바람.

## 회귀 확인 (엣지 경유)

- `/` 200 · `/studio/` 200 · `/drawing/` 200 · `/nexus/` 200 · `/envsync/` 200 · `/healthz` 200

## gap② nucboxg3:8766 (2세대 Spring+React) — 미해소 유지

- tailscale 경유 `100.97.180.0:8766` 실측: `000` 불도달 (2026-09-07 16:20)
- 조치 주체 불변: nucboxg3 로컬 — Java 0.0.0.0(또는 tailscale IP) 바인딩 + Windows 방화벽 허용 (gmwin 측)

## 후속

- 봇 안내 정본 주소를 `http://43.201.34.144/policies`·`http://43.201.34.144/governance`로 확정 사용 가능
- gap②만 잔존 — 원사이트(Spring+React) 트랙에서 추적

## 후속 2 — 2026-09-07 17시대, 43.201.34.144 외부 접속 불가 원인·Funnel 임시 개설

- 이사님 보고: 공인 IP 접속 "err timed out". 원인 특정 3단:
  1. 엣지 OS 레벨 깨끗 — nginx `0.0.0.0:80` 리슨, ufw inactive, iptables는 tailscale 표준 체인만, nginx deny/geo 없음 (SSH 직접 확인, 키 `~/.ssh/lightsail-512ram.pem`)
  2. 매니저 박스(13.125.131.126) → 80 OK / 이사님 네트워크 → timeout
  3. 결론: **Lightsail 인스턴스 방화벽**(OS 바깥 레이어)이 80을 특정 소스만 허용. 서버 내부에서는 조회·수정 불가(AWS 자격 이 박스에 없음), 콘솔 권한자 작업 필요.
- **임시 공인 HTTPS 개설 (aws-audit, 이사님 지시로 엣지 SSH 접속해 조치)**:
  - `sudo tailscale funnel --bg 80` → `https://aws512-edge.tail1cf879.ts.net/` 가 공인 인터넷에 개설됨 (Lightsail 방화벽 우회, 자동 TLS)
  - 실측(매니저 박스, funnel 릴레이 경유): `/` 200 · `/policies` 200 · `/governance` 200 · `/drawing/` 200 · `/healthz` 200
  - 해제: `sudo tailscale funnel --https=443 off`
  - 한계: Tailscale 릴레이 경유 대역폭 제한 — 대용량 트래픽 서비스는 원 IP 복구가 정석
- **잔여**: Lightsail 콘솔에서 aws512-edge의 HTTP(80)를 Any(0.0.0.0/0)로 개방하면 `43.201.34.144` 정본 주소 복구 (콘솔 권한자: 이사님 또는 gmwin)
