# IDENTITY_PROBE v1

각 actor에게 아래 본문을 독립적으로 전달한다. 다른 actor의 예상 답을 함께 주지 않는다.
회신은 Telegram과 controller 회수 경로에 같은 내용을 남기되 비밀값과 session ID를 넣지 않는다.

```text
[AGENT-MAIL IDENTITY_PROBE v1]

아래 정체 후보를 읽고 본인 정보만 확인해 주세요.
작업·파일 수정·새 기획은 하지 마세요.

candidate_actor_id: <ACTOR_ID>
candidate_display_name: <DISPLAY_NAME>
registry_ref: notes/projects/agent-ops/actors.json
protocol_ref: notes/projects/agent-ops/README.md

다음 형식으로 짧게 회신하세요.

ACK: yes | correction_required | cannot_verify
actor_id:
display_name:
role:
owned_repos:
provider_runtime:
startup_identity_sources:
can_receive_via:
can_execute:
must_not_execute:
active_route_blockers:
registry_corrections:

Telegram token, Cokacdir key, session UUID, cookie, client token, capability URL,
로컬 절대경로는 회신하지 마세요.
```

ACK 판정:

- `yes`: registry와 일치하고 자신의 역할·금지 경계를 설명했다.
- `correction_required`: 수정할 필드와 근거를 명시했다.
- `cannot_verify`: 시작 정체성 자료가 없거나 서로 충돌한다.

모든 ACK를 controller가 검토하기 전 registry의 `ack_status`를 변경하지 않는다.
