"""Reduced public state records for the inspection facade."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class PublicOwnerId:
    value: str


@dataclass(frozen=True)
class PublicTreeId:
    value: str


@dataclass(frozen=True)
class PublicFruit:
    id: str
    tree_id: str
    owner_id: str
    content: str
    is_current: bool
    provenance_turn_id: str


@dataclass(frozen=True)
class PublicTreeSnapshot:
    schema_version: int
    tree_id: str
    owner_id: str
    current_fruit: PublicFruit | None = None
    fruit_history: tuple[PublicFruit, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PublicTreeTurnRequest:
    request_id: str
    tree_id: str
    owner_id: str
    input_text: str
    prior_fruit: PublicFruit | None = None


class PublicConsequenceKind(str, Enum):
    RESULT = "result"
    NO_CHANGE = "no_change"


@dataclass(frozen=True)
class PublicConsequenceEnvelope:
    request_id: str
    tree_id: str
    owner_id: str
    kind: str
    result_content: str | None = None


@dataclass(frozen=True)
class PublicTreeTurnResult:
    accepted: bool
    snapshot: PublicTreeSnapshot
    rejection_code: str | None = None
