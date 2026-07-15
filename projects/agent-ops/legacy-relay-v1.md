---
title: Agent Mail legacy approval-board relay
status: reviewed temporary bridge
updated: 2026-07-15
---

# Legacy relay contract

The approval board is a wake/status bridge only. It is not the Agent Mail lifecycle authority,
and `accepted` records router claim rather than actor acknowledgement.

A controller-originated request must contain:

- one accountable actor;
- logical `repo_id`;
- full input commit;
- exact repository-relative specification path;
- attempt and stable idempotency key;
- ACK, blocked, and submitted receipt contracts;
- controller-owned escalation instructions.

Before sending, the controller verifies that the declared repository contains both the commit
object and the exact specification object. A runtime checkout path may be used for verification,
but it never enters Git, Agent Mail, or the relay packet.

The legacy service provides list retrieval and does not guarantee a singular
`GET /api/request/{id}` route. Actors must not guess an endpoint or search another repository.
Missing repository, commit, specification, route, or transport metadata is returned to
`windows-codex`; it is not escalated to `director` unless a genuine director decision is needed.

Until the transactional mailbox is deployed, the actor returns one sanitized receipt through its
registered Cokacdir/Telegram route. Windows Codex recovers and reviews that receipt. The actor
stops at submitted; only the controller verifies and closes the work.
