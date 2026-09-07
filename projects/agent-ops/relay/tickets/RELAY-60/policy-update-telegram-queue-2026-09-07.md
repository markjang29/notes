# [policy-update] RELAY-60 — Telegram 큐 수신·응답 사칙 편입

- 출처: 이사님 2026-09-07 Telegram 직접 지시
- 지시 요지: "`큐시작`~`큐끝` 긴 입력 수신 규칙을 사칙으로 추가 관리"

## 반영

- `principles/telegram-queue-protocol.md` 신설
- `policy-index-v1.json`에 `telegram-queue` 등록
- `new-bot-onboarding.md` 일하는 규칙에 큐 사칙 요약 추가
- `aws-audit-policy-steward.md` 담당 업무에 대화 사칙 관리 추가

## 핵심 규칙

`큐시작` 이후 `큐끝` 전까지는 답변·실행하지 않고 수신만 한다. `큐끝` 뒤에는 긴 출력은 파일 또는
분할 메시지로 내고, Telegram 표 대신 목록/웹/이미지/파일을 우선하며 끝에 ELI5를 붙인다.

