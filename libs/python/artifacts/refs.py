from __future__ import annotations

import hashlib
import json
import pathlib
from dataclasses import dataclass

import jsonschema

_SCHEMA_PATH = (
    pathlib.Path(__file__).resolve().parents[3]
    / "protocols"
    / "schemas"
    / "artifact_manifest"
    / "artifact_manifest.schema.json"
)
_CHUNK = 1024 * 1024


class ManifestError(ValueError):
    pass


@dataclass(frozen=True)
class ArtifactRef:
    namespace: str
    name: str
    media_type: str
    digest_algorithm: str
    digest_hex: str
    size_bytes: int
    storage_locator: str
    classification: str
    lineage_ref: str | None = None

    @property
    def uri(self) -> str:
        return f"mindclade://{self.namespace}/{self.name}@{self.digest_algorithm}:{self.digest_hex}"


def _validator() -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(json.loads(_SCHEMA_PATH.read_text()))


def to_manifest(ref: ArtifactRef) -> dict:
    doc = {
        "schemaVersion": "v1",
        "namespace": ref.namespace,
        "name": ref.name,
        "mediaType": ref.media_type,
        "digest": {"algorithm": ref.digest_algorithm, "hex": ref.digest_hex},
        "sizeBytes": ref.size_bytes,
        "storageLocator": ref.storage_locator,
        "policy": {"classification": ref.classification},
    }
    if ref.lineage_ref is not None:
        doc["lineageRef"] = ref.lineage_ref
    _check(doc)
    return doc


def from_manifest(doc: dict) -> ArtifactRef:
    _check(doc)
    if isinstance(doc["sizeBytes"], bool) or not isinstance(doc["sizeBytes"], int):
        raise ManifestError("sizeBytes must be an integer")
    return ArtifactRef(
        namespace=doc["namespace"],
        name=doc["name"],
        media_type=doc["mediaType"],
        digest_algorithm=doc["digest"]["algorithm"],
        digest_hex=doc["digest"]["hex"],
        size_bytes=doc["sizeBytes"],
        storage_locator=doc["storageLocator"],
        classification=doc["policy"]["classification"],
        lineage_ref=doc.get("lineageRef"),
    )


def _check(doc: dict) -> None:
    errors = list(_validator().iter_errors(doc))
    if errors:
        raise ManifestError("; ".join(e.message for e in errors))


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()
