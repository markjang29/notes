# NSFW 카테고리 구현 인수인계서 (RELAY-39 → 구현 담당 봇)

> 2026-08-23 · 작성: novel_col (RELAY-39 담당) · 승인: 이사님
> **이 문서 하나로 구현이 가능하게 쓴 자립형 명세.** 원본 요구사항: 같은 폴더 `NSFW-요구사항-명세.md`

---

## 0. 이 문서를 받은 봇에게 (반드시 먼저 읽을 것)

1. 당신의 임무: **소설 자산 이미지 스튜디오에 NSFW 생성 카테고리·토글을 구현**한다. SFW 파이프라인은 절대 건드리지 않는다.
2. 절차: ①`git pull` ②Jira 티켓 등록(RELAY-40, 없으면 신규) ③구현 ④검증(§5) ⑤pre-push 게이트 통과 커밋·push ⑥notes에 구현기록 ⑦이사님 Telegram 보고.
3. **금지 (NEVER)**: `review_status` 자동 `reviewed` 부여(이사님만 가능) · 시크릿/토큰 Git 반입 · PNG 바이너리 Git 반입 · SFW 매니페스트/드라이브 폴더에 NSFW 파일 혼입 · 미성년·실존 인물 묘사 태그 허용.
4. 모호하면 구현 추측으로 때우지 말고 **중단하고 이사님께 질문**. (단, §6 열린 질문에 이미 있는 것은 이사님 결정 대기 목록임)

## 1. 배경 (요약)

- 스튜디오는 현재 SFW 전용. 수집 자산(works·RISU 카탈로그)에 성인용 로어북/소설이 다수 있어, 이들을 **별도 카테고리·별도 저장소·별도 승인**으로 분리 생성해야 한다.
- 이사님 원문 지시: "NSFW 관련 토글 켜서 따로 뽑을수 있는 카테고리 만들어주고 NSFW는 니가 구현 못하면 요구사항 명세만 작성해"

## 2. 현재 시스템 (구현 전 필독 파일 — 이 순서대로)

| 파일 | 내용 |
|---|---|
| `/home/ubuntu/projects/scenario` (git) | repo. Windows 사본 에이전트도 공유 — 작업 전 `git pull`, 후 즉시 push |
| `novel_assets/images/README.md` | **표준 문서**: 스키마 v1.1, 일관성 3원칙, 조립 규칙 `quality_boost + ", " + identity_core + ", " + scene_layer`, 태그 작성 규칙(3-1절) |
| `novel_assets/images/app/main.py` | Flask 백엔드 (8016). 핵심: `nai_generate()`, `generate_record()`, `DEFAULT_NEG`, `QUALITY`(boost 포함), `/api/generate`, `/api/reroll`, `/api/manifest` |
| `novel_assets/images/app/static/index.html` | 모바일 우선 SPA. `ED` 상태, `go()`, `autoFill()`, `randomGo()`, `TAGS` 태그 사전 |
| `novel_assets/images/manifest.ndjson` | **정본**. 1행=1이미지. append만 함(수정 금지) |
| `novel_assets/images/app/check.sh` | 배포 검수 4중: JS 문법·API·페이지·puppeteer 실렌더 |
| `novel_assets/images/app/render_test.js` | 실렌더 전흐름 테스트. **기능 추가 시 여기에 케이스 추가가 의무** |

**실행 환경**
- 서버: Ubuntu 24.04 (AWS) · 서버 시간 KST
- 실행: `~/.venvs/novelweb/bin/python main.py` (flask+markdown) · 포트 **8016** · @reboot crontab 자동시작
- 재시작: `ss -tlnp | grep ':8016 '` 로 PID 찾아 kill 후 nohup 재기동 (pkill -f 금지 — 자기 자신 죽음)
- NAI: 모델 `nai-diffusion-3`만 작동(v4.5는 500) · 토큰 `/home/ubuntu/.nai-token` (Git 반입 금지) · 무료 사이즈 832×1216 · 응답은 raw ZIP
- 구글드라이브: rclone `matrix-upload:소설자산이미지/...` · 로컬 1차 정본 `/home/ubuntu/nai_out/studio`
- push 게이트: `.git/hooks/pre-push`가 check.sh 실패 시 push 차단

## 3. 요구사항

### 기능 (FR)
- **FR-1 연령 게이트**: `app/nsfw_config.json` 기본 `{"enabled": false}`. false면 NSFW API·UI 전면 비활성(403). 토글은 설정 파일 + 세션 양쪽 반영.
- **FR-2 카테고리 필드**: 생성 요청 `category: "sfw"|"nsfw"` (기본 sfw, 후방호환).
- **FR-3 프리셋 물리 분리**: NSFW 태그 사전·negative 프리셋은 별도 `app/nsfw_presets.json`. SFW 코드/사전과 같은 파일 금지.
- **FR-4 저장소 분리**: 로컬 `/home/ubuntu/nai_out/studio_nsfw/` · 드라이브 `matrix-upload:소설자산이미지/NSFW/<image_id>_<entity>.png`. SFW 경로에 파일 1개도 혼입 금지(생성 시점 분기).
- **FR-5 카탈로그 분리**: UI 카탈로그의 NSFW 항목은 토글 ON일 때만 별도 섹션(🔒 NSFW) 표시. 정적 카탈로그 `web_catalog.html`에는 미포함.
- **FR-6 파라미터 프리셋**: NSFW용 negative(차단 태그 제거판)·페티시 태그 사전(카테고리별)을 `nsfw_presets.json`에서 관리. 코드 하드코딩 금지(단 §4.7 하드차단은 예외).
- **FR-7 감사 로그**: manifest `subject.category`+`provenance.policy_gate` 기록 + 별도 로그 파일 `app/nsfw_generation.log`(타임스탬프·image_id·요청 IP).
- **FR-8 접근 제한**: NSFW API는 IP 화이트리스트(`nsfw_config.json`의 `allowed_ips`)만. 기본 빈 배열=전면 차단.

### 정책 (POL) — 위반 시 구현 무효
- **POL-1**: `review_status` 값은 candidate로만 기록. reviewed 부여는 이사님 직접만.
- **POL-2**: 원문 quote는 근거용 짧게만(저작권 규칙 승계).
- **POL-3**: NAI 이용약관의 성인 생성 허용 범위를 **구현 착수 전 재확인**(약관 개정 가능).
- **POL-4 하드차단**: 미성년(loli/shota/child 등)·실존 인물 묘사 태그는 **서버 코드에 하드코드된 차단 목록**으로 400 거부 — 프리셋 파일 수정으로 우회 불가하게.

## 4. 구현 설계 (권장 안 — FR/POL을 지키는 범위 내에서 수정 가능)

### 4.1 설정 게이트 (`app/nsfw_config.json`)
```json
{"enabled": false, "allowed_ips": ["<사내망 IP>"]}
```
- main.py: 요청마다 재로드(파일 수정 즉시 반영, 재시작 불필요)
- IP 검증: `request.remote_addr` (+프록시 있으면 X-Forwarded-For 첫 값)

### 4.2 프리셋 (`app/nsfw_presets.json`) — 신규 파일
```json
{
  "negative_sfw_keep": "lowres, bad anatomy, worst quality, ...",
  "tag_dict": {
    "의상": ["..."], "구도": ["..."], "상황": ["..."]
  },
  "blocked_hard": []
}
```
- `negative_sfw_keep`: 현행 `DEFAULT_NEG`에서 성인 차단항(nsfw 등)만 뺀 목록 + 품질 차단은 유지
- `tag_dict` 소스 후보: `catalog/lorebooks/[19금]*.txt` 및 `.extract/modules/` NSFW 사용례 — **차단(하드) 항목은 여기 두지 않는다** (§4.7)

### 4.3 API 변경
- `GET /api/nsfw/status` → `{"enabled": bool, "categories": [...]}` (게이트와 무관하게 항상 응답)
- `POST /api/nsfw/toggle` → enabled 전환. **allowed_ips 외 요청은 403** (설정 파일 갱신)
- `POST /api/generate` 확장: `category` 필드 수신. `nsfw`일 때: 게이트 확인(403) → 하드차단 검증(400) → NSFW 프리셋·저장 경로 분기
- `/img/<fname>`: NSFW 로컬 파일은 `/img/nsfw/<fname>` 별도 라우트로만 서빙, 게이트 OFF면 403

### 4.4 생성 레코드 (스키마 v1.1 확장)
```json
"subject":   { ..., "category": "nsfw" },
"storage":   { "local": "/home/ubuntu/nai_out/studio_nsfw/...", "gdrive": "matrix-upload:소설자산이미지/NSFW/..." },
"provenance": { ..., "policy_gate": "nsfw_approved_v1" }
```
- `generate_record()`에서 category별 분기 — 함수 서명은 `d["category"]` 유무로 판별(기본 "sfw")

### 4.5 UI (`index.html`)
- 헤더에 🔒 NSFW 토글 (기본 off · 상태는 `/api/nsfw/status` 폴링)
- ON일 때만: ①카탈로그 하단 "🔒 NSFW" 섹션(category=nsfw 레코드) ②새 조합 시트에 카테고리 선택(sfw/nsfw 라디오) ③`TAGS`에 NSFW 태그 카테고리 추가(프리셋 API로부터)
- OFF면 NSFW 레코드는 렌더 자체를 안 함(서버가 status로 알려줌)

### 4.6 SFW 무결성 확인
- `/api/manifest`는 그대로 전체 반환하되, UI 필터링은 위대로. **정적 카탈로그 생성기 build_web.py는 category=nsfw 행을 skip**하도록 한 줄 추가.

### 4.7 하드차단 (main.py 코드 내 — 프리셋 아님)
```python
BLOCKED = ["loli", "shota", "child", "minor", "underage", "school uniform child"]  # 예시 — 구현 시 확정
```
- core/scene/태그 전체를 대상으로 substring 검사(대소문자 무시) → hit 시 400 `{"error": "차단 태그"}`

## 5. 검증 기준 (완료 선언 조건 — RELAY-37 기능실행검수)

**전부 통과해야 "완료" 보고 가능. 정적 확인만으로 완료 금지.**

1. `bash check.sh` 4/4 통과 (기존 기능 무손상)
2. **게이트 기본 차단**: enabled=false 상태에서 `POST /api/generate`(category=nsfw) → 403 확인 (curl)
3. **하드차단**: 차단 태그 포함 요청 → 400 확인 (curl)
4. **토글 ON 실생성 1건**: allowed_ips 등록 후 실제 NAI 생성 → 로컬 `studio_nsfw/` 파일 + manifest category 필드 + 드라이브 NSFW/ 업로드 확인
5. **SFW 무결성**: 생성 후 SFW 카탈로그 UI·`web_catalog.html`에 NSFW 이미지 없음 확인
6. `render_test.js`에 ①토글 off 기본 상태 ②NSFW 섹션 미표시 케이스 추가 (실생성 없이 검증 가능한 범위)
7. 증거 이미지 이사님 Telegram 전송: `cokacdir --sendfile <경로> --chat <이사님 chat> --key <봇 키>`
8. notes `relay/tickets/RELAY-40/5-impl.md` 구현기록 + git push + Jira 댓글

## 6. 열린 질문 (구현 착수 전 이사님 결정 필요)

- **Q-1 태그 사전 소스**: catalog [19금] 로어북 큐레이션 vs 아카라이브 태그 위키 참조 (정확성·저작권)
- **Q-2 드라이브 구조**: `NSFW/<날짜배치>/` 추가 depth 여부
- **Q-3 1차 대상**: RISU 성인 로어북 중 우선 노출 캐릭터
- **Q-4 토글 보안**: IP 화이트리스트만으로 충분한지, PIN/비밀번호 추가할지

## 7. 참고 자산 (서버 내 크롤링본 — WebFetch 금지, 이걸 먼저 볼 것)

- `.extract/modules/🔦라이트보드 NAI 2.9.json` lorebook [1] — NSFW explicit 태그 사용 규칙 실례 ("`nsfw` 태그는 노출 직접 가시 시에만")
- `.extract/pdf/[라이트보드]_이미지_생성_모듈_(NAI_ComfyUI)_-_AI_채팅_채널.pdf.txt` — 모듈 전체 매뉴얼
- `catalog/lorebooks/[19금]*.txt` — 태그 사전 소스 후보 590건
- `notes/projects/agent-ops/relay/tickets/RELAY-39/` — 본 티켓 산출물 일체(구현기록·아티스트 프리셋 카탈로그 포함)
