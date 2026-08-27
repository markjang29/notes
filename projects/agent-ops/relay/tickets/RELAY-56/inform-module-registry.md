# [inform] 이미지 모듈 레지스트리 + 자동 감시 설계 (zcode → 전 봇, 2026-08-27)

> 이사님 지시: "니가하고 인폼 남겨. 아카라이브 크롤링해서 버전업데이트나 새로운게 추가되면
> 업데이트 되도록 설계해줘. 레지스트리가 그거임?" → **네, 그 레지스트리가 그것입니다.**

## 현재 상태

- **모듈 레지스트리**: `matrix_asset_agent:tools/scene_to_nai.py`의 `list_image_modules()` — 14종.
  라이트보드 NAI 9버전(✅사용가능) + Inlay Nexus 2.3.98 tagger(✅) + Works 3종(⏳등록대기).
  조회: 워크벤치 `/modules`. 교체생성: `/scene_draw/<plan>?module=<이름일부>`.
- **자동 감시**: `tools/module_watch.py` — crontab 매일 06:05. 3계층:
  1. 아카 AI봇판 검색(라이트보드/이미지모듈/NAI/삽화 키워드, 하루1회·5초간격 — IP차단 방지)
  2. 로컬 드롭판 `~/Works/inbox/modules/` — .json 즉시등록, .risum 등록대기 기록
  3. 기록: `tools/assets/module_watch_state.json` + `module_watch.log`

## 제약 (솔직 보고)

- **아카 직접 크롤링 현재 불가**: 서버(AWS) IP가 arca.live에 차단(403/챌린지404).
  → 감시기는 이 상태를 기록하고 스킵. 해제 방법: `ARCA_PROXY` 환경변수로 프록시 지정 시 자동 사용,
  또는 가정망/미러에서 드롭판에 파일 낙하(이 경로는 항상 동작).
- **Works 3종(지르코트·이계의 신격·TSF) 등록대기 이유**: .risum이 RISU 세이브와 다른
  인코딩(msgpack trailer 불일치)이라 프롬프트 추출 디코더가 아직 없음. RISU 앱 내 수입→재추출
  경로가 빠름. **asset_agent 담당 가능** (risum 구조조사 티켓 필요).

## 다음 단계 권고

1. 아카 신버전(라이트보드 3.x 등) 포착 시: 드롭판 낙하 → 감시기가 등록 → `/modules` 반영.
2. 버전업 감지 시 notes 인폼 자동 1건 작성은 매니저 게이트 권고 (봇 직접 커밋은 기존 규칙 유지).
3. risum 디코더 제작되면 ⏳ 3종이 ✅로 전환 — `?module=지르코트` 식 생성 가능.
