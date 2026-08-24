# Protocol compatibility baselines

`protocols.binpb` is the protected baseline image. CI runs
`buf breaking --against protocols/compatibility/baselines/protocols.binpb`
on every change. The baseline is regenerated (`buf build -o ...`) only in the
same reviewed change that intentionally evolves the contract, never to make a
failing check pass. Breaking changes additionally require the migration plan
demanded by BLUEPRINT.md section 10.2.
