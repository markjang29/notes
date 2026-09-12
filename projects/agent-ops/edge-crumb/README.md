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
