# Healthcheck 스킬 도입 전 체크포인트

**작성일:** 2026-07-02
**대상:** 매니저 생존 시스템 (healthcheck 스킬)

---

## 1. 스킬 구조 검증

### 1.1 필수 파일 존재 확인
- [x] `~/.claude/skills/healthcheck/SKILL.md` 존재
- [ ] `SKILL.md` YAML frontmatter 정상 (name, description)
- [ ] description이 명확하게 "언제 사용하는지" 명시

### 1.2 리소스 파일 연결
- [ ] `~/scripts/healthcheck/` 모든 스크립트 실행 가능
- [ ] `recovery_middleware.py` import 오류 없음

---

## 2. 단위 테스트 (Unit Tests)

### 2.1 bot-healthcheck.sh (light mode)
```bash
~/scripts/healthcheck/bot-healthcheck.sh --mode light
```
- [ ] 환경 변수 없을 때 emergency 파일 작성
- [ ] 환경 변수 있을 때 정상 종료
- [ ] 로그 파일 정상 기록 (`~/scripts/healthcheck/healthcheck.log`)

### 2.2 emergency-write.sh
```bash
~/scripts/healthcheck/emergency-write.sh "테스트" "테스트 작업"
```
- [ ] emergency 파일 atomic write 확인
- [ ] 파일 내용 형식 확인
- [ ] 시간대 정상 (KST)
- [ ] 테스트 후 정리: `rm ~/notes/emergency-*.md`

### 2.3 llm-probe.sh
```bash
~/scripts/healthcheck/llm-probe.sh --provider anthropic
```
- [ ] API 키 없을 때 에러 처리
- [ ] API 키 있을 때 HTTP 코드 반환
- [ ] timeout 10초 동작

### 2.4 recovery_middleware.py
```python
python3 ~/scripts/healthcheck/recovery_middleware.py
```
- [ ] 테스트 실행 (모듈 내부 테스트)
- [ ] 에러 분류 정상 (429/529/quota)
- [ ] emergency 파일 작성 확인

---

## 3. 통합 테스트 (Integration Tests)

### 3.1 스킬 호출 테스트
```
/healthcheck --mode light
```
- [ ] Claude가 스킬을 인식하는지 확인
- [ ] 스킬이 정상 실행되는지 확인
- [ ] 결과가 사용자에게 명확히 전달되는지 확인

### 3.2 LLM 호출 실패 시나리오
**mock으로 429/529 강제 주입:**
- [ ] recovery_middleware가 에러를 감지하는지
- [ ] 폴백 로직이 동작하는지 (Haiku → Opus → 읽기 전용)
- [ ] emergency 파일이 작성되는지

### 3.3 복구 절차 테스트
1. 장애 발생 시켜 emergency 파일 작성
2. `/clear` 로 세션 정리
3. emergency 파일 확인
4. work-queue.md에서 작업 재개
- [ ] 모든 단계가 순서대로 동작하는지

---

## 4. 각 봇 온보딩 테스트

### 4.1 매니저 (heav_lnx)
- [ ] 첫 세션에서 onboarding.md 읽기
- [ ] manager-recovery-principle.md 읽기
- [ ] healthcheck 스킬 인지
- [ ] recovery_middleware 통합

### 4.2 RPG 팀장 (heav_lnx_rpg)
- [ ] 첫 세션에서 onboarding.md 읽기
- [ ] manager-recovery-principle.md 읽기
- [ ] healthcheck 스킬 인지
- [ ] recovery_middleware 통합

### 4.3 Trader 팀장 (heav_lnx_trader)
- [ ] 첫 세션에서 onboarding.md 읽기
- [ ] manager-recovery-principle.md 읽기
- [ ] healthcheck 스킬 인지
- [ ] recovery_middleware 통합

### 4.4 Scenario 팀장 (heav_lnx_scenario)
- [ ] 첫 세션에서 onboarding.md 읽기
- [ ] manager-recovery-principle.md 읽기
- [ ] healthcheck 스킬 인지
- [ ] recovery_middleware 통합

---

## 5. 운영 환경 검증

### 5.1 환경 변수 확인
- [ ] `ANTHROPIC_API_KEY` 설정됨
- [ ] `COKACDIR_KEY` 설정됨
- [ ] `TELEGRAM_CHAT_ID` 설정됨 (선택)
- [ ] `TELEGRAM_BOT_TOKEN` 설정됨 (선택)

### 5.2 디스크 공간 확인
```bash
df -h ~/notes
```
- [ ] 최소 100MB 여유 공간

### 5.3 권한 확인
```bash
ls -la ~/scripts/healthcheck/
```
- [ ] 모든 스크립트에 실행 권한 (chmod +x)

---

## 6. Cron 설정 전 검증

### 6.1 full mode 테스트
```bash
~/scripts/healthcheck/bot-healthcheck.sh --mode full
```
- [ ] LLM 호출이 정상 동작하는지
- [ ] 레이트 리밋 감지가 동작하는지

### 6.2 cron 테스트 (1회 실행)
```bash
# 테스트: 1분 후 실행
echo "sleep 60 && ~/scripts/healthcheck/bot-healthcheck.sh --mode full" | at now
```
- [ ] cron이 정상 실행되는지
- [ ] 로그가 기록되는지

### 6.3 cron 등록 (실제)
```bash
crontab -e
```
```
*/5 * * * * /home/ubuntu/scripts/healthcheck/bot-healthcheck.sh --mode full
```
- [ ] cron 등록 완료
- [ ] 5분 후 첫 실행 확인

---

## 7. 장애 복구 훈련 (Disaster Recovery Drill)

### 7.1 시나리오 1: 레이트 리밋 (429)
- [ ] mock으로 429 발생
- [ ] 각 봇이 스스로 감지
- [ ] emergency 파일 작성
- [ ] 복구 절차 수행

### 7.2 시나리오 2: 할당 초과 (quota exceeded)
- [ ] mock으로 quota exceeded 발생
- [ ] 재시도 금지 동작
- [ ] emergency 파일 작성
- [ ] 복구 절차 수행

### 7.3 시나리오 3: 서비스 과부하 (529)
- [ ] mock으로 529 발생
- [ ] 짧은 backoff 후 재시도
- [ ] 재시도 초과 시 emergency 작성
- [ ] 복구 절차 수행

---

## 8. 문서 완성도 확인

### 8.1 필수 문서 존재
- [x] `manager-recovery-principle.md` 완성
- [x] `onboarding.md` 업데이트 (skillify 방법론)
- [x] `healthcheck/SKILL.md` 완성
- [x] `~/scripts/healthcheck/README.md` 완성
- [x] `manager-survival-implementation-8d.md` 완성
- [ ] `healthcheck-deployment-checklist.md` (이 파일)

### 8.2 사용자 가이드
- [ ] 이사님용 빠른 참조 카드
- [ ] 팀장용 단계별 가이드

---

## 9. 성공 기준 (Acceptance Criteria)

### 9.1 기능적 요구사항
- [ ] 모든 봇이 레이트 리밋을 스스로 감지
- [ ] emergency 파일이 atomic하게 작성
- [ ] 복구 절차가 명확하고 실행 가능

### 9.2 비기능적 요구사항
- [ ] light mode 실행 시간 < 1초
- [ ] full mode 실행 시간 < 10초
- [ ] emergency 파일 크기 < 10KB
- [ ] 로그 파일이 disk를 과도하게 점유하지 않음

### 9.3 신뢰성 요구사항
- [ ] 장애 발생 시 99% 확률로 emergency 작성
- [ ] 거짓 양성 (false positive) < 1%
- [ ] 거짓 음성 (false negative) < 1%

---

## 10. 롤백 계획 (Rollback Plan)

### 10.1 롤백 트리거
- [ ] emergency 파일이 정상 작성되지 않음
- [ ] 스킬 호출이 실패함
- [ ] 봇이 crash를 반복함
- [ ] 성능 기준 미달

### 10.2 롤백 절차
1. 스킬 삭제: `rm -rf ~/.claude/skills/healthcheck`
2. onboarding.md 되돌리기
3. 기존 방식(수동 복구)으로 복귀
4. 원인 분석 및 재수정

---

## 11. 도입 결정 (Go/No-Go)

### 11.1 Go 조건 (모두 충족 시 도입)
- [ ] 단위 테스트 100% 통과
- [ ] 통합 테스트 100% 통과
- [ ] 각 봇 온보딩 완료
- [ ] 운영 환경 검증 완료
- [ ] 장애 복구 훈련 완료
- [ ] 문서 완성도 100%

### 11.2 No-Go 조건 (하나라도 있으면 보류)
- [ ] 단위 테스트 실패
- [ ] emergency 파일 작성 실패
- [ ] 봇 crash 반복
- [ ] 성능 기준 미달
- [ ] 거짓 양성/음성 비율 높음

---

## 12. 도입 후 모니터링 (Post-Deployment)

### 12.1 첫 24시간
- [ ] emergency 파일 생성 횟수 모니터링
- [ ] 각 봇 응답 시간 모니터링
- [ ] 로그 파일 크기 모니터링
- [ ] 이사님 피드백 수집

### 12.2 첫 1주일
- [ ] 일일 healthcheck 리포트
- [ ] 장애 발생 시 즉시 대응
- [ ] 개선 사항 반영

---

## 우선순위별 실행 순서

### Phase 1: 기본 검증 (즉시)
1. 스킬 구조 검증 (1.1, 1.2)
2. 단위 테스트 (2.1, 2.2, 2.3, 2.4)

### Phase 2: 통합 테스트 (Phase 1 완료 후)
1. 통합 테스트 (3.1, 3.2, 3.3)
2. 운영 환경 검증 (5.1, 5.2, 5.3)

### Phase 3: 각 봇 온보딩 (Phase 2 완료 후)
1. 각 봇 온보딩 테스트 (4.1 ~ 4.4)

### Phase 4: 운영 투입 준비 (Phase 3 완료 후)
1. Cron 설정 전 검증 (6.1, 6.2)
2. 장애 복구 훈련 (7.1, 7.2, 7.3)
3. 문서 완성도 확인 (8.1, 8.2)

### Phase 5: 도입 결정 (Phase 4 완료 후)
1. 성공 기준 확인 (9.1, 9.2, 9.3)
2. Go/No-Go 결정 (11.1, 11.2)

---

## 참고 문헌

- [Software Deployment In 2026: 7 Strategies & 5 Steps With Checklist](https://octopus.com/devops/software-deployments/)
- [Software Deployment in 2026: Strategies & Best Practices](https://keploy.io/blog/community/software-deployment)
- [An Ultimate Software Deployment Checklist to Use in 2026](https://www.spaceo.ca/blog/software-deployment-checklist/)
