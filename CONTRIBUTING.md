# Contributing to the Mindclade monorepo

Read `BLUEPRINT.md` first; it is the repository constitution. The short version:
organize by domain, implement in the language that owns the domain, cross
process and language boundaries only through versioned contracts.

## First checkout

```bash
nix develop
just doctor
just bootstrap
just test-affected
```

## Normal change

```bash
just format
just lint
just test-affected
just build-affected
```

## Rules that reviews enforce

- Every maintained package has a `README.md`, `BUILD.bazel`, tests, and (when
  releasable or deployable) a `component.yaml` with a valid owner.
- Dependency laws in `BLUEPRINT.md` section 7 are non-negotiable; exceptions
  require an ADR in `docs/adr/` with an owner and a removal condition.
- `libs/python` stays free of torch, CUDA, and model dependencies.
- Generated code is never hand-edited.
- No datasets, model weights, generated experiment output, or secrets in Git.
- Decisions that change boundaries, contracts, or release semantics need an ADR.

Local commands never publish or deploy by default.
