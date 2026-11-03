# QA 측정 베이스라인 1차 (measure-only) — 2026-11-03

> GOV#29 [QA-0] QA-3 1단계. 도구: `scripts/qa-measure.py`(pytest-cov + radon, ~/.venvs/novelweb).
> 단계: measure-only 1주(11-03~11-10) → 경보 → 강제. 본 기록은 측정값만 — 판정 아님.

## 측정 결과 (1차)

| 대상 | 커버리지 | 복잡도 C 이하 | 비고 |
|---|---|---|---|
| services/taiga-bridge | 17% (dispatcher 위주 테스트 3건 기준) | 0건 (전 구역 A/B) | 첫 측정. 미달 수치는 경보 대상 아님(measure-only) |

- 게이트 목표: 커버리지 80%+ · radon grade C 이하 경보 (강제는 3단계부터)
- 재측정: 감사봇 정기 턴에 `qa-measure.py <대상> <테스트...>` 실행·본 파일 표에 추가
