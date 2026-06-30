---
name: memory-tick
description: 매 대화 턴마다 메모리 저장 가치가 있는 순간을 감지해 조용히 후보(candidate) 메모로 저장. stop-hook-throttle.sh가 일정 경과마다 Stop 훅으로 강제 발화. 텔레그램 reply 후 사용자와 직접 대화한 턴 후 트리거. "기억해/저장해줘" 명시 요청에도 활성화.
---

# memory-tick

> 사용자가 명시적으로 호출할 필요 없음. 빌트인(시스템 프롬프트 자율 판단)과互补 — memory-tick은 **stop 훅으로 강제 발화하는 독립 실행** 장치.

## 목적
세션 구간을 돌아보고 학습 가치가 있는 조각을 **후보(candidate)** 메모로 저장. 승인 전까지 지식이 아니다 (`~/notes/memory/README.md` 상태 모델: 후보 → 승인 → 지식).

## 메모리 저장소
- **쓰기 canonical (목표 / 현재 보류):** Obsidian `~/notes/memory` 일원화가 목표. 단 `autoMemoryDirectory`는 보류(작동 미검증 + 기존 메모리 충돌). 현재는 빌트인 메모리가 기존 경로(`~/.claude/projects/.../memory`)에서 작동.
- **읽기 복구入口:** `~/.claude/projects/.../memory/MEMORY.md` 인덱스 + `~/notes` + `/akl0hdys`

## 트리거 조건
1. `stop-hook-throttle.sh`가 일정 경과 후 Stop 훅으로 찔렀을 때 (강제 발화)
2. 텔레그램 reply 후, 사용자와 직접 대화한 턴 이후
3. "기억해 / 메모리 저장해줘 / 이거 기억해" 명시 요청

## 발화 시 동작
1. 마지막 저장 이후 구간을 돌아봄.
2. **저장 가치 판단** — 반복 패턴(2회 이상 등장) · 결정 · 학습 · 실패 극복 · 1회성 사실은 제외.
3. 가치 있으면 후보로 저장 — 한 사실 한 파일 + `MEMORY.md` 인덱스 한 줄.
4. 이미 있으면 **갱신(overwrite)**, 누적 금지(중복 방지).
5. 미승인 후보는 '검증 대기(candidate)'로 표시.

## 빌트인과의 관계
빌트인 = 시스템 프롬프트 레벨 모델 자율 판단 지침. memory-tick = stop 훅 강제 발화 독립 실행. 목표는 두 경로가 같은 저장소(`~/notes/memory`)로 일원화되는 것. 단 `autoMemoryDirectory`는 현재 보류(미검증 + 충돌)라, 지금은 빌트인 기존 경로 + tick 발화 메시지로 작동. 기억은 모델의 선의에만 맡기지 않는다.
