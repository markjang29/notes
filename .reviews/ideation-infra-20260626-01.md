# 실행·데이터 인프라 조사 — autotrader 아이디에이션 20260626-01

- **역할:** 실행·데이터 인프라 조사원
- **작성일:** 2026-06-26
- **목적:** 2026년 현재 자동매매 실행/데이터 스택 옵션을 조사, 소규모 자본·싱글 서버에서 시작해 확장 가능한 스택 방향을 추출.
- **배제 원칙:** "파이썬 + ccxt + 백트레이더" 같은 뻔한 평균 추천은 지양. 백테스트↔라이브 갭(backtest-live gap)을 각 옵션의 핵심 평가축으로 삼음.
- **사용자 취향 추측 금지.** 데이터 기반으로만 평가. (시장/전략 축은 형제 보고서 `ideation-market-*`, `ideation-strategy-*` 참조)

> 평가 프레임(각 옵션 공통): ① 비용 ② 신뢰성/라이선스 ③ 러닝커브 ④ **백테스트↔라이브 갭** ⑤ 소자본·싱글서버 적합도 ⑥ 확장 한계.

---

## 0. 평가 척도 및 후보 요약

| 축 | 1순위 후보 | 대안 | 비고 |
|---|---|---|---|
| CEX API | 거래소 자체 REST/WS (ccxt 추상화 위) | ccxt 통합, FIX(고용량만) | WS가 시장데이터, REST는 주문. 펀딩/오픈인터레스트 WS 스트림 |
| DEX/온체인 | Solana(Helius/Jito) + EVM L2(Base/Arb) | QuickNode, 자체 RPC | 개인 RPC 운영은 비효율, 관리형 RPC가 기본 |
| 히스토리컬 데이터 | 무료(거래소 덤프) + Tardis(정제 L2) | Kaiko(고가), CoinAPI | 소자본은 거래소 덤프→Parquet가 80%, 정밀 검증에만 유료 |
| 백테스트/라이브 프레임워크 | NautilusTrader(parity 최우선) | vectorbt(빠른 탐색), freqtrade(상세조작) | parity가 핵심 차별점. backtrader는 레거시 |
| 데이터 저장 | Parquet+Arrow(기본) + ClickHouse(필요시) | TimescaleDB, DuckDB | 틱은 Parquet 분할, 쿼리는 ClickHouse/DuckDB |
| 언어/실행 환경 | Python(전략) + Rust 코어(Nautilus) | 순 Rust(고빈도), Go(인프라) | 5-25ms 레이턴시 플로어가 언어 선택의 분기점 |
| 실행 리스크 모델 | TCA(arrival price 벤치마크) + 임팩트 모델 | Almgren-Chriss, 정규화 슬리피지 | 백테스트에 반드시 비용 모델 주입 |

---

## 1. 거래소/프로토콜 API (CEX)

### 1.1 아키텍처 기본 (2026 기준)
- **WS = 마켓데이터, REST = 주문/계정**가 사실상 표준. Bybit는 WS 마켓데이터가 **rate limit에서 제외**되어 풀 스트림 수신에 유리.
- Binance는 WS API에 **CONNECTIONS rate limit**을 신규 도입(기존 RAW REQUESTS 한도 폐지). 연결 수 관리가 새로운 병목.
- OKX v5: 공개 REST는 IP 기반, 프라이빗 REST/WS 로그인은 커넥션 기반. 펀딩레이트/오픈인터레스트 채널 WS 지원.
- **FIX 프로토콜**: Kraken(파생상품 세션 레벨), Coinbase International(키당 1커넥션, 800msg/s, 1000에서 끊김), Deribit(크레딧 시스템). 고용량/저지연 기관용. **소자본·싱글서버에서는 과잉**이며 REST/WS로 충분.

### 1.2 주요 CEX 비교 (현물/선물/펀딩)

| 거래소 | WS 마켓데이터 | 선물/펀딩 WS | rate limit 특성 | 신뢰성 |
|---|---|---|---|---|
| Binance | 풀 L2 depth, trades, markPrice(펀딩) | O | CONNECTIONS 한도 신규, IP/UID 가중치 | 최상, 다만 정책 변경 잦음 |
| Bybit | O, **rate limit 제외** | O(펀딩/오픈인터레스트) | WS 시장데이터 무제한에 가까움 | 상, 파생상품 유동성 강 |
| OKX | O | O | IP(공개)/커넥션(프라이빗) 이중 | 상, 문서 품질 양호 |
| Kraken | O | FIX(파생) | 세션 레벨 | 중상, 과거 아웃티지 이력 |
| Coinbase Int'l | O | FIX | 키당 1커넥션, 800msg/s | 중상, 기관 지향 |
| Deribit | O | 크레딧 | 크레딧 기반 | 상, 옵션/퍼페 중심 |

**소자본 시사점:** Bybit(WS 시장데이터 rate limit 면제) + Binance(유동성) 2개 거래소를 WS로 묶는 것이 비용/대역 효율 최적. 단일 거래소는 거래소 리스크(출금정지/램프업)에 취약.

### 1.3 ccxt vs 자체 SDK

| 기준 | ccxt | 자체(거래소 공식 SDK) |
|---|---|---|
| 진입장벽 | 최저(100+ 거래소 통합) | 거래소별 개별 학습 |
| 거래소 특화 기능(펀딩 곡면/조건부오더) | 추상화 뒤 숨김/누락 | 직접 노출 |
| WS 통합 | 부분(별도 보조 필요) | 공식 스트림 직결 |
| 버전/정책변경 추적 | ccxt 버전 의존 | 거래소 changelog 직접 추적 |
| 라이브 주문 경로 안전성 | 추상층 버그 = 실손실 위험 | 통제 가능 |

- **ccxt**: 프로토타입/멀티거래소 진입장벽 최저. 단점: (a) 추상화가 거래소 특화 기능을 숨김, (b) 버전 호환/정책변경 추적 부담, (c) 라이브 주문 경로에 쓰면 추상층 버그가 실손실로 연결.
- **자체(또는 거래소 공식 SDK)**: 펀딩레이트/베이시스 차익처럼 마이크로구조를 다룰 땐 필수. **ccxt는 "발견/탐색"용, 자체 SDK는 "실행"용**으로 분리하는 패턴이 2026 실무에서 흔함.
- **백테스트↔라이브 갭:** ccxt는 라이브 실행 추상화에 집중(백테스트 자체 미포함). 갭은 별도 프레임워크(Nautilus 등)에서 통제.

### 1.4 API 옵션 평가 카드

| 옵션 | 비용 | 신뢰성 | 라이선스 | 러닝커브 | parity 기여 | 소자본 |
|---|---|---|---|---|---|---|
| REST + WS 직접 | 무료 | 최상(직접 통제) | 해당없음 | 중 | 중(재생 정렬 필요) | 상 |
| ccxt 통합 | 무료(OSS) | 중(추상층) | MIT | 하 | 하 | 상(탐색) |
| FIX(기관) | 거래소별/협상 | 상 | 사설 | 상 | 중 | 하(과잉) |

---

## 2. DEX / 온체인 API

### 2.1 체인별 2026 상황
- **Solana**: 2026년 볼륨이 이더리움을 역전(volume flippening). Alpenglow 업그레이드로 **인스턴트 파이널리티 + 최소 비용** 달성. 고속 온체인 오더북에 이상적. Jupiter/Meteora/Phoenix가 주 DEX/AMM.
- **Ethereum L2 (Base, Arbitrum)**: 메인넷 대비 수수료/속도 우위. Arbitrum은 79+ 파생상품 프로토콜 보유, Base는 멀티체인 아비트라지 스캔 대상으로 편입.
- **Ethereum L1**: 볼륨은 쟁점이나 MEV/가스 비용으로 인해 소자본 직접 실행은 비효율. L2 경유가 기본.

### 2.2 인프라 벤더
- **Helius**(Solana): 관리형 RPC + 강화된 API. Jito(MEV/백런) 연동으로 private mempool 경로 확보. 2026 솔라나 자동매매 사실상 표준.
- **QuickNode**: 멀티체인 RPC, Base/Arbitrum 빌더 가이드 제공.
- **자체 RPC 운영**: 소자본에서는 비효율(인프라 비용·업타임 부담). 관리형 RPC가 기본값.

### 2.3 MEV/아비트라지 현실 (전략 보고서와 교차)
- 전략 보고서(`ideation-strategy`)는 MEV/DEX 아비트라지를 "포화·개인 사실상 불가"로 분류. 인프라 관점에서도 동일: **private mempool·백런·번들러 경쟁**에서 개인이 전문 검색자(searcher)를 이길 인프라 예산 부족.
- 단, **DEX 시장데이터 수집/신호**(유동성 풀 상태, 온체인 지표)는 CEX 전략 보조 신호로 유용 → 실행은 CEX에서 수행하는 하이브리드가 소자본 적합.

### 2.4 DEX 인프라 옵션 평가 카드

| 옵션 | 비용 | 신뢰성 | 러닝커브 | parity 기여 | 소자본 |
|---|---|---|---|---|---|
| Helius(Solana 관리형 RPC+Jito) | 유료 티어(무료 한도) | 상 | 하 | 중(신호용) | 상(솔라나 표준) |
| QuickNode(멀티체인) | 유료 티어 | 상 | 하 | 중 | 상(L2 다수) |
| 자체 RPC 노드 운영 | 인프라비 高 | 중(업타임 부담) | 상 | 중 | 하(비효율) |
| 순 DEX 실행(MEV/백런) | 인프라비 매우 高 | 하(경쟁 패배) | 최상 | — | 불가(소자본) |

**소자본 결론:** DEX는 **신호 수집용**으로 Helius/QuickNode 관리형 RPC 사용, 실행은 CEX. 순 DEX 실행·MEV/백런은 인프라 예산 한계로 배제.

---

## 3. 히스토리컬 마켓데이터

### 3.1 무료 vs 유료 벤더

| 벤더 | 데이터 종류 | 가격대 | 소자본 적합 | 비고 |
|---|---|---|---|---|
| 거래소 공식 덤프(Binance/Bybit/OKX) | 틱/캔들/펀딩/오프북 | 무료 | 최상 | 80% 커버, 정제 직접 필요, 과거 깊이 제한 |
| Tardis.dev | 틱 L2 오더북, 트레이드, 오픈인터레스트, 펀딩, 옵션체인, 청산 | 유료(크레딧) | 중(정밀 검증용) | 가장 정밀, 백테스트 L2 재생에 적합 |
| Kaiko | L1/L2, 거래활동, 유동성 | 고가(기관) | 하 | 기관급, 소자본 과잉 |
| CoinAPI | 통합 REST/WS, 실행품질 지표 | 중~고 | 중 | TCA/슬리피지 측정 가이드 보유 |
| Amberdata/CryptoCompare/CoinGecko | 집계/인덱스 | 중 | 중 | 보조/검증용 |

- **시장 규모**: 크립토 API 시장 2025년 $1.1B → 2026년 말 $1.3B 예상(CAGR 22.2%). 벤더 경쟁 심화로 무료 티어/크레딧 모델 확산.
- **소자본 전략**: 거래소 직접 덤프 → Parquet 분할 저장이 기본(비용 0). Tardis는 **전략 정밀 검증 단계에서만** 크레딧 구매로 L2 재생. Kaiko/CoinAPI 고가티어는 보류.

### 3.2 라이브 데이터
- 라이브 마켓데이터는 거래소 WS 직접 수신이 기본(벤더 경유 불필요, 지연·비용 추가). 다만 다중 거래소 집계/정규화가 필요하면 CoinAPI 같은 정규화 계층이 편의 제공.

### 3.3 데이터 옵션 평가 카드

| 옵션 | 비용 | 신뢰성 | 러닝커브 | parity 기여 | 소자본 |
|---|---|---|---|---|---|
| 거래소 공식 덤프 → Parquet | 무료 | 최상(원시) | 하(정제 직접) | 상(원시 L2 재생) | 최상(기본값) |
| Tardis.dev(틱 L2/펀딩/옵션/청산) | 유료 크레딧 | 최상(정제) | 중 | 상(정밀 재생) | 중(검증 단계만) |
| CoinAPI(정규화/TCA) | 중~고 | 상 | 하 | 중 | 중(편의/집계) |
| Kaiko(기관 L1/L2) | 고가 | 최상 | 중 | 상 | 하(과잉) |
| CoinGecko/CryptoCompare(집계) | 중 | 중 | 하 | 하 | 중(보조) |

### 3.4 데이터 비용 전략 (소자본)
- **80% 커버**: 거래소 덤프(무료) → Parquet 분할 → DuckDB 쿼리. 비용 0으로 히스토리컬 캔들/트레이드/펀딩 확보.
- **정밀 검증(20%)**: 전략이 마이크로구조 의존(L2 오더북, 청산, 옵션)이면 Tardis 크레딧으로 정밀 재생. Kaiko/CoinAPI 고가티어는 자본/엣지가 정당화되기 전 보류.
- **라이브**: 거래소 WS 직접 수신(비용 0, 최저지연). 벤더 정규화 계층은 다중 거래소 집계 필요 시만.

---

## 4. 백테스팅/라이브 프레임워크

> **핵심 평가축 = 백테스트↔라이브 갭(parity).** 같은 전략 코드가 백테스트와 라이브에서 동작하는 정도가 알파 신뢰도를 결정.

### 4.1 후보 비교

| 프레임워크 | 언어 | parity(백테↔라이브) | 속도 | 러닝커브 | 라이선스 | 소자본 적합 |
|---|---|---|---|---|---|---|
| **NautilusTrader** | Python API + Rust 코어 | **최상(설계 목표)** | 고(Rust) | 중상 | LGPL(오픈) | 상 |
| vectorbt / vectorbt PRO | Python(NumPy 벡터) | 하(라이브 미흡, 탐색용) | 최고(벡터) | 중 | OSS + PRO 유료 | 상(탐색) |
| freqtrade | Python | 중(자체 백테↔라이브) | 중 | 중 | GPL | 상(상세조작/텔레그램) |
| hummingbot | Python/Cython | 중(마켓메이킹/아비特化) | 중 | 중상 | OSS | 중(MM/아비 한정) |
| backtrader | Python | 중 | 저(레거시) | 중 | GPL | 중(유지보수 의문) |
| HftBacktest | Rust(+Python) | 중상(레이턴시/큐 모델) | 고 | 상 | OSS | 중(고빈도 특화) |
| 자체 구축 | 임의 | — (직접 통제, 단 부담) | 임의 | 최상 | — | 하(초기) |

### 4.2 NautilusTrader — parity의 핵심
- **Rust 네이티브 코어 + Python 전략 API**: 성능은 Rust, 접근성은 Python.
- **결정론적 백테스팅**: 같은 전략 코드가 히스토리컬 데이터와 라이브 양쪽에서 동작(backtest-live parity)이 **명시적 설계 목표**. 이것이 다른 프레임워크 대비 가장 강한 차별점.
- 멀티자산·멀티베뉴, 바이낸스/바이빗 통합 가이드 존재("Setting Up NautilusTrader for Binance Futures").
- **비용/라이선스**: 오픈소스(LGPL). 러닝커브는 중상이나 parity 효과가 학습 비용을 상회.
- **소자본 시사점**: parity가 알파 신뢰도(과적합/룩어헤드 의심)를 직접 낮추므로, 단일 프레임워크로 백테→페이퍼→라이브를 일관되게 통과하려면 사실상 유일한 강력한 선택지.

#### NautilusTrader 평가 카드

| 기준 | 평가 |
|---|---|
| 비용 | 무료(LGPL 오픈소스) |
| 신뢰성 | 상(프로덕션 등급, Rust 코어) |
| 러닝커브 | 중상(이벤트기반 패러다임, 데이터 카탈로그 학습) |
| parity(백테↔라이브) | **최상 — 설계 목표** |
| 소자본 적합 | 상(싱글서버로 시작, Rust 코어로 지연 회피) |
| 확장 한계 | 고빈도/MM 극단 지역은 순 Rust/C++ 대비 한계; 대부분 소자본 전략엔 충분 |
| 주의 | 문서가 방대하나 학습 곡선 존재, 거래소 어댑터 버전 호환 추적 필요 |

### 4.3 vectorbt / freqtrade 포지셔닝
- **vectorbt(PRO)**: 파라미터 스윕/아이디어 빠른 탐색에 최적. 단, 라이브 실행 미흡 → **탐색 단계 전용**, parity 통제는 Nautilus로 이관하는 2단계 파이프라인이 효율적.
- **freqtrade**: 크립토 특화, 텔레그램 제어, 자체 백테↔라이브 일관성 보유. 단순 전략(스캘핑/그리드 변형)엔 실용적이나 마이크로구조 모델링(펀딩 곡면, L2 임팩트)에는 한계.
- **hummingbot**: 마켓메이킹/아비트라지 특화. 해당 전략 클래스면 1순위, 그 외엔 과잉.

### 4.4 백테스트↔라이브 갭 — 일반적 함정 (인프라 관점)
- 백테스트에 **비용(수수료/슬리피지/펀딩/임팩트)가 주입되지 않으면** 라이브 진입 시 수익이 허구로 붕괴. → 섹션 5(실행 리스크 모델) 참조.
- WS 스트림 vs REST 폴링의 **데이터 시점 차이**: 백테스트 재생 데이터의 타임스탬프 해상도가 라이브와 안 맞으면 신호 왜곡.
- **조건부오더/타임인포스** 차이: 백테스트에선 항상 체결 가정, 라이브에선 거부/부분체결/타임아웃 발생. parity 높은 프레임워크만 이를 시뮬레이션.
- **데이터스누핑/룩어헤드**: 리스크·검증 보고서(형제)와 교차. 인프라 측에선 재생 엔진이 미래 픽스를 방지해야 함.
- **펀딩/오픈인터레스트 시점**: 펀딩 carry 전략에서 펀딩 타임스탬프가 신호 시점과 정렬 안 되면 허구 수익. WS 펀딩 스트림과 백테 재생의 정렬이 parity의 숨은 병목.
- **재시결/네트워크 실패**: 라이브에선 주문 재시도/네트워크 장애가 빈번. 백테스트가 이를 무시하면 라이브 실측이 하회.

#### 2026 관찰 — "백테스트는 천장, 라이브는 진실"
- 라이브에선 "깨끗한 과거 진입가가 존재하지 않을 수 있음" — 결정 시점과 체결 시점 사이 가격 이동이 백테에 누락. 2026-06 Medium 분석("The Backtest Is the Ceiling")은 백테를 보장이 아닌 **필터**로 보아야 한다고 강조.
- **Event Stream Processing**가 갭 축소 방안으로 거론됨(Wakett) — 라이브와 동일한 이벤트 스트림을 백테 재생에 사용(Nautilus의 이벤트기반 아키텍처가 이 패러다임 구현).
- 백테에 비용·룩어헤드·과적합 누락 시 라이브 실측이 체계적 하회 — 인프라 관점에선 비용 모델 주입 + parity 엔진이 2대 축.

### 4.5 프레임워크 parity 비교 카드 (핵심 차별점)

| 프레임워크 | 같은 코드 백테↔라이브 | 비용 모델 주입 | L2 재생 | 부분체결/거부 시뮬 | 결론 |
|---|---|---|---|---|---|
| NautilusTrader | **O(설계 목표)** | O | O | O | parity 1위 |
| HftBacktest | 부분(레이턴시/큐 강) | O | O | 부분 | 고빈도 특화 parity 강 |
| freqtrade | O(자체) | 부분 | X | 부분 | 단순 전략용 무난 |
| vectorbt(PRO) | X(라이브 미흡) | 부분 | X | X | 탐색 전용, parity 낮음 |
| hummingbot | 부분(MM/아비 한정) | O | 부분 | 부분 | 해당 전략 클래스만 |
| backtrader | 부분 | 부분 | X | 부분 | 레거시, 권장 안 함 |
| 자체 구축 | 직접 통제(부담) | 직접 | 직접 | 직접 | 초기 비용 최고 |

**parity 우선순위:** NautilusTrader > HftBacktest(고빈도) > freqtrade(단순) > 기타. parity가 알파 신뢰도의 근간이므로 프레임워크 선택 = parity 선택.

---

## 5. 실행 리스크 모델링 (지연·슬리피지·수수료·임팩트)

### 5.1 핵심 개념 구분
- **가격 임팩트(price impact)**: 유동성 소비로 시장을 움직여 발생하는 비용.
- **슬리피지(slippage)**: 더 넓은 개념, "즉시성의 비용(cost of immediacy)" — 도착가(arrival price) 대비 실제 체결가 차이.
- **TCA(트랜잭션 비용 분석)**: arrival price를 벤치마크로 한 체계적 슬리피지 측정(Talos 등 제공).

### 5.2 2026 연구 발견 (임계 수치)
- **레이턴시 차익의 손익분기점: 5-25ms** (변동성 체제에 따라). 이 구간 이하로 지연을 줄여야 latency arbitrage가 지불. → 소자본·싱글서버에서는 **이 영역을 노리는 HFT 전략은 불가능**(인프라 비용이 자본 초과).
- **언어별 tick-to-trade 실측**: Python ~12ms(스파이크 80ms) vs Rust ~40µs(~300x 빠름). Python 스파이크(80ms)가 이미 레이턴시 차익 플로어(5-25ms)를 넘어섬 → Python 순수 전략은 레이턴시 차익 불가, Rust/Nautilus 코어로만 진입 가능. 단 중빈도 전략(펀딩 carry/페어/이벤트)은 Python 지연이 엣지를 잡아먹지 않으므로 Python 그대로.
- **AgenticAITA PoC**: 크립토 퍼페추얼 유동성에 보정된 임팩트 계수 모델 제시(2026). Almgren-Chriss류 정규화 임팩트 모델을 백테스트에 주입 가능.
- **임팩트 계수 보정**: 크립토 퍼페 특화. 대형 주문이 슬리피지로 비용을 크게 키움 → 백테스트에 반드시 모델링.

### 5.3 인프라 결론 (언어 선택 분기점)
- 5-25ms 플로어가 **언어 선택의 자연스러운 분기점**:
  - **Python** 전략(지연 수십~수백 ms)은 레이턴시 차익이 아닌 **중빈도/구조적 전략**(펀딩 carry, 페어, 이벤트)에 적합. 여기선 Python이 충분.
  - **Rust/Go/C++** 는 레이턴시 병목이 실제 전략 엣지일 때만(고빈도/MM). 소자본은 보통 해당 안 됨.
- **소자본 권장**: Python 전략 + Rust 코어(Nautilus) 하이브리드. 순 Rust 전환은 자본/엣지가 레이턴시에 의존하게 될 때로 연기.

### 5.4 비용 모델 적용 체크리스트 (백테스트 주입)
- [ ] **수수료**: 메이커/테이커 차등, 거래소/티어별 정확 값 (Binance VIP/Bybit 등급).
- [ ] **슬리피지**: 테이커 주문 시 오더북 소비량 기반 선형/제곱근 임팩트.
- [ ] **임팩트**: Almgren-Chriss 또는 퍼페 임팩트 계수(AgenticAITA PoC 참조)로 보정.
- [ ] **펀딩**: 퍼페 포지션 펀딩 지불/수취 시점·금액 정확 반영 (carry 전략 생사).
- [ ] **지연 모델**: 주문 제출→체결 간 네트워크/매칭 지연 (Nautilus/HftBacktest에서 큐 모델).
- [ ] **거부/부분체결**: 라이브처럼 거절·부분체결·타임아웃 확률 주입.
- [ ] **arrival price TCA**: 벤치마크로 실측 슬리피지 측정/비교 가능해야 함.

> 비용 모델 1개라도 누락 시 백테 수익이 허구. parity가 높은 프레임워크(Nautilus)만 이 통제를 엔진 수준에서 제공.

---

## 6. 실행 환경 (클라우드/엣지, 언어)

### 6.1 언어 매트릭스 + 정량 레이턴시 (2026 실측)

| 언어 | tick-to-trade 레이턴시(실측) | 역할 | 장점 | 단점 | 소자본 포지션 |
|---|---|---|---|---|---|
| **Python** | ~12ms 평균, 스파이크 80ms | 전략·연구·오케스트레이션 | 생태계(ccxt/pandas), 빠른 프로토타입 | GIL, GC 일시정지, 지연·스파이크 | 기본 전략 언어 |
| **Rust** | ~40µs (마이크로초, ~300x 빠름) | 고성능 코어(Nautilus/HftBacktest) | 지연·메모리 안전, GC 없음, C++급 속도 | 러닝커브 가파름, 정량 생태계 작음 | Nautilus 코어로 우회 사용 |
| **Go** | (중간, 미공개) | 인프라/데이터 파이프라인 | 동시성(goroutine), 배포 단순 | 정량 생태계 빈약 | 데이터 수집기/글루 용도 |
| **C++** | 최저(극저지연 HFT 표준) | 극저지연 HFT | 최고 성능, 하드웨어 제어 | 복잡도, 수동 메모리, 유지비 | 소자본 비권장 |

> **핵심 수치(Python vs Rust, 동일 전략)**: 평균 tick-to-trade **12ms → 40µs** (~300x). 스파이크는 **80ms → 수µs**. — 한 HFT 개발자 사례: Python에서 레이턴시 스파이크가 실제 손실을 유발해 Rust로 전환. "시장이 움직일 때 봇이 '생각하느라 멈출 수 없다'".

#### 2026 언어 결정 매트릭스 (언제 전환하는가)
- **Python으로 시작**: 전략 프로토타입, 백테스트, 데이터 분석, 중빈도(지연 수십~수백 ms 허용). Python 3.14(2026) No-GIL로 멀티스레드 성능 개선, Rust 기반 툴링(uv) 통합로 생태계 강화.
- **Rust로 전환하는 조건**: 지연이 실제 엣지일 때(레이턴시 차익 5-25ms 플로어 이하), 중대형 시스템, 메모리 안전 필수. 2026 Rust 전문가 연봉 $400K — 성능 크리티컬 시스템에서 수요 급증.
- **Go**: 성능+생산성 균형, 마이크로서비스 아키텍처, 단순 동시성 모델 원할 때. 인프라/데이터 글루에 적합.
- **C++**: 팀에 강력한 전문성 있거나 초저지연(<10µs) 필수일 때만. 레거시 통합.
- **하이브리드가 2026 실무 표준**: Python(전략 개발) + Rust/C++(실행 엔진) — Nautilus가 이 패턴을 내재화.
- **Python 3.14(2026) No-GIL**: 멀티스레드 성능 개선으로 일부 병렬 워크로드(파라미터 스윕, 멀티심볼)에서 순수 Python 성능 향상. 단, 핵심 실행 경로 지연 개선은 아니므로 Rust 코어 필요성은 유지.

### 6.2 실행 환경 — 호스팅 옵션 비교 (2026)

| 호스팅 | 월비(소자본 기준) | 지연특성 | 적합 전략 | 비고 |
|---|---|---|---|---|
| **클라우드 EC2/Compute**(현재 홈) | $50-300 (범용 인스턴스) | 중(가상화 오버헤드, 노이지네이버) | 중빈도, 연구, 페이퍼 | 유연성 최고, 스케일 쉬움 |
| **베어메탈 전용 서버** | AWS 대비 **50-80% 저렴** (동급) | 상(전용 하드웨어, 예측가능) | 중~중고빈도 | 비용/성능 비 최고, 스케일 탄력성 낮음 |
| **거래소 colocation VPS**(도쿄/싱가포르) | $50-200+ | 최상(거래소 랙 인접) | HFT/MM, 지역 민감 | 지연 한 자릿수 ms, 자본/엣지 정당화 시만 |
| **온프렘/코로케이션** | CapEx + 회선비 | 최상(통제) | HFT/기관 | 소자본 과잉, 운영 부담 |
| **하이브리드**(연구=클라우드, 실행=베어메탈/colo) | 혼합 | 부분 최적 | 확장 단계 | Phase 2-3 이관 패턴 |

#### 호스팅 결정 (소자본)
- **Phase 1 (현재)**: 단일 EC2/베어메탈 범용 서버. 중빈도 전략(펀딩 carry, 페어, 이벤트)은 가상화 지연이 엣지를 잡아먹지 않음 — Python 전략 레이턴시(수십 ms)가 호스팅 지연(수 ms)을 지배.
- **Phase 2 (지연 의존 판명 시)**: 베어메탈 전용 서버로 이관(비용 절감 50-80% + 지연 예측성). 또는 거래소 리전 colocation VPS(도쿄/ap-northeast가 Binance/Bybit 아시아 엔드포인트에 근접).
- **Phase 3 (HFT/MM)**: 거래소 colocation 랙 + Rust 코어. 자본/엣지가 인프라 비용($수백~/월)을 정당화할 때만.
- **베어메탈 vs 클라우드 함정**: 벤치마크상 베어메탈이 AWS/Azure/GCP 대비 월비 50-80% 절감 + 동급 성능이나, 탄력적 스케일·관리 편의는 클라우드 우위. 트레이딩은 보통 정상 부하(스파이크 예측 가능)라 베어메탈 비용 우위가 실제로 큼.

### 6.3 장애 내성 (싱글 서버 SPOF 완화)
단일 서버는 단일 장애점(SPOF). 봇이 단절 시 포지션이 방치되면 손실이 무한히 확대되므로 장애 내성은 선택이 아닌 필수. 최소:
- (a) **systemd 자동재시작** + 헬스체크(전략 프로세스, WS 연결, 포지션 동기화).
- (b) **상태/포지션 DB 영속화**(PostgreSQL ACID) — 재시작 후 포지션 복구 필수(미복구 = 중복 주문/노출).
- (c) **킬스위치**(리스크 보고서 `ideation-risk` §4.5와 교차) — 최대드로다운/일일손실한도/연결단절 시 자동 청산·주문 취소.
- (d) **WS 재연결/구독 복구** 로직 — 거래소 WS 끊김 시 구독 복원 + 갭 감지(누락 틱).
- (e) **시계 동기화**(NTP/chrony) — 타임스탬프 정렬이 parity·감사의 기반.

---

## 7. 데이터 저장 (Parquet/Arrow/ClickHouse)

### 7.1 옵션 비교 (2026)

| 저장 | 용도 | 압축 | 쿼리 | 소자본 적합 |
|---|---|---|---|---|
| **Parquet + Arrow** | 틱/캔들 원시 아카이브 | LZ4/ZSTD | DuckDB/Polars 온디맨드 | 기본값(비용 0) |
| **DuckDB** | 임베디드 분석 쿼리 | — | SQL, 단일 바이너리 | 상(탐색) |
| **ClickHouse** | 대규모 틱 컬럼형 저장/쿼리 | LZ4/ZSTD | 고속 집계 | 중(규모 커지면) |
| **TimescaleDB** | 시계열(PostgreSQL) | 90%+ columnstore | SQL | 중(Postgres 친화) |
| **PostgreSQL** | 포지션/주문/메타(OLTP) | — | 트랜잭션 | 상(상태 저장) |

### 7.2 추천 패턴 (소자본·싱글서버)
1. **마켓데이터(틱/캔들/L2)**: Parquet 분할(거래소/심볼/일자 파티션)로 객체 저장. Arrow 포맷으로 메모리 적재. 비용 0, 선형 확장.
2. **분석 쿼리**: DuckDB(임베디드, Parquet 직접 쿼리)로 시작 → 틱 볼륨이 수 TB 넘으면 ClickHouse로 이관.
3. **상태(포지션/오더/잔고/리스크)**: PostgreSQL(ACID, 장애 복구). TimescaleDB는 Postgres 위에 올라가 중복 회피 가능.
4. **백테스트 재생**: Parquet → Arrow 스트림 → Nautilus 데이터 카탈로그. ClickHouse와 Parquet 상호운용(`clickhouse local`)로 Lakehouse 패턴 지원.

### 7.3 백테스트↔라이브 갭 (저장 관점)
- 재생 엔진이 Parquet 타임스탬프를 라이브 WS 시점과 동일 해상도로 정렬해야 parity 유지.
- L2 오더북 스냅샷 갱신 주기(백테) vs WS 스트림(라이브) 불일치가 전형적 갭 원인. Nautilus 데이터 카탈로그는 이 정렬을 통제.

---

## 8. 종합: 소자본·싱글서버 → 확장 스택

### 8.1 핵심 텐션 (평균 추천 회피)
- "Python + ccxt + backtrader"는 진입은 쉬우나 **parity/비용모델/마이크로구조 통제가 약해** 알파 신뢰도가 낮아짐.
- 반대로 순 Rust 자체 구축은 parity/지연은 최고이나 **러닝커브·유지비가 소자본을 압도**.
- **2026 최적점**: Python 전략 API + Rust 코어(NautilusTrader), 거래소 직접 WS, Parquet/DuckDB 저장, 비용 모델 주입. 이 조합이 parity·비용·확장성의 균형.

### 8.2 확장 경로 (단계별)
- **Phase 1 (소자본·싱글서버)**: Python + NautilusTrader + 거래소 WS(Binance/Bybit) + Parquet/DuckDB + PostgreSQL 상태. 무료 데이터(거래소 덤프). 단일 전략, 페이퍼→라이브.
- **Phase 2 (검증 심화)**: Tardis 크레딧으로 L2 정밀 재생, 비용 모델(임팩트 계수) 주입, Walk-forward/몬테카를로(리스크 보고서).
- **Phase 3 (규모 확대)**: 다중 거래소/체인, ClickHouse 틱 저장, 자본/엣지가 레이턴시 의존으로 판명되면 Rust/colocation 전환.

---

## 9. 추천 스택 방향 3개 (한 줄씩)

1. **parity 우선 (권장)**: Python + NautilusTrader(Rust 코어) + Binance/Bybit WS 직접 + Parquet/DuckDB + PostgreSQL, 거래소 무료 덤프로 시작.
2. **탐색 속도 우선**: Python + vectorbt PRO(빠른 스윕) → 후보 전략을 Nautilus로 이관해 parity 검증; 데이터는 Parquet/Tardis(정밀 단계).
3. **DEX/온체인 하이브리드**: Python 전략(CEX 실행) + Helius/Jito(Solana 데이터 신호) + CoinAPI 정규화; 순 DEX 실행(MEV/백런)은 소자본 불가하므로 신호만 온체인.

> **공통 기반**: 어느 방향이든 백테스트에 비용 모델(수수료/슬리피지/임팩트/펀딩) 주입 + 단일 서버 장애 내성(systemd/상태 DB/킬스위치/NTP)은 최소 전제. parity 없는 백테스트는 허구이고, SPOF 봇은 단절 시 무한 손실 노출.

---

## 출처

### 거래소 API / FIX
- OKX API 가이드: https://www.okx.com/docs-v5/en/
- Binance API 개발자 문서 (WS CONNECTIONS limit): https://developers.binance.com/
- Bybit API (WS 시장데이터 rate limit 제외): https://bybit.com
- Kraken FIX API (세션 레벨): https://docs.kraken.com
- Coinbase International Exchange FIX (키당 1커넥션, 800msg/s): https://international.coinbase.com
- Deribit 크레딧 시스템: https://docs.deribit.com
- Delta Exchange (500 ops/s): https://docs.delta.exchange

### 마켓데이터 벤더
- Tardis.dev (틱 L2/펀딩/옵션/청산): https://tardis.dev/
- Kaiko (L1/L2, 기관): https://www.kaiko.com/
- CoinAPI (execution quality/TCA): https://www.coinapi.io/blog/execution-quality-in-crypto
- Amberdata / CryptoCompare / CoinGecko (집계·인덱스)
- 크립토 API 시장 규모 2025 $1.1B → 2026 $1.3B (CAGR 22.2%)

### DEX / 온체인
- Helius (Solana RPC/Jito): https://www.helius.dev/
- QuickNode (멀티체인 RPC, Arbitrum/Base): https://www.quicknode.com/
- Solana Alpenglow 업그레이드(인스턴트 파이널리티), 2026 볼륨 flippening
- Jupiter / Meteora / Phoenix (Solana DEX/AMM)
- Aster DEX (멀티체인 퍼페): https://thegrid.id/discovery/productType/decentralised-exchange

### 백테스팅/라이브 프레임워크
- NautilusTrader (Rust 코어 + Python, backtest-live parity): https://nautilustrader.io/ , https://github.com/nautechsystems/nautilus_trader
- "Setting Up NautilusTrader for Binance Futures" 가이드
- vectorbt / vectorbt PRO: https://vectorbt.dev/
- freqtrade (백테↔라이브 일관성, 텔레그램): https://www.freqtrade.io/en/stable/backtesting/
- hummingbot (MM/아비트라지 특화)
- HftBacktest (Rust, 레이턴시/큐 모델): https://hftbacktest.readthedocs.io/
- backtrader (레거시)
- "Python Backtesting Landscape 2026" (vectorbt PRO/Nautilus/Zipline/Backtesting.py/Backtrader): https://python.financial/
- "Python Paper Trading Frameworks Compared (2026)": https://gist.github.com/rmbell09-lang/01281551ac4672bd5d1a42bb58575144
- "Best Tools for Backtesting Crypto 2026": https://kiploks.com/research/best-tools-for-backtesting-crypto-trading-strategies-in-2026

### 실행 리스크 모델링
- CoinAPI — Execution Quality in Crypto (슬리피지/유동성/임팩트): https://www.coinapi.io/blog/execution-quality-in-crypto
- "The Mathematics of Slippage: When Latency Arbitrage Stops Paying" (5-25ms 손익분기): https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=6661618
- AgenticAITA — Execution Cost Modeling & Slippage (퍼페 임팩트 계수): https://arxiv.org/html/2605.12532
- Talos — TCA Benchmarks (arrival price): https://www.talos.com/insights/execution-insights-through-transaction-cost-analysis-tca-benchmarks-and-slippage
- Reddit r/rust — "Rust for HFT and Backtesting" (Nautilus Python 바인딩 접근성): https://www.reddit.com/r/rust/comments/1esus4t/
- "The Backtest Is the Ceiling. Live Trading Is the Truth" (2026-06, 라이브 진입가 비현실성): https://medium.com/@NFS303/the-backtest-is-the-ceiling-live-trading-is-the-truth-cffef1e49cd0
- PineConnector — "Backtesting vs Live Trading: Bridging the Gap": https://www.pineconnector.com/blogs/pico-blog/backtesting-vs-live-trading-bridging-the-gap-between-strategy-and-reality
- Wakett — "Backtesting vs Real-Time Trading: Why There's A Discrepancy" (Event Stream Processing 해법): https://wakett.com/the-wakett-blog/backtesting-vs-real-time-trading-why-theres-a-discrepancy-and-how-to-fix-it

### 언어/실행 환경
- "I Love Python, But It Was Costing Me Money: Why I Switched to Rust for HFT" (Python ~12ms / Rust ~40µs 실측, 300x): https://medium.com/@frankdotdev/i-love-python-but-it-was-costing-me-money-why-i-switched-to-rust-for-high-frequency-trading-15c095d2b136
- Servers.com — "Hosting Trading Infrastructure? Cloud vs Bare Metal vs Hybrid": https://www.servers.com/blog/when-it-comes-to-hosting-trading-should-you-choose-dedicated-servers-or-the-cloud
- BlastVPS — "Dedicated Server vs Cloud: Why Bare Metal Still Wins" (베어메탈 50-80% 비용 절감 벤치마크): https://blastvps.com/blog/cheap-dedicated-server-guide
- Reddit r/sysadmin — 베어메탈 vs 클라우드 비용 의견: https://www.reddit.com/r/sysadmin/comments/p0nbjv/why_are_comparison_to_the_cloud_rarely_mention/
- Cycle.io — "On-Prem vs Colocation vs Bare Metal Cloud": https://cycle.io/learn/on-prem-vs-colo-vs-bare-metal-cloud

### DEX/온체인 (보강)
- QuickNode Swap API (Jupiter 봇 빌드 가이드): https://www.quicknode.com/swap-api
- QuickNode Marketplace — 0x Swap API (이더리움 DEX aggregation): https://marketplace.quicknode.com/add-on/0x-swap-api
- Dysnix — "Top 9 Solana RPC Node Providers in 2026": https://dysnix.com/blog/solana-node-providers

### 데이터 저장
- ClickHouse + Parquet (Lakehouse): https://clickhouse.com/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics
- Arrow → Parquet 변환 (`clickhouse local`): https://clickhouse.com/resources/engineering/convert-arrow-to-parquet
- "Best Time-Series Databases Compared 2026" (TimescaleDB columnstore 90%+ 압축, ClickHouse LZ4/ZSTD): https://www.tigerdata.com/learn/the-best-time-series-databases-compared
- ClickHouse vs TimescaleDB 2026: https://www.tinybird.co/blog/clickhouse-vs-timescaledb
- PostgreSQL vs TimescaleDB vs ClickHouse 2026 성능: https://sanj.dev/post/postgresql-timescaledb-clickhouse-comparison/
- 컬럼 저장 포맷(Parquet/ORC/Arrow): https://clickhouse.com/resources/engineering/columnar-storage-formats

### 형제 보고서 (교차 참조)
- 시장·자산 엣지: `ideation-market-20260626-01.md`
- 전략 클래스: `ideation-strategy-20260626-01.md`
