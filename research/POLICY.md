# Research policy

## Allowed

- notebooks
- one-off studies
- prototypes
- ablations
- exploratory datasets represented only by references
- paper reproduction

## Not allowed

- production services importing research code
- notebooks as training launchers for official runs
- committed large outputs
- hidden dependencies installed manually
- production model checkpoints without manifests
- secrets or restricted data

## Graduation path

```text
research prototype
-> reproducible experiment
-> named owner and design note
-> domain package implementation
-> unit/parity tests
-> integration with build graph
-> qualification suite
-> production recipe/service adoption
```

Graduated code leaves `research/`; two authoritative implementations are
never maintained.
