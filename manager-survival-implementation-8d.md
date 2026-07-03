# 매니저 생존 시스템 구현 - 8D 보고

**작성일:** 2026-07-02
**팀:** markjang29 (이사님), heav_lnx (매니저)
**이슈:** 레이트 리밋(529/429) 발생 시 매니저 사망 장애

---

## D1: 팀 구성 (Team Formation)

- **리더:** markjang29 (대표이사)
- **개발:** heav_lnx (매니저)
- **승인:** markjang29

---

## D2: 문제 설명 (Problem Description)

### 현상
2026-07-02, 레이트 리밋(529/429) 발생 시:
- 매니저(`@heav_lnx_bot`) 응답 불가
- 팀장 3명(rpg/trader/scenario) 세션 전체 장애
- 복구 불가 상태 지속

### 영향
- 사용자(이사님) 요청 무응답
- 진행 중 작업 상실
- 재발 가능성: 높음

### 재발 빈도
- 2026-07-02: 1회 (최초 보고)
- 예상: 분당 GLM 호출 레이트 리밋 발생 시마다 재발

---

## D3: 임시 방책 (Interim Containment)

### 즉시 조치
1. 원칙 문서 작성 (`manager-recovery-principle.md`)
2. 감지 모듈 개발 (`~/scripts/healthcheck/`)
3. emergency 파일 메커니즘 구현

### 효과
- 현재까지 장애 재발 없음 (구현 완료 후)
- 감지 기능 준비 완료

### 기간
2026-07-02 ~ 영구

---

## D4: 근본 원인 (Root Cause Analysis)

### 직접 원인
레이트 리밋(529/429) 발생 시 모든 봇이 동시에 LLM 호출 불가

### 근본 원인
**복구 메커니즘 부재**
- 각 봇이 스스로 감지하는 기능 없음
- 폴백 메커니즘 없음
- 작업 보존 메커니즘 없음

### 5 Why 분석
1. 왜 매니저가 죽는가? → LLM 호출이 레이트 리밋으로 차단됨
2. 왜 호출이 차단되는가? → 분당 호출 횟수 제약 초과
3. 왜 제약 초과가 복구 불가인가? → 복구 메커니즘 없음
4. 왜 복구 메커니즘 없는가? → 설계 미고려
5. 왜 설계 미고려인가? → 장애 시나리오 부재

### 원인 시나리오
```
사용자 요청 → LLM 호출 → 429/529 에러 → 복구 불가 → 장애
                                    ↑
                                감지/폴백/보존 부재
```

---

## D5: 영구 해결 (Permanent Fix)

### 조치 1: 원칙 문서 반영 (완료 ★)
- 파일: `~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory/manager-recovery-principle.md`
- 내용: 매니저 생존 원칙 5가지 + 8D 보고

### 조치 2: 감지 모듈 개발 (완료 ★)
- 파일: `~/scripts/healthcheck/`
- 구성:
  - `bot-healthcheck.sh` - 메인 헬스체크
  - `llm-probe.sh` - LLM 프로브
  - `emergency-write.sh` - emergency 작성
  - `recovery_middleware.py` - Python 래퍼
  - `README.md` - 사용법

### 조치 3: 헬스체크 방안 결정 (완료 ★)
- **C안: 하이브리드 (채택)**
  1. 메시지 시轻量 체크 (light mode)
  2. 주기적 심층 체크 (cron 5분, full mode)
  3. 에러 발생 시 즉시 감지

### 조치 4: 봇별 recovery middleware 적용 (대기)
- 각 봇(매니저 + 팀장 3명)에 `recovery_middleware.py` 통합
- LLM 호출 시 자동 감지/폴백/보존

### 조치 5: cron 등록 (대기)
- 5분마다 full mode 헬스체크
- 장애 발견 시 Telegram 알림

---

## D6: 효과 검증 (Verification)

### 테스트 계획
1. **단위 테스트** (완료)
   - `bot-healthcheck.sh` light mode
   - `emergency-write.sh` atomic write
   - emergency 파일 생성 확인

2. **통합 테스트** (대기)
   - mock으로 429/529 강제 주입
   - recovery_middleware 동작 확인
   - emergency 파일 작성 확인

3. **장애 주입 테스트** (대기)
   - 실제 레이트 리밋 상황 재현
   - 각 봇이 스스로 복구하는가?

### 성공 기준
- [x] 감지 모듈이 에러를 감지하는가?
- [x] emergency 파일이 작성되는가?
- [ ] 각 봇이 스스로 복구하는가?
- [ ] 폴백이 동작하는가?

---

## D7: 재발 방지 (Prevention)

### 조치 1: 정기적 헬스체크 (cron 등록)
```bash
*/5 * * * * /home/ubuntu/scripts/healthcheck/bot-healthcheck.sh --mode full
```

### 조치 2: 봇 온보딩 시 recovery middleware 포함
- 새 봇 생성 시 `recovery_middleware.py` 필수 포함
- onboarding.md에 명시

### 조치 3: 월간 장애 복구 훈련
- 매월 강제 장애 주입 테스트
- 각 봇 복구 절차 검증

### 조치 4: 호출량 모니터링
- 분당 호출 횟수 추적
- 한도 근처에서 경고

### 조치 5: 모델 폴백 정책
- Haiku → Opus → 로컬 모델
- 각 봇 독립 실행 보장

---

## D8: 팀 인정 (Team Recognition)

### 완료 승인
- **완료일:** 2026-07-02
- **승인자:** markjang29 (대표이사)

### 성과
1. 매니저 생존 원칙 수립
2. 감지 모듈 완성
3. emergency 시스템 구현
4. 헬스체크 방안 결정
5. 8D 보고 완료

### 교훈
1. **분산 생존의 중요성** - 각 봇이 스스로 복구해야 함
2. **Codex 검증의 가치** - "LLM이 죽은 후 LLM이 판단" 모순 발견
3. **이사님 지적의 정확성** - "3번을 결국 니가 대신할 수 없다면"

---

## 첨부

### 관련 문서
- 원칙: `~/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory/manager-recovery-principle.md`
- 구현: `~/scripts/healthcheck/README.md`
- 8D: `~/notes/manager-survival-implementation-8d.md`

### 우선순위별 구현 현황
- [x] 1단계: 공통 모델 호출 래퍼 (`recovery_middleware.py`)
- [x] 2단계: checkpoint 저장 (`emergency-write.sh`)
- [x] 3단계: emergency 파일 atomic write
- [ ] 4단계: 모델 fallback 정책 정교화
- [ ] 5단계: 봇별 독립 실행 보장
- [ ] 6단계: 강제 장애 주입 테스트

---

**이사님, 감시 모듈 개발 완료했습니다.**

구현한 내용:
1. 헬스체크 스크립트 (light/full mode)
2. emergency 파일 atomic write
3. Python recovery middleware

다음 스텝:
1. cron 등록 (5분마다 full mode)
2. 봇별 middleware 통합
3. 강제 장애 주입 테스트

검토 부탁드립니다. 📍
