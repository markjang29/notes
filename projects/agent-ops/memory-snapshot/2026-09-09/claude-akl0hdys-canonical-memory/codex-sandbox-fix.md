---
name: codex-sandbox-fix
description: Codex plugin sandbox disabled (danger-full-access) because bwrap loopback fails on this host; patch location to re-apply
metadata: 
  node_type: memory
  type: reference
  originSessionId: 471bf542-7577-448f-8d74-7dd7548495f8
---

이 서버에서 Codex 플러그인(`/codex:rescue`, task/review)이 bwrap loopback 실패(`Failed RTM_NEWADDR: Operation not permitted`)로 로컬 파일을 못 읽었음. config.toml만으로는 우회 안 됨 — companion이 스레드마다 sandbox를 명시 전달하기 때문.

**적용한 패치(핵심)**: `~/.claude/plugins/cache/openai-codex/codex/<버전>/scripts/lib/codex.mjs` 의 `runAppServerTurn()`에서 `sandbox: options.sandbox` (2곳) → `sandbox: "danger-full-access"`. `~/.codex/config.toml` 에도 `sandbox_mode="danger-full-access"`, `approval_policy="never"` 추가. bubblewrap도 apt로 설치됨.

**Why:** 호스트에 CAP_NET_ADMIN 제한이 있어 bwrap 네트워크 네임스페이스가 안 됨.
**How to apply:** 플러그인 업데이트 후 패치가 날아가면 동일 위치 재적용. 상세는 ~/notes 의 "Codex 샌드박스 설정" 노트 참고.
연관: [[workspace-layout]]
