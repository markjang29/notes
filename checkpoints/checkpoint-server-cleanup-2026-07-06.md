# Checkpoint — 서버 폴더 1차 청소

일시: 2026-07-06 KST  
처리: 감사봇(Codex)  
상태: 완료

## 목적

서버 주요 폴더(`/home/ubuntu`)의 대형 파일·캐시·임시 산출물을 점검하고, 세션/프로젝트 복구에 필요한 파일은 보존하면서 명백한 청소 후보만 제거했다.

## 삭제/정리한 것

### 설치 후 남은 원본 압축파일

설치본이 이미 존재하는 것을 확인한 뒤 원본 압축파일만 제거했다.

- `/home/ubuntu/tools/godot-templates.tpz` 약 1.2GB
- `/home/ubuntu/tools/cmdline-tools.zip` 약 146MB
- `/home/ubuntu/tools/godot.zip` 약 72MB

보존:

- `/home/ubuntu/tools/Godot_v4.7-stable_linux.x86_64`
- `/home/ubuntu/tools/godot` symlink
- `/home/ubuntu/tools/android-sdk`
- `/home/ubuntu/.local/share/godot/export_templates/4.7.stable`

### 캐시

- pip 다운로드 캐시 purge: 420개 제거
- autotrader `__pycache__` 제거
- RPG Godot `.godot` 캐시 제거

보존:

- RPG APK export 산출물
- `debug.keystore`
- Godot `.import` 파일
- autotrader `data_cache`

### Claude 구버전 바이너리

현재 symlink가 2.1.197을 가리키는 것을 확인하고 구버전만 제거했다.

- `/home/ubuntu/.local/share/claude/versions/2.1.195`
- `/home/ubuntu/.local/share/claude/versions/2.1.196`

보존:

- `/home/ubuntu/.local/share/claude/versions/2.1.197`

## 전후 결과

최상위 `/home/ubuntu`:

- 청소 전: 약 6.5GB
- 청소 후: 약 4.4GB
- 절감: 약 2.1GB

주요 폴더 최종:

- `/home/ubuntu/tools`: 595MB
- `/home/ubuntu/.cache`: 6.4MB
- `/home/ubuntu/.local/share/claude`: 235MB
- `/home/ubuntu/.cokacdir`: 13MB
- `/home/ubuntu/.claude`: 68MB
- `/home/ubuntu/projects`: 117MB
- `/home/ubuntu/notes`: 3.6MB

## 남긴 것 / 임의 삭제하지 않은 것

- Godot export templates: 실제 export 기능에 필요할 수 있어 보존.
- RPG `demo/export/` APK들: 산출물일 수 있어 보존.
- RPG `debug.keystore`: 서명/빌드에 필요할 수 있어 보존.
- autotrader `data_cache`: 작지만 재현/백테스트 속도에 영향 가능해 보존.
- `.reviews/session-reaper.log`: 자동 로그이며 Git 정책 미정이라 기존처럼 보류.

## Git 상태

프로젝트 repo:

- `autotrader`: clean
- `rpg_game`: clean
- `scenario`: clean

notes:

- 기존 보류 항목: `.reviews/session-reaper.log`

