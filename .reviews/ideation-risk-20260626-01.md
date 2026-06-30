# 자동매매 아이디에이션 — 리스크 관리 + 검증 방법론 조사 (2026-06-26)

> 역할: 리스크·검증 방법론 조사원
> 기준일: 2026-06-26
> 목적: 정량 자동매매의 **리스크 관리 + 검증 방법론**을 2026년 기준으로 조사하고, autotrader 설계에 **반드시 들어가야 할 원칙**을 도출.
> 원칙: 뻔한 "분산투자하라" 수준 회피. **실행가능한 메커니즘** 우선. 백테스트·포지션사이징·검증·킬스위치 모두 코드로 구현 가능한 형태로.
> 산출처: 웹 검색 10회 + arXiv/López de Prado/Thorp/StrategyQuant/SOPHIE Quant Blog 등 1차 소스 직독.

---

## TL;DR — 핵심 결론

1. **백테스트는 "나쁜 전략을 거르는" 용도로만 쓴다.** "좋은 전략을 증명"하려는 목적으로는 본질적으로 신뢰 불가. López de Prado: "완벽한 백테스트도 아마 틀렸다" — 시도 횟수를 보고하지 않는 백테스트 결과는 사기에 가깝다.
2. **과적합은 다중검정(p-hacking) 문제.** 해답은 Deflated Sharpe Ratio(DSR) + 시도 횟수 로깅 + OOS 데이터 "사전 고정". autotrader는 **백테스트 시도 카운터**를 시스템 필드로 가져야 한다.
3. **포지션 사이징은 부분 Kelly(¼~½)가 정답이지만, 이유는 "엣지 과대추정 방어" + "파산위험 방어" + "하방 백분위 최적화"가 중첩(overdetermined).** 순수 불확실성만으로는 Kelly가 크게 안 바뀜 — Thorp/Downey 시뮬레이션 확인.
4. **페이퍼→라이브 갭의 주원인은 슬리피지·지연·용량·숨은 유동성.** 이 갭을 **백테스트 안에서 모델링**해야(비관적 slippage, 지연 주문, 시장충격). 갭이 모델링 안 된 백테스트는 무효.
5. **킬스위치는 "위반 직전"에 발동되어야 의미가 있다.** 위반 후가 아님. autotrader는 **3단계 회로차단기**(경고→축소→전면중단) + 강제 쿨다운(≥2주) + 인간 승인 재기동을 기본 구조로.
6. **검증은 Walk-Forward + Monte Carlo(블록 부트스트랩) + CPCV/PBO의 3종 세트.** 단일 백테스트 결과는 보고 가치조차 없음. **5백분위 콘(cone)**을 전방 투영해 라이브 모니터링 기준으로 사용.

---

## 1. 백테스트의 함정 (Backtesting Pitfalls)

### 1.1 왜 백테스트는 위험한가 — 근본 원인

López de Prado(2018, *Advances in Financial Machine Learning*)의 핵심 명제:
> "백테스트는 **실험이 아니다.** 반복 불가능하므로 아무것도 증명하지 않는다. 심지어 과거로 돌아가도 무작위 추출이 달라져 같은 Sharpe가 안 나온다."

"역설": **완벽한 백테스트일수록 더 의심해야 한다.** 전문가일수록 수많은 백테스트를 돌렸을 것이고, 그만큼 허위 발견(false discovery)이 필연적으로 발생. 즉 "잘 나온 백테스트 = 실력"이 아니라 "많이 돌린 결과"일 확률이 높다.

백테스트의 **유일한 올바른 용도**: 나쁜 모델을 걸러내는 것. 백테스트 결과로 모델을 수정하면 안 됨(과적합 사이클). 모델이 완전히 정의된 **뒤에** 한 번만 돌린다.

### 1.2 과적합 (Overfitting / Curve-Fitting)

- **정의**: 노이즈가 아닌 구조를 잡아야 하는데, 특정 과거 관측치(noisy)에 맞춰진 상태. 미래에 재현 안 됨.
- **von Neumann 명언**: "파라미터 4개로 코끼리를 그리고, 5개로 코를 흔들게 한다."
- **복잡한 전략일수록 치명적**: 적은 시도로도 가짜 고성능 전략 발견 가능(Bailey et al. 2014).
- **탐지**: in-sample vs OOS 격차, 파라미터 민감도(jitter), PBO(Probability of Backtest Overfitting).

**적용 메커니즘 (autotrader):**
1. **파라미터 수 경량화** — 자유도 3개 이하 목표. 정규화·모델 앙상블로 분산 축소.
2. **파라미터 jitter 테스트** — 각 파라미터를 ±10~20% 흔들었을 때 성능 붕괴 폭 측정. 특정 값에 날카롭게 의존하면 기각(국소 최적값 피크).
3. **모델 평균화(model averaging)** — 단일 파라미터 세트가 아니라 가중 평균으로 과적합 분산.

### 1.3 룩어헤드 편향 (Look-ahead Bias)

- **정의**: 해당 시점에 알 수 없었던 정보를 사용. 대표 사례: 다음 캔들 시가로 체결 가정, 미래 재무제표 사용, 정제된(current) 티커 리스트 과거에 적용.
- **왜 은밀한가**: 코드가 "논리적으로" 맞아 보여도 point-in-time 정보 집합 위반.
- **Walk-forward에서의 함정**: 데이터 스냅샷이 각 시점의 "알고 있던 것"으로 롤백되지 않으면 무의미. (Reddit r/algotrading 반복 교훈)

**적용 메커니즘 (autotrader):**
1. **정보 집합(Information Set) 엄격 적용** — `I_t = {P_τ : τ ≤ t}`. arXiv:2512.12924의 Definition 1. 특징·시그널·실행 결정 모두 `t` 이하 데이터만.
2. **주문은 항상 `t+1` open에 체결** — arXiv:2512.12924 모델: t 종가 기준 신호 → t+1 시가 체결 + 슬리피지.
3. **point-in-time 유니버스** — 상장폐지/인수된 티커를 과거 시점에 "없었던 것"으로 처리(purged, 생존편향 §1.4와 결합).
4. **데이터 변환(표준화·변동성 스케일링)은 사전 고정** — 연구 시작 후 샘플/변환 변경 금지(Arnott, Harvey, Markowitz 2019).

### 1.4 생존편향 (Survivorship Bias)

- **정의**: "오늘 살아남은 자산"만 과거에도 거래 가능했다고 가정. 상장폐지/상장거부/인수 티커 누락 → 수익률 과대.
- **크립토 특화**: 코인이 0이 되는 경우 빈번(de-list, rug pull, 프로토콜 해킹). "현재 시총 상위 N개"로 백테스트하면 치명적.
- arXiv:2512.12924도 이 편향을 인정하고 "보수적 결과"로 정당화. 자산 클래스 전체로 모델링하면 편향 완화(López de Prado 권고).

**적용 메커니즘 (autotrader):**
1. **point-in-time 유니버스 재구성** — 각 날짜별로 "그날 거래 가능했던 코인/종목" 리스트 사용. delisting/rug 기준으로 퇴출.
2. **자산 클래스 단위 모델링** — 개별 티커가 아닌 자산군/투자유니버스로 모델 → 허위 발견 확률 감소.
3. **0 수익률(파산) 경로 포함** — 크립토는 코인이 -100% 되는 경로를 백테스트에 반드시 포함.

### 1.5 다중검정 / p-hacking / 데이터 스누핑

- **정의**: 여러 가설을 검정하고 유의한 것만 발표(cherry-picking). 시도 횟수 은폐. Harvey(2017): "금융경제학 연구의 대부분은 p-hacking 때문에 거짓일 가능성이 높다."
- **Bailey & López de Prado (2014)**: "시도 횟수를 보고하지 않는 백테스트는 사기에 가깝다." 비교적 적은 시도만으로도 가짜 고성능 전략 발견 가능.
- **Harvey, Liu, Zhu (2016)**: 316개 팩터 제안. 새 팩터는 t-통계량 **3.0 이상**(종래 2.0 아님)이어야 유의. McLean & Pontiff(2016): OOS에서 수익률 26% 하락, 출판 후 58% 하락. Hou et al.(2020): 452개 anomaly 중 65%가 단일검정에서도 실패.

**적용 메커니즘 (autotrader):**
1. **백테스트 시도 카운터 로깅** — 동일 데이터셋에 대해 돌린 백테스트 횟수 `N`을 시스템 필드로 영구 저장. DSR 계산에 필수.
2. **Deflated Sharpe Ratio(DSR) 보고** — Sharpe를 (a) 다중검정 보정, (b) 비정규성 보정, (c) 트랙레코드 길이 보정. 원래 Sharpe 보다 DSR만 보고.
3. **최소 트랙레코드 길이(MinTRL)** — 신뢰할 데이터 길이 사전 계산. 짧으면 결과 자체가 무의미.
4. **사전 가설 설정** — 경제적 근거를 데이터 마이닝 **전에** 명시. 사후 합리화(ex post rationalization) 금지.
5. **"진짜 OOS는 라이브뿐"** 전제 — 연구자가 holdout 기간을 경험했으므로 OOS도 완전히 독립 아님(Arnott et al. 2019). 포워드 테스트(§5.4)가 유일한 진짜 OOS.

### 1.6 백테스트 함정 — autotrader 설계 원칙 (요약)

> **[원칙 B1]** 백테스트는 "나쁜 전략 거르기" 용도. 좋은 전략 증명 금지. 모델은 백테스트 **전**에 완전 고정.
> **[원칙 B2]** 백테스트 시도 카운터 + DSR을 모든 결과에 의무 첨부. 시도 횟수 은폐 = 사기.
> **[원칙 B3]** point-in-time 정보 집합 + point-in-time 유니버스. `t+1` 체결 가정 필수.
> **[원칙 B4]** 파라미터 수 ≤3, jitter 테스트 의무화, 모델 앙상블로 과적합 분산.

---

## 2. 페이퍼 → 라이브 성능 갭 (Paper-to-Live Gap)

### 2.1 갭의 원인 (정량화 가능 항목)

| 원인 | 메커니즘 | 정량화 |
|---|---|---|
| **슬리피지** | 주문 제출→체결 사이 가격 이동 | 일반적으로 5~20bp, 변동성 높을 때 확대 |
| **네트워크 지연** | API 라운드트립, 주문 라우팅 | 100ms~수 초 (Alpaca 포럼: 다른 유동성 제공자 도달 지연) |
| **대기/실행 지연** | 캔들 오픈→주문 체결 사이 | Streak 사례: 18~20초 지연 보고 |
| **시장 충격(market impact)** | 내 주문이 시장을 움직임 | 주문 크기/유동성 비례. 소형 자산에서 치명적 |
| **숨은 유동성** | 다크풀/중간 LP가 보이지 않음 | 백테스트에 반영 불가 (Alpaca 포럼) |
| **부분 체결** | 유동성 부족 시 일부만 체결 | 대형 주문에서 빈번 |
| **수수료/펀딩 누락** | 페이퍼에서 현실 비용 미반영 | 메이커/테이커/펀딩레이트/스왑 |
| **심리/행동** | 실제 손실에 대한 반응 | 정량화 어려움 — 하지만 시스템 자동화로 회피 가능 |

Harvey 계열 문헌: "라이브에서 학술 전략 90%+ 실패" (arXiv:2512.12924 인용). Pardo(1992) 이후 walk-forward가 gold standard이지만, **실행 비용이 현실적으로 모델링되지 않으면 무용**.

### 2.2 갭을 줄이는 메커니즘 (실행 가능)

**A. 비관적 비용 모델 (Pessimistic Cost Model)**
- 슬리피지: 고정 5bp가 아니라 **ATR/스프레드 기반 동적 모델**. 변동성 높을 때 자동 확대.
- 지연: 주문은 항상 `t+1` open이 아니라 `t+1` open + 지연 분포 샘플링(arXiv 모델에서 `c_slippage=0.0005` 출발점).
- 시장 충격: 주문 크기 × (1/평균거래대금) 항목 추가. square-root impact model 권장.
- 펀딩/스왑: 보수적 상한선 적용.

**B. 사전 용량(Capacity) 추정**
- 전략별 **최대 AUM 추정**: 주당 거래대금의 X% 이상 거래 시 가격 왜곡. 이 한계 초과하면 전략 무효.
- 용량 초과 시 자동 축소 또는 전략 폐기.

**C. 라이브 모니터링으로 갭 측정**
- 실제 체결가 vs 백테스트 예상가 차이 추적 → "실행 갭 지표" 롤링 계산.
- 갭이 임계치 초과 시 전략 자동 중단(시장 구조 변화 신호).

**D. 자동화로 심리 제거**
- 인간 개입 최소화 = 행동 편향 회피. 단, 인간 감독은 킬스위치/재기동에만 개입(§4.4).

### 2.3 페이퍼→라이브 — autotrader 설계 원칙

> **[원칙 L1]** 백테스트 안에 비관적 slippage + 지연 분포 + 시장충격 모델 의무 포함. 비용이 0인 백테스트는 무효.
> **[원칙 L2]** 전략별 사전 용량(Capacity) 한도 설정. 초과 시 자동 축소/폐기.
> **[원칙 L3]** 라이브 체결가 vs 예측가 "실행 갭" 롤링 추적. 갭 임계 초과 시 전략 중단.

---

## 3. 포지션 사이징 (Position Sizing)

### 3.1 켈리 / 부분 켈리 (Kelly / Fractional Kelly)

**Full Kelly**: 기대 로그 성장률 최대화. `f* = p/a − (1−p)/b` (a=손실 분율, b=승리 시 추가 수익 분율).

**부분 Kelly(½, ¼)가 정답인 진짜 이유** — Thorp/Downey 시뮬레이션 결과 (Downey 2024):
1. **순수 불확실성만으로는 충분치 않다**: σ=5%일 때 최적 f가 0.40→0.38로 거의 안 바뀜. σ=20%도 0.36. 순수 불확실성은 주요 원인이 **아님**.
2. **파산 위험(risk of ruin)**: 1% 파산 확률만으로 0.80→0.46. 2%→0.39. 백분의 일의 "코인이 0이 되는" 테일 위험이 주원인.
3. **하방 백분위 최적화**: Full Kelly는 "50% 확률로 자본의 50% 드로다운" 감수. p10(10백분위) 최적화하면 0.40→0.28. "9/10 가상 세계에서 수익" 선호 → 큰 하향 조정 정당화.
4. **체계적 과대추정 방어**(Thorp): 인간은 엣지를 체계적으로 과대추정. 과소베팅(underbetting)보다 **과대베팅(overbetting)**이 더 치명적(비대칭). ½ Kelly는 성장률 25% 포기로 음의 성장률 방어.

**결론**: 부분 Kelly는 **overdetermined**(여러 이유가 중첩). 단일 이유 아님.

**한계**:
- Kelly는 **정확한 p(승률)·b(페이오프) 추정**을 전제. 추정 오차 크면 무효.
- 정규분포 가정 아님. 테일 리스크(§4)와 결합해야.
- 크립토의 극단적 변동성에서 Full Kelly = 자살.

### 3.2 변동성 타겟팅 (Volatility Targeting)

- **메커니즘**: 포지션 크기 = 목표 변동성 / 자산 변동성(ATR 또는 realized vol). 변동성 오르면 포지션 축소, 내리면 확대.
- **효과**: 일관된 위험 노출, 드로다운 완화.
- **한계(치명적)**: 변동성 **예측**이 틀리면 의미 없음. vol clustering 가정. **급변(black swan) 직전 vol이 낮으면 포지션 과대** → 2020-03, 2022-05(LUNA)에서 치명적. 변동성 타겟팅만으로 테일 방어 불가.

### 3.3 리스크 패리티 (Risk Parity)

- **메커니즘**: 각 자산/전략에 **동일 위험 기여(equal risk contribution)** 할당. 변동성 역수 가중.
- **효과**: 한 자산이 전체 위험 지배 방지.
- **한계**: 상관관계 추정에 민감. **상관관계가 스트레스 시 1로 수렴**하면(§4.4) 리스크 패리티 붕괴 — 다 같이 떨어지면 분산 효과 소멸. 레버리지 필요 시 자금조달 리스크 추가.

### 3.4 고정 분할 (Fixed Fractional)

- **메커니즘**: 자본의 고정 비율(전형 1~2%)을 trade당 위험으로 할당. 간단, 강건.
- **장점**: 추정 의존도 최소. Kelly보다 보수적 기본값.
- **한계**: 시장 체제 변화에 비적응. 변동성 급변 시 위험 노출 급변.

### 3.5 포지션 사이징 — autotrader 설계 원칙

> **[원칙 S1]** 기본은 **¼~½ Kelly + 파산 위험 조정**. 순수 Full Kelly 금지. 추정 p/b의 신뢰구간을 넓혀 보수적 f 산출.
> **[원칙 S2]** 변동성 타겟팅은 **보조**로만. 단독 사용 금지(테일 직전 vol 낮음 함정). 킬스위치와 결합 필수.
> **[원칙 S3]** trade당 위험 한도(예: 자본 0.5~1%) 하드캡 의무. 전략 간 상관관계 스트레스 테스트(상관=1 시나리오) 의무화.

---

## 4. 테일 / 파국 위험 + 드로다운 관리 / 킬스위치

### 4.1 블랙스완 / 테일 위험

- **특성**: 저확률·고영향. 수익률 분포 fat tail(첨도). 정규분포 가정 백테스트는 테일 숨김(SOPHIE Quant: "Normal 분포 생성기는 Black Swan 위험을 숨긴다").
- **LTCM(1998) 교훈**: 레버리지 × 상관관계 붕괴 → 테일 사건이 준파산으로 확대.
- **크립토 특화**: 코인 -100%(rug/hack), 거래소 파산(FTX 2022), 스테이블코인 탈피(UST 2022). "1% ruin"이 현실적.

**적용 메커니즘**:
1. **스트레스 시나리오** 시뮬레이션 — 역사적 극단 경로(2020-03, 2022-05, 2022-11 FTX, 2024-08 니꼬)에 전략 노출. 단일 역사 경로가 아닌 **시나리오 시뮬레이션**(López de Prado 권고).
2. **fat tail 모델링** — 정규분포 아닌 Student-t / 극값이론(EVT) 기반 몬테카를로.
3. **파산 확률 명시 추정** — 전략/자산별 "0이 될 확률" 추정, 사이징에 반영(§3.1 ②번).

### 4.2 강제청산 / 레버리지 리스크

- **메커니즘**: 레버리지는 테일을 **승수**로 확대. 마진콜/청산 → 영구 손실(회복 불가 경로).
- **크립토 perp 특화**: 자동 청산 엔진, 연쇄 청산(cascade). 펀딩레이트 차익이라도 청산 리스크 존재.
- **핵심**: **회복 불가 경로(path to ruin)** 회피가 성장률 최대화보다 우선. Thorp: 과대베팅 > 과소베팅 위험.

**적용 메커니즘**:
1. **레버리지 하드캡** — 자본 대비 최대 노출 한도(예: 2x). 전략이 자발적 한도보다 낮게.
2. **청산가 거리 모니터링** — 현재가 ↔ 청산가 거리의 롤링 추적. 거리 < X% 시 자동 디레버리징.
3. **연쇄 청산 감지** — 시장 전체 OI 급감 + 가격 급락 동시 발생 시 자동 축소.

### 4.3 거래소 / 컨트랙트 리스크 (크립토 특화)

**FTX(2022) 교훈** — 단일 거래소 과집중 = 파국. 2026년에도 Binance/Bybit/OKX 집중 리스크 존재. 약 50% 설문 응답자가 컨트러파티 리스크를 핵심 우려로 지목(Merkle Science).

**적용 메커니즘**:
1. **다거래소 분산** — 자본/포지션을 최소 2~3개 거래소에 분산. 단일 거래소 비중 하드캡(예: 50%).
2. **온체인 자산은 자체 커스터디** — 장기 보유분은 콜드월렛/HSM. 거래소 잔고는 실행 최소분만.
3. **출금 지연 모니터링** — 거래소별 출금 처리 시간 추적. 지연 임계 시 자동 잔고 축소.
4. **컨트랙트 리스크** — 스마트컨트랙트(deFi) 노출 시 감사 내역 + TVL 한도. 단일 프로토콜 집중 금지.

### 4.4 상관관계 붕괴 (Correlation Breakdown)

- **메커니즘**: 평시 낮은 상관관계가 **스트레스 시 1로 수렴**. 분산 효과 소멸. LTCM, 2008-09, 2020-03 모두 동일 패턴.
- **리스크 패리티·분산포트폴리오의 치명적 함정**: 평시 백테스트는 분산 효과 과대, 스트레스 시 붕괴.

**적용 메커니즘**:
1. **스트레스 상관관계(=1) 시나리오** — 백테스트에 "모든 자산이 동시에 -X% 하락" 시나리오 의무 포함.
2. **롤링 상관관계 모니터링** — 평시 상관이 급등하면 "스트레스 임박" 신호 → 포지션 축소.
3. **헤지 수단 명시** — 분산만 믿지 말고 옵션/선물 헤지 비중 사전 할당.

### 4.5 드로다운 관리 + 킬스위치 / 자동중단 / 회복

**드로다운 수학**: 25% 손실 → 33% 수익 필요 회복. 50% 손실 → 100% 수익 필요. 비선형 악화. 그래서 **드로다운 깊이 자체가 복리의 적**.

**전문가 목표**: 최대 드로다운 15~20% (Tradetron). 프로펌 킬스위치는 "규정 위반 **직전**" 발동 — 위반 후가 아님(MQL5).

**3단계 회로차단기 (autotrader 권장 구조)**:

| 단계 | 드로다운 | 액션 | 회복 조건 |
|---|---|---|---|
| L1 (경고) | 예: -5% | 신규 포지션 축소(½), 알림 발송 | 롤링 DD 0 복귀 시 자동 해제 |
| L2 (축소) | 예: -10% | 신규 진입 전면 중단, 기존 포지션 점진 청산 | 수동 검토 + 48시간 쿨다운 |
| L3 (킬스위치) | 예: -15~20% | 전면 청산·주문 차단 | 인간 승인 + **2주 이상 강제 쿨다운** |

**회복 프로토콜** (JournalPlus/TradeZella 종합):
1. **강제 쿨다운 ≥2주** — 킬스위치 발동 후 즉각 재기동 금지.
2. **전략 검토 게이트** — 재기동 전 사전 가설 점검, 비용 모델 점검, 갭 분석.
3. **점진 재기동** — ¼ 사이즈 → ½ → 풀 사이즈 단계적. 각 단계별 관찰 기간.
4. **회복 시간 추정**: 드로다운 형성 기간의 약 **3배** (5 trade 형성 시 ~15 trade 회복).
5. **재발 방지**: 동일 트리거 반복 시 킬스위치 임계치 하향(더 민감하게).

**행동 모니터링 (behavioral kill switch)** — 3forge 권고: 단순 포지션 한도 넘어 **주문 생성 빈도·취소/체결 비** 등 알고리즘 행동 패턴 모니터링. runaway 알고리즘 감지(예: 폭주 주문).

### 4.6 테일/킬스위치 — autotrader 설계 원칙

> **[원칙 R1]** 3단계 회로차단기(L1 경고/L2 축소/L3 전면중단) + 강제 쿨다운 ≥2주 + 인간 승인 재기동 의무화.
> **[원칙 R2]** 거래소/컨트랙트 분산(단일 ≤50%), 출금 지연·청산가 거리·롤링 상관관계 실시간 모니터링 → 이상 시 자동 축소.
> **[원칙 R3]** 스트레스 시나리오(상관=1, 코인 -100%, 거래소 파산) 의무 시뮬레이션. 정규분포 기반 몬테카를로 금지.

---

## 5. 검증 절차 (Validation Procedures)

### 5.1 Walk-Forward 분석 (WFA)

- **정의**: 롤링 윈도우로 학습→테스트 반복. 전략이 "하나의 운 좋은 백테스트"가 아닌 **반복 증명**.
- **Pardo(1992)** 이후 gold standard. arXiv:2512.12924: 훈련창 252일, 테스트창 63일, 스텝 63일 → 10년에 34개 독립 테스트 기간.
- **핵심**: 각 폴드는 **엄격 정보 분리** — 테스트 기간 정보가 학습에 누출되면 무효.

**arXiv:2512.12924의 현실적 결과** (엄격 WFA 후): 연 0.55% 수익, Sharpe 0.33, p-value 0.34(유의 아님), 최대 DD -2.76%. 통상적 발표 15~30%와 극단적 대비 → **엄격 검증이 성과를 얼마나 축소하는지** 보여줌.

**적용 메커니즘 (autotrader):**
1. **WFA를 기본 검증** — 단일 백테스트 결과는 보고 금지.
2. **다수 폴드**(≥30) — 10% 통계 검정력만 나와도 폴드 수 확보가 원칙. arXiv는 34폴드에서 12% 검정력 → 더 많은 폴드(국제 시장·고빈도)로 확장 권고.
3. **체제별 분해** — 저변동성 vs 고변동성, 강세 vs 약세로 성과 분할. 체제 의존성 명시.
4. **비유의 결과 정직 보고** — p-hacking 회피. "유의하지 않음"도 결과.

### 5.2 몬테카를로 시뮬레이션

단일 백테스트는 "운이 좋았던 하나의 경로". 몬테카를로는 **성과 분포**를 만든다.

**5가지 핵심 방법** (StrategyQuant 2025):

1. **MACHR Block Randomization (체제 블록 재배열)** — 연속 trade 블록(기본 5개)을 재표본. "같은 체제가 다른 순서로 왔을 때" 테스트. 체제 의존성 노출.
2. **Parameter Jitter** — 조건 누락(진입 누락 시뮬레이션) + 종가 변동. 파라미터 피크(국소 최적) 탐지.
3. **Randomly Degrade Execution** — 무작위 trade의 체결가 악화(슬리피지 모델링). 비관적 실행.
4. **Randomize SWAP (개별)** — trade별 롤오버 비용 무작위.
5. **Randomize SWAP (전체)** — 일관된 금리 환경 시나리오.

**SOPHIE Quant Blog 프레임워크** (정량 루틴):
- **Cone of Uncertainty**: 10,000 MC 시뮬레이션 → equity curve 부채꼴. 50백분위(중앙), 5백분위(불운 경계), 99백분위 DD(진짜 자본 요구량).
- **5백분위를 킬스위치 기준으로** — 라이브 성과가 5백분위 이탈 시 "깨진 것"이지 "불운"이 아님.
- **시퀀스 리스크**: 시작일 무작위화. 2010 시작 Sharpe 2.0 전략이 2008 시작에 파산할 수도.
- **"진실 혈청(Truth Serum)" 테스트**: 위상 섞기(phase shuffle) 노이즈 데이터에서 전략 성과 측정. 노이즈에서 Sharpe >1.0이면 과적합.
- **블록 부트스트랩 함정**: 트렌드 추종 전략에 IID 부트스트랩 적용하면 알파 파괴 → 리스크 과소추정. 직렬 상관 유지하는 stationary block bootstrap 사용.
- **정규분포 생성기 금지**: fat tail 숨김. 실제 수익률 재표본 또는 EVT 기반.

**적용 메커니즘 (autotrader):**
1. **5가지 MC 방법 의무화** — 각 전략마다 블록 재배열·jitter·실행 열화·비용 무작위 실행.
2. **5백분위 콘(cone)을 라이브 모니터링 기준** — 이탈 시 자동 중단.
3. **위상 섞기 "진실 혈청"** — 노이즈 데이터에서 Sharpe 임계 이상이면 전략 기각.
4. **최소 500~10,000 시뮬레이션** — 100은 부족.

### 5.3 OOS / PBO / CPCV

- **CPCV (Combinatorial Purged Cross-Validation)** — López de Prado. 교차 검증 + 레이블 누출 차단(purge). ML 전략에 필수. Arian(2024) 비교: ML 금융 검증에서 CPCV가 과적합 완화에 우월(단 WFA가 "현실적 거래 시뮬레이션"으로는 여전히 업계 표준).
- **PBO (Probability of Backtest Overfitting)** — CSCV(Combinatorially Symmetric Cross-Validation, Bailey & López de Prado 2015)로 계산. "IS(in-sample) 상위 전략이 OOS(out-of-sample) 하위로 떨어질 확률". >50%면 과적합 확정. 로직: IS 최적 파라미터의 OOS 랭킹 분포를 대칭 분할로 평가.
- **DSR(Deflated Sharpe Ratio)** — Sharpe를 (a) 다중검정·시도횟수, (b) 비정규성(왜도·첨도), (c) 트랙레코드 길이로 보정. 원래 Sharpe 대신 **항상** DSR 보고.
- **MinTRL (Minimum Track Record Length)** — 관측 Sharpe가 우연이 아님을 주장하려면 필요한 최소 기간. 높은 Sharpe 주장치나 짧은 트랙일수록 MinTRL 미달 → 신뢰 불가. 자산/전략별 추정치 사전 산출.
- **독립 베팅 수(number of independent bets)** — Sharpe의 유효 표본 크기. 자산/전략 간 상관이 높으면 "독립 베팅"이 적어 통계 유의성 급감. 홀드 주기 대비 독립성 보정 필수.

**Harvey, Liu, Zhu(2016)**: 새 팩터는 **t ≥ 3.0** 요구(종래 2.0 아님). 316개 제안 팩터 대부분 허위 가능. **Harvey(2017)**: "금융경제학 실증연구는 p-value에 과도하게 의존하며, 이는 오해되기 쉽다."

### 5.3.1 PBO 해석 가이드

| PBO | 해석 | 조치 |
|---|---|---|
| < 10% | 과적합 낮음 | 추가 검증 진행 |
| 10~50% | 과적합 중간 | 경고, 파라미터 단순화·앙상블 |
| ≥ 50% | 과적합 확정 | 전략 기각 |

### 5.4 포워드 테스트 (Forward / Live)

- **유일한 진짜 OOS** — 연구자가 holdout을 경험했으므로 "OOS"도 완전 독립 아님(Arnott et al. 2019).
- **라이브 트랙레코드** — 최소 길이(MinTRL) 도달 전까지 결과 신뢰 안 함. DSR과 결합.
- **체제 다양성 확보** — 강세·약세·고변동·저변동 모두 경과해야. 단일 체제 라이브 결과는 무의미.
- **라이브-백테스트 갭 추적** — 실제 vs 예측 지속 비교(§2.2 C).

### 5.5 검증 절차 — autotrader 설계 원칙

> **[원칙 V1]** 단일 백테스트 결과 보고 금지. WFA(≥30폴드) + MC(≥500) + PBO/DSR 의무.
> **[원칙 V2]** 5백분위 "불운 경계" 콘을 라이브 킬스위치 기준으로 사용. 라이브 성과 이탈 = "깨진 전략".
> **[원칙 V3]** 최소 트랙레코드 길이(MinTRL) + 다 체제 통과 전까지 자본 완전 배정 금지. 점진적 스케일업.

---

## 6. 통합 — autotrader 설계에 반드시 들어가야 할 원칙 (체크리스트)

> 아래는 본 조사에서 도출된 **반드시 설계에 포함해야 할 리스크/검증 원칙**을 코드/시스템 레벨로 정리한 것.

### 6.1 검증 게이트 (배정 전 통과 의무)

- [ ] **G1 — 백테스트 시도 카운터 + DSR 보고** (모든 백테스트 결과에 첨부, 시도 횟수 은폐 금지)
- [ ] **G2 — Walk-Forward ≥30폴드, 체제별 분해, 비유의 결과 정직 보고**
- [ ] **G3 — 몬테카를로 5종(블록재배열/jitter/실행열화/비용×2) ≥500회**
- [ ] **G4 — PBO/DSR 임계 통과 (과적합 확률 허용치 이하)**
- [ ] **G5 — "진실 혈청" 위상 섞기: 노이즈에서 Sharpe 임계 미만**
- [ ] **G6 — 포워드 테스트: MinTRL + 다 체제 통과 전 점진 스케일업**

### 6.2 리스크 통제 (라이브 상시)

- [ ] **R1 — 3단계 회로차단기 + 강제 쿨다운 ≥2주 + 인간 승인 재기동**
- [ ] **R2 — 거래소/컨트랙트 분산(단일 ≤50%) + 출금지연·청산가·롤링상관 모니터링 → 자동 축소**
- [ ] **R3 — 스트레스 시나리오 의무(상관=1, 코인 -100%, 거래소 파산) + fat tail MC**
- [ ] **S1 — ¼~½ Kelly + 파산위험 조정, trade당 위험 하드캡(자본 0.5~1%)**
- [ ] **S2 — 변동성 타겟팅은 보조만(테일 직전 vol 낮음 함정), 킬스위치와 결합**
- [ ] **L1 — 비관적 slippage + 지연 + 시장충격 모델 백테스트 내 의무**
- [ ] **L2 — 전략별 용량(Capacity) 한도 설정, 초과 시 자동 축소/폐기**
- [ ] **L3 — 라이브-백테스트 "실행 갭" 롤링 추적, 임계 초과 시 전략 중단**

### 6.3 정보 위생 (편향 차단)

- [ ] **B1 — 백테스트는 "나쁜 전략 거르기" 용도로만, 모델은 백테스트 전 완전 고정**
- [ ] **B2 — 사전 경제 가설(ex ante) 의무화, 데이터 마이닝 후 합리화(ex post) 금지**
- [ ] **B3 — point-in-time 정보 집합 + point-in-time 유니버스, `t+1` 체결 가정**
- [ ] **B4 — 파라미터 수 ≤3, jitter 테스트 의무, 모델 앙상블로 과적합 분산**
- [ ] **B5 — 거래 비용·수수료·펀딩 항상 포함, 비용 0 백테스트 무효**

### 6.3.1 비용·지연 모델 구체값 (시작점)

| 항목 | 보수적 시작값 | 비고 |
|---|---|---|
| 슬리피지(현물) | 5~10bp | ATR·스프레드 기반 동적 확대 |
| 슬리피지(perp/소형) | 10~30bp | 변동성 급등 시 더 보수적 |
| 체결 지연 | 1초~수 초 분포 샘플링 | 거래소·자산별 측정값 |
| 시장충격 | sqrt(주문/평균거래대금) | square-root model |
| 메이커/테이커 수수료 | 거래소 실제값 | 테이커로 비관 가정 |
| 펀딩/스왑 | 직전 N기간 평균 ×(1+버퍼) | 극단 펀딩 시나리오 추가 |

### 6.4 최우선 3원칙 (한 줄씩)

> **①  백테스트는 "나쁜 전략을 거르는" 용도로만** — 좋은 전략 증명 금지, 모델은 백테스트 전에 완전 고정, 시도 카운터 + DSR을 모든 결과에 의무 첨부(시도 횟수 은폐 = 사기).
> **②  3단계 회로차단기 + 강제 쿨다운 ≥2주 + 인간 승인 재기동** — 킬스위치는 규정 위반 "직전"에 발동되어야 의미, 위반 후가 아님; 비관적 비용·지연·시장충격 모델이 백테스트 안에 의무 포함되어야 라이브 갭이 통제 가능.
> **③  단일 백테스트 결과 보고 금지, Walk-Forward(≥30폴드) + Monte Carlo(5종 ≥500회) + PBO/DSR 의무** — 검증의 산물은 "숫자"가 아니라 "성과 분포와 5백분위 콘"이며, 라이브 성과가 이 콘을 이탈하면 "불운"이 아니라 "깨진 전랴g"으로 간주해 자동 중단.

---

## 7. 출처 (Sources)

### 1차 학술/기술 문헌
- López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. — §8.3 "The Dangers of Backtesting" (https://portfoliooptimizationbook.com/book/8.3-dangers-backtesting.html)
- Bailey, D. H., & López de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality." *Journal of Portfolio Management*, 40(5), 94–107. (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)
- Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J. (2014). "Pseudo-mathematics and financial charlatanism." *Notices of the AMS*, 61(5), 458–471.
- Bailey, D. H., Borwein, J., & López de Prado, M. (2016/2017). "The probability of backtest overfitting." *Journal of Computational Finance*, 20(4).
- Arnott, R., Harvey, C. R., & Markowitz, H. (2019). "A backtesting protocol in the era of machine learning." *J. Financial Data Science*, 1(1), 64–74.
- Harvey, C. R. (2017). "Presidential address: The scientific outlook in financial economics." *Journal of Finance*, 72(4), 1399–1440.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). "…And the cross-section of expected returns." *Review of Financial Studies*, 29(1), 5–68.
- McLean, R. D., & Pontiff, J. (2016). "Does academic research destroy stock return predictability?" *Journal of Finance*, 71(1), 5–32.
- Hou, K., Xue, C., & Zhang, L. (2020). "Replicating anomalies." *Review of Financial Studies*, 33(5), 2019–2133.
- Deep, G., Deep, A., & Lamptey, W. (2025). "Interpretable Hypothesis-Driven Trading: A Rigorous Walk-Forward Validation Framework." arXiv:2512.12924. (https://arxiv.org/html/2512.12924v1)
- Pardo, R. (2008). *The Evaluation and Optimization of Trading Strategies* (2nd ed.). Wiley.
- Thorp, E. O. "The Kelly criterion in blackjack, sports betting, and the stock market"; "Good and bad properties of the Kelly criterion."
- Downey, M. (2024). "Why fractional Kelly? Simulations of bet size with uncertainty and risk of ruin." (https://matthewdowney.github.io/uncertainty-kelly-criterion-optimal-bet-size.html)
- "Optimal Betting Under Parameter Uncertainty: Improving the Kelly Criterion." ResearchGate. (https://www.researchgate.net/publication/262425087)
- "Bayesian Kelly Criterion with Parameter Uncertainty." SSRN 6195358. (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6195358)

### 실무/도구
- StrategyQuant (2025). "5 Monte Carlo Methods to Bulletproof Your Trading Strategies." (https://strategyquant.com/blog/new-robustness-tests-on-the-strategyquant-codebase-5-monte-carlo-methods-to-bulletproof-your-trading-strategies/)
- SOPHIE Daddy Quant Blog (2025). "Monte Carlo Robustness Protocols." (https://www.sophie-ai-finance.com/articles/monte-carlo-robustness-protocols-stress-testing-systematic-trading)
- LuxAlgo (2025). "Risk Management Strategies for Algo Trading." (https://www.luxalgo.com/blog/risk-management-strategies-for-algo-trading/)
- 3forge. "Algorithm Monitoring and Kill Switches." (https://3forge.com/use-cases/regulatory-adherence/algorithm-monitor-and-kill-switches)
- MQL5. "The Prop Firm Kill-Switch: How to Stop Drawdown." (https://www.mql5.com/en/blogs/post/767321)
- Tradetron. "7 Risk-Management Techniques for Algo Traders." (https://tradetron.tech/blog/reducing-drawdown-7-risk-management-techniques-for-algo-traders)
- NYIF. "Trading System Kill Switch: Panacea or Pandora's Box?" (https://www.nyif.com/articles/trading-system-kill-switch-panacea-or-pandoras-box)
- TradingWyckoff. "Drawdown in Trading: The Definitive Guide." (https://tradingwyckoff.com/en/algorithmic-trading/drawdown-trading-guide/)
- JournalPlus. "Drawdown Management Guide." (https://journalplus.co/learn/guides/drawdown-management-guide)
- TradeZella. "Drawdown Recovery: The Math." (https://www.tradezella.com/blog/drawdown-recovery)
- Merkle Science. "Counterparty Risk in Crypto." (https://www.merklescience.com/counterparty-risk-in-crypto-understanding-the-potential-threats)
- Investopedia. "FTX Crypto Exchange Collapse: Causes, Consequences." (https://www.investopedia.com/what-went-wrong-with-ftx-6828447)
- HKMA. "Sound Risk Management Practices for Algorithmic Trading." (https://brdr.hkma.gov.hk/eng/doc-ldg/docId/getPdf/20200306-4-EN/20200306-4-EN.pdf)

### 페이퍼→라이브 갭
- Alpaca Forum. "Slippage - Paper Trading vs. Real Trading." (https://forum.alpaca.markets/t/slippage-paper-trading-vs-real-trading/2801)
- markrbest. "Paper vs Live Slippage Analysis." (https://markrbest.github.io/paper-vs-live/)
- PineConnector. "Backtesting vs Live Trading." (https://www.pineconnector.com/blogs/pico-blog/backtesting-vs-live-trading-bridging-the-gap-between-strategy-and-reality)
- Waylandz. "Execution System Guide." (https://waylandz.com/quant-book-en/Lesson-19-Execution-System/)
- OANDA. "Slippage & Execution Risk." (https://www.oanda.com/us-en/trade-tap-blog/trade-knowledge/slippage-execution-risk-in-trading/)

---

*본 문서는 autotrader 아이디에이션의 리스크/검증 축 조사 결과. 시장·자산 축(ideation-market-20260626-01.md)·전략 클래스 축(ideation-strategy-20260626-01.md)과 결합하여 IDEATION.md 종합 예정.*
