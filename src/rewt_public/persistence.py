"""Atomic persistence for reduced public snapshot envelopes."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from rewt_public.models import PublicFruit, PublicTreeSnapshot


class PublicPersistenceError(ValueError):
    pass


def _fruit_from_mapping(data: object) -> PublicFruit:
    required = {"id", "tree_id", "owner_id", "content", "is_current", "provenance_turn_id"}
    if not isinstance(data, dict) or set(data) != required:
        raise PublicPersistenceError("invalid_public_fruit")
    if not all(isinstance(data[key], str) and data[key] for key in (
        "id", "tree_id", "owner_id", "content", "provenance_turn_id"
    )) or not isinstance(data["is_current"], bool):
        raise PublicPersistenceError("invalid_public_fruit")
    return PublicFruit(**data)


def encode_snapshot(snapshot: PublicTreeSnapshot) -> str:
    return json.dumps(asdict(snapshot), sort_keys=True, separators=(",", ":"))


def decode_snapshot(payload: str) -> PublicTreeSnapshot:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as error:
        raise PublicPersistenceError("invalid_public_snapshot") from error
    required = {"schema_version", "tree_id", "owner_id", "current_fruit", "fruit_history"}
    if not isinstance(data, dict) or set(data) != required:
        raise PublicPersistenceError("invalid_public_snapshot")
    if not isinstance(data["schema_version"], int) or data["schema_version"] != 1:
        raise PublicPersistenceError("unsupported_public_snapshot")
    if not all(isinstance(data[key], str) and data[key] for key in ("tree_id", "owner_id")):
        raise PublicPersistenceError("invalid_public_snapshot")
    current = None if data["current_fruit"] is None else _fruit_from_mapping(data["current_fruit"])
    if not isinstance(data["fruit_history"], list):
        raise PublicPersistenceError("invalid_public_snapshot")
    history = tuple(_fruit_from_mapping(item) for item in data["fruit_history"])
    if current is not None and (current.tree_id != data["tree_id"] or current.owner_id != data["owner_id"]):
        raise PublicPersistenceError("public_snapshot_ownership_mismatch")
    if any(item.tree_id != data["tree_id"] or item.owner_id != data["owner_id"] for item in history):
        raise PublicPersistenceError("public_snapshot_ownership_mismatch")
    return PublicTreeSnapshot(data["schema_version"], data["tree_id"], data["owner_id"], current, history)


class AtomicPublicSnapshotStore:
    """Atomic write/replace store for one opaque public snapshot."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def save(self, snapshot: PublicTreeSnapshot) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_name(f".{self.path.name}.tmp")
        try:
            with temporary.open("w", encoding="utf-8", newline="") as target:
                target.write(encode_snapshot(snapshot))
                target.flush()
                os.fsync(target.fileno())
            os.replace(temporary, self.path)
        except OSError as error:
            temporary.unlink(missing_ok=True)
            raise PublicPersistenceError("public_snapshot_commit_failed") from error

    def load(self) -> PublicTreeSnapshot | None:
        if not self.path.exists():
            return None
        try:
            return decode_snapshot(self.path.read_text(encoding="utf-8"))
        except OSError as error:
            raise PublicPersistenceError("public_snapshot_read_failed") from error
