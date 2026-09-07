---
title: 작업 패키지 — 소설 장면 요약→NAI (gmwin zcode 위임, 이사님 09-07 지시)
date: 2026-09-07
status: v1 — firewin zcode가 회의방 봇 송신 API로 @heav_gmwin_zcode_bot 배정
tags:
  - nai
  - scene
  - gmwin
  - novel
---

# 작업 패키지 — 소설 장면 요약 → NAI (gmwin zcode)

> 이사님 09-07 지시: "지앰 윈도 zcode에 소설 장면 요약해달라고 던져서 NAI 뽑는 것도 해야해".
> firewin zcode가 작업 패키지를 정본화하고 회의방 봇 송신 API(/api/bot/send, ROOM_BOT_TOKEN)로
> @heav_gmwin_zcode_bot에 배정한다. 본 문서가 유일 정본.

## 1. 역할 분담 (NAI 키 보안 원칙)

- **gmwin zcode**: 소설 원문/요약에서 **장면 선별 → 장면 요약 → danbooru 태그 변환 → scenes.jsonl 산출**.
- **AWS(scene_to_nai.py)**: scenes.jsonl을 입력으로 **이미지 생성**(NAI 키는 AWS `/home/ubuntu/.nai-token`에만 상주 — 키 분산 금지, RELAY-58 선례 준용). gmwin은 NAI 키를 요청·저장하지 않는다.
- gmwin에서 직접 NAI API를 돌리려면 키 이전 승인이 필요 — 이사님 대기 결정(현재는 AWS 경유).

## 2. 입력 소스 (1차)

- **망나니 PD 아이돌로 살아남기** 표본 장면(이미 요약됨): 1화(저주·시스템 발동)·51화(〈Kismet〉 데뷔 무대)·105화(민지헌 내기 카페)·239화(할로윈 팬덤)·487화(동반 입대·새벽) — 요약본은 scenario repo `novel_assets/works/망나니_PD_아이돌로_살아남기/` 와 notes `projects/agent-ops/roles/` 의 사이클 4~5 산출 참조.
- 2차: 100조로 갑질하기(273·275·276화), 지구식 구원자(프롤로그·비말록) — 순차 확대.
- 원문 원본: AWS `~/Works/novel/epub 파일/`(읽기만, byte 반입 금지).

## 3. 산출 형식 (scenes.jsonl, 1장면 1행)

```json
{"scene_id":"pd-s01","work":"망나니_PD_아이돌로_살아남기","ep":"1",
 "summary":"편집실에서 아이돌에게 저주받는 악마 PD — 담배 연기, 뒤돌아 나가는 실루엣",
 "place_tags":["office interior, night","neon light through blinds"],
 "char_tags":["1boy, suit, cigarette","1girl, idol outfit, tears"],
 "act_tags":["smoking","turning away","angry expression"],
 "mood_tags":["noir lighting","cynical mood"],
 "prompt_draft":"1boy, suit, smoking, office interior, night, neon light, cynical mood, cinematic lighting, no humans on floor",
 "negative":"lowres, text, watermark",
 "src_ref":"works/망나니_PD_아이돌로_살아남기/전수심독/ep001-487_표본직독.md"}
```

- 태그 문법: danbooru 스타일(소문자, 쉼표 구분) — `matrix_asset_agent/docs/INLAY-NEXUS-NAI-REFERENCE.md` 참조.
- 프롬프트 조립 표준: `matrix_asset_agent/tools/scene_to_nai.py`의 LOC/ACT/CHAR 사전 패턴 준용(해당 사전 확장은 환영 — 개선 커밋 환영).

## 4. 생성 규격 (AWS side — scene_to_nai.py 계승)

- 모델: nai-diffusion-4-5-full 권장(구형 3은 기존 스크립트 기본). 파라미터: INLAY 레퍼런스 준수 — `skip_cfg_above_sigma`: 4-5는 58.
- 산출 이미지: `scenario/novel_assets/images/<work>/scene_<scene_id>.png` + 생성 메타(json) 동반. 기존 images app(scenario/novel_assets/images/app/main.py)과 연결 가능하면 연결.

## 5. 절차·규칙

1. notes 최신 main pull → 본 문서 확인.
2. scenario repo pull --rebase → 산출 경로만 git add(타 봇 WIP 금지) → commit `scene(망나니 PD): 장면 요약 N건 — NAI 프롬프트 패키지` → push.
3. 완료·진행은 회의방 보고(@매니저 경유로 이사님 보고 체계 유지).
4. 금지: 원문 byte Git 반입 / NAI 키 요청·저장 / 다른 봇 WIP 수정 / 대량 생성 남발(1차 배치는 10장면 이내).
5. 승인 범위: 위 1차 입력(5장면)만 — 확대는 이사님 지시 후.

## 6. firewin zcode가 하는 것

- law4743 집중 소진 요약(병행) — 양쪽 요약이 모두 장면 소스로 축적.
- scenes.jsonl가 올라오면 AWS에서 scene_to_nai.py로 시험 생성 1~2장 → 회의방 보고(생성 결과는 경로만 보고).
