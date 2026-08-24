from __future__ import annotations

import importlib.util
import pathlib

_TOOLS_CI = pathlib.Path(__file__).resolve().parents[2] / "tools" / "ci" / "affected.py"
_spec = importlib.util.spec_from_file_location("mindclade_affected", _TOOLS_CI)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

affected_targets = _module.affected_targets
