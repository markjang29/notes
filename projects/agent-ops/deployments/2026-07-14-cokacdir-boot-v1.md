---
title: Cokacdir Agent Mail boot v1 rollout
date: 2026-07-14
status: verified
---

# Cokacdir Agent Mail boot v1 rollout

## Pinned sources

- Notes registry/template: `f939ed48eefa6ab483907d502408f9e392b4fe40`
- Scenario installer/skill: `97a89a922faa79c647ebafb2a36eae3749914d2a`

## Applied scope

- Reviewed AWS actors: 5
- Registered Cokacdir chat scopes: 10
- Per-chat persistent instruction entries: 10
- Unresolved template placeholders: 0

## Safety verification

- The installer dry-run matched all five reviewed actor transports before mutation.
- Cokacdir was stopped before the atomic settings replacement and restarted immediately after it.
- A byte-for-byte local backup was created outside Git and its digest matched the pre-change file.
- Settings mode remained `0600`.
- The session-binding digest was identical before and after the change.
- The Cokacdir user service returned active.
- Telegram identity checks returned 5/5.
- No Notes working-tree reset, clean, checkout, or pull was performed; reviewed objects came from
  `origin/main`.

## Post-restart identity proof

All five actors independently loaded the reviewed registry after restart and returned exact
`BOOT ACK` evidence with `registry=ok identity=ok rules=loaded`. Manager and trader required one
format-only retry because their first responses placed explanatory text before the required two
lines; no identity or registry mismatch occurred.

R3 is complete. R4 transactional mailbox and R5 no-op mail round trips remain pending, so this is
identity/startup-rule unification, not yet full durable work-mail automation.
