# NSFW 카테고리 구현 인수인계서 (RELAY-39 → 구현 담당 봇, 티켓번호 RELAY-41)

> 2026-08-23 · 작성: novel_col (RELAY-39 담당) · 승인: 이사님
> **이 문서 하나로 구현이 가능하게 쓴 자립형 명세.** 원본 요구사항: 같은 폴더 `NSFW-요구사항-명세.md`
> ⚠ RELAY-40은 RPG 팀 조사 티켓이 선점(2026-08-23) — NSFW 구현 티켓은 **RELAY-41**.

---

## 0. 이 문서를 받은 봇에게 (반드시 먼저 읽을 것)

1. 당신의 임무: **소설 자산 이미지 스튜디오에 NSFW 생성 카테고리·토글을 구현**한다. SFW 파이프라인은 절대 건드리지 않는다.
2. 절차: ①`git pull` ②티켓 확보 — **Jira가 응답하면** `RELAY-41` 등록, **Jira 불가(404 등)면 RPG 봇 선례(2026-08-23)대로 notes `relay/tickets/RELAY-41/1-req.md`에 `jira: RELAY-41` 헤더를 남기고 로컬 폴더를 정본으로 작업** (Jira 복구 시 역동기화) ③구현 ④검증(§5) ⑤pre-push 게이트 통과 커밋·push ⑥notes에 구현기록 ⑦이사님 Telegram 보고.
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

### 기능 (FR) — 2026-08-23 이사님 수정: 나이인증·접근통제 없음, 토글만
- **FR-1 NSFW 토글**: `app/nsfw_config.json` 기본 `{"enabled": false}`. off면 NSFW API·UI 비활성(403), on이면 전면 사용 가능. **연령 인증·IP 화이트리스트·PIN 등 인증 절차 없음** (이사님 결정 2026-08-23).
- **FR-2 카테고리 필드**: 생성 요청 `category: "sfw"|"nsfw"` (기본 sfw, 후방호환).
- **FR-3 프리셋 물리 분리**: NSFW 태그 사전·negative 프리셋은 별도 `app/nsfw_presets.json`. SFW 코드/사전과 같은 파일 금지.
- **FR-4 저장소 분리**: 로컬 `/home/ubuntu/nai_out/studio_nsfw/` · 드라이브 `matrix-upload:소설자산이미지/NSFW/<image_id>_<entity>.png`. SFW 경로에 파일 1개도 혼입 금지(생성 시점 분기).
- **FR-5 카탈로그 분리**: UI 카탈로그의 NSFW 항목은 토글 ON일 때만 별도 섹션(🔒 NSFW) 표시. 정적 카탈로그 `web_catalog.html`에는 미포함.
- **FR-6 파라미터 프리셋**: NSFW용 negative(차단 태그 제거판)·이미지 카테고리 태그 사전(§4.2)을 `nsfw_presets.json`에서 관리. 코드 하드코딩 금지(단 §4.7 하드차단은 예외).
- **FR-7 감사 로그**: manifest `subject.category`+`provenance.policy_gate` 기록 + 별도 로그 파일 `app/nsfw_generation.log`(타임스탬프·image_id).

### 정책 (POL) — 위반 시 구현 무효
- **POL-1**: `review_status` 값은 candidate로만 기록. reviewed 부여는 이사님 직접만.
- **POL-2**: 원문 quote는 근거용 짧게만(저작권 규칙 승계).
- **POL-3**: NAI 이용약관의 성인 생성 허용 범위를 **구현 착수 전 재확인**(약관 개정 가능).
- **POL-4 하드차단**: 미성년(loli/shota/child 등)·실존 인물 묘사 태그는 **서버 코드에 하드코드된 차단 목록**으로 400 거부 — 프리셋 파일 수정으로 우회 불가하게.

## 4. 구현 설계 (권장 안 — FR/POL을 지키는 범위 내에서 수정 가능)

### 4.1 설정 토글 (`app/nsfw_config.json`)
```json
{"enabled": false}
```
- main.py: 요청마다 재로드(파일 수정 즉시 반영, 재시작 불필요). 인증 절차 없음.

### 4.2 이미지 카테고리 태그 사전 (`app/nsfw_presets.json`) — ★ works/catalog 자산 기반 (이사님 2026-08-23 지시)

**NSFW 토글 ON 시 선택 가능한 이미지 카테고리 = 수집 자산에서 발굴한 7종.** 각 카테고리의 태그는 아래 소스에서 큐레이션해 Danbooru 표준 태그(README 3-1 규칙)로 등록한다.

| 카테고리 | 예시 태그 방향 | 자산 소스 (works/catalog) |
|---|---|---|
| 의상·코스튬 | lingerie, maid outfit, bunny suit, nurse uniform, gym uniform | `[19금]` 로어북 코스튬/의상 시나리오 다수 + works character_archetype 146명의 복장 서술 |
| 장소·상황 | bedroom, bathroom, onsen, fitting room, adult shop, love hotel | `[19금]` 성인용품점 방문·목욕·온천 시나리오 등 314건 파일명·본문 |
| 포즈·구도 | presenting, all fours, squatting, arched back, legs up | 로어북 시나리오 묘사 + 라이트보드 [Angle] 체계 |
| 액세서리·도구 | collar, leash, rope, blindfold, vibrator | `[19금] (이상성욕 포함) 쿰질용 이상한 아이템 모음집` 등 아이템 로어북 |
| 신체·체형 | body size/build 태그 (Danbooru 표준) | works character_archetype identity_kernel |
| 분위기·조명 | candlelight, dim lighting, moonlit room | 로어북 분위기 서술 + SFW TAGS '시간·조명' 확장 |
| 관계·상호작용 | `source#`/`target#`/`mutual#` NSFW 액션 태그 | 라이트보드 NAI 2.9 액션 태그 문법 (`.extract`) |

```json
{
  "negative_sfw_keep": "lowres, bad anatomy, worst quality, ... (DEFAULT_NEG에서 nsfw 차단만 제거)",
  "tag_dict": { "의상·코스튬": [...], "장소·상황": [...], "포즈·구도": [...],
                "액세서리·도구": [...], "신체·체형": [...], "분위기·조명": [...],
                "관계·상호작용": [...] }
}
```
- 큐레이션 절차: ①`catalog/lorebooks/[19금]*.txt` 314건 파일명 스캔 → 시각 카테고리 분류 ②works components 의상 서술 교차 ③Danbooru 태그로 번역·등록. **차단(하드) 항목은 이 파일에 두지 않는다**(§4.7)
- NSFW 대상 캐릭터 풀: 기존 `/api/characters`(소설 146 + RISU 58) 그대로 — 토글 ON 시 같은 풀에서 선택

### 4.3 API 변경
- `GET /api/nsfw/status` → `{"enabled": bool, "categories": [...]}` (토글과 무관하게 항상 응답)
- `POST /api/nsfw/toggle` → enabled 전환 (설정 파일 갱신). 인증 없음.
- `POST /api/generate` 확장: `category` 필드 수신. `nsfw`일 때: 게이트 확인(403) → 하드차단 검증(400) → NSFW 프리셋·저장 경로 분기
- `/img/<fname>`: NSFW 로컬 파일은 `/img/nsfw/<fname>` 별도 라우트로만 서빙, 토글 OFF면 403

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
2. **토글 기본 차단**: enabled=false 상태에서 `POST /api/generate`(category=nsfw) → 403 확인 (curl)
3. **하드차단**: 차단 태그 포함 요청 → 400 확인 (curl)
4. **토글 ON 실생성 1건**: enabled=true 전환 후 실제 NAI 생성 → 로컬 `studio_nsfw/` 파일 + manifest category 필드 + 드라이브 NSFW/ 업로드 확인
5. **SFW 무결성**: 생성 후 SFW 카탈로그 UI·`web_catalog.html`에 NSFW 이미지 없음 확인
6. `render_test.js`에 ①토글 off 기본 상태 ②NSFW 섹션 미표시 케이스 추가 (실생성 없이 검증 가능한 범위)
7. 증거 이미지 이사님 Telegram 전송: `cokacdir --sendfile <경로> --chat <이사님 chat> --key <봇 키>`
8. notes `relay/tickets/RELAY-41/5-impl.md` 구현기록 + git push + Jira 댓글(가능 시)

## 6. 열린 질문 (구현 착수 전 이사님 결정 필요)

- **Q-1 태그 사전 우선순위**: §4.2 7개 카테고리 전부 1차 구현할지, 핵심 3개(의상·장소·포즈)만 먼저할지
- **Q-2 드라이브 구조**: `NSFW/<날짜배치>/` 추가 depth 여부
- ~~나이인증/PIN~~ — 2026-08-23 이사님 결정으로 제외 (인증 없는 토글만)

## 7. 참고 자산 (서버 내 크롤링본 — WebFetch 금지, 이걸 먼저 볼 것)

- `.extract/modules/🔦라이트보드 NAI 2.9.json` lorebook [1] — NSFW explicit 태그 사용 규칙 실례 ("`nsfw` 태그는 노출 직접 가시 시에만")
- `.extract/pdf/[라이트보드]_이미지_생성_모듈_(NAI_ComfyUI)_-_AI_채팅_채널.pdf.txt` — 모듈 전체 매뉴얼
- `catalog/lorebooks/[19금]*.txt` **314건** — 이미지 카테고리 태그 사전 1차 소스 (§4.2)
- `novel_assets/works/*/components.ndjson` — character_archetype 146명 (의상·신체 서술, NSFW 캐릭터 풀 그대로 사용)
- `notes/projects/agent-ops/relay/tickets/RELAY-39/` — 본 티켓 산출물 일체(구현기록·아티스트 프리셋 카탈로그 포함)
