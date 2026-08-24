# sdk

Client SDKs layered over public protocols. Each SDK provides: generated
protocol client, transport/authentication, typed public resource models, an
ergonomic high-level client, polling/streaming helpers, artifact
upload/download helpers, an error hierarchy, conformance tests, and
examples/API documentation. Generated protocol code is never the public
surface.

- Owner: developer-experience
- SDKs consume generated protocol clients and public convenience layers
  only; they never import service implementation code.
- `go/` and `rust/` are reserved until external demand exists; public SDKs
  may later move to dedicated public repositories when external distribution
  requires an independent lifecycle.
- `conformance/` runs the cross-language behavior suite; `examples/` holds
  runnable usage samples.
