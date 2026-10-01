"""Generic structural validation, deliberately without semantic assessment."""

from __future__ import annotations

from rewt_public.models import PublicConsequenceEnvelope, PublicConsequenceKind, PublicTreeTurnRequest


class PublicValidationError(ValueError):
    """An envelope is structurally inadmissible and must not be persisted."""


def validate_envelope(request: PublicTreeTurnRequest, envelope: object) -> PublicConsequenceEnvelope:
    if not isinstance(envelope, PublicConsequenceEnvelope):
        raise PublicValidationError("invalid_envelope_type")
    if envelope.request_id != request.request_id:
        raise PublicValidationError("request_id_mismatch")
    if envelope.tree_id != request.tree_id:
        raise PublicValidationError("tree_id_mismatch")
    if envelope.owner_id != request.owner_id:
        raise PublicValidationError("owner_id_mismatch")
    try:
        kind = PublicConsequenceKind(envelope.kind)
    except ValueError as error:
        raise PublicValidationError("invalid_kind") from error
    content = envelope.result_content
    if kind is PublicConsequenceKind.RESULT and not (isinstance(content, str) and content.strip()):
        raise PublicValidationError("missing_result_content")
    if kind is PublicConsequenceKind.NO_CHANGE and content is not None:
        raise PublicValidationError("unexpected_no_change_content")
    return envelope
