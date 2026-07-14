---
title: Cokacdir registry auto-refresh rollout
date: 2026-07-14
status: verified
---

# Cokacdir registry auto-refresh rollout

The first boot rollout read the already-fetched `origin/main` ref. That could leave AWS actors on a
stale registry after a later Notes push. The installer was therefore updated so each new/resumed
session fetches the Notes `main` remote ref without touching its dirty working tree, then reads the
registry Git object.

## Pinned implementation

- Scenario skill/installer: `81c555c188539cb75eb71860a41ac494ae971abf`
- Notes ref used for deployment verification: `4c963697749846df50360f314b4d1f084b6542e6`

## Verification

- Updated persistent instructions: 5 actors / 10 chat scopes
- Instructions containing the fetch command: 10/10
- Repeated installer dry-run after apply: `settings_changed=false`
- Cokacdir service: active
- Telegram identities: 5/5
- Session-binding digest: unchanged from both pre-rollout checks
- Live audit actor smoke: exact `SYNC ACK`, `registry=latest identity=ok rules=loaded`

The fetch changes only the remote-tracking ref. It does not pull, reset, checkout, clean, or merge
the Notes working tree.
