"""Reduced public facade: identity, validation, persistence, and restore only."""

from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from rewt_public.forest import PublicForest
from rewt_public.models import PublicConsequenceKind, PublicFruit, PublicOwnerId, PublicTreeId, PublicTreeSnapshot, PublicTreeTurnRequest, PublicTreeTurnResult
from rewt_public.ports import PublicTreeTurnPort
from rewt_public.validation import PublicValidationError, validate_envelope


class PublicRewtFacade:
    """Public architectural facade; it intentionally contains no reasoning engine."""

    def __init__(self, forest: PublicForest) -> None:
        self._forest = forest

    @staticmethod
    def create_owner() -> PublicOwnerId:
        return PublicOwnerId(uuid4().hex)

    @staticmethod
    def create_tree(owner: PublicOwnerId) -> PublicTreeSnapshot:
        return PublicTreeSnapshot(1, uuid4().hex, owner.value)

    def save(self, snapshot: PublicTreeSnapshot) -> None:
        self._forest.save(snapshot)

    def restore(self, tree: PublicTreeId, owner: PublicOwnerId) -> PublicTreeSnapshot | None:
        return self._forest.load(tree.value, owner.value)

    def turn(self, snapshot: PublicTreeSnapshot, input_text: str, provider: PublicTreeTurnPort) -> PublicTreeTurnResult:
        request = PublicTreeTurnRequest(uuid4().hex, snapshot.tree_id, snapshot.owner_id, input_text, snapshot.current_fruit)
        try:
            envelope = validate_envelope(request, provider.tree_turn(request))
        except PublicValidationError as error:
            return PublicTreeTurnResult(False, snapshot, str(error))
        if envelope.kind == PublicConsequenceKind.NO_CHANGE.value:
            self.save(snapshot)
            return PublicTreeTurnResult(True, snapshot)
        prior = tuple(replace(item, is_current=False) for item in snapshot.fruit_history)
        fruit = PublicFruit(uuid4().hex, snapshot.tree_id, snapshot.owner_id, envelope.result_content or "", True, request.request_id)
        updated = PublicTreeSnapshot(1, snapshot.tree_id, snapshot.owner_id, fruit, (*prior, fruit))
        self.save(updated)
        return PublicTreeTurnResult(True, updated)
