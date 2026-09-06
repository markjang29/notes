---
title: firewin 자산창고 저장·동기화 설계 v1 (백업정책 v2 확정 반영)
date: 2026-09-06
status: v1 — 이사님 09-06 정책 확정(3계층·삭제금지·자율순서·웹 오너쉽 인수) 반영
tags:
  - asset
  - sync
  - firewin
  - gmlnx
---

# firewin 자산창고 저장·동기화 설계 v1

## 1. 확정 정책 (이사님 09-06)

- **3계층 확정**: firewin 로컬(원본 1차) → **gmlnx(duradev) 운영서버 미러(2차)** → **Google Drive 콜드(3차)**.
  별도 백업서버는 신설하지 않는다 — gmlnx가 운영+2차 사본 겸임.
- **삭제 금지·압축 우선**: 정리는 압축으로 한다. 동기화 도구의 자동 삭제는 항상 차단
  (`--backup-dir`→`assets-trash/타임스탬프/`, GDrive는 휴지통 기본).
- **순서 자율**: 수집·편입 순서는 자산창고가 관리(현 우선순위: 2026-08-08 이후 증분,
  페르소나·모듈·로어북 먼저 — 구 수집 담당 인계 기준).

## 2. "이동하면 동기화가 깨진다" 문제 — 3중 해법

문제: rsync/rclone은 이동을 "삭제+새로복사"로 본다 → 대형 자산 재업로드·양측 불일치·삭제 사고.

1. **불변 경로(근본 해법)**: inbox 검증 통과 시 최종 경로를 1회 배정하고 그 뒤 물리 이동 금지.
   재분류는 원장 태그만 수정 — 이동 자체를 대부분 없앤다.
2. **원장 선행 이동 프로토콜**(부득한 이동 시): ① 원장에 새 경로 선기록 →
   ② 계층별 `rclone moveto`(삭제+복사 아닌 이름변경 연산) → ③ sha256 재검증 → ④ 원장 완료 갱신.
3. **도구 옵션 안전망**: `--track-renames`(해시로 이름변경 감지해 재업로드 회피) +
   `--backup-dir`(덮어쓰기 발생 시 기존 파일 폐기 대신 trash 보관). 단방향 sync만 사용 —
   bisync(양방향)는 분리 금지.

## 3. 압축 정책 구체화

- **압축 대상**: 텍스트류 — 게시판 HTML 스냅샷·인덱스 JSON·본문 텍스트. 보드×연도 단위
  `tar + zstd`로 `derived/archives/{board}/{year}/`. 원본 트리는 그대로 두고 압축본은 derived에.
- **무압축 유지**: jpg·png·epub·zip 등 이미 압축된 포맷(재압축 이득 없음) — 원본 보관.
- **중복 처리**: 동일 sha256은 물리 사본 1개 + 원장에 경로 alias 다중 기록(중복 폴더 사본 늘리지 않음).
  gmlnx에서는 선택적으로 하드링크 허용.

## 4. 검증

- **매 동기화 후**: 양측 sha256 manifest 차집합 대조(`assets/tools/verify_manifests.sh` — ssh만으로 동작, 설치 완료).
- **주 1% 샘플 재해시**: 원장에서 무작위 추출해 3계층 동일성 표본 감사, 결과는 원장 상태 필드에 기록.

## 5. 자산 현황 웹 오너쉽 인수 (이사님 09-06 지시)

- **대상**: 8018 matrix-home의 자산 뷰 — `/asset/<key>`(마스터번호 MA-xxx 조회·SHA-256·원본 경로),
  `/cards`, `/dossiers`, `/api/stats`(raw_epub 1537·raw_lorebook 590·raw_persona 345 등),
  `/s0` + 8015 workbench_web `/city`(구역별 스카이라인).
- **데이터 실체**: duradev mongo `workbench.assets`(마스터번호·kind·sha256·source_path).
- **계승**: RELAY-50/56에서 AWS zcode가 만든 것을 이사님 지시로 firewin zcode가 인수.
  기존 페이지·DB는 그대로 — 중복 신규 제작 금지, 이어받아 자산창고 현황(수집·검증·동기화·오류) 확장.
- 관제 roster/회의방 등록 갱신은 매니저 창구로 요청(본 봇 직접 수정 금지).

## 6. 설치 현황 (2026-09-06)

- firewin 창고 골조 완료: `C:\Users\n100\assets\` (inbox·종류별·derived·ledger·tools) + README 4원칙.
- `verify_manifests.sh` 설치 완료(rclone 불요), `sync_to_gmlnx.sh` 설치(rclone 필요).
- 스모크: firewin → arca.live **HTTP 200**(0.7s) — AWS IP 403과 달리 수집 가능 IP 확인.

## 7. 남은 설치 과제 (순서대로)

1. rclone 설치(winget) + AWS의 GDrive remote 설정 이식 — 자격 이동이므로 이사님/매니저 확인 후.
2. gmlnx `~/assets-mirror/` 초기 생성 + 첫 전체 미러.
3. 이사님 로그인 세션 수령(로그인 필요 첨부용) — 미수령 상태에서도 공개글 증분은 가능.
4. 증분 수집기 가동(커서 = 게시판별 `_index_*.json` max post_id, 요청 간격 유지, 페르소나·모듈·로어북 우선).
