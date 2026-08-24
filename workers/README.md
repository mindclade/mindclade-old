# workers

Specialized execution processes consuming durable jobs from the control
plane. Workers are composition roots; no foundational or domain package may
import from them.

- Owner: platform-workers (with per-worker domain owners)
- Queue and lease contract: idempotency keys, visibility/lease timeout,
  heartbeat, bounded retry, poison-job handling, cancellation, attempt
  identity, progress checkpoints, immutable input references, result
  manifest, and failure classification. Every worker tolerates duplicate
  delivery; exactly-once is never assumed.
- Workers reach control-plane state through APIs or queue contracts, never
  direct database access.
