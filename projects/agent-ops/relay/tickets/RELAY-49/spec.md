# [spec] RELAY-49 통합 파이프라인 — 4단계 캡슐화·7단계 CLI 하네스 확정판

- jira: RELAY-49 · 작성: zcode(SE) · 근거: req.md (이사님 08-24 승인 방향 결정 5항)
- 상위 정본: `relay/PIPELINE-ARCHITECTURE.md` (v1, e74fe84) — 본 spec은 그 4·7단계를 계약 수준으로 확정

## 1. 용어 분리 (전 봇 공통 — 혼용 금지)

| 용어 | 정의 | 위치 |
|---|---|---|
| **매트릭스화 (S3)** | 자산 캡슐화 — 승인 자산을 매트릭스 정본 캡슐로 변환·등록 | Git (matrix_asset_agent) |
| **매트릭스 코어 (S6)** | CLI 하네스 — 클로드코드류 CLI 본체 (matrix_codex 뼈대) | matrix_codex |

## 2. S3 매트릭스화 = 자산 캡슐화 계약

**입력**: approval 레코드 (matrix-human-approval-v1, 이사님 판정 서명 포함) + 삼중보관 자산(risu-native-harness-v1 / semantic projection / self-contained fixture, ADR-0005)

**변환 (materializer 자동, 서명 대리)**:
```text
approval.service    → capsule 스키마 검증 (matrix-asset-release-v1)
                    → provenance 주입: 실사 SHA-256 + 플랜 id + 판정 영수증
                    → matrix_components.ndjson append + lock manifest commit
출력: release ID (불변) — 아케이드·8011/8012의 유일한 참조 키
```

**검증 게이트 (게이트 통과 못하면 release 불가)**:
1. 스키마 검증: 승인 17필드 + 삼중보관 3본 존재 + SHA 일치
2. 서명 검증: publisher-only key hmac (봇은 대리 서명만)
3. 정합성: capsule ↔ components ↔ lock manifest 상호 참조 일치
4. 소비자 확인: 아케이드가 release ID 1건 읽어 "미검토 아님" 표시 (S4 도입 검사)

**비목표**: 요약 재생성·자동 승격·원본 JSON 병합 — 전부 금지 유지.

## 3. S6 매트릭스 코어 = CLI 하네스 계약 (matrix_codex 뼈대 재사용)

### 3.1 통합점 8종 (이사님 구상 → 계약)
| 기능 | 계약 | 재사용 |
|---|---|---|
| Interactive REPL | 프롬프트 대기·멀티라인·히스토리 | matrix_codex command bus |
| prompt 실행 모드 | `-p` 원샷 — 브리지·크론 소비 | 기존 |
| 내장도구 | 파일·검색·셸·웹 — 권한 게이트 경유 | 기존 + approval-board 연동 |
| RAG | 매트릭스 캡슐(release) 검색 — 벡터+정확키 혼합 | MemoryBank 저장소 공유 |
| MCP | 도구 프로토콜 — 외부 서비스 슬롯 | 신규 |
| LSP | 코드 지능 — TRACK-4 작품 개발용 | 신규 |
| 세션관리 | 세션 저장·resume·compact (300k 규칙) | 전 봇 공통 정책 |
| 자동 컨텍스트·에러복구 | ContextManager + IterationGuard가 담당 | 노드 9종 참조 |

### 3.2 노드 9종 스위치형 계약 (Triage 3분류가 첫 관문)

| 노드 | 책임 | direct | simple | complex |
|---|---|---|---|---|
| **Triage** | 입력 3분류 | ✅ 항상 | ✅ 항상 | ✅ 항상 |
| **HierarchicalPlanner** | 명시적 다단계 계획 | ❌ | △ 1단계 | ✅ 다단계 |
| **Verifier** | 결과 별도 검증 | ❌ | ✅ 1회 | ✅ 단계별 |
| **Reflection** | 10종 실패 패턴 감지·전략조정 | ❌ | ▷ 실패 시 | ✅ |
| **Debate** | process/critic/resolver 3역 토론 | ❌ | ❌ | ✅ |
| **MemoryBank** | 작업 경험 벡터 저장·회상 | ▷ 읽기 전용 | ✅ | ✅ |
| **ToolLearningSystem** | 패턴 학습 후 도구 추천 | ❌ | ▷ 학습만 | ✅ |
| **ContextManager** | 토큰 능동 최적화 | ▷ 계산만 | ✅ | ✅ |
| **IterationGuard** | 최대 반복 횟수 제한 | ✅ 상수 | ✅ | ✅ (예산 계약) |

✅ 가동 ▷ 조건부/축소 △ 축소판 ❌ 미가동

**"단일 에이전트+얇은 하네스" 원칙과의 조정** (req 방향결정 4항): 기본 골격은 단일 에이전트.
complex 경로에서만 노드 전체가 켜지는 **스위치형** — 노드는 별도 프로세스가 아니라
같은 명령 안의 검사 단계로 구현. 그래프 확장(다중 작업자)은 금지 유지.

### 3.3 경로별 완료 기준 (MATRIX.md 상속)
- 시작 전 고정: 최대 모델 호출·토큰·시간·자동 교정 횟수
- direct/simple: "상태 변경+검사 종료" 즉시 완료. complex: Verifier+Reflection 통과 후 완료
- 잘못된 JSON 재요청은 생성 명령 1회 한결 유지

## 4. 8018 홈 갱신 사항
- S3 카드: "매트릭스화 = 자산 캡슐화 (approval→release)" 문구 확정
- S6 카드: "코어 = CLI 하네스 (REPL·RAG·MCP·LSP·노드 9종 스위치형)" 문구 확정
- 로드맵 페이지에 노드 9종 표·경로 표기 추가

## 5. 완료 기준 (본 spec)
1. 본 문서 push + 매니저 관제그룹 보고 ✅
2. 8018 홈 갱신 배포 (별도 커밋)
3. S3 구현은 TRACK-A 티켓으로, S6 구현은 TRACK-3 티켓으로 분리 — 본 spec이 양쪽의 계약 정본
