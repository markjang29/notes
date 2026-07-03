---
title: "[DRAFT] 매니저 cron key 이관 + 시나리오 봇 그룹 설정 — 시나리오 팀장 비활성 근인 fix"
date: 2026-07-04
status: DRAFT (이사님 07:00 승인 대기)
tags: [ops, cron, scenario, fix]
---

# [DRAFT] 매니저 cron key 이관 + 시나리오 봇 그룹 설정

> 2026-07-04 01:00(KST) 야간 배정 사이클에서 진단. 구조적 cron 변경 = 야간 금지 → 이사님 아침 승인 후 적용.

## 증상
- 시나리오 팀장 `@heav_lnx_scenario_bot` 이 **2026-07-01 12:56 이후 산출 0건**.
- 07-03 01:00 야간 배정(B01 scene/case)도 미이행 → 매니저가 시드1을 폴백으로 완료.
- rpg / trader 팀장은 동일 배정에 정상 응답(WIP 산출 양호).

## 근인 — 매니저 cron이 시나리오 봇 key로 등록됨
매니저 cron 3종이 모두 **시나리오 봇 key(`c6a54f44dab7dfe7`)** 로 등록:
- `432D035D` 01:00 야간 배정
- `3CC484D7` 07:00 아침 브리프
- `E755367D` 08:00 시나리오 리포트

### 증거
- `--cron-list` 시나리오 key → 매니저 cron 3종 모두 표시 / 매니저 본키(`f5c0501a3a7999ad`) → **0건**.
- `bot_settings.json`: 시나리오 봇 `last_sessions` = `8315615299 → /home/ubuntu/.cokacdir/workspace/ndznfeai` (= 본 야간 사이클이 실행 중인 워크스페이스).
- `bot_settings.json`: 시나리오 봇은 그룹 `-5495363819` 의 `as_public_for_group_chat` 항목 **없음**(rpg/trader는 `true`).

### 결과
매니저 사이클이 시나리오 봇의 direct-chat 세션(ndznfeai)에서 실행 → `--message --to heav_lnx_scenario_bot` 가 **자기 자신에게 송신(no-op)**. 시나리오 팀장은 과제를 수신·실행할 독립 세션이 없음 → 07-01 이후 "비활성"으로 관측.

## 제안 fix (승인 후 적용)
1. 시나리오 key(`c6a54f44dab7dfe7`)의 매니저 cron 3종 제거(`--cron-remove`).
2. **매니저 본키(`f5c0501a3a7999ad`, `heav_lnx_bot`)** 로 동일 cron 3종 재등록. 본키 세션 = `akl0hdys`(canonical 매니저 메모리).
3. 시나리오 봇을 그룹 `-5495363819` 에 public 참여: `bot_settings.json` 의 `as_public_for_group_chat["-5495363819"]=true`, `context["-5495363819"]=0`. (BotFather privacy off + 그룹 재초대 필요 가능.)
4. 검증: 차회 01:00 배정 이후 시나리오 팀장 산출(시드2) 발생 확인.

## 리스크 / 롤백
- **리스크:** 재등록 실수 시 07:00 브리프·08:00 리포트 누락 → key 이관 직후 `--cron-list`(본키)로 3종 존재 확인 필수.
- **롤백:** 시나리오 key로 3종 재등록(종전 상태). cron 표현·프롬프트는 변경 없음.

## 비고
- 야간 금지(구조적 cron 변경) → 아침 승인 후 적용. 적용 시점부터 시나리오 팀장 정상 가동 예상.
- 관련: `work-queue.md` 시나리오 섹션 / `org-structure.md` 메시지 프로토콜.
