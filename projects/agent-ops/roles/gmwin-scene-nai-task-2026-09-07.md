---
title: 작업 패키지 v2 — 소설 장면 요약→NAI (gmwin zcode 전담, 이사님 09-07 결정)
date: 2026-09-07
status: v2 — 이사님 AskUserQuestion 결정 반영(gmwin 전담+NAI 생성 포함, 소스=파싱 중 작품)
tags:
  - nai
  - scene
  - gmwin
  - novel
---

# 작업 패키지 v2 — 소설 장면 요약 → NAI (gmwin zcode 전담)

> 이사님 09-07 결정(AskUserQuestion): ① gmwin이 **요약+NAI 생성 전부** 담당(NAI 키 gmwin 배포 승인 포함)
> ② 장면 소스 = **지금 파싱 중인 작품(『이것이 법이다』, law4743)**. v1(망나니 PD 표본·gmwin 요약만·AWS 생성)은 폐기.

## 1. 역할 (v2)

- **gmwin zcode(전담)**: 『이것이 법이다』 원문에서 장면 선별 → 장면 요약 → danbooru 태그 → scenes.jsonl 작성 → **NAI 이미지 직접 생성**(키 배포됨) → 결과 보고.
- **firewin zcode**: law4743 배치 요약(집중 소진 루프) 병행 — gmwin의 장면 선별 참고자료. scenes.jsonl 병합 관리는 유지.
- **매니저**: 자격 배포 — ① NAI 키(원본 AWS `/home/ubuntu/.nai-token`)를 gmwin zcode로 안전 복사 ② gmwin의 AWS 읽기 접근(law4743 원문) 확보. (gmwin엔 엣지 SSH 키가 없음 — 매니저 09-07 실측)

## 2. 소스

- 『이것이 법이다』(자카예프): AWS `~/matrix_asset_agent/.runtime/novel/law4743/` — ch00001~ch06068(63MB, SHA 0be7248174502dd245e0d036a2b7cb64d892fcd62937d617b49e28aceeeb0d74).
- 본문 이중 인코딩 — `iconv -c -f UTF-8 -t CP949` 복구해 읽을 것. firewin의 배치 요약 노트(`_batch_notes/`, 현재 ch00014까지)를 참고 자료로 병용 가능.
- 원문 byte의 Git 반입 금지 유지 — 원문은 AWS/.runtime에서만 읽고, 요약·태그만 내보낸다.

## 3. 산출 (gmwin)

1. **장면 요약**: `scenario repo novel_assets/images/scene_summaries/이것이_법이다/scenes.jsonl`
   1장면 1행: {scene_id:"law-sNNN", work, ep, summary(3문장), place_tags, char_tags, act_tags, mood_tags, prompt_draft, negative, src_ref:"law4743/chXXXXX"}
   — 태그는 danbooru 스타일. 표준 참조: `matrix_asset_agent/docs/INLAY-NEXUS-NAI-REFERENCE.md` + `tools/scene_to_nai.py` 사전 패턴.
2. **NAI 이미지 생성**(gmwin 로컬): 모델 nai-diffusion-4-5-full 권장(`skip_cfg_above_sigma: 58`). 초기 배치는 10장면 이내로 시험.
3. **보고**: 회의방에 scenes.jsonl 커밋 해시 + 생성 이미지 경로(로컬 경로·장수) 보고. AWS 웹 노출(8016/Caddy 연계)은 매니저 결정 후.

## 4. 절차·규칙

1. 매니저가 자격(NAI 키·AWS 접근) 배포 완료 확인 전까지 생성 착수 금지 — 요약 원고 작성은 선작업 가능.
2. scenario repo 산출 경로만 git add(타 봇 WIP 금지) → pull --rebase → push → 회의방 보고.
3. 금지: 원문 byte Git 반입 / NAI 키의 Git·로그·사이트 기록 / 887 수집 큐·novel_col 영역 침범 / 이미지 대량 남발(배치 10장 이내).
4. 저작권 주의: 생성 이미지는 내부 자산 — 공개 배포 금지(이사님 지시 원칙 유지).

## 5. firewin zcode 병행

- 집중 소진 루프(15분)로 law4743 배치 요약 지속 — 현재 ch00014, 배치 3/152.
- gmwin의 scenes.jsonl 커밋을 감시해 중복 scene_id 방지(병합 관리).
- v1 산출(망나니 PD scenes.jsonl+시험 생성 2장, 커밋 736636b·nai_out/scene_test/)은 시험 사례로 보존.
