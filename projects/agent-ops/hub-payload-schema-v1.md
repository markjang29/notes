# 봇간 통신 규격 payload 스키마 v1 (2026-09-11)

- 발행: 이사님 지시 — "01/02 봇이 만든 걸 03 봇(다른 사이트)에 전달, 테스터 봇 품질게이트, 코드리뷰, 파일교환" 전부 규격화
- 원장: 이 문서. 구현: meeting-room/hub.py(파이썬 failover) + hub-spring(스프링 8026, 주) — REST는 1:1 동일
- 정합: notes/projects/agent-ops/gwanje-hub-rest-queue-v1.md (v0 큐) 본 확장

## 주소계 (failover)
- 공인: `http://43.201.34.144/api/hub/*` — 엣지가 8026(스프링, 주) → 8023(파이썬, backup) 자동전환
- 홈 내부: `http://100.109.91.0:8026`(스프링)·`:8023`(파이썬)
- **봇 클라이언트 주소 무변경** — 43.x를 계속 쓰면 됨. 봇간 본통신은 tailscale 경유(엣지가 중계하지만
  duradev↔엣지·nucboxg3는 tailscale direct 연결로 NAT 오버헤드만 있고 초당수백KB 체감 대응), 
  같은 duradev 안 봇(awslnx 9기)은 127.0.0.1로 직결 — tailscale 미경유.

## 봇 구분 (roster.json site 기준 — 2026-09-11 실측)
- awslnx 9 = duradev 내부 봇(매니저·RPG·시나리오·감사·trader·자산·아케이드·소설·dev1)
- 원격: firewin 3(N100) · gmwin 3 · gmlnx 1 · asus 1 — 각자 폴링, wake 불필요

## 전송 규격 (POST /api/hub/send)
```json
{"from":"heav_lnx_bot","to":"heav_lnx_rpg_bot","type":"task",
 "payload":{...}, "key":"rpt-20260911-001","priority":5,"ttl":86400,"wake":true}
```
- type 7종: notice(전체공지, @all만, payload.text 필수) · task(지시, 수신봇 wake) ·
  ack(접수) · progress(진행) · blocked(장애, reason 필수) · submitted(제출물, artifact 필수) ·
  review(리뷰요청, @all 가능 — 전체 리뷰자 도달)
- 상태머신: queued→delivered→acked→done | fail(3회→dead) | 10분 무응답→재큐 | notice/review→expired
- 인증: 봇별 토큰(hub-tokens.json) → 없으면 공유 ROOM_BOT_TOKEN 폴백

## artifact(산출물) 스키마 — submitted·review·전달형 task 공용
```json
{"artifact":{"kind":"build|code|report|asset","path":"~/projects/rpg_game/build/…",
 "repo":"rpg_game","commit":"8a12144","branch":"main",
 "files":[{"path":"...","sha256":"...","bytes":0}],
 "summary":"사람이 읽는 1줄","test_report":"선택: 테스트 결과 경로"}}
```
- **핵심 규칙: 본체는 파일시스템·Git, 메시지는 위치(pointer)만** — 8KB 제한을 넘지 않게.
  원격 사이트(firewin·gmwin)는 같은 tailscale망이므로 100.109.91.0의 경로를 rsync/scp로 직접 회수.
  파일 바이너리 전송은 hub 메시지에 담지 않고, 경로+sha256만 적어 수신자가 검증 후 회수.

## 표준 플로우 4종
1. **개발→다른 사이트 봇 전달**: 01개발봇 →(submitted, artifact 본체=git commit)→ 03봇.
   03봇은 repo+commit으로 회수. 경로만 다른 사이트라도 tailscale直(100.109.91.0)이니 rsync.
2. **개발→테스터**: 개발봇 →(task+artifact)→ 아케이드(heav_lnx_arcade_bot, 플레이어블 검증)·
   gmwin 테스터. 테스터는 →(submitted: test_report)→ 개발봇과 이사님 동시 보고.
3. **테스터→개발반송**: 테스터 →(blocked, reason=재현절차+로그경로)→ 원개발봇. 재큐되지 않게
   fail 2회차에 반드시 blocked 먼저.
4. **코드리뷰**: 개발봇 →(review, to=@all or 지정)→ 리뷰봇(감사 CODEX 기본) →(submitted: 
   kind=code+지적사항)→ 개발봇. 리뷰는 만료(TTL 기본 86400)로 잠수큐 방지.

## 파일수신 규약
- 발신자: files[].sha256 필수. 수신자: 회수 후 해시 일치 확인, 불일치 시 blocked(reason=hash-mismatch).
- 8KB 초과 본문·바이너리·이미지: 원칙적으로 Git(repo+commit)이 정본. 비-Git 대형 산출은
  `~/projects/<bot>/out/` 컨벤션 + 경로만 메시지에.

## 검증 이력 (2026-09-11, 스프링 편입일)
- 8026(스프링) 전 사이클: send·멱등(deduped)·inbox·ack→done·notice @all→notices-active.jsonl(8023과 공유)·
  history·status — 전부 통과. wake 체인(8026→8023 dispatch→클로드 엔진) 실측 PID 516968 기동 확인.
- failover: 8026 다운 → 43.x가 8023으로 응답 → 복귀 후 8026 응답. 43.x 주소·봇 클라이언트 무변경.
