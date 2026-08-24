# tools

Repository tooling: Bazel rules/macros/aspects/transitions, CI programs,
code generation, developer utilities, repo policy checks, release
automation, qualification drivers, migration helpers, generators, and
license tooling.

- Owner: developer-experience
- Complex logic lives here as tested programs; `justfile` and CI configs
  only delegate. Build and developer-environment tools carry no product or
  domain logic.
