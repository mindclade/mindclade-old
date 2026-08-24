from __future__ import annotations

import hashlib
import json
import pathlib

import jsonschema
import yaml


class ConfigError(ValueError):
    pass


def _strict(schema: dict) -> dict:
    if schema.get("type") == "object" and "additionalProperties" not in schema:
        schema = {**schema, "additionalProperties": False}
    for key in ("properties", "$defs"):
        if key in schema:
            schema = {**schema, key: {k: _strict(v) for k, v in schema[key].items()}}
    if isinstance(schema.get("items"), dict):
        schema = {**schema, "items": _strict(schema["items"])}
    return schema


def load_config(path: pathlib.Path, schema: dict) -> dict:
    text = path.read_text()
    try:
        doc = yaml.safe_load(text) if path.suffix in {".yaml", ".yml"} else json.loads(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ConfigError(str(exc)) from exc
    errors = list(jsonschema.Draft202012Validator(_strict(schema)).iter_errors(doc))
    if errors:
        raise ConfigError("; ".join(e.message for e in errors))
    return doc


def config_digest(doc: dict) -> str:
    canonical = json.dumps(doc, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
