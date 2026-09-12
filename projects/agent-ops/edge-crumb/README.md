# edge-crumb v1 (2026-09-12, GM윈도)
이사님 지시: 전 페이지 상단에 홈→카테고리→사이트 트리경로(링크) + 기술스택·고유ID 표기.
감사 결과 26개 사이트 중 자체 표기 보유는 8018뿐, 고유 ID는 전무 → 엣지 nginx http-level
sub_filter 중앙 주입으로 즉시 전면 적용.

- matrix-crumb.conf: map "$server_port::$uri" → 사이트별 (site-id·implemented-with 메타 + 브레드크럼바)
- gen_crumb_conf.py: 8024 포털 카탈로그(sites.json)에서 conf 생성
- 적용 대상: 포트 18개(8003~8100) + :80 경로(/arcade/ /drawing/ /drawing2/ /insa/ /studio/ 등)
- 제외: 8024 홈 자체, 8018(자체 배너), :80 루트·/open·/sites·/tests(자체 표기/스프링 UI)
- 컨벤션 정렬: heav_aws512 소스 레벨 메타(site-id · implemented-with)와 동일 키 사용
- 부수 정리: socat 8027(pid 57068) 제거 — nginx listen 8027과 충돌해 reload가 전부 실패하던 블로커 해소
  (9/7부터 모든 nginx reload가 묵살되고 있었음)
- 롤백: 엣지 /etc/nginx git repo (79d2e00 = baseline+v1)
- 미해결: 8004 카드 site-id 값(port vs arcade-8004) 통일은 v2 과제, 소스 레벨 확산은 heav_aws512와 협업

## v1.2 (2026-09-13, GM윈도)
- 소스 자체표기 전수 순회(tailscale 직접) 반영: 8023 메타만(소스 정적 트리바 존중), 8009 엣지 개입 제외(소스 메타+바 완전 자체표기), 8004·8021·8100 바만(소스 의미론al ID 메타 위임 — arcade-8004·studio-8021·envsync-8100, SID_OVERRIDE로 바 표기도 정합), 8024 포털 홈 메타 보강(portal-8024)
- 파뱃윈도 6debe42의 :80 경로 7건(/nexus/ /envsync/ /home/ /hub /tests /readcheck /skills) 미채택 — 각 경로 소스 레벨 완전 자체표기 실측(home-8018·nexus-8030·envsync-8100·tests/readcheck/skills-8024·hub-8023) → 엣지 추가 시 이중 바·이중 메타
- duradev_hub upstream 8026→8023 정정: 8026은 nai-queue 별개 서비스(토큰 게이트 401) — /hub·/api/hub·/api/notices 오지칭 해소, 엣지 /hub 200 HTML 확보
- 교훈: 엣지 conf 직접 수정은 다음 재생성 시 덮어쳐진다 — 반드시 본 생성기+정본 경유. 병행 액터 수정분은 reflog에서 복구해 생성기에 정책 반영 후 통합
