# 2026-07-01 — rpg_game: 패링 데모 완성 + 모듈식 개발 방향 확정

> 참여: 이사님(한 준희) + RPG 팀장 에이전트(Linux 서버) · 직전 세션 API 529로 중단 → 본 세션 회수

## 결정

1. **엔진 Godot 4.7 확정** (GDScript, GL Compatibility). 타겟 모바일 Android 우선.
   - 서버 헤드리스 빌드 체인 완비: JDK17 + Android SDK(platform/build-tools 34) + Godot 4.7 export templates.
2. **스토리 전면 재검토**: "길 잇는 자 vs 길 끊는 자" + "잃어버린 길" 세계관 = 이사님 "유치하다" 판정 → 폐기. 2세력 진영 갈등 **메커니즘은 유지**, 서사는 백지에서 재검토 (데모와 병렬, 급하지 않음).
3. **모듈식 프로토타입 개발 채택** (이사님 핵심 지시):
   > 작은 모듈 단위 프로토타입 → 폰 검증 → 모듈 라이브러리 적립 → 본편 조립.
   - 세부 수치 튜닝은 본편 조립 시점으로 미룸. 지금은 "작동·느낌 사는가?"까지만.

## 산출물 (repo `rpg_game`, commit `99ddf9c`)

- `DEVELOPMENT.md` 신규 — 모듈식 개발 원칙·컨벤션·검증 루프·모듈 현황.
- `demo/` Godot 프로젝트, 모듈 구조 정립: `modules/<이름>/` (독립 실행 씬) + `shared/` (FX·사운드 등 공통 헬퍼).
- **첫 모듈 `modules/parry/`** (패링 손맛):
  - 판정: Perfect(±65ms) / Good(±140ms) / Miss, 시간 기반 (투사체가 패링 라인 도달까지 남은 시간).
  - 손맛 3축: 히트스톱(`Engine.time_scale`) + 스크린 셰이크(감쇠 진동) + 파티클/충격파 폭발 + 화면 플래시.
  - 사운드: python 표준 라이브러리로 절차 합성(`tools/gen_sfx.py`) — 비조화 배음 금속 클랭 / triangle 막기 / 저역 노이즈 타격 / 노이즈 sweep.
  - 폰 검증 완료 (이사님 "실행 잘 되는거 같고").

## 빌드 노하우 (헤드리스, 다음 모듈도 동일)

- export template은 `~/.local/share/godot/export_templates/4.7.stable/` **바로 아래**에 (templates/ 서브디렉토리 아님 — Godot 4.7이 거기를 찾음).
- SDK/JDK 경로는 `~/.config/godot/editor_settings-4.7.tres`의 `export/android/{java_sdk_path, android_sdk_path, debug_keystore*}`.
- 레거시 빌드(`gradle_build/use_gradle_build=false`)가 헤드리스에서 가장 간편 (android build template 별도 설치 불필요). 단 `compress_native_libraries=false` + ETC2/ASTC 텍스처 압축 on 필요.
- APK 50MB 초과 시 Telegram 전송 불가 → `python3 -m http.server 80`(공개 IP)로 링크. arm64만 넣으면 ~27MB로 절반.

## 다음

- 모듈 후보: **walk** (걷기=재화, 3겹 캡) / **color-dye** (색 염색) / territory / romance.
- 스토리 새 방향 탐색 (백지 — 데모와 병렬).
- 세부 튜닝(parry 수치 등)은 본편 조립 시점으로 보류.
