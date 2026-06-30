# 전략 클래스 조사 — autotrader 아이디에이션 20260626-01

- **역할:** 전략 클래스 조사원
- **작성일:** 2026-06-26
- **목적:** 2026년 현재 덜 붐비는 정량 전략 카테고리를 조사, 소규모 자본(개인/소규모 펀드)에서 구현 가능한 후보 추출.
- **배제 원칙:** RSI/볼린저 밴드 단타, 단순 그리드, 순방향 모멘텀, 단순 SMA 교차 등 뻔한 전략은 후보에서 제외.
- **사용자 취향 추측 금지.** 데이터 기반으로만 평가.

> 평가 프레임(각 전략 공통): ① 2026 알파 소진 정도 ② 구현 난이도 ③ 추정 샤프/수읥률대 ④ 자본 효율(레버리지/마진) ⑤ 구조적 하드함(실행/리스크) ⑥ 왜 아직 붐비지 않는지.

---

## 0. 평가 척도 및 후보 요약

| 전략 | 알파 잔존 | 구현난이도 | 추정 샤프 | 소자본 적합 | 비고 |
|---|---|---|---|---|---|
| 펀딩레이트/베이스 차익(carry) | 중상 | 중 | 1.5~3 | 중(자본집약) | 수익률은 낮지만 안정적, 자본회전율이 병목 |
| 통계차익(페어/코인테그레이션) | 중상 | 중상 | 1.0~2.0 | 중상 | 코인테그레이션 붕괴 리스크가 핵심 과제 |
| 시장중립 롱-숏(베헤지) | 중 | 중상 | 0.8~1.5 | 상 | 베타 안정성·청산 리스크 관리가 관건 |
| 온체인/대체데이터 정성→정량 | 상(비효율) | 중 | 불규칙(0.5~2.5) | 상 | 신호 발굴이 전부, 데이터 인프라가 모 |
| MEV/DEX 아비트라지 | 하(포화) | 최상 | 높으나 변동 | 하 | 인프라 경쟁 패배, 개인 사실상 불가 |
| 변동성·변동성패턴 거래 | 중상 | 상 | 1.5~2.5 | 중(옵션 필요) | Deribit 옵션 접근 필요, 갭 리스크 |
| 이벤트/발표 기반 | 중 | 중 | 변동 큼 | 상 | 드문 기회, 실행(슬리피지/거부)이 병목 |
| 기간구조/커브 거래 | 중상 | 중상 | 1.0~2.0 | 중 | CME/Deribit 만기 구조 활용, 자본 묶임 |

---

## 1. 펀딩레이트 / 베이스 차익 (Carry / Cash-and-Carry)

### 개요
현물 롱 + 선물(또는 퍼페추얼) 숏을 동시에 들어 방향 중립을 유지하고, 펀딩레이트(퍼페) 또는 베이시스(만기선물) 프리미엄을 수취하는 델타중립 전략. 크립토에서는 영구선물의 펀딩 메커니즘이 핵심 인프라.

### 2026 알파 소진 정도: 중상
- 학술 연구(MDPI)에 따르면 펀딩레이트 차익 포트폴리오가 **6개월간 최대 115.9%** 수익을 기록한 사례가 있으나, 이는 극단적 롱시장 국면이며 통상 연 8~25% APR 수준.
- AEA 2026 컨퍼런스 논문이 "constrained arbitrage"(제약받는 차익) 개념을 다루며, **자본비용·청산·거래소 리스크 때문에 차익이 완전히 소멸되지 않는 구조**임을 시사. 즉 알파가 존재하되 "비용/구조 장벽"이 프라이스 플로어 역할.
- 다만 동일 거래소 내 퍼페-현물 단순 차익은 **거래소 자체 제품화(earn/structured)**로 인해 수익률 압박. 차별화는 **크로스거래소 펀딩 스프레드, 비주류 알트/롱테일 자산, 펀딩 곡면 비정상성**에서 발생.

### 구현 난이도: 중
- 기본 로직(헤지 비율·리밸런싱)은 단순. 복잡도는 다음에서 발생:
  - 크로스거래소 자본 분배, 출금/이체 지연, 가용 잔고 관리
  - 펀딩 타이밍(8h/1h/4h 차별), 펀딩 직전 변동 헤징
  - 청산 회피용 오버콜레터럴 비율 최적화
- 인프라(데이터/주문/리스크)는 보통 수준이나, **자본집약적**이라 자본회전율이 병목.

### 추정 샤프/수익률대
- 샤프 1.5~3.0 (시장 국면에 따라 편차 큼), 연 APR 8~25%(일반), 30%+(강세·롱테일).
- 하방은 거의 점핑 리스크(거래소 해킹/페깅 붕괴/급철평)에 의해 결정.

### 자본 효율
- 퍼페 숏은 레버리지 가능 → 자본효율 상승, 단 **청산/변동 헤지 비용** 증가.
- 현물은 보통 1:1, 교차증거 방식으로 마진 효율화 가능.

### 구조적 하드함
- **거래소/커스트디 리스크**: 자본이 2곳 이상에 분산 → 해킹·출금정지·파산(FTX 사례) 노출. 이것이 "왜 수익이 남아있는가"의 주된 답.
- **테더/스테이블코인 페깅 리스크**: 헤지가 USDT/USDC 기반일 때 스프레드가 숨겨진 베이시스.
- **예상치 못한 펀딩 부호 반전**: 강세→약세 전환 시 단기 마이너스 펀딩으로 손실 구간.
- **세금/회계**: 숏 포지션·대출 형태가 복잡해 지역에 따라 불리.

### 왜 아직 붐비지 않는가
- 수익률(절대값)이 낮아 대형 펀드는 자본배분 우선순위에서 밀림.
- 자본이 묶이는 "저회전" 자산이라 ROE 한계.
- 반면 개인은 거래소 리스크·인프라 구축 부담으로 진입 장벽 존재 → **중간 규모 틈새**.

### 출처
- [The Two-Tiered Structure of Cryptocurrency Funding Rate Markets (MDPI)](https://www.mdpi.com/2227-7390/14/2/346) — 6개월 115.9% 수익 사례, 포트폴리오 평가.
- [Funding Rate Mechanism in Perpetual Futures (SSRN)](https://papers.ssrn.com/sol3/Delivery.cfm/6185958.pdf?abstractid=6185958) — 펀딩을 알고리즘 피드백으로 모델링.
- [Perpetual Futures and Basis Risk: Constrained Arbitrage (AEA 2026)](https://www.aeaweb.org/conference/2026/program/paper/ByyFEfr4) — 제약 차익 개념.
- [Designing funding rates for perpetual futures (arXiv 2025)](https://arxiv.org/html/2506.08573v1)
- [Basis Trading and Funding Rate Arbitrage on Perps (Hyperdash)](https://hyperdash.com/learn/basis-trading-and-funding-rate-arbitrage-on-perps)
- [Funding rate arbitrage in crypto (Kraken Learn)](https://www.kraken.com/be/learn/futures-trading-funding-rate-arbitrage)
- [Crypto Funding Rate Tracker — Sharpe.ai](https://www.sharpe.ai/products/funding-rates) — 13개 거래소·5,300+ 금리 추적.
- [BitMEX 2025 Q3 Derivatives Report](https://www.bitmex.com/blog/2025q3-derivatives-report)

---

## 2. 통계차익 (페어 / 코인테그레이션 / 스프레드)

### 개요
두 자산(예: BTC/ETH, 또는 알트-알트) 간 장기 균형관계를 코인테그레이션으로 추정하고, 스프레드가 평균회귀 범위를 이탈할 때 롱-숏 진입. 순수 모멘텀과 달리 **스프레드의 정상성**이 핵심 가정.

### 2026 알파 소진 정도: 중상
- 전통시장(주식)은 초포화이나, **크립토는 자산수 증가 + 펀더멘턜 부재**로 여전히 구조적 비효율 존재.
- 단순 상관관계 기반은 이미 한계가 드러남 → 2026 연구 흐름은 **Copula 기반 적응형 페어**(AIMSPress 2026 PDF)로 진화. 즉 "평균" 페어는 압축, **비선형·꼬리 의존 모델링**에 잔존 알파.
- IJSRA 학위논문은 BTC/ETH/LTC 등에서 코인테그레이션 차익이 유효함을 실증.

### 구현 난이도: 중상
- 핵심 과제:
  - **코인테그레이션 관계의 불안정성**: 크립토는 레짐 전환 잦음. 고정 윈도우 ADF/EG 테스트는 자주 실패 → 롤링/온라인 cointegration, 상태공간(Kalman) 필요.
  - **페어 발굴(screeing)**: 수천 개 조합 중 실제로 평균회귀하는 쌍 필터링. false positive 다수.
  - 헤지 비율 동적 추정, 진입/청산 임계값 최적화(볼린저 대신 Z-score/하프라이프).
- 코플라 접근은 구현 난이도 추가 상승(수학적·계산량).

### 추정 샤프/수익률대
- 샤프 1.0~2.0 (시장 상관 붕괴 시 하락). 연 수익률 15~40%(레버리지 시).
- 꼬리 리스크: **코인테그레이션 붕괴**(한쪽이 상장폐지/해킹/규제) → 스프레드 발산 손실.

### 자본 효율
- 양면 포지션으로 자본 2배 소요, 단 퍼페 활용 시 레버리지로 효율화 가능.
- 증거금 이체·청산 회피용 버퍼 필요.

### 구조적 하드함
- **레짐 체인지**: 2022 LUNA/FTX, 2024~25 규제 이벤트 등이 한쪽 자산만 타격 → 스프레드 폭주.
- **동시 체결(slippage/leg risk)**: 양측 주문이 부분 체결되면 노출된 방향 리스크. 취소/재주문 로직 필수.
- **자금조달 비용**: 숏 측 차입/펀딩 비용이 스프레드를 잠식.

### 왜 아직 붐비지 않는가
- 코인테그레이션 안정성 의심 + 잦은 붕괴 → "믿을 만한가" 논쟁.
- 모델링/재검증 부담이 커 단순 모멘텀보다 진입 장벽 높음.
- 개인이 접근 가능한 백테스트 인프라 부족(틱/호가 데이터 비용).

### 출처
- [Statistical Arbitrage Strategies Using Cointegration Analysis in Cryptocurrency (IJSRA)](https://ijsra.net/node/2582)
- [Adaptive Copula-based Pairs Trading with Market Overlay (AIMSPress 2026)](https://www.aimspress.com/aimspress-data/qfe/2026/2/PDF/QFE-10-02-016.pdf) — 2026 최신 코플라 접근.
- [Copula-based Trading of Cointegrated Cryptocurrency Pairs (Springer)](https://link.springer.com/article/10.1186/s40854-024-00702-7)
- [What is Pair Trading? Complete Guide 2026 (Pair-Sync)](https://www.pair-sync.com/blog/what-is-pair-trading)
- [Statistical Arbitrage: A Complete Guide 2026 (Quantt)](https://www.quantt.co.uk/resources/statistical-arbitrage-guide)

---

## 3. 시장중립 롱-숏 (베헤지 / 베타중립)

### 개요
베타(시장 민감도)가 다른 자산들을 장기/단기로 담아 시장 방향을 헤지하고 알파(특정 요인: 모멘텀, 밸류, 사이즈, 온체인 팩터)만 포착. 전통 시장의 long/short equity를 크립토로 이식.

### 2026 알파 소진 정도: 중
- Liquibit 등 전문 마켓중립 펀드가 등장(베타가중 달러중립). CryptoFundResearch에 따르면 2026 시장중립 카테고리 성장 중.
- Springer 학술: 크립토 마켓 베타의 **예측가능성**과 베헤지 전략 효과를 연구 → 베타가 시간가변적이라 단순 상수 헤지는 한계.
- "Don't pay alpha for beta" 논의 확산 → 단순 베헤지 자체는 상품화 압력, **팩터/시그널 품질**이 차별화.

### 구현 난이도: 중상
- 다자산 포트폴리오 최적화(롱 바스켓/숏 바스켓), 동적 베타 추정(롤링 회귀/Kalman).
- 숏 차입 가능 자산 제약(일부 알트는 차입 불가/비용 고).
- 포트폴리오 리밸런싱 빈도·비용 최적화.

### 추정 샤프/수익률대
- 샤프 0.8~1.5 (전통 L/S equity 대비 변동 큼). 연 10~30%.
- 베타 추정 오차 시 시장 노출 발생 → 하방 확대.

### 자본 효율
- 퍼페 활용 시 레버리지 1.5~3x 가능, 단 알트 숏 청산/펀딩 비용 주의.

### 구조적 하드함
- **베타 불안정성**: 시장 레짐 전환 시 헤지가 풀림.
- **숏 측 털림(short squeeze)**: 알트 숏은 가격 스파이크 시 무한 손실 가능.
- **청산 연쇄**: 레버리지 시 시장 급락이 롱 측 청산 유발.

### 왜 아직 붐비지 않는가
- 전통 금융에서는 보편이나 크립토에서는 차입 인프라·신용 한계로 소수만.
- 단순 방향(롱전용) 수익률이 과거 압도적이라 상대적 매력 낮았음. 2026 변동 시장에서 매력 부상.

### 출처
- [Market Neutral Strategy in Crypto: Does It Actually Work? (TV-Hub)](https://www.tv-hub.org/guide/market-neutral-strategy-crypto) — 5가지 유형, 2025~2026 실적 데이터.
- [Liquibit's Market Neutral Crypto Strategy (Hedge Fund Journal)](https://thehedgefundjournal.com/liquibit-market-neutral-crypto-strategy-traditional-trading/)
- [Crypto market betas: predictability and hedging (Springer)](https://link.springer.com/article/10.1186/s40854-025-00777-w)
- [Crypto Hedge Funds: Don't Pay Alpha for Beta (BlueSky)](https://www.blueskycapitalmanagement.com/crypto-hedge-funds-dont-pay-alpha-for-beta)
- [The Complete List of Crypto Hedge Funds 2026 (CryptoFundResearch)](https://cryptofundresearch.com/crypto-hedge-funds-list/)

---

## 4. 온체인 / 대체데이터 정성→정량

### 개요
온체인 흐름(거래소 유출입, 고래 지갑 행태, NVT, 활성주소, 스테이킹 락업), 소셜 센티먼트, 개발자 활동(GitHub 커밋), 거래소 오더북 불균형 등 비전통 신호를 정량 지표로 변환해 매매. LLM/ML로 정성→정량 파이프라인 구축이 2026 핵심.

### 2026 알파 소진 정도: 상(가장 비효율)
- **이 카테고리가 가장 큰 잔존 알파**로 평가. 이유: 신호가 비표준·비경제적(공개 데이터라도 해석 차이), 데이터 파이프라인 구축이 진입장벽.
- 크립토는 전통 기업 공시처럼 정형 펀더멘턜 부재 → 온체인/대체데이터가 사실상 유일한 "펀더멘턜 대체".
- CryptoQuant, Nansen, Santiment, Glassnode 등 인프라는 성숙하나 **신호 해석·조합**은 여전히 파편화.

### 구현 난이도: 중
- 신호 정의/백테스트는 난이도 중. 핵심은 **데이터 인프라**(RPC 노드, 인덱서, 지갑 클러스터링, ETL)가 모.
- 정성(뉴스/소셜)→정량 변환은 LLM 기반 분류·감성 추출이 2026 표준화 추세.
- 백테스트의 look-ahead/생존편향 함정 주의.

### 추정 샤프/수읥률대
- 매우 불규칙: 신호 품질에 따라 샤프 0.5~2.5. 연 20~100%(고변동).
- 신호 붕괴(시장에 가격화) 시 급락 → 모니터링/갱신 필수.

### 자본 효율
- 방향 전략이라 레버리지 가용, 단 신호 잡음에 레버는 위험.

### 구조적 하드함
- **신호 붕괴/과최적화**: 백테스트 좋지만 라이브 약화 흔함.
- **데이터 품질/지연**: 노드 동기화·인덱서 지연이 신호를 죽임.
- **해석 주관성**: "고래 유출 = 매도압력" 등 단순 해석은 이미 가격화.

### 왜 아직 붐비지 않는가
- 데이터 엔지니어링 부담 + 신호 연구가 "장인적" → 자동화·상품화 어려움.
- 공개 인디케이터(단순 NVT 등)는 포화, **복합·비선형 신호 조합**은 연구 부족.

### 출처
- [CryptoQuant](https://cryptoquant.com/) — 온체인 액셔너블 인사이트.
- [Nansen AI](https://nansen.ai/) — 지갑 흐름·고래 분석.
- [Santiment](https://santiment.net/) — 고래 트랜잭션·센티먼트.
- [Coin Metrics](https://coinmetrics.io/) — 주간 네트워크/온체인 뷰.
- [BingX: Top 10 On-Chain Analysis Tools 2026](https://www.bingx.com/)
- [TradingView On-Chain Indicators](https://www.tradingview.com/scripts/onchain/)

---

## 5. MEV / DEX 아비트라지

### 개요
DEX-DEX, CEX-DEX, 삼각차익, 샌드위치, 백러닝 등 블록체인 메모리풀/상태를 활용한 무위험 차익. Flashbots/private RPC, MEV-Boost 등 인프라 기반.

### 2026 알파 소진 정도: 하(포화) — **개인 사실상 불가**
- **90% 이상의 차익이 프라이빗 MEV-Boost 채널**로 라우팅(Extropy Academy 분석) → 퍼블릭 mempool은 잔해.
- CEX-DEX 차익 평균 마진 38.5%(Binance Research/PANews)로 보이나, 이는 **선두 봇 평균**이며 꼬리는 마이너스.
- NDSS 2026 논문이 MEV 봇 생애주기 수익 전략을 체계 연구 → 시장의 성숙/합리화 시사.
- Reddit/커뮤니티 "2026 온체인 차익 여전히 유효한가" 질문 증가 → 진입 의심.

### 구현 난이도: 최상 (인프라 경쟁)
- 5개 하드 레이턴시 버짓(RPC, Mempool, 시뮬레이션, 제출, 가스): Dysnix/Dwellir 분석.
- 전용 RPC, 블록 빌더 관계, MEV-Boost relay 최적화 필수.
- Solana/EVM별 별도 인프라.

### 추정 샤프/수익률대
- 샤프 매우 높으나 변동: 일/주 단위 손익이 0 또는 폭등. 연 환산 무의미.
- 자본 회전율 극단적(초단위)이나, **단위 자본당 수익은 이미 낮아짐**.

### 자본 효율
- MEV 자체는 자본 효율 좋으나, **인프라 고정비용**이 실질 병목(월 수천~수만 달러).

### 구조적 하드함
- **인프라 군비경쟁 패배**: 빌더/시퀀서/프라이빗 풀을 통제하는 플레이어가 독식.
- **가스/브리브 경매**: 50~99% 수익이 가스/팁으로 소거.
- **전략 수명 단기**: 새 패턴도 수일~수주 내 복제·소멸.

### 왜 아직 붐비지 않는가(주의: 사실상 **매우 붐빔**)
- "덜 붐비는" 카테고리가 아님. **오히려 가장 포화**. 개인/소자본에게는 비추천.
- 포함은 비교·배제를 위해. 실제 후보에서 **탈락**.

### 출처
- [Demystifying Profit Strategies Throughout the MEV Bot Lifecycle (NDSS 2026)](https://www.ndss-symposium.org/ndss-paper/light-into-darkness-demystifying-profit-strategies-throughout-the-mev-bot-lifecycle/)
- [r/defi: Is on-chain arbitrage still viable in 2026?](https://www.reddit.com/r/defi/comments/1sksndi/reality_check_is_onchain_arbitrage_still_viable/)
- [PANews Lab: CEX-DEX arbitrage 38.5% margin](https://www.panewslab.com/en/articles/91i7ihsl)
- [Binance Research (square post)](https://www.binance.com/en/square/post/27447721461986)
- [Extropy: MEV Crosschain Analysis 2025](https://academy.extropy.io/pages/articles/mev-crosschain-analysis-2025.html)
- [Dysnix: How to Build a Solana Arbitrage Bot 2026](https://dysnix.com/blog/solana-arbitrage-bot-setup)
- [Dwellir: MEV Arbitrage Bot Infrastructure](https://www.dwellir.com/blog/mev-arbitrage-bot-infrastructure)

---

## 6. 변동성·변동성패턴 거래 (Vol Arb / Dispersion / VVRP)

### 개요
내재변동성(IV) vs 실현변동성(RV) 차이, 변동성 벤더링, 디스퍼전(지수 vs 구성종목 vol), 변동성 리스크 프리미엄(VRP) 등을 옵션/델타헤지로 거래. 크립토는 Deribit 옵션 시장이 핵심.

### 2026 알파 소든 정도: 중상
- SSRN 연구: BTC/ETH 옵션에서 **변동성 스프레드 + 델타헤지 전략이 견고한 수익**을 보인다고 실증.
- 크립토 옵션 시장은 성장 중이나 여전히 **주류 자산(BTC/ETH) + 짧은 만기**에 집중 → **롱테일/중만기/변동성 곡면**에 비효율 잔존.
- 전통시장 대비 IV 프리미엄(변동성 리스크 프리미엄)이 크고 지속적.

### 구현 난이도: 상
- 옵션 헤딩(델타/감마/베가), 그릭 관리, 만기 롤, IV 서피스 모델링 필요.
- Deribit 옵션 API/청산/마진 이해 필수.
- 단순 숏 볼(covered call)은 쉽지만 진짜 vol arb는 정량 인프라 요구.

### 추정 샤프/수읥률대
- 샤프 1.5~2.5 (VRP 수취). 연 15~40%(레버리지·만기 구조에 따라).
- **테일 리스크(급등 시 숏볼 손실)**가 하방 결정.

### 자본 효율
- 옵션 포지션 증거금 방식. 풋 매입(롱 볼)은 자본 한정, 콜 매도/숏 볼은 증거금·청산 리스크.

### 구조적 하드함
- **갭/점핑 리스크**: 급등 시 델타헤지 불가(슬리피지).
- **유동성/만기 제약**: 깊은 옵션 시장이 BTC/ETH 일부 만기에만.
- **거래소(파생상품) 리스크**: Deribit/OKX 등에 자본 노출.

### 왜 아직 붐비지 않는가
- 옵션 거래 지식+인프라 진입장벽. 현물/퍼페 단거래자 대부분.
- 숏 볼은 " 무한 손실" 이미지로 인식, 소수만.
- IV 서피스·그릭 최적화는 전문 퀀트 영역.

### 출처
- [Derivative Arbitrage Strategies in Cryptocurrency Markets (SSRN)](https://papers.ssrn.com/sol3/Delivery.cfm/5138953.pdf?abstractid=5138953)
- [Volatility Models for Cryptocurrencies and Applications in Options Market (ResearchGate)](https://www.researchgate.net/publication/354534697) — 델타헤지 볼 스프레드 견고 수익.
- [Cryptocurrency Volatility Benchmarking (arXiv)](https://arxiv.org/html/2404.04962v1)
- [Volatility Arbitrage Strategies (QuestDB Glossary)](https://questdb.com/glossary/volatility-arbitrage-strategies/)
- [What is Volatility Arbitrage? (CQF)](https://www.cqf.com/blog/quant-finance-101/what-is-volatility-arbitrage)
- [Volatility Arbitrage (Investopedia)](https://www.investopedia.com/terms/v/volatility-arbitrage.asp)

---

## 7. 이벤트 / 발표 기반 거래

### 개요
FOMC, CPI, NFP, ETF 승인, 메인넷/에어드랍, 상장/상장폐지, 해킹 등 특정 이벤트 전후의 예측가능한 가격 반응 패턴을 거래. 사건 종류별·국면별 반응 템플릿 구축.

### 2026 알파 소진 정도: 중
- 미시구조상 **고빈도/HFT가 발표 직후 유동성을 장악** → 직후 진입은 어려움.
- 단, **사전 포지셔닝**(1~2일 전 기대 가격화)과 **과반응 평균회귀**(발표 후 15~60분~일)는 잔존 알파.
- NY Fed 연구: 비트코인-매크로 단절(장기 상관 낮음) → 단기 이벤트 반응만 거래 가능.

### 구현 난이도: 중
- 이벤트 캘린더, 실제/예상/이전값 데이터 파이프라인.
- 사건별 반응 분포 백테스트(통계적 유의성 확보 어려움: 표본 적음).
- 라이브 실행: 발표 순간 스프레드/거부/슬리피지 대응.

### 추정 샤프/수읥률대
- 변동 큼: 사건별 승률·배당 상이. 연 환산 샤프 1.0~2.0(양호) ~ 0(잡음).
- 기회가 드물어(월 수회) 자본 회전 낮음.

### 자본 효율
- 발표 전후 단기 보유 → 자본 회전 양호. 레버리지 가용하나 이벤트 갭에 위험.

### 구조적 하드함
- **실행(거부/슬리피지)**: 발표 직후 스프레드 폭발, 시장가 주문 손실.
- **정보 비대칭/레톡**: 일부 참여자가 더 빠른 데이터 피드.
- **과최적화 위험**: 표본 적어 커브피팅 흔함.

### 왜 아직 붐비지 않는가
- 기회가 드물고, 실행 인프라(저지연 데이터/주문)가 병목.
- 백테스트 유의성 확보가 어려워 학술/소매 전략으로 덜 체계화.

### 출처
- [BuildAlpha: News Event Trading](https://www.buildalpha.com/news-event-trading/) — FOMC/CPI/NFP 백테스트.
- [The Bitcoin–Macro Disconnect (NY Fed)](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1052.pdf)
- [Algorithmic crypto trading using information-driven bars (Springer)](https://link.springer.com/article/10.1186/s40854-025-00866-w)
- [CFTC: Perpetual Futures as Leveraged Retail Contracts (Feb 2026)](https://www.cftc.gov/media/13716/innovation_BlockchainAssn02242026)

---

## 8. 기간구조 / 커브 거래 (Calendar / Term-structure)

### 개요
동일 자산의 다른 만기 선물 간 스프레드(캘린더 스프레드) 거래. 콘탱고/백워데이션, 선물 곡선의 형태(기울기·만곡) 변화를 활용. CME BTC 선물, Deribit 옵션/선물, 토큰화 주식(2026 성장)이 무대.

### 2026 알파 소진 정도: 중상
- 2026 **토큰화 주식/증권 시장 부상**(Tiger Research 보고서) → 24/5 종목×크립토 선물 구조가 새로운 커브 비효율 창출.
- 단순 콘탱고 캐리는 이미 거래소가 earn 상품으로 흡수 → **곡면 형태·크로스자산 커브**에 잔존.
- CME 등 전통선물 만기 구조가 크립토에 "계절성" 부여.

### 구현 난이도: 중상
- 만기별 호가·유동성 파악, 롤 비용, 스프레드 증거금(SPAN/spread margin) 최적화.
- 캘린더 스프레드 자체는 중간 난이도, **곡면/디스퍼전 결합** 시 상승.

### 추정 샤프/수읥률대
- 샤프 1.0~2.0. 연 8~20%(캐리 중심, 안정적).
- 자본이 만기까지 묶임 → ROE 한계.

### 자본 효율
- 스프레드 마진 혜택(거래소별)으로 자본효율 양호, 단 자본이 묶이는 기간 비용.

### 구조적 하드함
- **롤/만기 리스크**: 근월물 청산·이월 시 유동성 부족.
- **롤오버 비용**이 수익 잠식.
- 유동성이 특정 만기에만 집중(근월물) → 원월물 슬리피지.

### 왜 아직 붐비지 않는가
- 수익률이 낮고 자본 묶임 → 대형 자본 비매력.
- 만기/커브 이해도 필요해 단순 단타 매력에 밀림.
- 토큰화 증권 등 **신흥 구조**는 아직 인프라·참여자 적음 → 초기 비효율.

### 출처
- [Tiger Research: 2026 Tokenized Stock Market Report](https://reports.tiger-research.com/p/2026-tokenized-stock-market-the-rise-eng) — 딸나 전략·크로스거래소 차익.
- [CME Group: What is Contango and Backwardation](https://www.cmegroup.com/education/courses/introduction-to-ferrous-metals/what-is-contango-and-backwardation)
- [Bookmap: Profiting from Calendar Relationships in Futures Spreads (2025)](https://bookmap.com/)
- [Exegy: Calendar Spreads based on Forward Curve](https://exegy.com/)
- [HedgeStar: Futures Calendar Spreads](https://hedgestar.com/)
- [Reuters: Perpetual Futures Traction (June 2026)](https://www.reuters.com/business/us-exchanges-extend-selloff-perpetual-futures-approval-unnerves-investors-2026-06-02)
- [a16z Crypto: How Perpetual Futures Are Rewriting Global Trading](https://a16zcrypto.substack.com/p/how-perpetual-futures-are-rewriting)
- [MetaMask: Bitcoin Futures Trading in 2026](https://metamask.io/news/bitcoin-futures-trading-in-2026)

---

## 9. 종합 평가 및 후보 우선순위 (소자본·개인 관점)

평가 기준(소자본 적합성 + 잔존 알파 + 구현가능성 + 구조적 하드함 수용):

1. **온체인/대체데이터 정성→정량** — 가장 큰 잔존 알파, 데이터 인프라 구축이 모이나 소자본에서 ML/LLM 파이프라인으로 차별화 가능. 단 신호 붕괴 관리 필수.
2. **통계차익(코인테그레이션/코플라)** — 비효율 잔존, 모델링 투자로 엣지. 레짐 전환 리스크 관리가 핵심.
3. **변동성·변동성패턴 거래** — VRP/디스퍼전 잔존, Deribit 옵션 인프라로 진입. 숏 볼 테일 관리가 관건.
4. **기간구조/커브 거래** — 안정적 캐리 + 토큰화 증권 신흥 비효율. 자본 묶임이 단점.
5. **펀딩레이트/베이스 차익** — 안정적이나 자본집약·거래소 리스크. 보조 수익원으로 적합.
6. **시장중립 롱-숏** — 팩터/시그널 품질이 전부. 차별화 어려움.
7. **이벤트/발표** — 기회 드물고 실행 병목. 보조용.
8. **MEV/DEX 아비트라지** — **탈락**(포화, 개인 진입 불가).

> 다음 조사(Task #1 시장·자산 엣지 / Task #3 인프라 / Task #4 리스크)에서 위 상위 3~4개 카테고리를 깊이 파고, 최종 IDEATION.md(Task #5)에서 1~2개 방향으로 수렴 예정.

---

## 부록: 데이터/인프라 힌트 (다음 조사용)
- 온체인: CryptoQuant, Nansen, Santiment, Glassnode, Coin Metrics, 자체 RPC/인덱서.
- 파생상품: Deribit(옵션), CME(선물), Sharpe.ai(펀딩), BitMEX 리서치.
- 백테스트: 자체 Python(틱/호가 데이터 확보가 핵심); look-ahead/생존편향 주의.
- 거래소 리스크: 분산 커스트디, 출금 한도, FTX 사례 반복 학습.

*문서 끝. 약 280줄(마크다운). 범위 내.*
