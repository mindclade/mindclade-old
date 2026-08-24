# control-plane

Go modular monolith owning durable business truth: tenants, projects, users,
datasets, artifacts, experiments, jobs, models, policies, and audit.

- Owner: platform-control-plane
- Deployable binary under `cmd/control-plane`; module code under `internal/`
  (service-local, unimportable from outside); shared platform infrastructure
  (database, transactional outbox, queue, storage) under
  `internal/platform/`.
- Owns the operational relational schema; migrations are forward-only by
  default, tested from supported historical states, with expand/migrate/
  contract for incompatible changes. Workers never query these tables
  directly.
- Kubernetes status is observed and reconciled into job state here; it is
  never the sole durable record.
- Health/readiness/metrics/diagnostics come from `libs/go/servicekit`.
