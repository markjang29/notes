# Shared Git access

Director decision: repository ownership is shared across registered agents.

- `windows-codex` is not the exclusive controller, reviewer, merger, or closer.
- Every registered agent may read, edit, commit, and push to `notes`, `scenario`, `rpg_game`,
  `autotrader`, and `approval-board` when the director or an accountable project owner assigns work.
- Cross-repository work does not require Windows Codex to relay or approve it.
- A worker may verify and close its own bounded task when its done criteria and repository rules pass.
- Preserve ordinary Git safety: no secrets in Git, no force-push to shared branches, no destructive
  history rewrite, and no overwriting unrelated dirty worktrees.
- Explicit director holds and stop orders still take precedence. This policy does not resume trader
  work or any stopped scheduler.

The actor registry is the machine-readable authority for these capabilities.
