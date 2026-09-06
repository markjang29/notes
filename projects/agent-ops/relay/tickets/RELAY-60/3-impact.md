# [impact] RELAY-60 — 영향성 검토

## 영향 repo

- `matrix-home`: 8018 홈 UI/API에 `/policies` 추가.
- `notes`: 정책 인덱스, aws-audit 정책 Steward 역할, 홈/홈서버 동기화 기준 추가.

## 영향 서비스

- 8018 홈: 첫 화면 카드 1개, 사이트맵 내부 링크 1개, `/api/policies`와 변경요청 API 추가.
- 홈서버 이관: 같은 Notes checkout과 같은 `POLICY_SHA`를 표시해야 완료로 본다.

## 위험

- 공개 홈에 과도한 원문이 노출될 위험 → 요약·짧은 발췌만 표시.
- 사이트 변경이 Git-first를 우회할 위험 → 변경요청은 `draft_site_intake_not_policy`로만 저장.
- 한쪽 홈만 고쳐 완료 보고할 위험 → 동기화 판정에 8018 legacy와 홈서버 `policy_sha` 일치를 명시.
- 홈서버 SSH 권한 부재 → 감사봇은 Git commit+push와 적용 요청문까지만 수행하고, 권한 보유 actor가 실측한다.

## 판정

조건부 가능. Git-first와 audit forbidden을 유지하고, 홈서버 실적용은 별도 권한 actor의 pull/restart
실측으로 닫아야 한다.

