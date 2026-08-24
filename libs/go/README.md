# libs/go

Horizontal Go foundations for the control plane and service infrastructure:
audit, auth, clock, connect/gRPC transport (`connectx`, `grpcx`), controller
runtime helpers, fault taxonomy, identifiers, Kubernetes clients, middleware,
observability, `servicekit` (standardized health/readiness/metrics/diagnostics
endpoints for every deployable), storage, and testing.

- Owner: platform-control-plane
- One root Go module: `go.mindclade.dev/mindclade` — no per-library go.mod.
- May depend on `protocols/`; never on domain packages, services, or workers.
- There is no standalone health service; deployables compose `servicekit`.
