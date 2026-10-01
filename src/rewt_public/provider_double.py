"""Offline demonstration provider. It is not Elian and performs no reasoning."""

from __future__ import annotations

from rewt_public.models import PublicConsequenceEnvelope, PublicTreeTurnRequest


class DemonstrationProvider:
    """Return a fixed result without interpreting input or touching storage."""

    provider_id = "demonstration-provider-double"

    def __init__(self, *, malformed: bool = False) -> None:
        self.malformed = malformed
        self.requests: list[PublicTreeTurnRequest] = []

    def tree_turn(self, request: PublicTreeTurnRequest) -> PublicConsequenceEnvelope:
        self.requests.append(request)
        if self.malformed:
            return PublicConsequenceEnvelope("wrong-request", request.tree_id, request.owner_id, "result", "fixed demonstration result")
        return PublicConsequenceEnvelope(request.request_id, request.tree_id, request.owner_id, "result", "fixed demonstration result")
