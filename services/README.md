# services

Composition roots for the control plane and network edges. The default
architecture is a Go modular control-plane monolith plus specialized
workers — not premature microservices.

- Owner: platform-control-plane
- `control_plane/`: modules for tenants/projects/users, datasets, artifacts,
  experiments/runs, jobs, models/checkpoints, policy, and audit. Modules own
  their domain types, commands/queries, repository interfaces, protocol
  adapters, authorization checks, and tests; they share platform
  infrastructure but never each other's database tables.
- Split a module into a service only for distinct scaling, trust boundary,
  availability, release ownership, data sovereignty, operational load, or
  durable team ownership.
- `webhook_dispatcher/` and `event_dispatcher/` are reserved seams: webhooks
  when external webhooks are real; event dispatch only after transactional
  outbox volume justifies the split.
- Durable jobs use the explicit state machine (PENDING -> VALIDATING ->
  QUEUED -> ADMITTED -> RUNNING -> SUCCEEDED, with CANCELLING/CANCELLED,
  RETRY_WAIT, FAILED); transitions are transactional and emit audit records
  and outbox events.
- No foundational or domain package may import from services.
