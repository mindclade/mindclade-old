from __future__ import annotations

import pathlib
import tempfile
import unittest

from libs.python.config.loader import ConfigError, config_digest, load_config

SCHEMA = {
    "type": "object",
    "required": ["name", "workers"],
    "properties": {
        "name": {"type": "string"},
        "workers": {"type": "integer", "minimum": 1},
    },
}


def _write(text: str, suffix: str) -> pathlib.Path:
    path = pathlib.Path(tempfile.mkdtemp()) / f"config{suffix}"
    path.write_text(text)
    return path


class LoadConfigTest(unittest.TestCase):
    def test_valid_yaml_loads(self) -> None:
        doc = load_config(_write("name: ingest\nworkers: 2\n", ".yaml"), SCHEMA)
        self.assertEqual(doc, {"name": "ingest", "workers": 2})

    def test_unknown_field_fails(self) -> None:
        with self.assertRaises(ConfigError):
            load_config(_write("name: ingest\nworkers: 2\nturbo: true\n", ".yaml"), SCHEMA)

    def test_type_violation_fails(self) -> None:
        with self.assertRaises(ConfigError):
            load_config(_write('{"name": "x", "workers": 0}', ".json"), SCHEMA)

    def test_digest_is_order_independent(self) -> None:
        self.assertEqual(
            config_digest({"a": 1, "b": [1, 2]}),
            config_digest({"b": [1, 2], "a": 1}),
        )
        self.assertEqual(len(config_digest({})), 64)

    def test_malformed_json_raises_config_error(self) -> None:
        with self.assertRaises(ConfigError):
            load_config(_write("{not valid json", ".json"), SCHEMA)

    def test_malformed_yaml_raises_config_error(self) -> None:
        with self.assertRaises(ConfigError):
            load_config(_write("name: [unterminated", ".yaml"), SCHEMA)


if __name__ == "__main__":
    unittest.main()
