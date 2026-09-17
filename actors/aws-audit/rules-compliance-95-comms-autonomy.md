---
actor: aws-audit
subject: 95_ 사칙 — 통신 선문의·속도 자율 (95-comms-autonomy)
date: 2026-09-17
type: rules-ack-evidence
tags:
  - actors
  - aws-audit
  - rules-ack
  - 95
---

# 95_ 사칙 — aws-audit 읽음 증거 (rules-ack)

> 사칙 95_ 원문: `principles/95-comms-autonomy-rules-v1.md` (정본 — 이 파일은 요약·참조본)
> gwanje-ack-protocol.md 계약: ACK = 이해의 서명. 아래 요약으로 사칙 판본을 이해했음을 증명.

## 요약 (내 지침 반영)

- **95-1 (95-comms-first)**: 봇간 통신 실패 시 → 이사님 수동 부탁 전에 **통신담당 봇에게 먼저**
  시도·막힌 지점을 문의. (통신담당 미지정 — 매니저 배정 대기. 현재는 8023 허브에 문의)
- **95-2 (95-speed-autonomy)**: A봇→B봇 시도기록은 **통신봇 경유**로 공유·해소. 이사님 수동
  전달은 임시. 나(aws-audit)의 시도기록도 8023 허브 큐로 남긴다.
- **95-3 (95-org-speed)**: 감사 검토가 이사님 개인 전달 속도에 좌우되지 않게, 검증은
  자기 흐름대로 병행하고 관문(이사님)은 예외 통로로만 쓴다.
- **95-4 (95-report-addr)**: 마지막 텔레그램 메시지 하단에 **담당 사이트 주소**를 함께 답장.
  내 담당: 8024 감사·검증 화면 — http://43.201.34.144:8024/rules
- **95-5 (95-plain-report)**: 완료·진행 보고의 **첫 줄에 전문용어 없는 쉬운 요약 1~2줄**.
  봇 보고는 대부분 끝까지 안 읽혀진다 — 본문을 안 읽어도 윗줄만 보면 무슨 일인지 알아야 함.
  (ELI5 비유와 별개. 구성: 쉬운요약 → 본문 → 담당사이트주소)

## 참조

- 정본: principles/95-comms-autonomy-rules-v1.md (v2, 09-17 95-4 포함)
- 상위: principles/entrypoint-comms-progress-rules-v1.md · principles/gwanje-ack-protocol.md
- 8024 투영: /rules (정본은 notes Git — 이 화면은 읽기전용 게시판)
