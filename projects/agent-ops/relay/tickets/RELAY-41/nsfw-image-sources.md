# NSFW 이미지 생성 자료 전수 리스틉업 (이사님 08-23 지시 — zcode 직접 처리)

> 스캔 범위: Works/arcalive 전체 + scenario/.extract + catalog/lorebooks
> 기준: "이미지 생성에 쓸 수 있는 NSFW 태그/프리셋/워크플로우 포함 자료"

## A. NAI 모듈 (삽화) — 1차 채굴 대상 ★
| 자료 | 위치 | 등급 |
|---|---|---|
| 라이트보드 NAI 2.1.1~2.9 (10종 버전) | scenario/.extract/modules/ | ★ 최상 — 2.9 이미 태그·부스트·액션문법 채굴 완료. 구버전은 delta 비교용 |
| 🌌NAI INRAY NEXUS 1.0 / 2.0 beta / 채팅 간섭 없이 3종 | Works/arcalive/자료/ | ★ 최상 — RELAY-13 심화 대상. 오버레이·프롬프트 변환 규칙 |
| 🆔 인레이 모듈 불법 마마개조 (검열 회피용) | Works/arcalive/자료/ | ⚠ 기술 참고만 — 검열회피 목적은 미사용, 변환 규칙만 역설계 |
| 🔦라이트보드 🌠 삽화 3.4.1 개조 테스트판 | Works/arcalive/자료/ | ★ — 3.x 최신 계보, 2.9와 비교 |

## B. SD/ComfyUI 계열 — 워크플로우 참고
| 자료 | 위치 | 등급 |
|---|---|---|
| 🔞)ComfyUI 삽화 워크플로우 V3 + ComfyUI 에셋 + Comfypack | Works/arcalive/자료/ | 참고 — NAI 외 파이프라인, 향후 확장 시 |
| SDXL 이미지 생성으로 봇 먹기 (PDF) | scenario/.extract/pdf/ | 참고 |
| 🔞 천박순애 SD 프리셋 1·2 | Works/arcalive/자료/ | ★ SD용 NSFW 태그 세트 — 태그는 NAI에 이식 가능 |
| 🔞 빠앙,쿰질용 가챠섬 로라 삽화세팅 | Works/arcalive/자료/ | 참고 — 로라 자체는 NAI 불가, 세팅 관점만 |
| 단부루 기반 AI 이미지 프롬프트 생성기 개조 / 단부루 검색 툴 v1.0.6 | Works/arcalive/자료/ | ★ 태그 검색·조합 관점 |
| 🔞 대충 리츠카마슈 sd스튜디오 세팅 | Works/arcalive/자료/ | 참고 |

## C. 삽화 로어북·태그 사전 — 태그 직접 소스 ★
| 자료 | 위치 | 등급 |
|---|---|---|
| 🔞 여인무립 삽화 모듈용 로어북 | Works/arcalive/자료/ | ★ — 삽화 전용 NSFW 로어북 |
| 🔞 종말도시 연대기 NSFW 이미지 추가 | Works/arcalive/자료/ | ★ |
| 삽화모듈용 아이돌마스터 288인 외형 태그 로어북 | Works/arcalive/로어북/ | ★ SFW — asset_agent 이관 |
| [자료] 나노 바나나 이미지 생성용 프롬프트 | Works/arcalive/lorebooks_raw/ | 참고 |
| [자료] 배경+감정 이미지 동시 출력 상태창 | Works/arcalive/lorebooks_raw/ | SFW — asset_agent 이관 |

## D. NSFW 에셋/모듈 (이미지 태그 부포함) — 발굴 후선
🔞 SDS 펨돔 NSFW 프리셋 / 조교아카 에셋 모음 / 진보촌 에셋 프리셋 / 흐으응 모듈 v1·v2 / 섹스 메모리 모듈 / 쿰종신기 / 자궁 소스코드 / Asset maid 3종 / 무림애사 / 얼헌 쉬메일 DLC 외 — 채팅 모듈이지만 이미지 태그 블록 포함 여부는 개봉 검사 필요. 후선 큐.

## E. 🚫 차단 등급 — 절대 미사입 (POL-4 하드차단)
| 자료 | 처리 |
|---|---|
| 🔞 깡통봇) 크롭탑 세일러복 자궁문신 절대영역 흑발 **로리** 에셋 | 격리 — 파일명부터 차단 범주. 열람·채굴 금지, 리스틉만 존재 |
| 기타 미성년 지시 포함 자료 (개봉 검사에서 발견 시 이 표에 추가) | 동일 |

## 다음 액션 (zcode)
1. A등급 INRAY NEXUS 2.0 심해 채굴 → nsfw_presets.json 고도화 (관계·상호작용 확장, 오버레이 규칙)
2. C등급 삽화 로어북 2종 개봉 → 태그 사전 반영
3. D등급 후선 큐 개봉 검사 — 이미지 태그 있으면 승격, 없으면 채팅 모듈로 분류(asset_agent 관할)
4. SD 프리셋(B) 태그 이식 검토

## asset_agent 이관 (SFW)
- 아이돌마스터 288인 외형 태그 로어북 → SFW core 사전 후보
- 배경+감정 상태창, 나노바나나 프롬프트, illust_preset 플러그인, 그림체 프롬프트 도서관, 초간단 이미지 분류기, Comfy Set Forge 원클릭 생성기 → SFW 이미지 자산 조사·카탈로그화
