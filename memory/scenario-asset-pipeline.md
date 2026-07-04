# scenario repo — RISU 에셋 추출 파이프라인

> 윈도우(에셋 공급) → 서버(소비·생산) 분업의 윈도우측 산출.
> repo: github.com/markjang29/scenario (로컬 `C:\Users\heave\projects\scenario`)

## 무엇을 했나 (2026-07-04)
RISU AI 에셋 포맷(`.risum` 모듈 / `.risup`·`.risupreset` 프리셋)을 역변환하는 파이프라인을 구축하고, 에셋 602건의 통합 메타 카탈로그를 완성해 scenario repo `main`에 반영.

## 역변환 스펙 (RISU 오픈소스로 확정)
- `.risum` = `[0x6F][0x00][u32le 길이][RPack(JSON 모듈본체)]...`. RPack→JSON. (암호화 없음)
- `.risup` = RPack→gzip→msgpack→`{preset:AES-GCM ct}`; `.risupreset`(구형) = gzip→msgpack→AES.
- AES 키/IV는 RISU 소스에 하드코딩된 고정값(`key='risupreset'`, IV=`0`×12). RPack은 RISU wasm(`rpack_bg.wasm`)을 node(v24)에서 재사용.
- 검증: 모듈/프리셋 536건 RPack 디코딩 전부 성공.

## 산출 (repo)
- `tools/`: `extract_risu.py`, `rpack_decode.js`(wasm RPack 디코더, 일괄모드), `build_catalog.py`, `extract_cards.py`(.charx)
- `catalog/`: `assets.csv`·`index.json`(602 통합), `modules.csv`(343), `prompts.csv`(205), `characters.csv`(53) + `README.md`
- `.extract/`(발췌본, gitignore)에 본문 보관. 원본 바이너리는 커밋 안 함(메타만).

## 경계
- 미성년 성화 마커 감지 에셋은 발췌·카탈로그에서 제외(이번 4건).
- 프리셋에 박힌 타인 API키/엔드포인트는 추출 단계에서 자동 제거(검증 0건 누출).

## 핸드오프
서버 시나리오 팀(`@hev_lnx_scenario`)은 `catalog/index.json`을 소비 → 임베딩 인덱스 + 랜덤 조합 엔진으로 시나리오 창의 양산. 서버측은 이미 자생 서사 시스템(oracle-audit·cases·worlds·RPG 시그니처) 구축 중 — 이 카탈로그가 그 창의 양산의 원료 풀.

## 재실행
`D:\LLM` 원료가 바뀌면 `python tools/extract_cards.py && python tools/extract_risu.py && python tools/build_catalog.py`. `.extract/`와 `catalog/`가 갱신됨.
