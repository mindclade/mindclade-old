from __future__ import annotations

import ast
import pathlib
import unittest

FORBIDDEN_ROOTS = frozenset(
    {
        "torch",
        "torchvision",
        "torchaudio",
        "triton",
        "flash_attn",
        "transformer_engine",
        "cuda",
        "cupy",
        "nvidia",
    }
)

LIBS_PYTHON = pathlib.Path(__file__).resolve().parent


def _imported_modules(path: pathlib.Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.module


class DependencyPolicyTest(unittest.TestCase):
    def test_libs_python_is_torch_free(self) -> None:
        violations = []
        for path in sorted(LIBS_PYTHON.rglob("*.py")):
            for module in _imported_modules(path):
                if module.split(".")[0] in FORBIDDEN_ROOTS:
                    violations.append(f"{path.relative_to(LIBS_PYTHON)}: {module}")
        self.assertEqual(
            violations,
            [],
            "libs/python must stay free of torch, GPU, and model dependencies",
        )


if __name__ == "__main__":
    unittest.main()
