# codex_dev_2 의견 — 승인 다ossier 자동 생성 기술 리스크

근거: `APPROVAL-DOSSIER-PROPOSAL.md` @ `c09c9928b496d9484faf08b181befa8f474db780`, `PIPELINE-ARCHITECTURE.md`, RELAY-8/36/39/49 실존 자산. 승인 재료는 `matrix-source-unit-v1` 계보로 추적되는 자산만 허용하며, 봇 창작은 `example_only`일 뿐 승격 근거가 아니다.

## 낙관 근거

- 자동 조립의 재료는 이미 분리돼 있다. 8015의 리수 플랜·3회 채팅, 8016의 NAI manifest, 기존 `sha256(원본) → source-unit → workbench plan → approval → release` ID 흐름을 공통 계약으로 묶으면 ①리수 셋업, ②3회 채팅, ③NAI, ④GATE, ⑤활용도, ⑥액션, ⑦승인을 새로 생성하기보다 수집·검증할 수 있다.
- **승인을 다ossier 완성 뒤 마지막에 두는 순서**는 구현에도 유리하다. ①~⑥의 증거가 고정된 뒤 하나의 digest를 만들고 ⑦승인이 그 digest만 가리키게 하면, release가 같은 digest인지 기계적으로 판정할 수 있다. 홈(8018)의 마블도 동일 상태 레코드에서 집계하면 화면과 승인 API의 상태 불일치를 줄인다.
- GATE를 NAI보다 먼저 실행하는 제안의 파이프라인 순서는 스키마·계보 불량을 외부 생성 호출 전에 탈락시켜 비용과 장애 전파를 줄인다. NAI v4.5 실패·v3 동작이라는 실존 운영 기록처럼 외부 모델 변화가 있어도 앞단 검증은 독립적으로 완료할 수 있다.

## 비관 근거

- 정본 안에서 7요소는 `NAI → GATE`로 열거되지만 실행 순서는 `GATE → NAI`다. 조립기·UI·재시도 워커가 서로 다른 순서를 구현하면 상태가 갈라진다. 순번은 화면 번호일 뿐인지, 의존 순서인지 스키마로 확정해야 한다.
- ① **리수 셋업**은 조합 JSON만으로 부족하다. 카드·모듈·로어·모델 각각의 불변 ID/해시와 정규화 규칙이 없으면 같은 조합이 다른 digest가 되거나 변경된 최신본을 참조한다. ② **3회 채팅**도 “3번 요청”과 “3개 정상 전문”이 다르다. timeout·부분 스트림·재시도·모델 변경을 성공으로 셀지 정의하지 않으면 자동 완료 판정이 비결정적이다.
- ③ **NAI**의 성공 썸네일을 필수로 잡으면 외부 API 장애가 승인 전체를 멈추고, “시도”만 요구하면 빈 오류도 완료로 위장될 수 있다. prompt/settings/model/seed, 요청·응답 해시, 비용, 실패 코드와 재시도 계보가 필요하다. ④ **GATE**는 어느 시점의 입력을 검사했는지 고정하지 않으면 통과 직후 셋업·전문·프롬프트가 바뀌는 TOCTOU가 생긴다.
- ⑤ **활용도**는 현재 source-unit의 빈약한 태그 위에 자동 추론을 얹을 위험이 크다. 산식·후보군·태그 출처를 버전화하지 않으면 재계산 시 값이 바뀌며, 생성 시나리오가 입력에 섞이면 “실존 자산만” 원칙을 우회한다. ⑥ **액션**이 mutable 최신본을 열거나 재생성을 제자리 덮어쓰기 하면 심사본과 체험본이 달라진다. ⑦ **승인**은 버튼 노출만 늦춰서는 부족하며 API가 미완성/구 digest 요청을 거부해야 한다.

## 수정안

1. **버전된 계약부터 확정한다.** `dossier-manifest-v1`에 `source_unit_id/source_sha256`, 단계별 `input_digest/output_digest/schema_version/tool_commit/attempt_id/status/evidence_uri`를 둔다. 7요소 표시 순서와 실행 의존 순서는 별도 필드로 명시하고, 실행은 `SOURCE → RISU → CHAT3 → GATE → NAI_ATTEMPT → UTILITY → SEALED → APPROVED → RELEASED` 하나만 허용한다.
2. **완료 의미를 닫힌 열거형으로 만든다.** 채팅은 사전 고정한 3슬롯 각각에 전문 또는 실패 증거가 있어야 하며 재시도는 새 attempt다. NAI는 `succeeded`와 증거가 충족된 `attempted_failed`를 구분한다. GATE는 동일 attempt의 전체 manifest와 검사기 버전을 검사하고, 필수 hard gate 실패 시 seal을 금지한다.
3. **7요소를 한 source-unit 계보에 결속한다.** ① 구성 해시, ② 3슬롯 실행 해시, ③ NAI 전 시도 해시, ④ 전체 GATE 결과, ⑤ 산식·후보군·근거 태그, ⑥ 고정 심사 링크/별도 실행 링크, ⑦ sealed digest 승인을 필수화한다. 활용도 입력은 source-unit 파싱값 또는 검토된 사전만 허용하고 봇 창작은 `example_only`로 격리한다.
4. **승인은 완성 뒤 마지막이라는 규칙을 서버에서 강제한다.** seal 전 승인 레코드 생성 금지, 승인 후 ①~⑥ 변경 시 새 attempt 및 재승인, release 시 승인 digest 일치 검사를 둔다. 계약 테스트는 교차 자산 혼합, 부분 채팅, NAI 장애, GATE 후 변조, mutable 액션, 승인 선행, release digest 불일치를 모두 실패시켜야 한다.
