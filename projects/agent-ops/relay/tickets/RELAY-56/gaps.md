# RELAY-56 gaps — Jira 404·정보 불일치 기록 (2026-08-26, 감사 정정 3cc92eb 반영)

## Jira 상세 API 404 (완료 처리 금지 — 복구 시 역동기화)
- RELAY-35, RELAY-41, RELAY-50, RELAY-54, RELAY-55, RELAY-56 — 상세 조회 404.
- `port-registry.json`에 일부가 실재 검증된 것처럼 기재되어 있으나 현재 API로 확인 불가.

## Notes ticket folder 공백
- RELAY-35, RELAY-50, RELAY-55, RELAY-56 — `origin/main` 기준 산출물 없음.
  (RELAY-56은 이번 커밋으로 1-req.md·gaps.md 추가. 5-impl은 구현 후 별도 커밋.)
- RELAY-54는 44건 요약 파일만 존재.

## 미구현 (이번 1순위~3순위 범위 밖 — 후순위)
- 8016 img2img 시드(RELAY-55), NAI 모듈 자산 선택·교체 UI(프롬프트 JSON에 extractor는 기록됨),
  마스터 자산번호 전사이트 관통 연결, 기존 채팅 기록 재실사(에코 데이터 대체).
