# Checkpoint — 시나리오봇 정체 확인/라우팅 교정

일시: 2026-07-06 17:44 KST  
책임/처리: 감사봇(Codex)  
상태: 적용 및 검증 완료

## 문제

RPG 팀장은 자기 key/역할을 식별할 수 있었으나, 시나리오 팀장은 `key: c6a54f44dab7dfe7`를 보고도 자기 정체를 확정하지 못했다.

## 확인된 원인

1. `~/.cokacdir/bot_settings.json`에서 시나리오봇만 group/context 설정이 비어 있었다.
2. 시나리오봇 개인 `last_sessions["8315615299"]`가 실제 프로젝트가 아니라 임시 workspace(`/home/ubuntu/.cokacdir/workspace/ndznfeai`)를 가리켰다.
3. `~/.claude/recovery-gate/DISABLE` 파일이 남아 있었다.
4. recovery gate 스크립트가 매니저 workspace에만 적용되고, `/home/ubuntu/projects/scenario` 같은 팀장 프로젝트 cwd에서는 L0 주입 없이 `exit 0` 했다.

## 적용한 조치

### 1. 시나리오봇 설정 교정

파일: `~/.cokacdir/bot_settings.json`

- `c6a54f44dab7dfe7` → `heav_lnx_scenario_bot`
- `as_public_for_group_chat["-5495363819"] = true`
- `context["-5495363819"] = 0`
- `last_sessions["8315615299"] = "/home/ubuntu/projects/scenario"`
- 기존 group last session으로 `"-5495363819": "/home/ubuntu/.cokacdir/workspace/ndznfeai"` 보존

### 2. recovery gate 재활성화

파일 제거:

- `~/.claude/recovery-gate/DISABLE`

### 3. recovery gate 적용 범위 확대

파일: `~/.claude/hooks/cokacdir-recovery-gate.sh`

기존:

- `~/.cokacdir/workspace/*`에만 L0/current-work-state 주입
- 팀장 프로젝트 cwd는 no-op

변경:

- `/home/ubuntu/projects/rpg_game*`
- `/home/ubuntu/projects/autotrader*`
- `/home/ubuntu/projects/scenario*`

위 팀장 프로젝트에도 L0/current-work-state 주입.

## 검증

JSON 파싱 정상:

- `username: heav_lnx_scenario_bot`
- `display_name: heav_lnx_scenario`
- `as_public_for_group_chat: {"-5495363819": true}`
- `context: {"-5495363819": 0}`
- `last_sessions["8315615299"]: /home/ubuntu/projects/scenario`
- `DISABLE exists: False`

recovery gate 샘플:

- cwd `/home/ubuntu/projects/scenario`
- `SessionStart`에서 `L0-agent-boot.md + current-work-state.md` additionalContext 정상 출력
- `.ok` marker 생성 확인

## 시나리오봇 재인증 지시문

```text
L0-agent-boot.md를 먼저 읽고, 현재 key를 ~/.cokacdir/bot_settings.json에 대조해 정체를 인증하라.
key c6a54f44dab7dfe7 = heav_lnx_scenario_bot = 시나리오 팀장이다.
작업 cwd는 /home/ubuntu/projects/scenario 기준으로 삼고, 정체 미확정 상태에서는 결정/발판/commit/push 금지.
```

