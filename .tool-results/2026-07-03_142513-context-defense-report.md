# 매니저 세션 컨텍스트 폭발 재발방지 작업 결과

- 시각: 2026-07-03 14:25:13 KST
- 범위: ctx-evac check, Stop 훅 등록, result-isolate 스킬, incident-8d 스킬
- 원칙: 큰 원문/코드 덤프는 메인 세션에 반환하지 않음

## 작업 ② — 사전방어선 강제화

변경 파일:

- `/home/ubuntu/scripts/ctx-evac.sh`
- `/home/ubuntu/.claude/settings.json`

요약:

1. `ctx-evac.sh check` 모드를 추가해 Stop 훅에서 70% 초과 시 checkpoint, emergency, `/clear` 권고를 실행하도록 했다.
2. `context-meter` usage가 0 또는 불가일 때 transcript JSONL byte 크기 기준으로 추정하며, 1.5MB를 70% 임계로 매핑했다.
3. `429`, `529`, `quota`, `context window limit`, `context_length_exceeded` 문자열을 check 모드 트리거로 감지하도록 했다.

검증:

- `bash -n /home/ubuntu/scripts/ctx-evac.sh`: 통과
- `jq empty /home/ubuntu/.claude/settings.json`: 통과

## 작업 ③ — tool_result 파일분리 스킬

생성 파일:

- `/home/ubuntu/.claude/skills/result-isolate/SKILL.md`

요약:

1. 5KB 초과 full Read, Codex 서브에이전트 긴 반환, 웹검색 결과를 `/home/ubuntu/notes/.tool-results/`에 저장하도록 규칙화했다.
2. 메인 세션에는 결과 파일 경로와 3줄 결론만 남기도록 보고 형식을 정의했다.
3. 같은 큰 파일 full 재독을 금지하고 offset/limit, `rg`, `sed`, `head`, `tail` 중심으로 재사용하도록 했다.

검증:

- frontmatter `name`/`description`: 확인 완료

## 작업 ④ — 8D 사고대응 스킬

생성 파일:

- `/home/ubuntu/.claude/skills/incident-8d/SKILL.md`

요약:

1. `context window limit`, `context_length_exceeded`, `429`, `529`, `quota`를 사고대응 트리거로 정의했다.
2. D1부터 D8까지 체크리스트와 산출물 템플릿을 한국어로 작성했다.
3. D3에는 보존, emergency 메모, 이사님 보고, `/clear` 또는 폴백 전환을 즉시 조치로 포함했다.

검증:

- frontmatter `name`/`description`: 확인 완료

## 변경 요약

- 기존 파일은 `ctx-evac.sh`의 check 서브모드/측정 폴백/트리거 감지와 `settings.json` Stop 훅 한 줄 추가만 변경했다.
- 신규 파일은 `result-isolate`와 `incident-8d` 스킬 문서만 생성했다.
- `/home/ubuntu/scripts/token-report.sh`는 존재하지 않았고, 현재 Stop 훅에는 `/home/ubuntu/.claude/skills/token-report.sh`가 등록되어 있어 기존 경로는 유지했다.

## 메모 필요

- Stop 훅이 실제로 전달하는 stdin JSON 스키마는 이 작업 중 확인 가능한 문서가 없었다. `ctx-evac.sh check`는 stdin, 추가 인자, `CLAUDE_ERROR`, `ERROR_MESSAGE`를 모두 보수적으로 감지하도록 처리했다.
- `git diff`는 현재 작업 디렉터리가 git 저장소가 아니라 실행할 수 없었다.
