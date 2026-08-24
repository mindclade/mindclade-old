# protocols

Stable cross-process and cross-language contracts. Protobuf is the source of
truth for internal RPC, durable job requests and status, service events, audit
payloads, and generated client models. JSON Schema owns artifact, dataset,
feature, checkpoint, and model manifests plus human-authored configuration
validated outside a Protobuf runtime. OpenAPI is generated only for public
HTTP edges and is never independently authoritative.

- Owner: platform-contracts
- Layout: `proto/` (RPC, `mindclade.<domain>.v1`), `events/` (immutable event
  envelopes), `schemas/` (JSON Schema manifests), `openapi/` (generated),
  `generated/` (per-language codegen output), `compatibility/` (protected
  baselines and breaking-change tests).
- Rules: never reuse a Protobuf field number; reserve removed names and
  numbers; events are immutable after publication; manifests carry
  `schemaVersion`; CI compares changes against `compatibility/baselines`.
- May not depend on implementation packages. Generated files are never
  hand-edited.
- Build/test: `just proto`, `bazel test //protocols/...` (pending wiring).
