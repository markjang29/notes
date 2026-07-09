# arca 크롤링 파이프라인 — @heav_ai_bot(노트북) 핸드오프

노트북(Windows, @heav_ai_bot)에서 돌리는 arca.live 자료 수집→발췌→분석→카탈로그 파이프라인. AWS(cokacdir) 봇과 분리.

## 상세
- **전체 문서/코드**: 시나리오 git `markjang29/scenario` 의 `HANDOFF_heav_ai_bot.md`(역할분리/상태/이어서 작업 가이드) + `tools/crawler/`, `tools/{extract_collected,analyze_collected,run_pipeline,build_catalog}.py`, `ecosystem/collected-pipeline.md`.
- **노트북 자동메모리**: `arca-collector-project.md`(.claude memory) — 정책/이슈 상세.

## 핵심 (한 줄)
노트북이 arca 자원 탭(자료/프롬/로어북/대회/에셋모듈봇/페르소나/모델공유)을 느리게 수집 → `D:\LLM\_새수집\` → 2차 클론(`D:\LLM\AI-정리-발췌-scenario`)에서 발췌(legacy `.extract/{characters,modules,prompts}/`)+GLM 분석+카탈로그 → git push. 서버(AWS)가 pull 해 매트릭스(scenario-generator) 랜덤 생성에 소비.

## 충돌 회피
- **catalog 쓰기 = 노트북만**(수집분 갱신). AWS는 읽기(pull 후 매트릭스).
- **`tools/scenario-generator/`(백엔드) = AWS 관리**. 노트북은 수정 X.
- 노트북 산출물(`.extract/`, `cookies.json`, PDF)은 gitignore(저작권/민감).

## 이어서 (노트북 세션)
- 세션 갱신: `python D:\LLM\_새수집\_crawler\collector.py --login`
- 한 번 실행: `python D:\LLM\AI-정리-발췌-scenario\tools\run_pipeline.py` 또는 `/arca-crawl`("아카라이브 크롤링 해줘")
- 대량 수집: `python D:\LLM\_새수집\_crawler\collect_top.py` (TOPN/PAGES/MIN_RATE/MIN_CC/SCALE)
- 수동 다운: `catalog/needs_manual_download.md` → 폴더에 파일 → 다음 run_pipeline 자동 통합

## 상태 (2026-07-09)
- 카탈로그 699에셋(601 기존 + 수집 98). 야간 심층 수집(개념+일반 p1~5, 추천3↑/댓글5↑, 버전 dedup, NSFW 포함) 진행.
- 수집분 본문: external(proton 등) → 수동 다운 리스트.
- 분석: z.ai GLM(Messages API, `~/.claude/settings.json` 토큰). 진짜 Anthropic 아님.
