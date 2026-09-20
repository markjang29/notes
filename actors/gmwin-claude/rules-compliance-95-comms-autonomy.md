---
actor: gmwin-claude
subject: 95_ 사칙 — 통신 선문의·속도 자율 (95-comms-autonomy)
date: 2026-09-20
type: rules-ack-evidence
tags:
  - actors
  - gmwin-claude
  - rules-ack
  - 95
---

# 95_ 사칙 — gmwin-claude 읽음 증거 (rules-ack)

> 사칙 95_ 원문: `principles/95-comms-autonomy-rules-v1.md` (정본 v3 — 이 파일은 요약·참조본)
> 아래 요약으로 사칭 판본(sha 834d9f8e22eecfc8306cf11e0920c4d9b9ba7bf9e12e52006ca942c814bd5ed0)을 이해했음을 증명한다.
> actor: gmwin-claude = heav_gmwin_claude_bot (99_[GM 윈도][인사] 클로드, 텔레그램 봇 99)

## 요약 (내 지침 반영)

- **95-1 (95-comms-first)**: 봇간 통신 실패 시 → 이사님 수동 부탁 전에 통신담당 봇(8023 허브 창구)에 "어떻게 시도했고 어디서 막혔는지" 먼저 문의. (09-15 RELAY-66 중계 부탁 사건의 재발 방지 조항 — 본 봇이 반례 당사자)
- **95-2 (95-speed-autonomy)**: 시도기록은 허브 큐·관제방 로그로 공유·해소. 수동 전달은 임시방편.
- **95-3 (95-org-speed)**: 검토·승인이 이사님 개인 전달 속도에 좌우되지 않게 자기 흐름대로 병행 진행. 관문(이사님)은 예외 통로.
- **95-4 (95-report-addr)**: 모든 마지막 텔레그램 메시지 하단에 **담당 사이트 주소** 필수.
  내 담당: 인사 명단 원장 — http://43.201.34.144/insa/ · 공지 ACK 보드 — http://43.201.34.144/insa/ack
- **95-5 (95-plain-report)**: 완료·진행 보고 첫 줄(또는 마지막 줄)에 전문용어 없는 쉬운 요약 1~2줄 필수.
  구성: ①쉬운 요약 → ②본문(상세·증거) → ③담당 사이트 주소(95-4).
- **95-4-a**: 담당 주소 원장 `projects/agent-ops/report-addresses.json`에 자기 행 등록 (주소 변경은 원장+정본 커밋으로만).

## 이행 상태 (2026-09-20 등록 시점)

- 허브 ACK: heav_lnx_audit_bot에게 type=ack "확인완료하였습니다" 발송 (09-20, key ack-95-comms-autonomy-v2-gmwin-claude)
- 계기: 09-17 공지(95-4)를 허브 공지 채널에서 즉시 수령하지 못함 → 이사님 09-20 지적. 재발 방지로 멘션 감시에 허브 공지 신규 확인을 병행토록 감시 도구 확장.

## 참조

- 정본: principles/95-comms-autonomy-rules-v1.md (v3, 95-4·95-5·95-4-a 포함, sha 834d9f8e22eecfc8306cf11e0920c4d9b9ba7bf9e12e52006ca942c814bd5ed0)
- ACK 원장: projects/agent-ops/rules-acks/rules-acks-v1.ndjson (본 파일 sha로 5행 등록)
- 8024 투영: http://43.201.34.144:8024/rules (notes Git 정본의 읽기전용 게시판)
