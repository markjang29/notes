---
title: 아카라이브 수집 인계 수령 기록 — firewin zcode (2026-09-06)
date: 2026-09-06
status: 수령 + 실측 검증 완료 (발신측 송신 전 정정 2건)
tags:
  - asset
  - arcalive
  - handover
  - firewin
---

# 아카라이브 수집 인계 — 수령·검증 기록

이사님 경유로 구 수집 담당(구 윈도우 쪽)의 인계 메시지를 수령. 수신 대상은 본 봇
(firewin zcode). 아래는 내용 요약과 본 봇의 AWS 읽기 전용 실측 검증 결과.

## 1. 인계 내용 요약 (발신 원문 기준)

1. **로그인**: 이사님이 세션/계정 직접 제공 — 받은 쿠키를 수집 세션에 심어 사용(우회 아님).
   미로그인 시 첨부 다운로드 불가 글 존재.
2. **정본 문서**: `handover-2026-08-16.md`(카테고리 매핑·catbox DNS 우회·risup AES 복호화·IP 밴 방지) — ⚠ 경로 문제 아래 §3-1.
3. **스냅샷(2026-08-08)**: 게시판 16개 인덱스 완료, 게시판당 최신 약 1,120건 HTML,
   첨부 원본 AI봇 244·로어북(raw) 590·에셋·모듈봇 372·페르소나 324·프롬 438·대회 179·자료 482.
   AWS `~/Works/arcalive` 전체 미러 = 중복 확인 기준선.
4. **증분 수집**: `_index_{게시판}.json`의 게시판별 max post_id를 커서로, 더 큰 post_id만 수집.
   스키마: post_id·board·board_kr·title·category·rate·body_length·attachments·download_links·
   exts_mentioned. 중복 기준 = post_id + 첨부 sha256, AWS 미러 겹침 스킵.
5. **기술 주의**: catbox DNS 우회(정본 참조) / 요청 간격 충분히(IP 밴 시 이사님 계정 위험,
   AWS IP는 이미 403) / risup(charx) AES 복호화 대상은 원본 보존, 복호화는 s0_worker가 담당 /
   정리·입고 표준 = `matrix_asset_agent/tools/s0_worker.py`·`basket.py`.
6. **우선순위**: 2026-08-08 이후 신규글(약 1개월 밀림) — 페르소나·모듈·로어북 우선.
7. **board 필드**: 인덱스의 board는 전부 `characterai`, 실제 구분은 `board_kr` — URL 슬러그↔한글명 매핑은 원본 html로 확정.

## 2. 본 봇 실측 검증 (2026-09-06, AWS 읽기 전용)

- `_index_페르소나.json`: **1,125건**, 키 실측 `post_id·board·board_kr·title·category·
  body_length·attachments·download_links·exts_mentioned` — **`rate` 필드는 실측에 없음**
  (append 시 기존 스키마 우준).
- **페르소나 max post_id = 93,029,846** — 발신 원문의 커서 수치(179,06만~179,10만)와 불일치(§3-2).
- `arca_html` HTML 실측 **17,339개**(스냅샷 주장 34,741과 기준 차이 — 게시판별 재대조 필요).
- `board`/`board_kr` 병존 확인(§1-7 사실과 일치). 로어북 raw 590은 duradev 8018 stats의
  `raw_lorebook: 590`과도 일치.

## 3. 발신측 송신 전 정정 요청 (이대로 보내면 안 되는 이유 2건)

1. **정본 문서 경로가 사망 링크**: `C:\Users\heave\ZCodeProject\docs\handover-2026-08-16.md`는
   퇴역한 구 윈도우 PC 경로. AWS 홈 전수·notes 검색에서도 원본 미발견(참조 조항만 존재).
   → 원문을 GitHub 또는 AWS로 옮겨 살아있는 경로를 명시하거나 문서 원본을 별도 전달해야 함.
2. **커서 수치 불일치**: "179,06만~179,10만"은 실측(페르소나 9,302만)과 50배 이상 차이.
   → "게시판별 `_index_*.json`의 실제 max post_id 사용"으로 문구 확정 권장(수치 예시 삭제).

## 4. 본 봇 수령 후 조치

- 승인 전 대량 수집 금지 유지 — 수집 실행은 이사님 범위 확정 후 firewin에서 시작.
- 로그인 쿠키·비밀키는 Git·로그·사이트에 기록하지 않고 로컬 세션에만 사용(금지사항 준수).
- 증분 수집 시작 시 커서는 각 `_index_*.json`의 max post_id로 자동 산출.
