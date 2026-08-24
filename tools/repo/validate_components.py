"""Validate every component.yaml against the repository component schema."""

from __future__ import annotations

import json
import os
import pathlib
import sys

import jsonschema
import yaml

SCHEMA_PATH = pathlib.Path(__file__).resolve().parent / "component_schema.json"
PLACEHOLDER_OWNERS = {"TBD", "tbd", ""}


def _in_bazel_output(root: pathlib.Path, path: pathlib.Path) -> bool:
    return any(part.startswith("bazel-") for part in path.parts[len(root.parts) :])


def validate_component(doc: dict) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = jsonschema.Draft202012Validator(schema)
    errors = [
        f"{'/'.join(str(p) for p in e.path)}: {e.message}" for e in validator.iter_errors(doc)
    ]
    owner = doc.get("metadata", {}).get("owner", "")
    maturity = doc.get("spec", {}).get("maturity", "")
    if maturity in {"supported", "production"} and owner in PLACEHOLDER_OWNERS:
        errors.append(f"metadata/owner: {maturity} component requires a real owner")
    return errors


def main() -> int:
    root = pathlib.Path(os.environ.get("BUILD_WORKSPACE_DIRECTORY", pathlib.Path.cwd()))
    failures = 0
    for path in sorted(root.rglob("component.yaml")):
        if _in_bazel_output(root, path):
            continue
        errors = validate_component(yaml.safe_load(path.read_text()))
        if errors:
            failures += 1
            for error in errors:
                print(f"{path.relative_to(root)}: {error}", file=sys.stderr)
        else:
            print(f"ok {path.relative_to(root)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
