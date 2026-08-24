"""Verify the local environment matches repository toolchain pins."""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys


def parse_pins(root: pathlib.Path) -> dict[str, str]:
    package = json.loads((root / "package.json").read_text())
    go_match = re.search(r"^go (\S+)$", (root / "go.mod").read_text(), re.M)
    rust_match = re.search(r'channel = "([^"]+)"', (root / "rust-toolchain.toml").read_text())
    assert go_match and rust_match
    return {
        "bazel": (root / ".bazelversion").read_text().strip(),
        "python": (root / ".python-version").read_text().strip(),
        "pnpm": package["packageManager"].split("@", 1)[1],
        "go": go_match.group(1),
        "rust": rust_match.group(1),
    }


def compare_version(pin: str, actual: str) -> bool:
    return actual == pin or actual.startswith(pin + ".")


def _probe(cmd: list[str], pattern: str) -> str | None:
    if shutil.which(cmd[0]) is None:
        return None
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    match = re.search(pattern, out)
    return match.group(1) if match else None


PROBES = {
    "bazel": (["bazelisk", "version"], r"Build label: (\S+)"),
    "python": (["python3", "--version"], r"Python (\S+)"),
    "pnpm": (["pnpm", "--version"], r"(\S+)"),
    "go": (["go", "version"], r"go version go(\S+)"),
}


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[2]
    pins = parse_pins(root)
    failures = []
    for tool, (cmd, pattern) in PROBES.items():
        actual = _probe(cmd, pattern)
        if actual is None:
            failures.append(f"{tool}: not found ({cmd[0]})")
        elif not compare_version(pins[tool], actual):
            failures.append(f"{tool}: pinned {pins[tool]}, found {actual}")
        else:
            print(f"ok {tool} {actual}")
    for name in ("uv.lock", "Cargo.lock", "go.sum", "pnpm-lock.yaml", "flake.lock"):
        if not (root / name).is_file():
            failures.append(f"lockfile missing: {name}")
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
