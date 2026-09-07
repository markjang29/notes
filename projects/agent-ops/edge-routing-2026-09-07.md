# 엣지(43.201.34.144) 라우팅 추가 — /drawing (2026-09-07 매니저)

- **배경**: gmwin zcode 요청(이사님 RELAY-62 진입점 통일 이행) — 매니저가 SSH 실측 후 직접 적용.
  gmwin은 엣지 SSH 키 부재로 자체 수행 불가.
- **엣지 실체**: Lightsail(ip-172-26-5-84, nginx 1.18, `sites-enabled/edge.conf`, sudo NOPASSWD,
  tailscale 가입 — duradev·nucboxg3·AWS 매니저 박스 모두 보임).
- **변경** (`edge.conf`, 백업: 엣지 `~/nginx-backups/edge.conf.bak-drawing-09070548`)
  ① `upstream nucboxg3_drawing { server 100.97.180.0:8765; }` 신설
  ② `location /drawing/` → prefix-strip 프록시(기존 `/studio/` 패턴과 동일)
  ③ `location /src-img/` → 경로보존 프록시 — 드로잉 앱이 절대경로 `/src-img/…` 참조(HTML 1곳 실측)라
     미추가 시 이미지 저장 후 브라우저 요청이 엣지 `/`(duradev 8018)로 새고 깨짐.
     홈 8018 `/src-img/` = 404라 충돌 0 확인 후 추가.
- **검증(공인 URL 실측)**: `/drawing/` 200(12.4KB) · `/src-img/routetest` → 앱 본인 응답
  "Cannot GET"(=8765 도달 증명) · 회귀 `/`, `/studio/`, `/nexus/`, `/envsync/`, `/healthz` 전부 200.
- **미해결 2건**
  ① **8766(2세대 Spring+React) 엣지에서 도달 불가**(AWS·엣지 양쪽에서 000 재관측) —
     nucboxg3 로컬 조치 필요: Java를 0.0.0.0(또는 tailscale IP 100.97.180.0) 바인딩 + Windows 방화벽 허용.
     엣지 conf에 보류 주석 기록. → gmwin 측 작업.
  ② **/policies·/governance 404 gap 불변**(이사님 지시대로 gap 보고 유지) — 원인: 엣지 `/`가
     duradev 홈 8018로 향하는데 정책센터·관제한판 페이지는 AWS 8018 쪽에 존재. 해소하려면
     (a) 해당 prefix만 AWS 8018로 라우팅하거나 (b) 페이지를 홈에 배치 — 원사이트 트랙에서 결정 필요.
- **교훈**: sites-enabled 안에 .bak 파일 두면 nginx가 함께 로딩해 중복 upstream 오류 — 백업은 밖에.

---

## 추가 — 09-07 16:20 감사실측 (aws-audit)

- **미해결 ① 해소 확인**: `43.201.34.144/policies`·`/governance`·`/api/*` 전부 200. 구동은 홈 duradev:8018,
  엣지는 Tailscale 패스스루(`/policies` 본문 해시 엣지=홈 동일). `policy_sha` `cc7946bbec48` = notes HEAD 일치.
  회귀 `/`·`/studio/`·`/drawing/`·`/nexus/`·`/envsync/`·`/healthz` 전부 200. 상세: `relay/tickets/RELAY-62/7-verify.md`
- **미해결 ② 유지**: `100.97.180.0:8766` 실측 `000` 불도달 — nucboxg3 로컬 조치(gmwin) 대기.

---

## 추가 — 09-07 UTC 14:25 `/hub`·`/api/hub/` 라우트 개설 (heav_gmwin_claude_bot)

- **요청**: 매니저(발신 codex_dev_1, 관제 오너) — 관제 허브 현황판 진입 경로 추가. ①지금 `/hub` → 13.125.131.126:8023(임시 8GB)
  ②홈 배치·스위치오버 승인 후 같은 경로를 duradev:8023으로 교체(프록시 대상만 교체, 경로 고정).
- **수행 경로**: gmwin 직접 엣지 SSH는 여전히 불가(ubuntu·root 등 5계정 publickey 거부 재실측) →
  **gmwin → duradev(`smlime21@100.109.91.0`) → 엣지(`ubuntu@43.201.34.144`, duradev `~/.ssh/edge-key.pem`, 09-07 스테이징분)**.
  키는 duradev에서 그대로 사용(복사·반출 없음).
- **변경** (`edge.conf`, 백업: 엣지 `~/nginx-backups/edge.conf.bak-hub-09071425`)
  ① `upstream gwanje_hub_tmp { server 13.125.131.126:8023; keepalive 4; }` 신설 — 주석으로 스위치오버 대상(100.109.91.0:8023) 기록
  ② `location = /hub` — `limit_except GET { deny all; }`(GET 전용) + 경로보존 프록시
  ③ `location /api/hub/` — 경로보존 프록시(현황판 history/status 호출용)
  삽입 위치는 catch-all `location /` 앱 — 기존 라우트 무영향.
- **검증(공인 URL 실측, gmwin에서)**: `/hub` 200(현황판 본문 7.5KB, "관제 허브 — 봇간 메시지 큐") · POST `/hub` 403(GET만 통과) ·
  `/api/hub/status` 401(백엔드 도달·토큰 인증 정상 전달) · 회귀 `/`·`/studio/`·`/drawing/`·`/nexus/`·`/envsync/`·`/healthz` 전부 200.
- **잔여**: 스위치오버(duradev:8023)는 이사님 승인 후 upstream 1행 교체 + reload만이면 됨 — conf에 대상 기록해 둠.
- 정본 반영: `gwanje-hub-rest-queue-v1.md` 진입 경로 상태 갱신.
