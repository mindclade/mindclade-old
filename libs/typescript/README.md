# libs/typescript

Horizontal TypeScript foundations: configuration, the design system,
observability, testing helpers, and browser-safe web utilities.

- Owner: product-web
- Scoped packages under `@mindclade/*`; consumers use declared exports, never
  relative paths escaping package roots.
- Browser-safe packages stay separate from Node-only packages.
- Apps consume the SDK and design system; they never import generated protocol
  clients directly throughout feature components.
