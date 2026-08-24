# runtime-gateway

Stateless Go gateway for model execution requests: authentication and
authorization, request validation, tenancy and quotas, durable inference job
creation, streaming/status protocol, routing, and public error mapping.

- Owner: platform-control-plane
- Contains no model execution; that belongs to `inference/` invoked by
  `workers/inference_worker`.
- Large results flow as artifact references.
