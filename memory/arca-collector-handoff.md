# arca 수집 핸드오프 — 단건 완결 정책

이 문서는 구형 야간 일괄 수집/GLM/수동 다운로드 정책을 대체한다.

정본: `C:\Users\heave\projects\scenario`

필수 문서:

- `docs/one-post-resolution-runbook.md`
- `docs/new-asset-ingestion-rules.md`
- `docs/current-pipeline-map.md`
- `docs/scenario-team-operating-rules.md`
- `docs/aws-request-bridge.md`

원칙: 게시물 한 건을 선택하면 실제 다운로드부터 parser-backed 추출, 검토, 정규화, 프롬프트 조각, 시나리오 빌더 가용성 판정까지 닫은 뒤 다음 건으로 넘어간다.

`/arca-crawl`, `run_pipeline.py`, 대량 수집, 야간 CATCHUP, `NEEDS_DL` 수동 위임, legacy `.extract`/GLM/catalog index 승격은 금지한다.

현재 `110558063`의 AWS 가용성 테스트 요청은 `req-20260712163919-ee11cc`다. 결과 검증 전 다른 게시물을 시작하지 않는다.
