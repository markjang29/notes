# RELAY-54 감사 기준 정정 및 ZCode 개발 브리프 (2026-08-26)

## 판정 요약

RELAY-54의 `director-directives-0825.md` 44건은 유용한 요약본이지만, 이사님이 AWS ZCode
Telegram 대화창에 평문으로 지시한 전체 요구사항의 전수본은 아니다. 구현 감사의 기준은
ZCode 입력 이력에서 복구한 2026-08-19~2026-08-26 사용자 입력 100건이며, 44건 문서는
그 하위 요약 또는 보조 대사표로만 사용한다.

## 바로잡은 기준

- 실제 협업 상대: AWS 서버에서 실행 중인 ZCode CLI/Telegram bridge.
- 감사 actor: `aws-audit`.
- 매니저 역할: 배분·중계·보고. 구현 검증 상대가 아니다.
- 통신 상태: 즉석 직접 호출과 로그 조회는 가능하지만, reviewed Agent Mail 수준의 내구성
  양방향 계약은 아직 아니다.
- 감사 기준: 사용자 평문 지시 100건 → RELAY-54 44건 포함 여부 → Jira/Notes/Git/실행 사이트
  구현 여부 순서로 판정한다.

## 즉시 확인한 불일치

- `port-registry.json`에는 RELAY-35, RELAY-50 등 일부 항목이 Jira 실재 검증된 것처럼 적혀
  있으나, 현재 Jira 상세 API 확인에서는 RELAY-35, RELAY-41, RELAY-50, RELAY-54, RELAY-55,
  RELAY-56 모두 404로 반환됐다.
- RELAY-35, RELAY-50, RELAY-55, RELAY-56의 Notes ticket folder 산출물은 현재 `origin/main`
  기준 비어 있다. RELAY-54에는 44건 요약 파일만 있다.
- 8016 이미지 스튜디오, 8018 통합 홈, 8015 Workbench는 응답하지만 “응답함”은 “요구사항 완료”
  근거가 아니다.

## 1차 구현 판정

### 8016 이미지 스튜디오

부분구현. NSFW status/toggle/presets, reroll, delete, image JSON 관련 API와 UI 테스트 흔적은
있다. 그러나 리롤 프롬프트가 실제 채팅 장면의 고유 특징을 보존하는지에 대해서는 실패
테스트가 생성됐다. `scene_to_nai.extract_tags()`는 현재 하드코딩 장소·행동 사전에 걸린 단서와
기본 캐릭터 묘사 위주로 프롬프트를 만든다.

### 8015 Matrix Workbench

부분구현. 현재 실행 clone의 `workbench_web.py`에는 마지막 턴만 가져오던 필터가 제거되어 있고,
연속 3턴 모드와 단발 실행 기록을 함께 보여주는 코드가 있다. 단, 실제 DB 데이터가 구버전 또는
비어 있으면 화면상 “실사 기록 없음”은 여전히 발생할 수 있다.

### 8018 통합 홈

부분구현. 사이트맵, 주요 포트 링크, `/sites`, `/roadmap`, `/dossiers` 경로는 있다. 하지만 Jira
이슈 연동이 404 상태와 충돌하므로, 이슈 표시와 승인 대기열은 신뢰할 수 있는 완료 근거가 아니다.
“마블이 파이프라인 따라 흐르는” 실시간 흐름·단계별 개수 시각화도 별도 확인/구현이 필요하다.

## 역할별 작업 분리

- AWS ZCode: 8016/8015/8018 UI·API 동작 검수와 8016 프롬프트 재추출 실패 수정.
- asset_agent: NSFW 태그 포함 자산 리스트업, 일반 자산 분리, 장르·성향 태그 체계, 마스터 자산번호.
- novel_col: 이미지 스튜디오 리롤/랜덤/JSON 표시, 작품 관련 장면 카테고리, 외부 core/scene 입력 계약.
- manager: Jira 404와 Notes ticket folder 불일치 정리. 상태 전이는 실제 증거가 생긴 뒤에만 수행.
- aws-audit: 위 결과를 사용자 입력 100건 기준으로 구현/부분구현/미구현/잘못구현/검증불가로 독립 판정.

## 다음 개발 지시문

AWS ZCode는 기존 기능을 제거하지 말고 RELAY-54/RELAY-56 범위에서 8016 이미지 스튜디오와 8015
Workbench의 검증 가능한 결함만 고친다. 1순위는 `scene_to_nai.extract_tags()` 및 8016 리롤 경로가
최근 3턴 채팅 본문의 고유 장면 단서와 작품 근거를 프롬프트 JSON에 보존하도록 수정하는 것이다.
2순위는 8016 UI에서 NSFW 토글, 태그 칩 중복 클릭 토글, 삭제 확인, 이미지 JSON 보기, 카드 클릭
NSFW 랜덤 리롤을 Playwright 또는 기존 `render_test.js`로 검증하는 것이다. 3순위는 8015
Workbench에서 3턴 연속 채팅 전문, 자동생성 사용자 발화 표시, 캐릭터 응답, asset/module/lore/persona
조합 전체가 실제 DB 레코드와 연결되어 보이는지 테스트로 고정하는 것이다. 수정 후에는 새 테스트와
기존 관련 테스트를 실행하고, 미구현 항목은 Jira가 404이면 Notes ticket folder에 gap으로 남긴다.

