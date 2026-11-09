---
actor: awslnx-novel-col
subject: DL-20261110-01 사칙 — 업무 위임 루프·공통 합류 읽음 증거
date: 2026-11-10
type: rules-ack-evidence
tags:
  - actors
  - awslnx-novel-col
  - rules-ack
  - delegation-loop
  - DL-20261110-01
---

# DL-20261110-01 — awslnx-novel-col 읽음 증거 (rules-ack)

> actor: awslnx-novel-col = heav_lnx_novel_col_bot (01_[GM윈도] 클로드 소설수집, 텔레그램 봇 01)
> 사칙 정본: `principles/delegation-loop.md` + 합류 절차 `projects/agent-ops/enrollment/README.md`
> 실제 읽은 commit: **89ff476** (notes main, 이사님 공지 URL과 일치 확인)
> 수신 시각: 2026-11-10 01:07 KST (이사님 방 공통지시 [DL-20261110-01])

## 요약 (내 지침 반영 — 요약으로 이해했음을 증명한다)

1. 캠페인은 기존 작업 중단 없이 현재 단위 완료 뒤 적용. 수신·선행작업은 로컬 보존.
2. 실행 계약: 작업=목표·원지시·구성요소·담당·완료증거 연결, 매뉴얼 Git 경로·버전 남김,
   입력확인→기존도구실행→증거검사→원인수정→재검증→제출 순서, blocked 정직 보존,
   최소수정·근거기록, 완료보고 4요소(결과·증거·미완료·다음), 구현자 단독 검수 완료 금지.
3. 합류: 읽은 commit 기록 → 부팅 문서/역할 카드에 정본 경로 참조 추가(전체 교체 금지) →
   신원·소속·장비·역할·현재작업·매뉴얼 참조 매니저 등록 → 매니저 응답+왕복 근거 있어야 연결확인.
   자기 채팅 ACK·송신 성공만으로 연결됐다고 보고하지 않는다.
4. 운영 경계: 승인된 통신·Git 권한만 사용, 비밀값·사설 경로 공개 Git 금지, 권한 자동 확대 금지.

## 실행 기록 (2026-11-10 01:07-01:10 KST)

| 항목 | 값 |
|---|---|
| 등록 요청 경로 | 8024 comm `bot.msg.heav_lnx_novel_col_bot.heav_lnx_bot` (type progress) |
| comm 메시지 id | 1794240583530-85 (brokered:true, fanout:1) |
| request_id (안정, 재시도 동일) | nvc-dl01-8f3a |
| 읽은 규칙 commit | 89ff476 (delegation-loop.md + enrollment/README.md) |
| 현재 상태 | **연결대기** — 매니저 왕복 확인(확인값 반환) 대기 |
| 선행 규칙 | telegram-comm-protocol-v1.md@2b0f4dc · L0-agent-common.md §6 · gwanje-ack-protocol.md |
| 부수 정리 | 미확인 방송 1793748455822-64(11-03, 비당사) 관제 7필드 ACK — bot.ack id 1794240610162-87 |

## 다음 세션 지속 적용 (부팅 참조)

- 부팅마다 이 파일과 `principles/delegation-loop.md` **최신 commit 대조** — 변경 시 재독·ACK 갱신.
- DL-20261110-01 미종결 시: 매니저 회신(확인값) → 동일 request_id nvc-dl01-8f3a로 반환 →
  매니저 최종 확인 근거 확보 뒤에만 이사님 방에 `연결확인` 보고.
- 등록 내용 정정 필요 시 매니저에게 재등록 요청(같은 request_id).
