# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`)가 관리. 활성 작업 · 대기 결정 · 다음 스텝. 산출물 마무리/새 작업 시 갱신.
> 최근 갱신: 2026-06-26 (온보딩 + 아이디에이션 v1 세션)

## 활성 작업

### 아이디에이션 v1 — 사용자 1차 리뷰 완료 (2026-06-26)
- **RPG** — `/home/ubuntu/projects/rpg_game/IDEATION.md` + `ideation/{01-research,02-mechanics,03-themes,04-genrehybrid}.md`. 파일 전달 완료.
- **trader** — `/home/ubuntu/projects/autotrader/IDEATION.md` + `notes/.reviews/ideation-{market,strategy,infra,risk}-20260626-01.md`. 파일 전달 완료.
- **상태:** v1 산출 완료 → 사용자 1차 피드백 수령 → v2 대기.

### 사용자 피드백 (v1 → v2 방향) ★
- *"기술적인 분석에만 너무 치우쳤다. 아이디어가 실체화된 건 피부에 와닿지 않는다."*
- **v2 과제:** 분류/분석 프레임(taxonomy) 축소 → **구체·체감적 인스턴스**. "말하지 말고 보여주기(show, don't tell)":
  - RPG: 플레이어가 한 판에서 실제로 겪는 체험 시나리오, 구체적 장면·컷, 손에 잡히는 컨셉.
  - trader: 전략이 실제로 굴러가는 구체 예시 거래·숫자·시나리오, "이렇게 돈 번다"가 보이는 한 판.
- **원칙:** 기술 분석은 뒷받침으로 뒤로. 아이디어의 "실체(체감)"가 앞에.
- **후속:** 이 기준은 반복 적용 가치 → 사용자 승인 시 `personas/markjang29.md` §10(리뷰 판정 기준) 승격 제안 (현재는 검증 대기).

## 대기 결정 (스택·엔진 — ADR 대기)
- RPG 엔진: Godot? Unity? 웹? — 아이디에이션 컨셉 수렴 후 ADR.
- trader 스택: Python + NautilusTrader(parity)? — v2 이후 ADR.
- 팀장 사칙 인증: v1은 미인증 '초안(발판 아님)'이라 허용. 결정·코드·commit 전엔 인증 필수.

## 다음 스텝 (사용자 재개 시)
1. v1 검토 방향 사용자 지정 → v2 아이디에이션 지시 (체감 우선, 기술 분석 최소화).
2. 팀장 사칙 인증 완료 여부 확정.
3. 쿼터/검색 장애 대응 프로토콜 적용 → `decisions/2026-06-26-quota-checkpoint-resume.md`.

## 세션 노트 (2026-06-26)
- 온보딩: 매니저 사칙 인증 완료. 팀장 2명 `/start` → 각 repo(rpg_game·autotrader) workspace 바인딩 확인.
- 핸들 오류 수정: 문서상 `@heav_lnx_rpg` 등 → 실제 `_bot` 접미사 핸들로 바로잡음 (commit `bc4d04b`).
- 아이디에이션 v1 산출(양 팀장) → 사용자 전달 → 피드백(실체화 부족).
- 이슈: 팀장들 병렬 검색 과다 → search API busy(MCP -429)/서버 과부하(529) 반복. → ADR로 대응 프로토콜 마련.
