---
name: feedback-risu-asset-real-content
description: RISU 자산 기반 창작은 '실제 내용' 사용 — 메타(이름/경로)만 쓰면 사칙 1번 미달. 시나리오팀 근본 정책.
metadata:
  type: feedback
---

이사님 2026-07-06 확정 (scenario-generator v5 작업 중): "이거 중간에 D:\LLM 이런거는 실제 저 파일내용을 쓴 게 맞아?" 질문 → 제 답(실제 내용 안 씀, 메타만) → 이사님 "2번(근본)으로 해야 해, 근본 정책이야".

**Why:** RISU 자산 기반 창작(사칙 1번)의 본질은 자산의 실제 설정·규칙·스타일이 창작에 반영되는 것. catalog 메타데이터(이름·경로·개수)만 프롬프트에 넣으면 LLM이 이름만 보고 상상으로 쓰므로 사칙 미달. 이사님이 정확히 이 약점을 짚으심.

**How to apply:**
- 자산 실제 내용 출처 = `.extract/` 디렉토리 (이사님 발췌, 서버 로컬, gitignore — NSFW 포함으로 GitHub 금지)
- 구조: `.extract/{characters,modules,prompts,persona}/<name>.json`
- scenario-generator `AssetContentLoader`(`backend/assets/content_loader.py`)가 읽어 `ASSEMBLE`이 프롬프트에 펼침
- 캐릭터: description+personality+scenario, 모듈: lorebook entries, 프롬프트: main+globalNote
- `.extract/` 미업로드 시 메타 fallback + 경고 문구로 동작 (실제 내용 반영 전 단계)
- 자산 발굴은 내용 보유 자산 우선 (`has_content` 태깅, DISCOVER)
- 관련 [[current-work-state]], scenario 사칙 `~/notes/principles/scenario-team-purpose.md`
