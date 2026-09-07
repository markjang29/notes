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
