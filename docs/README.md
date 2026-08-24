# docs

Repository documentation: architecture, ADRs, domain guides, standards,
developer onboarding, security, runbooks, operations, model cards, and
dataset cards.

- Owner: architecture-council (ADRs); each domain owns its guides.
- ADRs (`adr/`) are required for decisions changing top-level boundaries,
  protocol compatibility, storage formats, training/checkpoint contracts,
  kernel dispatch policy, security trust boundaries, release semantics, or
  infrastructure repository ownership. ADRs record context, decision,
  alternatives, consequences, and migration — not implementation docs.
- Component maturity ladder: experimental -> incubating -> supported ->
  production -> deprecated -> retired; maturity controls required tests,
  compatibility promises, owner expectations, and release eligibility.
- Production components must have runbooks here before promotion.
