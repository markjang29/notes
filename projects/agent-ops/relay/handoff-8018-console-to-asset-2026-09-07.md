# 인수인계서 — 8018 소설 수집 콘솔·플릿 관리 (novel_col → 자산 측)

> 2026-09-07 · novel_col 작성 · 이사님 지시 "두 페이지 자산 쪽 인수인계 + 홈서버 서비스 확인"
> 운영 주체 변경 가능 — 본 문서가 유일한 인계 정본. 질문은 novel_col 텔레그램으로.

## 1. 인계 대상 (2페이지 — matrix-home repo, 포트 8018)

| 페이지 | URL | 기능 |
|---|---|---|
| 📚 소설 수집 토큰 계획 | http://13.125.131.126:8018/novel-plan | 예산 스위치(토큰량·시간·로봇 수·자동 OFF)·수집 큐 887편 편집(장르·우선순위·상태)·시뮬레이터·정합성 보고·이벤트/스케줄 표 |
| 🔑 봇 플릿·API 키 관리 | http://13.125.131.126:8018/fleet | 공급선 전환(LMM Gateway↔Z.ai 직접)·전역 모델 매핑(haiku/sonnet/opus)·토큰 교체(자동 백업)·봇별 모델 변경·셀프 점검 지시/보고/점검일 |

- 홈(8018/) 카드 2개 + 🧭사이트맵 "내부 페이지" 2줄에서 프론트 연결 확인 완료(외부 200).
- API: GET·POST /api/novel-ops, /api/novel-queue, /api/bot-fleet (브라우저 UI와 봇 공용).

## 2. 서버 상태 (서비스화 완료)

- **systemd**: `matrix-home.service` (enabled·RELAY_TICKET=RELAY-57 env 주입, port-registry 요건 충족) — 재부팅 자동 기동. 기존 nohup 프로세스는 제거됨.
- 운영 명령: `sudo systemctl restart matrix-home` / 로그 `journalctl -u matrix-home -n 50`
- 코드: `/home/ubuntu/projects/matrix-home/main.py` (단일 파일 Flask) · repo는 GitHub `matrix-home` (최신 커밋 58e8c39 계열).

## 3. 데이터 파일 (repo 안, 손대기 전 용도 숙지)

- `novel_queue.json` — 수집 큐 887편 (git 추적·이사님 수정 보존됨)
- `novel_ops.json` — 스위치 상태·예산·지시/이벤트 이력 (untracked)
- `fleet_checks.json` — 봇 점검일·점검지시 대기열 (untracked)
- `fleet_providers.json` — **git 제외(.gitignore)**: 게이트웨이·Z.ai API 키 원본 보관. 절대 커밋 금지. 분실 시 이사님 재입력 필요.
- `~/.cokacdir/cokacdir_ops_key` (chmod 600) — cokacdir 스케줄 조회용 키. **git 절대 금지.**

## 4. 운용 규칙 (이사님 확정 — 변경 불가, 준수 필수)

1. **폴링 금지**: 30분 주기 cron 스케줄로 이 API를 주기 조회하는 방식 금지(토큰 낭비·8/31 공회전 사태). 수집 실행은 이사님이 말 걸거나 스위치 ON 후 "사이트 지시 반영해"라고 할 때만.
2. **이사님께 주는 URL은 항상 13.125.131.126** — 127.0.0.1·localhost 전달 금지.
3. API 키·토큰 파일 git 반입 금지 / review_status candidate 고정 / 원본 전문 반입 금지(RELAY-51 보안 제약 그대로).
4. 점검 프로토콜: `notes projects/agent-ops/relay/fleet-self-check-protocol.md` (봇은 지시 배지 받으면 4단계 수행 후 check_report POST).

## 5. 검증 이력 (인수 시 기준)

- 2026-09-07 systemd 전환 후 외부 3페이지·ops API 전부 200 확인.
- 스위치 자동 OFF 로직 실측 검증 완료(예산 1,000p → 6작품 차감 → 잔여 220p ≤ floor 300p → 자동 OFF).
- 큐 편집(장르·우선순위) 실측 검증 완료 — 재성원령기 pri 9 반영.
