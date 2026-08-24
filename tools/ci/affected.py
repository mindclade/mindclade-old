"""Compute Bazel targets affected by a change set."""

from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys
from collections.abc import Callable

UNIVERSE_TRIGGERS = {
    "MODULE.bazel",
    "MODULE.bazel.lock",
    ".bazelrc",
    ".bazelversion",
    ".bazelignore",
}
UNIVERSE_SUFFIXES = (".lock", "go.sum", "pnpm-lock.yaml")
_SKIP_DIR_NAMES = {"node_modules", "target"}


def _is_universe_trigger(path: str) -> bool:
    return (
        path in UNIVERSE_TRIGGERS
        or path.endswith(UNIVERSE_SUFFIXES)
        or path.endswith("BUILD.bazel")
    )


def to_label(changed_file: str, package_dirs: set[str]) -> str | None:
    parts = changed_file.strip("/").split("/")
    directory_parts = parts[:-1]
    for depth in range(len(directory_parts), -1, -1):
        candidate = "/".join(directory_parts[:depth])
        if candidate in package_dirs:
            return "//{}:{}".format(candidate, "/".join(parts[depth:]))
    return None


def _package_dirs(root: pathlib.Path) -> set[str]:
    packages: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name
            for name in dirnames
            if not name.startswith(".")
            and name not in _SKIP_DIR_NAMES
            and not (pathlib.Path(dirpath) / name).is_symlink()
        ]
        if "BUILD.bazel" in filenames:
            rel = pathlib.Path(dirpath).relative_to(root).as_posix()
            packages.add("" if rel == "." else rel)
    return packages


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[2]


def affected_targets(changed_files: list[str], query: Callable[[str], list[str]]) -> list[str]:
    if any(_is_universe_trigger(path) for path in changed_files):
        return ["//..."]
    package_dirs = _package_dirs(_repo_root())
    source_labels = set()
    for path in changed_files:
        label = to_label(path, package_dirs)
        if label is not None:
            source_labels.add(label)
    if not source_labels:
        return []
    labels = query("set({})".format(" ".join(f'"{label}"' for label in sorted(source_labels))))
    if not labels:
        return []
    expr = "rdeps(//..., set({}))".format(" ".join(labels))
    return sorted(set(query(expr)))


def _bazel_query(expr: str) -> list[str]:
    proc = subprocess.run(
        ["bazelisk", "query", expr, "--keep_going", "--output=label"],
        capture_output=True,
        text=True,
    )
    return [line for line in proc.stdout.splitlines() if line.startswith("//")]


def _changed_files(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"], capture_output=True, text=True, check=True
    ).stdout
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
    ).stdout
    files = set(out.splitlines())
    files.update(line[3:] for line in dirty.splitlines() if line)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD~1")
    args = parser.parse_args()
    for label in affected_targets(_changed_files(args.base), query=_bazel_query):
        print(label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
