---
title: ADR — autotrader 백테스트 엔진 스택
date: 2026-06-26
status: 결정 (이사님 번복 가능)
tags:
  - adr
  - autotrader
  - stack
---

# ADR: autotrader 백테스트 엔진 스택

> 트리거: 이사님 지시 "로직 명확히 → 한 종목 백테스트 프로그램 개발부터 착수". 스택 미확정 상태에서 코드 착수 전 결정 기록(agent-rules: "결정(ADR) 없이 발판 안 친다").

## 결정
- 백테스트 엔진 = **Python 3.12 + pandas (경량 자체 구현)**.
- parity/라이브 전환 = **NautilusTrader** (후순위 · 전략 확정 후).

## 선택 이유
- 이사님 "한 종목씩 백테스트 프로그램부터" = **빠른 검증 우선**.
- pandas 경량: 셋업/학습 비용 최소 → 이사님 빠른 피드백(체감 우선 원칙).
- 전략이 검증 중(하이브리드)인 단계에서 NautilusTrader 정석 세팅은 과투자.

## 버린 대안
- **NautilusTrader 즉시 채택** — parity 정석(v1 §4 원칙)이나 학습곡선·셋업 비용 큼. 검증 단계엔 과함.
- **vectorbt** — 탐색 전용(v1 §4 분류). 유사하나 자체 구현이 로직 제어·디버깅에 유리.
- **backtrader** — 레거시, 유지보수 미흡.

## 당시 제약
- 환경: pandas/numpy 미설치 → venv(`/home/ubuntu/.venvs/autotrader`) 신규 구성.
- **데이터 소스 불확실 (1차 리스크)**: Yahoo 429(rate limit), stooq JS PoW 막힘 → yfinance 테스트 중.
- 인터넷 rate limit 이력(MCP-429/529) 반복 가능.

## 트레이드오프
- 경량 선택 = **parity 재작업 비용(기술부채)**. 단, 빠른 검증·이사님 피드백 우선.
- 자체 엔진 = look-ahead 등 검증 버그 부담 → 첫 백테스트 후 Buy&Hold 교차검증으로 방어.

## 검증 기준
- 엔진 정합성: Buy&Hold 결과를 엔진이 정확 재현하는지.
- 전략 가치: 순수 DCA vs 하이브리드 비교 → 레짔필터 추가 가치 측정.

## 실패·복구
- 데이터 소스 전 차단 시 → **합성(synthetic) 데이터로 엔진 로직 먼저 검증**, 실데이터는 이사님 보고 후 대안(Alpha Vantage key 등) 협의.

## 후속 재검토 조건
- 전략 확정 + 라이브 전환 결정 → NautilusTrader parity 재작업 ADR.
- 단일 종목 범위 → 다자산/포트폴리오 확장 시 프레임워크 재평가.

## 산출물 포인터
- 전략 스펙: `/home/ubuntu/projects/autotrader/strategy-spec-v1.md`
- 엔진 코드(예정): `/home/ubuntu/projects/autotrader/backtest/`
