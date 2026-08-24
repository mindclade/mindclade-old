# apps

TypeScript product surfaces. Applications consume the `@mindclade/sdk` and
design-system packages only: no service database queries, no Protobuf
imports throughout feature components, no Kubernetes/job implementation
details, no business authorization in the browser, no duplicated state
machines.

- Owner: product-web
- `console/`: model runs, datasets, training, evaluation, artifacts,
  deployments, usage, developer workflows.
- `admin/`: tenancy, policy, audit, quotas, support, incident operations —
  kept separate only while its trust boundary and deployment policy are
  materially different.
- `docs/`: SDK documentation, API reference, tutorials, model/dataset cards,
  platform concepts.
