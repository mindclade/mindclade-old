# tests

Cross-cutting suites that span packages: conformance (cross-language
contracts), integration, end-to-end, distributed, failure injection,
performance, and security. Package-local unit tests live with their
packages; only multi-component evidence lives here.

- Owner: shared; each suite directory declares its owning team.
- Suites carry standard Bazel tags (integration, distributed, gpu*,
  exclusive, performance, ...) so CI selects them by affected targets and
  trust context. Quarantined flaky tests run on a visible lane with an owner
  and expiry — never silently removed.
- Evidence requirements per layer are defined in BLUEPRINT.md section 22.
