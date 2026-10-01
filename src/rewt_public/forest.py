"""Exact owner-bound public Tree storage; this module performs no selection."""

from __future__ import annotations

from pathlib import Path

from rewt_public.models import PublicTreeSnapshot
from rewt_public.persistence import AtomicPublicSnapshotStore, PublicPersistenceError


class PublicForestError(ValueError):
    pass


class PublicForest:
    def __init__(self, data_dir: str | Path) -> None:
        self._directory = Path(data_dir) / "forest"
        self._directory.mkdir(parents=True, exist_ok=True)

    def _store(self, tree_id: str) -> AtomicPublicSnapshotStore:
        if not tree_id or Path(tree_id).name != tree_id:
            raise PublicForestError("invalid_tree_identity")
        return AtomicPublicSnapshotStore(self._directory / tree_id / "snapshot.json")

    def save(self, snapshot: PublicTreeSnapshot) -> None:
        self._store(snapshot.tree_id).save(snapshot)

    def load(self, tree_id: str, owner_id: str) -> PublicTreeSnapshot | None:
        try:
            snapshot = self._store(tree_id).load()
        except PublicPersistenceError as error:
            raise PublicForestError("public_tree_restore_failed") from error
        if snapshot is None:
            return None
        if snapshot.tree_id != tree_id:
            raise PublicForestError("tree_identity_mismatch")
        if snapshot.owner_id != owner_id:
            raise PublicForestError("owner_identity_mismatch")
        return snapshot
