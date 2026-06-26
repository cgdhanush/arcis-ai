from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.agents.conflict_detector import detect_conflicts_with_policies
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_MANAGEMENT
from src.models.entities import Regulation
from src.schemas.api import ConflictResponse
from src.services.audit_service import append_audit_record

router = APIRouter(tags=["conflicts"])


class ConflictInput(BaseModel):
    regulation_id: int | None = None
    regulation_text: str | None = None


@router.post("/detect-conflicts", response_model=ConflictResponse)
def detect_conflicts(
    payload: ConflictInput,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> ConflictResponse:
    if payload.regulation_text:
        regulation_text = payload.regulation_text
    else:
        regulation = db.scalar(
            select(Regulation).where(Regulation.id == payload.regulation_id)
        )
        regulation_text = regulation.content if regulation else ""

    result = detect_conflicts_with_policies(
        regulation_text,
        ["old policy contradiction", "overlapping control", "missing control"],
    )

    append_audit_record(
        db,
        action_type="CONFLICT_DETECTED",
        resource_type="REGULATION",
        resource_id=str(payload.regulation_id or "manual"),
        payload=result,
    )

    return ConflictResponse.model_validate(result)
