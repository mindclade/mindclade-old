# ingestion-worker

Rust worker executing data-source ingestion jobs: fetch, verify, parse, and
publish immutable source snapshots through the connector lifecycle in
`data/`.

- Owner: data-platform
- CPU-only; honors source rate limits and terms; replays idempotently.
