# [design] Matrix Studio 통합 서비스 (RELAY-58 2-design, 2026-08-28)

이사님 승인 ("네 진행하세요"). 기존 12포트 서비스는 유지(읽기 병행), 신규 개발로 통합.

## 스택 (검토 확정)
- 프론트: Next.js(React) — 넷플릭스식 열 + 쇼핑몰식 바구니 사이드바 + 아케이드식 4슬롯 장비 프리뷰
- 백엔드: FastAPI — 기존 파이썬 자산 파이프라인 승계
- DB: MongoDB(자산·채팅) + Postgres(이력·승인 관계链) + Redis(큐)
- 배포: Docker Compose(프론트/ api/ workers/ db/ nginx) → 필요시 k8s
- 큐: Redis + RQ — 실사 러너·NAI 생성·창고 정리 워커 흡수

## 관통 ID 체인 (핵심 설계)
basket_set → loadout_apply → unit_run → approval_card → release
하나의 set_id가 바구니→장착→유닛테스트→승인카드→릴리스를 관통 (감사 지적 해소).

## MVP 단계
1. MVP: matrix-studio 셸 + 자산 브라우저(몽고 직접 읽기) + 바구니 상태변화 시 자동 재검사 (검사버튼 불필요)
2. 흡수: 워커 큐화 → 기존 8015/8018 기능 이전(기존은 읽기전용 병행)
3. 매트릭스: 엔진 컨테이너

## 포트
8021 (matrix-studio v0 셸) — 디버그 ID 접두사 MS.
