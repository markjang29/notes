---
title: ARCA PIPELINE HANDOVER v1 — 아카라이브 에셋 수집 파이프라인 인계
date: 2026-09-10
status: active — 파뱃윈도(firewin) 파이프라인 운영 정본
tags: [agent-ops, arca, pipeline, risu, nai]
source: 이사님 제공 인계 문서 (원본: ZCodeProject docs/handover-2026-08-16.md)
---

# 아카라이브 에셋 수집 파이프라인 인계 (2026-09-10 기준)

## 개요

아카라이브(arca.live) characterai 게시판에서 AI 봇/에셋(캐릭터카드, 모듈, 프롬프트, 로어북)을
**수집 → 다운로드 → 디코딩 → matrix 캡슐화 → git push** 하는 5단계 파이프라인.
실행 환경은 Windows(`C:\Users\heave`). 코드는 `C:\Users\heave\ZCodeProject\engine\`,
자산은 `D:\LLM`. 최종 자산은 .charx 원본이 아니라 **matrix-component-v1 캡슐(NDJSON)** 이며
`github.com/markjang29/scenario` 저장소로 push한다.

## 5단계 명령어 (ZCodeProject 기준 상대경로)

1. **HTML 수집**: `python engine/arca_collector.py all 25`
   - 16카테고리 × 25페이지 ≈ 17,000개, 약 3시간, **반드시 백그라운드 실행**
   - 중단 후 재실행해도 중복 자동 스킵으로 이어서 진행됨
   - 저장: `D:\LLM\arca_html\[카테고리]\게시글제목.html` + `_meta\[게시글ID].json`(다운로드 링크 포함)
2. **파일 다운로드**: `python engine/asset_downloader.py proton|gdrive|mega|realm|catbox|all|--status`
   - 저장: `D:\LLM\YYYY-MM-DD\[카테고리]\게시글제목\*.charx` 등 (현재 통합본: `D:\LLM\2026-08-08`)
3. **디코딩**: `python engine/asset_pipeline.py extract`
   (단일 파일: `node ~/.agents/skills/risu-extract/scripts/decode_rpack.js "파일" --out result.json`)
4. **matrix 캡슐화**: `python engine/asset_pipeline.py transform`
   (ingest.py는 `C:\Users\heave\matrix_zcode\engine\ingest.py`, build_capsule에 source_card 포함 수정 완료)
5. **git push**: `python engine/asset_pipeline.py push`

## 카테고리 매핑 (표시명 ≠ 내부값 — 제일 흔한 실수 포인트)

단일 게시판 characterai를 category 파라미터로 분류한다.
AI봇=자작봇 · 에셋·모듈봇=감정봇 · 프롬=프롬프트 · 후기=리뷰 · 🔞일반=19 · 후기🔞=review19 ·
AI대화🔞=19금 · AI대화(하드)=하드주의 · AI대화=대화 · 연구소=개발.
페르소나/자료/대회/일반/질문은 표시명=내부값.
**NSFW 포함 전부 수집 — 제외 금지, 판단은 사용자가 함.**

## 다운로드 도메인별 방법

- **drive.proton.me (90%)**: Chrome을 9222 포트로 띄워 CDP로 제어, 첨부 비밀번호는 aichat.
  Chrome 기동(기존 chrome 종료 후):
  `chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\Users\heave\chrome_debug --no-first-run`
  확인: `curl -s http://127.0.0.1:9222/json/version`
- **files.catbox.moe (6%)**: 한국 DNS 차단 → 8.8.8.8로 직접 조회해 IP+Host 헤더로 접속(verify=False). 우회 로직 코드에 내장됨
- **drive.google.com (2.5%)**: gdown 사용. 폴더 URL은 실패 다수. "성공" 파일에 로그인 HTML이 섞일 수 있어 타입 검증 필요(미완)
- **mega.nz (0.6%)**: 미해결(mega.py 복호화 버그, CDP도 실패). 필요시 megadown CLI 시도. 21개 남음
- **realm.risuai.net (0.2%)**: GET `/api/v1/download/charx-v3/{UUID}` — 비번 없음, 가장 쉬움

## IP 차단 방지 (필수)

- 요청 간 딜레이 0.8초 이상 하한, 페이지 전환 시 2초 추가, 실패 시 5초 대기
- **병렬/멀티스레드/asyncio 절대 금지. 단일 스레드 순차 수집만.**

## 로그인 만료 감지와 복구

공지만 5개 이상 + 일반 게시글 0개면 LoginRequiredError로 전체 수집 즉시 중단.
복구: Edge에서 arca.live 로그인 → chromlevator.exe로 쿠키 복호화 →
`C:\Users\heave\.scenario-automation\cookies.json` 갱신 → 수집 재실행(중복 스킵으로 이어서).

## RisuAI 디코딩 노하우 (decode_rpack.js)

- `.risum`: magic 0x6f + rpack WASM 디코드 → JSON. 에셋은 assets[i]=[id,_,type] 튜플 형태
- `.risup`: rpack → gzip → msgpack → AES-256-GCM(key=SHA256('risupreset'), IV=12바이트 0, tag=끝 16바이트) → 다시 msgpack
- `.charx`: ZIP. card.json(Character Card v3) + embeded:// URI로 내부 에셋 매핑. x_meta 있으면 리소스 번들
- PNG 카드: tEXt 청크 chara/ccv3 + chara-ext-asset_N. "rcc||" 접두가 있으면 암호화라 열 수 없음
- WASM 위치: `D:\LLM\RisuAI-main\src\ts\rpack\rpack_bg.wasm` (decode 후 memory.buffer 재참조 필수 — detach 방지)

## 중복 제거 원칙

- SHA256 완전 동일 → post_id 큰 쪽(더 새 글) 유지
- 게시판이 다르면 같은 파일이라도 별도 자산으로 유지(복원함)
- 같은 게시판의 구버전만 `_dedup`로 분리

## 현재 진행 상태

- HTML 수집 완료 17,339개 / 다운로드 링크 추출 3,575개 / 다운로드 약 2,130개(77GB) 완료
- 중복 제거 242개(_dedup 분리), `D:\LLM\2026-08-08`로 날짜 폴더 통합 완료
- **남은 작업**: ① 2,130개 캡슐화(transform) — .charx 안의 module.risum 별도 캡슐 분리 추출 미구현
  ② 캡슐 NDJSON git push ③ mega 21개 미해결 ④ gdrive 성공 파일 타입 검증 후 재분류

## 운영 규칙

- 백그라운드 작업은 반드시 **실제 실행/로그로 확인**(조용히 실패한 사례 2회 있음)
- 코드는 ZCodeProject에만, 자산/데이터는 `D:\LLM`로
- 원본 문서: `C:\Users\heave\ZCodeProject\docs\handover-2026-08-16.md`
- 스킬 정의: `C:\Users\heave\.agents\skills\arca-collect\SKILL.md` 및 `risu-extract\SKILL.md`
- 매트릭스 방향 정본: `F:\repo\matrix_asset_agent\NORTH-STAR.md` (자산 3층 구조, 정식 자산의 세 표현, 증명된 것/아직 아닌 것)
