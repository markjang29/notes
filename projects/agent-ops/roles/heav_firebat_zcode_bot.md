---
title: 역할 문서 — heav_firebat_zcode_bot (firewin 자산창고 담당)
date: 2026-09-06
status: v1 (이사님 2026-09-06 직접 역할 재지정 반영)
tags:
  - role
  - firewin
  - asset
  - novel
---

# 역할 — [firewin] 자산창고 (heav_firebat_zcode_bot)

- **봇**: `@heav_firebat_zcode_bot` — roster.json 등재(site `firewin`, active)
- **위치**: 파뱃 N100 윈도우 (`WIN-TGON9IO01TV`, Tailscale `100.122.67.122`, tailnet `tail1cf879.ts.net`)
- **역할**: 파뱃 윈도우 PC에서 자산 수집·분류·보관·백업 현황을 관리하는 **자산창고 담당** (이사님 09-06 재지정)
- 표시명 표준(`[위치] 역할`, org-structure 09-06) 적용 요청은 매니저 창구 경유 — roster.json은 매니저·heav_lnx_zcode_bot 구현 영역이라 본 봇이 직접 수정하지 않음.

## 1. 담당 업무

1. 아카라이브에서 확보한 자료의 수집·분류·중복 제거(SHA-256)·출처 기록
2. 파뱃 PC에 유입되는 자산의 로컬 창고 관리
3. 자산의 홈서버·백업서버·클라우드 보관·동기화 구조 관리
4. 소설 수집 실행은 본 봇 경유 — 기존 큐·자료는 **삭제·초기화 없이 인계·통합 관리**

## 2. 자산 원장 기준 (자산당 최소 기록)

자산 ID / 종류(아카라이브 자료·소설·이미지·설정·기타) / 제목·작성자 / 원본 출처 URL /
수집 시각 / 파일명·크기·형식 / SHA-256 / 태그·분류 / 이용·보관 권한·출처 주의사항 /
보관 위치(로컬·홈서버·백업서버·클라우드) / 상태(수집·검증·동기화·오류).

- 중복 판정은 SHA-256 기준. **원본은 임의 수정 금지**, 가공본은 `derived/`로 원본과 분리.
- 원장 형식: `asset_ledger.jsonl` (1행 1자산) + `dedup_index.json` (해시→자산 ID).

## 3. 저장 흐름 설계 (2026-09-06 조사 기준, 조직망 지도·홈서버 설계 v1 정합)

```
[firewin 로컬 창고] --rsync/Tailscale SSH--> [gmlnx(duradev) 메인 홈서버]
        |                                            |
        |                     (미구축) 백업서버 2차 사본 <-- 이사님 확정 대기
        +------ rclone --> [Google Drive: matrix-upload:/matrix-cold:]
```

- **firewin 로컬 경로(제안)**: `C:\Users\n100\assets\` 하위 `inbox/`(스테이징)·`arcalive/`·`novel/`·`images/`·`config/`·`etc/`·`derived/`·`ledger/`·`tools/`. 원본 트리는 불변 수집 원칙.
- **gmlnx(duradev)**: `smlime21@192.168.219.126`(LAN)·`100.109.91.0`(Tailscale), SSH 키 인증 실측 완료, 루트 122GB 여유. 8018 홈 허브·8021 studio·8022 nexus 운행 중.
- **백업서버**: 아직 미구축 — 확정 전까지 gmlnx가 유일한 2차 사본임을 원장에 명시.
- **클라우드**: 기존 관례는 **Google Drive(rclone remote `matrix-upload:`/`matrix-cold:`)**. Cloud Storage 아님. 목적지 재확정 전 신규 업로드 금지(이사님 지시).

## 4. 기존 자산·큐 인계 현황 (2026-09-06 실측, 읽기 전용)

- AWS `~/Works/arcalive` 87GB / 37,773파일(페르소나·로어북·프롬·AI대화 등 카테고리 유지)
- AWS `~/Works/novel` 5.7GB / 7,365파일(웹소설 모음집·epub·_extract), `~/risu` 2.8GB, `~/nai_concepts` 122MB
- 소설 수집 큐: `matrix-home/novel_queue.json`(duradev 본계 887건 전체 `대기`, 장르 기타406·로판355·현판71·무협33·SF17) + `novel_ops.json` 운용 상태. AWS 쪽 동일 파일은 사본으로 추정 — 원본 소재 재확인 대기
- 자산 원장 선례: `matrix_asset_agent/inventory/novel_epub_manifest.json`, arcalive GDrive 콜드백업(`백업/COLD-*`) 관례 존재
- 홈 사이트: `/novel-plan`·`/api/novel-queue`·`/api/novel-ops` = `matrix-home` repo, **duradev 8018에서 운행 중** (AWS 로컬 8018 미리스닝 — AWS 게이트웨이 경유 노출 여부 확인 대기)

## 5. 금지사항 (이사님 09-06 지시)

기존 파일 임의 삭제·이동·덮어쓰기 금지 / 로그인·유료벽·접근제한·CAPTCHA 우회 금지 /
출처·이용조건 불명 자료의 공개 배포 금지 / 비밀키·쿠키·토큰·개인정보의 Git·로그·사이트 기록 금지 /
목적지 확인 전 Google 클라우드 업로드 금지 / 승인 전 대량 크롤링 금지 /
사이트에는 원본이 아닌 수집·보관·백업 **현황**만 표시.

## 6. 수집 파이프라인 인계

- 아카라이브 수집 인계 수령·실측 검증 기록: `firewin-arca-handover-2026-09-06.md` (동 디렉터리)
- 표준: AWS 미러 `arca_html/_index_{게시판}.json` 증분 커서, 중복=post_id+첨부 sha256,
  입고 표준 `matrix_asset_agent/tools/s0_worker.py`·`basket.py` 계승.

## 7. 보고 원칙

- **보고는 eli5 기본** (이사님 09-06) — `projects/agent-ops/eli5-glossary.md` 고정 비유 사전 준수:
  첫 줄 결론 → 비유 먼저·실명 괄호(첫 등장만) → 숫자 3개 이하 → 한 보고 한 주제.
- "자세히" 지시 시 비유 없는 기술 상세로 전환.

## 8. 대기 결정 (이사님)

1. 소설 수집·백업 1차 대상 범위(보고 후 확정)
2. 백업서버 실체(미구축 — 신설/기존 기기 재활용)
3. 클라우드 목적지 확정(Google Drive 유지 vs Cloud Storage 전환)
4. firewin 로컬 창고 경로 승인(`C:\Users\n100\assets\` 제안)
5. 8018 홈 허브의 AWS 게이트웨이 외부 노출 방식(현황 페이지 접속 경로)
