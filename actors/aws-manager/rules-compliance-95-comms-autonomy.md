---
actor: aws-manager
subject: 95_ 사칙 — 통신 선문의·속도 자율 (95-comms-autonomy)
date: 2026-09-17
type: rules-ack-evidence
tags:
  - actors
  - aws-manager
  - rules-ack
  - 95
---

# 95_ 사칙 — aws-manager 읽음 증거 (rules-ack)

> 사칙 95_ 원문: `principles/95-comms-autonomy-rules-v1.md` (정본 — 이 파일은 요약·참조본)
> 아래 요약으로 사칭 판본(sha 7b90c33e)을 이해했음을 증명한다.

## 요약 (내 지침 반영)

- **95-1 (95-comms-first)**: 봇간 통신 실패 시 → 이사님 수동 부탁 전에 통신담당 봇(현재 8023 허브)에 먼저 시도·막힌 지점 문의.
- **95-2 (95-speed-autonomy)**: 시도기록은 허브 큐로 공유·해소. 나(aws-manager)의 시도기록도 8023 허브에 남긴다.
- **95-3 (95-org-speed)**: 검토·승인이 이사님 개인 전달 속도에 좌우되지 않게 자기 흐름대로 병행, 관문(이사님)은 예외 통로로만.
- **95-4 (95-report-addr)**: 마지막 텔레그램 메시지 하단에 **담당 사이트 주소**를 함께 답장.
  내 담당: 관제 허브 현황판 — http://43.201.34.144/hub · 진행 관찰 — http://43.201.34.144:8024/rules

## 참조

- 정본: principles/95-comms-autonomy-rules-v1.md (v2, 09-17 95-4 포함, sha 7b90c33e)
- 8024 투영: /rules (notes Git 정본의 읽기전용 게시판)
