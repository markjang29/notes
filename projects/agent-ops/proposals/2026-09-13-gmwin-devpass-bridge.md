---
title: gmwin devpass 1:1 브리지 — 등록 요청 정본 (제안)
date: 2026-09-13
status: 제안 (director 승인 전 — 기존 문서 병합 시 같이 검토)
author: devpass-code @ gmwin WSL (TUI 세션)
tags:
  - agent-ops
  - proposal
  - telegram
  - bridge
---

# gmwin devpass 1:1 브리지 — 등록 요청

ELI5: 이사님 전용 초인종 봇 하나를 gmwin에 달았습니다. 기존 누구와도 번호가 겹치지 않아(신규 봇) 409 충돌이 없고, 관제 방·허브에는 참여하지 않는 **1:1 전용**입니다.

## 1. 무엇인가

- **봇**: `@heav_gmwin_devpass_bot` (telegram id 8976499851, 이사님이 09-13 BotFather 신규 생성 — 기존 봇과 토큰 충돌 0)
- **엔진**: gmwin WSL의 `devpass-code`(Node, 저장소 `/mnt/c/duradev_wslhome`) — `run --format json` + `-s`(세션 연속 = 대화 기억)
- **브리지**: `~/telegram-bridge/bridge.py` + systemd 사용자 유닛 **`devpass-telegram.service`**(enabled, 5초 재시작) — TG long-poll → 엔진 → 3900자 분할 송신, 409 백오프
- **규칙 준수**: 답 끝 🧒 ELI5 · 표 금지(목록형) · `큐시작/큐끝` 수신 · `/new`(기억 초기화) · `/status` · 절대금지 3(토큰 미게시, 무단삭제 금지, push 전 repo 확인)

## 2. 위상 (정체 혼동 방지 — 조직의 만성 병)

| 구분 | 이 브리지 | cokacdir(claude/codex) | zcode | 관제 방 |
|---|---|---|---|---|
| 통로 | TG 1:1 | TG 1:1·그룹 | TG 1:1(자체 소비) | 8023 |
| 참여 | ✗(1:1 전용) | ✓ | ✗ | — |
| 세션 | state.json 1개 연속 | cokacdir 관리 | ZCode 관리 | workspaces |

- 이 봇의 답은 **관제 정본이 아니라 이사님 1:1 실무 대화**다. 결론이 정본이 되려면 notes/허브 경유(기존 Git-first 사칙 동일).
- 기계 내 이중 기동 금지(같은 토큰 2중 폴링 = TG 409). ZCode의 TG 소비 방식과 충돌 나지 않게 신규 봇으로 분리한 이유.

## 3. 구축 중 실측·인시던트 (재발 방지 기록)

1. 구 AWS 주소(13.125.131.126:8023) 참조로 gmwin 폴러 2기·asset-agent·gmlnx 폴러 단절 → 09-13 복구(100.109.91.0 / 127.0.0.1 교체, .bak-20260913).
2. 브리지 1차 버그: sendMessage GET+문자열 조합에 개행 미인코딩 → 5회 재시도 후 유실 → POST+urlencode로 수정. 유실 답변은 세션 Export(`devpass-code export`)로 복구·재전송.
3. 일시 오류 "Upstream stream terminated unexpectedly before completion"(llm-gateway↔GLM 구간) 2회 — 재시도로 회복. 재시프트 정책: 브리지는 실패 시 신규 세션 1회 재시도.

## 4. 등록 요청 (director 결정 필요)

- `actors.json`에 신규 actor 등록(제안: actor_id `gmwin-devpass`, kind agent, location gmwin-wsl, transport telegram 1:1, capabilities report/repo_read, jira RELAY). 셀프등록 하지 않고 본 문서로만 요청.
- 회의방 명부·허브 토큰 등록 여부: 1:1 전용이므로 **미등록 유지 제안**(필요 시 이후).
- 본 제안은 F1~F4(2026-09-12 리뷰)와 함께 일괄 검토 권장.

## 5. 근거

- 운영 증적: TG 세션 `ses_f69ad1d7cffe...`(16 메시지, `[HANDOFF-RECEIVED]` 접수 완료 09-13 14:40), 로그 `~/telegram-bridge/bridge.log`
- 기계측 인수인계: `C:\duradev_wslhome\HANDOFF-2026-09-13-devpass-telegram.md` + `AGENTS.md`(이 디렉토리 진입 세션 자동 상속)
