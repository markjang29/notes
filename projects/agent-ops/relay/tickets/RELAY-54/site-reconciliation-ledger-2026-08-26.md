# 사이트·요구사항 정합성 장부 (2026-08-26)

## 목적

이 장부는 이사님이 AWS ZCode Telegram 대화창에서 지시한 사이트 구현 요구사항을
Jira, Notes, Git, 실행 사이트, 담당 봇과 한 줄로 맞추기 위한 공통 기준이다.

기능을 새로 만들기 전에 모든 봇은 이 장부를 먼저 읽고, 기존 구현을 삭제하거나 임시로
무시하지 말고 `구현됨`, `부분구현`, `잘못구현`, `미구현`, `검증불가`, `정리필요` 중
하나로 상태를 남긴다.

## 정본 기준

- 사용자 원문 기준: AWS ZCode 입력 이력 2026-08-19~2026-08-26 사용자 입력 100건.
- 보조 요약: `projects/agent-ops/relay/tickets/RELAY-54/director-directives-0825.md`.
- 감사 정정: `projects/agent-ops/relay/tickets/RELAY-54/audit-correction-zcode-brief-2026-08-26.md`.
- 공통 가이드: `projects/agent-ops/relay/site-integration-guide-2026-08-24.md`.
- 포트 등록표: `projects/agent-ops/relay/port-registry.json`.

## 현재 핵심 불일치

1. RELAY-54의 44건은 전수본이 아니다. 구현 감사는 AWS ZCode 입력 100건을 기준으로 한다.
2. port-registry에는 일부 티켓이 Jira 실재 검증된 것처럼 적혀 있으나, 현재 확인한
   RELAY-35, RELAY-41, RELAY-50, RELAY-54, RELAY-55, RELAY-56은 Jira 상세 API에서 404였다.
3. RELAY-35, RELAY-50, RELAY-55, RELAY-56의 Notes ticket folder 산출물은 origin/main 기준
   비어 있다.
4. 8016, 8015, 8018은 응답하지만, 사이트 응답은 요구사항 완료 근거가 아니다.
5. AWS ZCode와 aws-audit 사이에는 즉석 직접 호출과 ACK는 가능하지만, reviewed Agent Mail
   수준의 내구성 왕복 계약은 아직 없다.

## 사이트별 현재 상태

### 8016 이미지 스튜디오

상태: 부분구현.

확인된 구현:

- NSFW status/toggle/presets API.
- reroll API.
- delete API.
- image JSON 확인 경로.
- NSFW 관련 UI/클릭 테스트 흔적.

검증 또는 수정 필요:

- NSFW 버튼이 실제 UI에서 ON/OFF로 안정 동작하는지.
- 태그 칩을 여러 번 눌렀을 때 중복 append가 아니라 토글되는지.
- NSFW ON일 때 별도 카테고리 또는 기존 생성창 내 명확한 NSFW 표시가 있는지.
- 카드 클릭 시 NSFW 랜덤다이스 리롤이 되는지.
- 삭제 확인이 실제 tombstone과 UI에 반영되는지.
- 리롤 시 최종 JSON 프롬프트를 볼 수 있는지.
- 리롤 프롬프트가 최근 3턴 채팅 본문의 고유 장면 단서를 보존하는지.
- 작품 근거문서와 작품 관련 장면 카테고리를 선택할 수 있는지.

현재 감사 테스트:

- `matrix_asset_agent:tests/test_relay54_audit_contract.py`.
- 결과: 6개 중 5개 통과, 1개 실패.
- 실패 내용: `scene_to_nai.extract_tags()`가 `붉은 우산`, `깨진 바이올린` 같은 장면 고유 단서를
  프롬프트에 보존하지 못한다.

### 8015 Matrix Workbench

상태: 부분구현.

확인된 구현:

- 연속 3턴 모드.
- 자동생성 사용자 발화 표시.
- 캐릭터 응답 전문 표시.
- 단발 실행 기록과 연속 3턴 기록 병행 표시.
- asset/module/base_stack 표시 코드.
- coverage engine 흔적.

검증 또는 수정 필요:

- 실제 DB의 최신 레코드에서 3턴 전문이 모두 보이는지.
- 구버전 데이터에서 “실사 기록 없음”으로 잘못 보이는지.
- 사용자 자동발화와 실제 사용자 발화가 명확히 구분되는지.
- 모듈, 로어북, 페르소나, 캐릭터, 모델, NAI 설정 전체가 조합으로 묶여 보이는지.
- RISU 왕복 증거가 표시되고 승인 전 gate로 쓰이는지.

### 8018 통합 홈

상태: 부분구현.

확인된 구현:

- 주요 사이트 링크.
- 사이트맵 페이지.
- 로드맵 페이지.
- 승인 카드 페이지.
- Jira 이슈 표시 코드.

검증 또는 수정 필요:

- Jira 404 문제 때문에 이슈 표시를 완료 근거로 볼 수 없다.
- 전체 사이트의 실제 상태와 티켓 상태가 동기화되는지.
- 단계별 마블 개수와 흐름이 실시간으로 보이는지.
- “다음 승인”이 무엇을 의미하는지 쉽게 설명되는지.
- 승인보드, Workbench, 이미지 스튜디오, Arcade 사이 URL이 RESTful하게 연결되는지.

### 8005 승인보드

상태: 정리필요.

확인된 구현:

- 서비스는 인증 요구 상태로 응답한다.

검증 또는 수정 필요:

- 승인 카드가 이사님에게 쉬운 말로 설명되는지.
- 승인 전 필요한 근거가 연결되는지.
- 승인 이력이 Jira 또는 Notes 정본에 남는지.
- Jira 404 상태에서 승인보드가 어떤 정본을 참조하는지.

## 봇별 역할

### AWS ZCode

- 8016/8015/8018 구현 및 UI/API 테스트.
- 기존 기능 제거 금지.
- 실패 테스트를 먼저 재현하고 수정.
- 수정 후 관련 테스트 실행, 커밋, 푸시.

### asset_agent

- NSFW 태그 포함 자산 전수 리스트업.
- NSFW가 아닌 자산은 별도 일반 자산 흐름으로 분리.
- 여성향, 무협, 판타지, 현대물, 연애소설, 웹소설식 태그 체계 설계.
- 마스터 자산번호와 sha256 alias 체계 설계.

### novel_col

- 이미지 스튜디오의 NAI 프롬프트 JSON 표시.
- 리롤·랜덤·삭제 확인 UX.
- 작품 근거문서와 작품 관련 장면 카테고리.
- 외부에서 전달된 core/scene을 이미지 생성에 쓰는 인터페이스.

#### novel_col 상태 표시 (2026-08-26 실측, commit 기준 8676ae2·147449e·a32562e)

- NAI 프롬프트 JSON 표시: **구현됨** — `/image/<id>` REST(프롬프트·시드·negative·provenance 전체, 라이브 200 확인) + 상세 시트 "📄 생성 JSON 보기" details 토글.
- 리롤·랜덤·삭제 확인 UX: **구현됨** — 리롤 2종 명확화("같은 장면 다른 테이크"/"NSFW 랜덤다이스"), 삭제 confirm 문구→"삭제 중…"→목록 갱신+`deleted` 필터 tombstone. 최종 실클릭 검증은 render_test.js로 AWS ZCode와 공동 진행.
- 작품 근거문서·작품 장면 카테고리: **구현됨** — `/api/scene_ideas`(works 기반)+applyIdea 근거 기입, "이 작품의 장면" 섹션, RISU 근거문서 `/api/work/<work>`, a32562e로 채팅 3턴 근거(작품·발췌) scene_basis 보존.
- 외부 core/scene 인터페이스: **부분구현** — RELAY-54 URL 프리필 `?core=&scene=&entity=` 동작 확인. gap: 공식 API 계약(스키마·문서화) 부재, 고유 장면 단서 보존 테스트 실패(extract_tags — AWS ZCode 담당 구분).
- RELAY-35·41은 Jira 404 → 완료 처리하지 않고 gap 유지.

### manager

- Jira 404와 Notes ticket folder 불일치 정리.
- 티켓 없는 완료 보고 금지.
- 단계 라벨 전이는 산출물 커밋이 있을 때만 수행.
- 각 봇의 gap을 중복 없이 취합.

### rpg

- 8017 자산 워크벤치 운영·기능 확장(레시피 조립·목업·내보내기).
- 8009 게임(걷기×전술) 기능 검증·정합 관리.
- 매트릭스 승인 자산의 RPG 수용 포맷 조율.

#### rpg 상태 표시 (2026-08-26 실측, rpg_game repo commit ed5a6d5·2ac01ef·79681e9 계열)

- **8017 RPG 자산 워크벤치: 부분구현** — 라이브 200 확인(갤러리 8자산).
  구현됨(검증): 유형 6종(CHR/WLD/WPN/ITM/UI/EFX)·스타일 3종(도트 포함)·UI 하위 5종·테마 4종,
  NAI 생성(오푸스 무료조건 고정 ≤1MP·28스텝), 리롤(시드 변경), 감정·시선 변형(같은 시드·계보 기록,
  시선=공격 분류 연결), 캐릭터 프로필 별도 파일(profiles/, 메타엔 참조만), 갤러리·메타 조회,
  접속키 인증, NAI 토큰 서버 사이드(~/.nai-token, Git 제외), RELAY_TICKET=RELAY-36 주입,
  port-registry 8017 등록.
  미구현(gap): 레시피(전장+캐릭+EFX 세트) 조립, 모바일 목업 미리보기, 배치 스크립트, 후보 비교 diff,
  드라이브 RPG저장고 업로드 버튼, 매트릭스 승인자산 주입(승인보드 연계), 승인 상태 파이프라인 UI,
  systemd化(재부팅 시 수동 기동).
- **8009 RPG 게임(걷기×전술): 기능 검증불가(운영은 구현됨)** — gunicorn 2워커 라이브 200,
  title "RPG 시스템 — 걷기×전술", RELAY_TICKET=RELAY-47 주입, 배포 `/home/ubuntu/apps/rpg-game-01`
  (current→releases/20260727-215555, 2026-07-27 배포, rpg 봇이 만들지 않음 — RELAY-47 담당 추정).
  gap: 시그니처(패링·걷기 버퍼·전술) 반영 수준 미검증, 정본 repo(projects/rpg-game-01)와 배포 사본
  정합 미확인, 릴리즈 7-27 이후 갱신 없음.
- **RELAY-40 아카라이브 RPG식 채팅 자산 조사: 구현됨** — Notes 아티팩트 1-req + findings 1·2차
  커밋(150자산 발굴, TRPG MASTER·상태창 2.2v·던전·RPGM 루프 분석).
- **RPG Jira 프로젝트(아이디어 티켓 RPG-1~9): 미구현→유실(gap)** — 2026-08-22 생성 확인했으나
  현재 404. 재건 여부는 매니저 결정 대기.
- ★ **Jira 전면 장애 보고(2026-08-26 실측)**: 프로젝트 목록 API가 `[]`(200) — RELAY/RPG/MAT 전
  프로젝트·전 티켓 404. 본 장부의 404 목록(일부)이 아니라 전면 유실 상태. 매니저 긴급 확인 필요
  (플랜 만료·사이트 삭제·이전 여부). Jira 회복 전 티켓 추적은 Notes relay/tickets/ 경유.

### aws-audit

- 사용자 입력 100건 기준으로 구현/부분구현/잘못구현/미구현/검증불가 판정.
- 완료 보고와 실제 Git/Jira/사이트 근거를 분리.
- 검증 전 완료·closed 판정 금지.

## 지금 일할 순서

1. Jira/Notes/port-registry 정합성 복구.
2. 8016 이미지 스튜디오 실패 테스트 수정.
3. 8016 UI 클릭 테스트로 NSFW, 토글, 리롤, 삭제, JSON 검증.
4. 8015 Workbench 3턴 전문·자산 조합 표시 검증.
5. 8018 홈 사이트맵·이슈·승인 의미·마블 흐름 검증.
6. asset_agent가 자산 태그와 마스터 번호 체계를 설계.
7. novel_col이 이미지 생성 인터페이스와 작품 근거 연결을 정리.

## 모두에게 전달할 문장

RELAY-54 정합성 장부가 추가됐다. 모든 봇은 notes origin/main의
`projects/agent-ops/relay/tickets/RELAY-54/site-reconciliation-ledger-2026-08-26.md`를 먼저
읽고, 이사님 AWS ZCode 대화 100건 기준으로 자기 담당 사이트와 산출물을
`구현됨/부분구현/잘못구현/미구현/검증불가/정리필요` 중 하나로 표시하라. 기존 기능 삭제나
임시 우회 금지. Jira가 404인 RELAY-35/41/50/54/55/56은 완료 처리하지 말고 gap으로 남긴다.
AWS ZCode는 8016 실패 테스트와 8015/8018 검증부터, asset_agent는 NSFW·일반 자산 분리와
마스터 번호부터, novel_col은 NAI JSON·리롤·작품 근거 연결부터, manager는 Jira/Notes/port-registry
불일치 정리부터 진행하라.

