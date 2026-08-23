# [impact] 영향성 검토 (감사 CODEX)

- jira: RELAY-42
- 검토 기준: notes-registry `a0c80b56737733c5d9d3fac88b6e75f90b8b01d7`
- 대상 기준: `markjang29/music_video` `a273c47054a83c6ba8cad25aea15ac657cccb250`
- 영향 repo/서비스/봇 목록:
  - repo: `markjang29/music_video` (`index.html`, `app.js`, `styles.css`, 필요 시 `server.py`와 테스트)
  - service: AWS systemd `music-video.service`, 공개 HTTP 8020
  - runtime data: 기존 여행 체크 상태·언어·사이드바 localStorage, 새 일상 일정·서류 localStorage
  - existing write path: 편집 키 → GLM KO/EN/VI 번역 → `content.json` commit/push
  - bots: 5-구현 담당자(미지정), 6-코드리뷰 담당자, 게이트 운영 `aws-manager`
- 되돌릴 수 없는 변경 여부:
  - 코드와 정적 UI는 직전 검증 commit을 고정하면 되돌릴 수 있다.
  - localStorage 스키마를 파괴적으로 변경하거나 기존 키를 재사용하면 사용자 브라우저 데이터는 Git rollback으로 복구할 수 없다. 새 일상 데이터는 별도 versioned namespace를 사용하고 마이그레이션·초기화 전에 JSON 내보내기를 제공해야 한다.
  - 배포 중 기존 `/api/content`가 새 `content.json` commit을 만들 수 있으므로 단순 `reset` rollback은 사용자 편집 commit을 잃을 수 있다. 배포 시 편집 쓰기 중단/배수, clean tree 확인, `pull --ff-only`, 배포 전후 full commit 기록과 content commit 보존 절차가 필요하다.
- 기존 안건과 충돌:
  - 현재 `AGENTS.md`는 첫 화면 우선순위를 촬영→여행 동선→참고로 고정한다. 2분할 랜딩은 이 기존 규칙을 바꾸므로 4-설계에서 AGENTS 갱신 범위와 Director 승인을 명시해야 한다.
  - 기존 앱은 단일 문서의 고정 DOM ID와 초기화 흐름에 촬영·날짜·편집·언어·영감 보드를 결합한다. 여행 UI를 재작성하면 회귀 위험이 크므로 기존 여행 DOM/API를 유지한 채 얇은 영역 라우팅을 앞에 두는 구조가 우선이다.
  - 기존 체크·언어·편집 키 저장 키를 일상 CRUD 키와 혼용하면 안 된다. 촬영 편집은 서버/Git 쓰기이고 일상 데이터는 브라우저 전용이라는 경계를 UI와 코드에서 분리해야 한다.
  - 현재 페이지는 `https://unpkg.com`의 실행 스크립트를 로드한다. 같은 origin 페이지에서 실행되는 제3자 스크립트는 localStorage를 읽을 수 있으므로 혼인·비자 생활 데이터 도입 전 스크립트를 self-host/pin하고 CSP 또는 동등한 공급망 경계를 설계해야 한다.
  - 공개 HTTP는 전송 기밀성을 제공하지 않는다. 일상 기능은 여권번호·등록번호·문서 스캔·인증정보 입력란을 만들지 말고, 서버 API·로그·Git으로 전송하지 않음을 네트워크 테스트로 증명해야 한다.
- 위험도(상/중/하)와 근거: **상**
  - 운영 중인 단일 페이지와 self-mutating Git API를 동시에 변경·재시작한다.
  - 기존 여행 기능의 회귀 표면이 날짜 선택, 체크 상태, 촬영 5필드 편집, KO/EN/VI, 러프컷, 영감 보드, 여행 링크, GLM 번역, Git push까지 넓다.
  - 혼인·TOPIK·F-6 데이터는 개인 생활정보이며 localStorage는 서버 미업로드만으로 충분히 보호되지 않는다.
  - 현재 기준 GET `/`, `/api/content`, `/api/health`는 200이고 숨김 경로는 404, service와 원격 main은 정상·clean이다. 이 baseline을 구현 후 그대로 재검증해야 한다.
- 판정: **조건부**
  1. 4-설계에서 여행 화면을 가능한 한 그대로 보존하는 영역 라우팅, 브라우저 뒤로가기·직접 진입·새로고침 동작을 고정한다.
  2. 새 일상 저장소는 별도 versioned localStorage namespace, 스키마/크기 제한, 안전한 DOM 출력, JSON export를 사용한다. import를 구현하면 명시적 확인과 엄격 검증을 추가한다.
  3. 제3자 실행 스크립트의 localStorage 접근 위험을 제거하거나 self-host/pin+CSP로 제한한다. 민감 식별자·원문 문서 업로드 필드는 금지한다.
  4. 기존 여행 기능 전체와 390px/1440px를 자동화 또는 재현 가능한 체크리스트로 회귀 검증하고, 5-구현 repo 게이트에 순수 로직 단위 테스트를 추가한다.
  5. 배포 전 편집 쓰기 배수, clean/FF-only 확인, full commit checkpoint, 서비스 재시작, GET/API/숨김경로 확인, 실패 시 사용자 `content.json` commit을 보존하는 rollback 절차를 설계한다.
  6. 법률·시험 일정의 정확성은 이 영향성 검토의 승인 대상이 아니다. 구현 직전 spec의 공식 출처와 기준일을 다시 확인하고 불확실한 값은 확정 표현하지 않는다.
  7. 이 판정은 3-영향성검토 산출물이며 4-설계 승인, 5-구현, 배포 또는 release 승인을 대신하지 않는다.
