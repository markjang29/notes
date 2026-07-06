# 야간 자율 배정 — 2026-07-06 01:00 KST

> 07:00 아침 브리프용 취합 자료. 매니저(heav_lnx_bot) 작성. **야간 자율 처리 — 이사님께 직접 보고 X (07:00 브리프에서 통합).**
> 세션: cron `2D8F5150` (매니저 본키, 단일 실행). 컨텍스트 시작 3.7%.

## 사칙 상속 확인
- L1 onboarding.md 읽음, L2 work-queue.md 읽음.
- 정체: 매니저 `@heav_lnx_bot` (key `f5c0501a3a7999ad`, 유일 매니저 키).
- 야간 자율 범주 준수: 리서치/draft/설계 ONLY, WIP 팀당 2건 한도, commit/push/전략채택/ADR/외부송신/실거래 금지(아침 승인 필수).

## 배정 전 repo 상태 (모두 clean ★)
어제(07-05) "감사브리프(보존)" 커밋들로 codex 감사(07-04) 지적 미추적 산출물이 일괄 커밋됨 → 3 repo 전부 working tree clean. 이전 야간 WIP 마무리 상태.

| repo | 최근 커밋 | 상태 | 비고 |
|---|---|---|---|
| rpg_game | `ddbc02d` 보존: WIP 보스전 구현설계 2건 | clean | 07-05 야간 WIP 흡수 완료 |
| autotrader | `e20e9f5` 보존: 미추적 산출물 일괄 | clean | codex 지적 전량 커밋 |
| scenario | `c6f272c` tools: risupreset 변형 역변환 | clean | 07-05 이후 신규 2건 (사칙 역할 4 진행) |
| notes | `1971107` docs: 감사봇 직접 처리 원칙 | M .reviews/session-reaper.log만 (자동로그) | 정상 |

## 3팀장 배정 (07-06 01:03, 모두 status:ok)

### RPG (`msg_...68923145`)
1. **"한 판 체험" 플레이스루 시나리오 draft** — 첫 보스전 turn-by-turn 구체 장면. 참모 추론→지휘관 결정→패막 손맛 흐름. show-don't-tell(체감 우선).
2. **Reasoning-Parry 전투 루프 상태머신 설계(Godot)** — reasoning.gd·grid_parry 연결, 턴 진행·상태전이. 설계만.

### autotrader (`msg_...bd33f5d8`)
1. **비중 슬라이드 전략 설계 draft** — 07-02 리서치(exit=0 압도) 후보 (a). 파라미터(base/k/cap/슬라이드함수) + 예시 거래 숫자표. 구현 금지.
2. **Oracle 설치 방식 리서치 메모** — Docker vs 직접 트레이드오프. 매니저 대기 결정(`work-queue` "남은 결정") 지원용.

### scenario (`msg_...0f218930`)
1. **RISU 자산 기반 독자적 창작 draft** — first-boss 보류 피드백 근본 대응. catalog(602점) 자산 선정·조합, PROVENANCE 의무. 의뢰서 풀어쓰기 금지.
2. **tools 발췌 파이프라인 계속 개선** — 사칙 역할 4. 단 v2 scenario-generator 구현은 컨펌 후.
- ★ 컨펌 게이트: DESIGN v2 컨펌 대기(4점) → v2 구현 착수 금지.

## 07:00 아침 브리프 안건 (예정)
1. 3팀장 야간 결과 취합 (show-don't-tell 산물 중심).
2. **대기 결정(이사님 승인 안건):**
   - autotrader 비중 슬라이드 전략 채택 여부 (draft 검토 후)
   - Oracle 설치 방식(Docker vs 직접) — 팀장 리서치 메모 기반
   - scenario DESIGN v2 컨펌(4점) — 여전히 대기
   - RPG 전투 루프 상태머신 설계 ADR화 여부
3. **recovery gate DISABLED 지속** — codex 감사(07-04) "경고" 지적. 07-05 체크포인트에서도 미해결. 이사님 확인 필요 안건으로 재상신 예정.

## 사칙 준수 자가 점검
- ✅ 매니저 = 기획·배분·보고만. 실행은 팀장.
- ✅ 야간 자율 범주(리서치/draft/설계) 엄수. commit/push/전략채택/ADR/외부송신/실거래 전부 아침 승인 게이트로 봉쇄.
- ✅ WIP 팀당 2건 한도 준수.
- ✅ show-don't-tell(체감 우선) — 3팀 전부 구체 장면/숫자/창작 산물 지시.
- ✅ 자기 팀만, 매니저 영역·ops 팀장 금지 명시.
- ✅ KST 기준.
- ✅ 시나리오 컨펌 게이트 준수(v2 구현 봉쇄).
