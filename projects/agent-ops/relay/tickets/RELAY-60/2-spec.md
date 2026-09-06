# [spec] RELAY-60 — 사칙·정책 센터

## 인수조건

1. 8018 홈 첫 화면과 사이트맵에서 `/policies`로 이동할 수 있다.
2. `/api/policies`가 Notes 정책 인덱스, Notes HEAD, `POLICY_SHA`, 문서별 ref·상태·요약을 반환한다.
3. 공개 화면은 원칙 요약과 짧은 발췌만 보여주며, 비밀·토큰·세션 값을 노출하지 않는다.
4. 변경요청 API는 승인 토큰 없이는 401로 실패한다.
5. 접수된 변경요청의 상태는 초안이며, Notes commit+push 전까지 정책 정본이 아니라고 표시한다.
6. 홈서버 이관 문서에 동기화 기준과 실패 조건을 남긴다.

## 테스트

- `python -m py_compile main.py`
- Flask test client로 `/policies`, `/api/policies`, `/api/policies/change-request` 401 확인
- `/api/policies` 응답의 `policy_sha`가 Notes HEAD와 일치하는지 확인

