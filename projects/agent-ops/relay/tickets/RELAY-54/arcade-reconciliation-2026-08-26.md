---
jira: RELAY-54 (Jira 404 — gap 유지, 완료 처리 안 함)
bot: arcade (aws-arcade)
date: 2026-08-26
basis: site-reconciliation-ledger-2026-08-26.md @ 8801615 + AWS ZCode 대화 100건 기준 보조 문서 + 라이브 실측
---

# arcade 담당 사이트·산출물 정합성 판정

판정 근거는 전부 2026-08-26 라이브 실측이다. 기존 기능 삭제·임시 우회 없음.

## 8004 arcade-playable — 판정: 부분구현

확인된 구현 (실측):
- 서비스 응답: 내부/외부 HTTP 200
- user systemd 유닛 `arcade-playable.service` 등록·enabled,
  drop-in `relay-ticket.conf`로 `RELAY_TICKET=RELAY-44` 주입 — 라이브
  프로세스 env에서 직접 확인
- port-registry `registered` 목록에 8004 → RELAY-44 사후등록 기록 존재
- 콘텐츠: "PLAYABLE 자산화 보고서" 페이지 (일정·카테고리별 자산 총량·
  Codex 승격 게이트 표시)

gap (검증·미완):
- RELAY-44가 여전히 `relay:1-확보` — 소급등록 티켓 자체의 단계 전이 안 됨
  (매니저 게이트. Jira 404 목록엔 없지만 완료 처리 근거 없음)
- `/api/status` 등 API 표면 404 — 보고서 정적 페이지는 응답하지만
  프로그래밋 검증 경로가 없어 "사이트 응답≠요구사항 완료" 경고에 해당
- 5단계 본연 기능(매트릭스화 자산의 실사용 품질 시험)은 상류 4단계
  매트릭스화가 구상 중이라 **재테스트 대상 자산이 아직 없음** —
  파이프라인 자리는 유효, 실제 시험 운영은 미시작
- directive 43 "리수 자산 분류 → 아케이드 연결" 요구는 분류 체계가
  asset_agent 설계 대기 상태라 연결 시작 못함

## 8010 arcade (matrix-engine) — 판정: 부분구현 (기능 유지, 데이터 동결)

확인된 구현 (실측):
- systemd `matrix-web.service` v0.3.0, 외부 `/arcade` HTTP 200
- 카드 JSON 조회·publication workbench 카나리(49ddfe3/488f0e0) 유지
- matrix_asset_agent repository guard 테스트 6/6 통과

gap:
- 데이터 30셋 동결(08-14) → 최신 카탈로그(1,066)·8011(1,271) 미연결
  — 매니저 티켓 대기 중 (미발행)
- 모듈/LORE 요약 보강·캐릭터 제목 보강 미완 (producer 근본 수정
  95270ea·캡슐 복원 a713eb9는 push 완료 상태)
- 8010은 7단계 파이프라인 공식 사이트 표에 없음 — 폐기 지시를 받은
  적 없으므로 유지하나, 토폴로지상 위치(8004와의 관계) 확정 필요

## 산출물 (Arcade 세션 커밋 전부 push 완료)

- scenario 95270ea — producer risup 중첩 봉투 결함 수정 (175만 자 회수 기반)
- scenario a713eb9 — 누락 캡슐 3건 복원 (haru 포함, ingress digest 계약 준수)
- notes-registry 0df357c → cb7a128 — RELAY-8 확장안 spec 작성 후 방향전환
  폐기 기록 (독립 웹 8015로 이관, 보안 3원칙 이식 요구 명시)
- matrix-engine 49ddfe3/488f0e0 — publication workbench 카나리 (타 세션,
  수신·검증만 함)

## 남기는 gap 요약

1. RELAY-44 단계 전이 (매니저 게이트)
2. 아케이드 데이터 재연결 티켓 미발행 (매니저 1-확보 대기)
3. 8004 API 검증 경로 부재 — 재테스트 운영 시작 시 스펙 필요
4. 8010의 파이프라인상 위치 미확정 — 매니저 조율 필요
5. RELAY-35/41/50/54/55/56 Jira 404 — 본 판정 문서도 RELAY-54 소속이므로
   완료 처리하지 않고 gap으로 둔다
