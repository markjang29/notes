# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`) 전관. 활성 작업·대기 결정·다음 스텝만 유지한다.
> 과거 상세는 Git 이력, `work-archive.md`, checkpoints를 본다.

## 최상위 원칙

- 이사님 최종 결정.
- 팀장은 자기 산출물만. 통합·우선순위·ops는 매니저 전관.
- 중요한 `.md`/ADR/checkpoint/work-queue 변경은 Git 보존 후 세션 클리어.
- 긴 문서 전체 재독 금지. 필요한 부분만 읽는다.

## 활성 작업

### 1. 시나리오팀 — RISU 기반 창작 체계

- 사칙: `principles/scenario-team-purpose.md`
- 존재 이유: RISU 자산 기반 창작 스튜디오. 창작은 자유, 디벨롭은 이사님 컨펌 후.
- 현재 쟁점:
  - scenario-generator v5 재설계 흐름 확인
  - RisuAI 실제 데이터 구조 이해 부족 보완
  - 컨펌 없는 구현/디벨롭 방지
- 다음:
  - 시나리오팀 자기 정체 재인증
  - `scenario-team-purpose.md` 기준 작업 재정렬
  - 큰 소스 읽기는 요약/파일분리

### 2. RPG — Reasoning-Parry / Godot

- 엔진: Godot 확정.
- 시그니처: 참모 추론 × 지휘관 결정 × 패막 손맛.
- 다음:
  - 시나리오팀 산출이 RPG 요구와 맞는지 클라이언트 관점 검토.

### 3. autotrader — 백테스트/대시보드

- 스택: FastAPI + 기존 pandas 백테스트 + Oracle 23ai.
- 대시보드: Streamlit 8002 + 80.
- 포트 정정:
  - 8003 = 시나리오팀 scenario-generator backend
  - autotrader REST API는 미기동/포트 미확정
- 다음:
  - autotrader REST API 포트/소유 재정리 필요 시 ADR 갱신.

### 4. 매니저/감사/복구

- 감사봇: Codex 감사 봇 1개. Claude 매니저/팀장 감시.
- 일일 감사: `9AE18D26` 매일 09:10.
- ctx-evac:
  - Stop 훅 JSON 오탐 수정 완료
  - 실제 `API Error: context window limit`는 별도 장애로 취급
- recovery-gate:
  - L1 문구 명확화 완료
  - L0 도입 후 L0 + current-work-state 주입으로 단순화 예정

## 대기 결정

1. 대청소 후 recovery gate L0 적용 범위 확정.
2. recovery-gate `DISABLE` 제거 여부.
3. `.reviews/session-reaper.log` 커밋/무시 정책.
4. scenario-generator 방향 컨펌 여부.

## 세션 클리어 전 체크

```bash
git -C ~/notes status --short
git -C ~/projects/scenario status --short
git -C ~/projects/rpg_game status --short
git -C ~/projects/autotrader status --short
```

필요 시:

```bash
python3 ~/scripts/export-chat-backup.py --latest --out /tmp/chat-backup.md
```

