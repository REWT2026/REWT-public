"""Provider-neutral public boundary."""

from __future__ import annotations

from typing import Protocol

from rewt_public.models import PublicConsequenceEnvelope, PublicTreeTurnRequest


class PublicTreeTurnPort(Protocol):
    """A provider may propose an envelope; it never owns public state."""

    def tree_turn(self, request: PublicTreeTurnRequest) -> PublicConsequenceEnvelope: ...
