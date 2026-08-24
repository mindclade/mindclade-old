# deploy

Service-owned deployment packages: CRDs and generated CRD documentation,
per-component Helm/Kustomize bases, local and integration-test deployment
definitions, policy tests, and canonical non-secret defaults.

- Owner: platform-delivery
- This directory must NOT contain production cluster names or credentials,
  environment-specific secret references, mutable image tags for production,
  environment promotion state, or Terraform root modules for live
  environments. The `gitops` repository consumes versioned packages and
  immutable image digests produced here and owns actual environment mapping
  and promotion (Argo CD / ApplicationSets, with Kueue/JobSet for GPU
  scheduling).
- Application code must not parse live environment overlays from here.
