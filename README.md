# Mindclade

Domain-first polyglot monorepo for the Mindclade product, platform, data,
model, training, evaluation, inference, and developer tooling source. The full
architecture, dependency laws, and rationale live in [BLUEPRINT.md](BLUEPRINT.md).

## Language lanes

- **Python** — models, training, evaluation, inference, scientific semantics
- **Rust** — biological parsing, data-plane I/O, artifact streaming, bounded Python extensions
- **Go** — control plane, durable jobs, Kubernetes controllers, service infrastructure
- **TypeScript** — console, admin, docs app, web/server SDKs
- **Protobuf / JSON Schema** — cross-process and cross-language contracts
- **TileLang / CUDA / C++** — qualified accelerator kernels only

Bazel is the integration graph; native lockfiles (`uv.lock`, `Cargo.lock`,
`go.mod`/`go.sum`, `pnpm-lock.yaml`, `flake.lock`) remain ecosystem dependency
truth. There is no repository-wide release version.

## Coordinates

- Git remote: `github.com/Mindclade/mindclade`
- Go module: `go.mindclade.dev/mindclade` (vanity import; the
  `go.mindclade.dev` redirect service must be provisioned in
  `infrastructure-live` before external `go get` works)
- Python namespace: `mindclade.*`
- TypeScript scope: `@mindclade/*`
- Protobuf namespace: `mindclade.<domain>.v1`
- Kubernetes API group: `mindclade.dev`

## First checkout

```bash
nix develop
just doctor
just bootstrap
just test-affected
```

## Boundaries

This repository does not own organization governance (`github-config`),
foundational cloud trust (`bootstrap`), live cloud desired state
(`infrastructure-live`), or Kubernetes environment promotion (`gitops`).
Deployment packages here are consumed by `gitops` as immutable digests.
