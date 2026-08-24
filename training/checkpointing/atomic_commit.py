from __future__ import annotations


def commit(manifest, shard_writers) -> str:
    """Completion marker is written only after every shard is durable."""
    raise NotImplementedError
