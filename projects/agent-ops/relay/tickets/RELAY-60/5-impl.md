# [impl] RELAY-60 — 8018 사칙·정책 센터

## 산출 커밋

- `matrix-home`: `4aa38cd6230d691fe5cce23a1224abe735a7c210`
- `notes`: 본 RELAY-60 정본 커밋

## 구현 내용

1. 8018 홈 첫 화면에 `📜 사칙·정책` 카드 추가.
2. 사이트맵 내부 페이지에 `/policies` 링크 추가.
3. `/api/policies` 추가:
   - Notes 정책 인덱스
   - Notes HEAD
   - `POLICY_SHA`
   - 문서별 `notes:<ref>`, 상태, owner, ELI5, 요약, 짧은 발췌
4. `/policies` 추가:
   - 정책 묶음 카드형 표시
   - Git-first 안내
   - 변경요청 초안 폼
5. `/api/policies/change-request` 추가:
   - 승인 토큰 없으면 401
   - 접수 상태는 `draft_site_intake_not_policy`
   - Notes commit+push 전까지 정본이 아니라고 응답
6. 8025 봇 대시보드도 8018 사이트맵에 등록.

## 테스트

- `python -m py_compile main.py` 통과
- Flask test client:
  - `/policies` 200
  - `/api/policies` 200
  - `/api/policies`의 `policy_sha == notes HEAD`
  - `/api/policies/change-request` 무토큰 POST 401
- `policy-index-v1.json` JSON 문법 검사 통과

## 남은 적용

- 현재 감사봇은 홈서버 SSH public key 인증이 없어 홈서버 pull/restart 실측을 직접 닫지 못했다.
- 홈서버 권한 actor가 `matrix-home`과 `notes`를 최신 main으로 동기화한 뒤 `/api/policies`의
  `policy_sha` 일치를 확인해야 이관 동기화 완료다.

