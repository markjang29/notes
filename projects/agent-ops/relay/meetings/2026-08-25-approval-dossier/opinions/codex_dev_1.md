# codex_dev_1 의견 — 승인 다ossier 자동 생성 기술 리스크

근거: `APPROVAL-DOSSIER-PROPOSAL.md` @ `c09c9928b496d9484faf08b181befa8f474db780`, `PIPELINE-ARCHITECTURE.md`, RELAY-8/35/49 계보. 승인 대상은 실존 `matrix-source-unit-v1`에서 파생된 자산으로 한정하며 봇 생성 예시는 근거로 승격하지 않는다.

## 낙관 근거

- 기존 자산 ID 흐름은 이미 `sha256(원본) → source-unit → workbench plan → approval → release`를 지향한다. 따라서 새 시스템 전체를 발명하기보다 이 ID를 ①리수 셋업, ②3회 채팅 전문, ③NAI 프롬프트·결과, ④GATE 결과, ⑤활용도 산출, ⑥액션 링크, ⑦승인에 관통시키면 자동 조립이 가능하다.
- 8015는 플랜·자산·3회 채팅 전문, 8016은 이미지 매니페스트, 승인보드는 판정이라는 실존 경계가 있다. 각 서비스가 증거 manifest를 내고 다ossier 조립기가 읽기만 하는 구조면 운영 서비스에 대한 결합과 쓰기 권한을 줄일 수 있다.
- “다ossier 완성 후 승인”은 UI 관례가 아니라 상태기로 강제할 수 있다. 완성 manifest digest에 승인을 묶고 동일 digest만 release가 받게 하면, 승인 선행 및 승인 후 바꿔치기를 기술적으로 차단한다.

## 비관 근거

- 현재 가장 큰 위험은 분산 트랜잭션이다. 8015 채팅은 성공했지만 NAI가 실패하거나, GATE 중 검사기 버전이 바뀌거나, 재시도로 동일 자산에 중복 실행이 생길 수 있다. 단순히 7개 링크의 존재만 검사하면 서로 다른 실행·source-unit의 결과가 한 카드에 섞인다.
- ① 셋업은 카드·모듈·로어·모델의 버전과 실제 request body가 고정되지 않으면 재현 불가다. ② “3회”는 동시 실행·선별 실행·부분 전문 저장에 따라 의미가 달라지며 실행 ID, seed/모델, 오류·중단까지 남기지 않으면 좋은 결과만 고르는 편향이 생긴다.
- ③ NAI는 외부 API·모델 가용성의 영향을 받는다. 실존 기록상 v4.5가 실패하고 v3만 작동한 사례가 있어, 성공 썸네일을 필수 완료조건으로 두면 파이프라인이 장기 정지한다. 프롬프트/설정/seed/모델/응답 해시와 실패 시도를 동일하게 증거화해야 한다.
- ④ GATE가 자기 자신이 만든 요약을 검증하면 순환 신뢰다. 검사기 commit, 규칙 버전, 입력 digest, 전체 pass/fail이 필요하고, 통과 뒤 입력 변경(TOCTOU)은 seal 없이는 막지 못한다. ⑤ 활용도는 태그 출처·산식·후보군 버전이 없으면 재계산할 수 없고, 봇이 만든 시나리오가 점수 입력에 섞여 source-unit 원칙을 우회한다.
- ⑥ “RISU에서 계속”, “NAI 재생성”, “JSON 보기”가 최신 mutable 자산을 열면 열람본과 승인본이 달라진다. 재생성은 새 attempt를 만들어 기존 seal을 보존해야 한다. ⑦ 승인 버튼을 먼저 발급해 숨기는 방식은 API 직접 호출 우회를 남긴다. 승인 엔드포인트 자체가 sealed 상태와 actor 권한을 검증해야 한다.

## 수정안

1. **불변 dossier manifest**를 정본으로 둔다. `source_unit_id + source_sha256`, 각 단계의 schema/version/input/output digest, 실행 ID·시각·도구 commit, 원문 증거 URI를 기록하고 전체를 content digest로 seal한다. URI는 화면 링크와 별도로 심사 당시 blob/version을 고정해야 한다.
2. **단일 상태기와 append-only 이벤트**로 순서를 강제한다: `SOURCE_BOUND → RISU_READY → CHAT_3_RECORDED → GATE_PASSED → NAI_RECORDED → UTILITY_SCORED → SEALED → REVIEWED → APPROVED → RELEASED`. 전 단계 digest가 일치하지 않으면 다음 단계와 승인 API를 거부한다. 변경·재생성은 덮어쓰지 말고 새 attempt로 분기하며 idempotency key로 중복 실행을 막는다.
3. 7요소 완료 규칙을 구체화한다. ① 실제 조합 JSON, ② 성공/실패를 포함한 사전 정의 3회 전문, ③ 모든 NAI 시도의 prompt/settings/result digest(외부 장애는 `attempted_failed`로 명시), ④ 독립 검사기의 전체 결과, ⑤ source-unit/검토 사전 태그만 입력한 산식·후보군 버전, ⑥ 고정 심사본 링크와 별도 재실행 링크, ⑦ sealed digest에 대한 최종 승인으로 한다. `example_only` 창작은 ⑤ 설명에만 표시하고 점수·승격 입력에서 제외한다.
4. 다ossier 조립기는 각 서비스 DB를 직접 수정하지 않는 read-only 수집기+검증기로 두고, 계약 테스트 fixture로 동일 source-unit 결속, 누락/교차자산 혼합, 중복 재시도, GATE 후 변조, 승인 선행, 승인 후 변경, release digest 불일치를 반드시 실패시키라. 홈(8018)의 마블 수는 이 상태 이벤트에서 집계해 UI와 실제 승인 조건이 같은 정본을 보게 한다.

