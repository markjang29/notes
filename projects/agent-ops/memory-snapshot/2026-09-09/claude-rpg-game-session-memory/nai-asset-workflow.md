---
name: nai-asset-workflow
description: NAI(NovelAI) Opus로 RPG 게임 자산 생성하는 워크플로우 — API 실측 노하우 + RPG저장고 + RELAY-36 도구화 착수
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f7dfab6-fab6-4ae5-8b5c-129799683889
  modified: 2026-09-05T15:52:13.399Z
---

이사님 NAI Opus 구독으로 RPG 게임 자산(칼·세계·코어·UI)을 생성한다(2026-08-22 시작). 토큰(pst-...)은 이사님이 세션에서 직접 전달 — **파일/Git/메모리 저장 금지, 세션 내 사용만**.

**API 실측 (2026-08-22):**
- 호스트 `https://image.novelai.net/ai/generate-image` (api.novelai.net 아님 — 안내 메시지 뜸). 구독 확인도 image 호스트에서 200.
- `nai-diffusion-4-5-full` 사용 가능 — 단 `parameters`에 `v4_prompt`/`v4_negative_prompt` 캡션 구조 필수(누락 시 500). RELAY-34의 "v4.5 불가" 결론은 이 구조 몰라서였음.
- 인증: Bearer + 브라우저 UA 필수(python 기본 UA=Cloudflare 1010 차단). 응답 = raw ZIP → zipfile로 image_0.png 추출.
- 오푸스 무료 조건: ≤1MP(832x1216 세로 추천·모바일 무드에 적합)·28스텝·1장 — Anlas 미소모.
- 프롬프트/시드 기록: `~/nai_concepts/<날짜>/_prompts.json`.

**보관:** 구글드라이브 rclone `matrix-upload:RPG저장고/` (RELAY-34가 1차 업로드). rclone 공유 client_id 폐기 NOTICE 있음.

**1차 도트 배치 (2026-09-06, 파랜드 택틱스풍):** 31장 전량 성공 — 스크립트 배치 `~/nai_concepts/2026-09-06_batch/generate_batch.py`(재실행 가능, 카테고리 6종: 배경7·타일4·캐릭터8·무기5·이펙트4·UI3, 픽셀 스타일 접미어 + 시드 고정 기록). 드라이브 `RPG저장고/도트에셋_1차_파랜드풍/01_배경~06_UI` + 폴더별 `_prompts.json`. 컨택트시트 스크립트도 같이(Pillow 설치 완료). 도트 스프라이트 캐릭터·UI창·이펙트는 잘 나옴, 타일은 시트 형태 참고용(실제 타일 분해 필요).

**2차 배치 (로맨틱·편안):** 14장 — 이사님 피드백 "파랜드가 좋았던 건 배경의 로맨틱·편안한 느낌". 드라이브 `RPG저장고/도트에셋_2차_로맨틱/`. ★프롬프트 교훈: pastel/dreamy를 단독으로 쓰면 대상이 하얗게 씻김 — **구도·디테일 묘사 먼저, 무드 키워드(golden hour·romantic·nostalgic)는 뒤에 얹는다.** 무드 프리셋을 워크벤치에 넣을 때 이 순서로.

**도구화:** 이사님 요구로 단발 생성이 아닌 **게임 자산 워크벤치(웹, 알만툴식)** 프로그램化 — RELAY-36 (포트 8017 운영, 접속키 `~/.rpg_wb_key`). 감정·시선 변형·UI프리셋·프로필 별도 파일 반영 완료. Jira 전면 404 중 — 티켓 추적은 notes `relay/tickets/` 경유. 관련 [[rpg-game-01-canon-location]] · [[matrix-scenario-team-state]].
