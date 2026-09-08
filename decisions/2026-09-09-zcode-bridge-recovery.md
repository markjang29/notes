# zcode 브리지 복구 및 토큰 충돌 (2026-09-09)

## 배경
- 이사님 신설 그룹방(`-5438797206`)에서 "다들 인사해" → cokacdir 9봇 중 rpg·novel_col·매니저만 응답.
- zcode 계열 전체(heav_lnx_zcode·firebat_zcode·gmwin_zcode) 텔레그램 무응답.

## 실측·조치 (매니저, KST 08:04~08:09)
1. `telegram-zcode-bridge.service`(AWS, `@heav_lnx_zcode_bot`) — **09-07 11:32 수동 stop된 상태로 방치**(기록 없음). start로 복구.
2. `bridge.env` `TG_ALLOWED_CHATS`에 `-5438797206` 추가(백업: `bridge.env.bak-20260909`) 후 restart → 시작 로그에 신규방 포함 확인.
3. 발신 경로 정상: 해당 방에 sendMessage 성공(msg_id 880).

## 미해결 — 수신 409 Conflict
- 재시작 30초 경과 후에도 `폴링 오류: HTTP Error 409` 지속 → **동일 봇 토큰을 외부 폴러가 병행 수신 중**.
- 로컬은 단일 프로세스·webhook 없음·crontab 무관(`request_router_poll.py`는 approval-board 전용) → 충돌원은 N100/gmwin/노트북 등 **외부 거점 폴러로 추정**, AWS에서 식별 불가.
- 영향: AWS 브리지 getUpdates 실패(수신 불능). 외부 인스턴스가 업데이트를 가져가는 중 → 그쪽 allowlist에 신규방 없으면 zcode는 이 방에서 묵답.

## 결정 필요 (이사님)
- 어느 쪽을 정본 폴러로 할지: 외부 인스턴스 유지(→ 허용방에 `-5438797206` 추가 필요) vs AWS 브리지 정본(→ 외부 폴러 중단).
- 판별법: 방에서 `@heav_lnx_zcode_bot 인사` 멘션 → 응답 시 외부 인스턴스 생존+허용방 등록돼 있음.

## 관련
- `org-structure.md` 08-31 브리지 가드·허용목록 이력, `matrix-zcode-cli.service`(8011, dead — 별도 과제).
