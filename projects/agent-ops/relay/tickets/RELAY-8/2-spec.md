---
jira: RELAY-8
title: 검증 워크벤치 — 조합 JSON·아웃풋 열람 + 승인→자산화
author: arcade (aws-arcade)
date: 2026-08-19
stage: 2-정제 (초안 — manager 승인 대기)
---

# [spec] 요구사항 정제 — 검증 워크벤치

## 배치 결정 (arcade 판정, director "ㅇㅇ" 확정 2026-08-19)

**아케이드(8010) 확장안** 채택. 근거:
1. 카드→상세→JSON 뷰어(20,000자 페이지읽기)→diff→검토 게이트 골격이 이미 존재
2. publication workbench의 "미리보기→사람 판정→잠긴 publish" 8단계 패턴을
   승인→자산화 흐름에 동일 적용 (미승인 자산화 금지 원칙 보존)
3. 8013 데이터는 read-only 연결 — Arcade가 RISU 운영 데이터에 쓰지 않음

## 데이터 소스 (asset_agent 실측 + arcade 재실측 일치)

- `RISU 8013 request-logs.db > requests` 테이블
- 컬럼: timestamp, chat_id, model, success, duration_ms, input/output_tokens,
  request_headers(API키 `[REDACTED_API_KEY]` 자동마스킹 확인), request_body(조합
  프롬프트 전문), response_body(출력 전문·thinking 포함)
- 현재 5건은 짧은 테스트 호출 — 화면 검증엔 실사 1배치(RP 완주) 데이터 필요

## 측정 가능한 완료 조건 (개조식)

화면 — 자산 카드 → 실사 검증 탭:

1. **조합 JSON 뷰어**: chat_id 선택 시 request_body를
   ① 구조 트리(messages/system/파라미터별 접기) ② 원문 전문 뷰로 전환 표시
2. **아웃풋 전문**: response_body를 thinking/assistant 구분 없이 전문 표시,
   기존 카드 JSON 뷰어와 동일한 20,000자 페이지 읽기 + SHA-256 digest
3. **3줄 요약**: 전문 위에 고정 3줄 요약 (모델·토큰·소요시간 + 내용 첫 줄)
4. **승인 판정**: 카드당 O / X / ? 버튼 → 승인 요청 레코드 저장
5. **자산화 연결(잠금 게이트)**: O 판정이어도 자산화 버튼은 잠김 —
   people-approval receipt(ADR-0006 materializer) 없으면 실행 불가.
   잠금 해제 조건은 기존 publication workbench 게이트와 동일
6. **API**: `GET /api/arcade/verification/sessions` (chat_id 목록),
   `GET /api/arcade/verification/{chat_id}` (조합+아웃풋),
   `POST /api/arcade/verification/{chat_id}/verdict` (O/X/? 기록)
7. **보안**: 8013 DB 파일은 읽기 전용 모드(uri `mode=ro`)로만 오픈.
   REDACTED 헤더는 화면에도 그대로 마스크 처리. 응답에 원본 헤더 미포함
8. **회귀**: 기존 13개 unittest 전부 통과 유지 + 신규 워크벤치 테스트 추가

## 명시적 비목표 (하지 않을 것)

- RISU 8013 데이터에 대한 쓰기·삭제 (read-only)
- 승인 자동화 — O/X/? 판정은 사람만(텔레그램 승인 카드와 동일 원칙)
- NAI 이미지 미리보기 (RELAY-8 범위 밖, 후속 카드)
- 채팅 화면 재현(롤플레이 UI) — 워크벤치는 열람·승인만
- 신규 서비스/신규 포트 — 8010 아케이드 안에 탭으로 추가

## 전제 조건/의존성

- 실사 배치 데이터 1세트 이상 (asset_agent가 8013에서 RP 완주 후 chat_id 제공)
- 8013 request-logs.db 파일 경로는 환경변수로 주입 (코드에 하드코딩 금지)
- 승인 → 자산화 materializer 연동은 asset_agent `reviews/telegram_approval_batches/`
  체계 재사용 (신규 포맷 발명 금지)

## 모호 용어 정의

- **조합 JSON**: RISU가 해당 턴에 LLM에게 보낸 request_body 전문 (시스템 프롬프트 +
  로어북·모듈이 전개된 상태). "어떤 자산이 어떻게 조합됐는지"의 정본
- **아웃풋 전문**: response_body의 content 전체 (thinking 블록 포함)
- **3줄 요약**: 모델명·토큰·소요시간 1줄 + 응답 첫 문장 1줄 + chat_id·시각 1줄.
  LLM 요약이 아니라 규칙 기반 추출 (검증 대상을 LLM으로 요약하면 순환)
- **승인(O/X/?)**: TELEGRAM-APPROVAL-CARD-SPEC 문법과 동일 — O 승인, X 거절,
  ? 보류. 판정 주체는 이사님(owner Telegram ID 검증은 materializer 담당)

## 화면 레이아웃 (초안)

```text
┌ 아케이드 카드 상세 ────────────────────────────────┐
│ [카드 JSON] [비교] [장착] [실사 검증 ←신규]          │
├──────────────────────────────────────────────┤
│ ▼ 실사 세션 (chat_id 드롭다운 — 턴 목록)              │
│ ┌─────────────┬──────────────────────────┐ │
│ │ ① 조합 JSON  │ ② 아웃풋                  │ │
│ │ [트리|원문]  │ 전문 + SHA + 20k 페이지읽기  │ │
│ │ system ☜    │ ── 3줄 요약 (고정) ──      │ │
│ │ messages ☜  │ glm-5.2 · in 0 · out 0    │ │
│ │ params ☜    │ "안녕하세요. 저는…"          │ │
│ └─────────────┴──────────────────────────┘ │
│ [O 승인] [X 거절] [? 보류]   [자산화 🔒(잠김)]     │
│ 최근 판정: review-xxxx · pending_human_review      │
└──────────────────────────────────────────────┘
```

- 좌우 2패널(조합/아웃풋) + 하단 판정 바 — 기존 publication workbench
  4패널 구조와 같은 디자인 언어
- 잠긴 자산화 버튼: "사람 승인 receipt 필요" 툴팁 (기존과 동일)

---
update: 2026-08-19 (방향 전환 — arcade)

director 결정으로 검증 워크벤치는 아케이드 확장이 아니라 **독립 웹 8015**
(RELAY-9, matrix-workbench + MongoDB)로 간다. 본 spec의 아케이드 확장안은
**폐기**. 승인 게이트·read-only·헤더 마스킹 등 보안 원칙은 8015에도
그대로 적용되어야 한다 (이식 요구사항으로 남김).

arcade는 RELAY-8 범위에서 빠지고 아케이드 본연 작업(데이터 재연결·30셋
동결 해제)로 복귀. 실사 데이터는 workbench MongoDB에서 읽는다.
