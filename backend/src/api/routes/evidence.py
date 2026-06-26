from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.agents.orchestrator import validate_evidence
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_DEPARTMENT
from src.models.entities import Evidence, MapItem
from src.schemas.api import EvidenceValidationResponse
from src.services.audit_service import append_audit_record

router = APIRouter(prefix="/evidence", tags=["evidence"])


class EvidenceInput(BaseModel):
    map_item_id: int
    file_name: str
    summary: str


@router.post("/upload", response_model=EvidenceValidationResponse)
def upload_evidence(
    payload: EvidenceInput,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_DEPARTMENT)),
) -> EvidenceValidationResponse:
    map_item = (
        db.execute(select(MapItem).where(MapItem.id == payload.map_item_id))
        .scalars()
        .first()
    )
    if not map_item:
        raise HTTPException(status_code=404, detail="MAP item not found")

    status, confidence, reasoning = validate_evidence(payload.summary, map_item.title)

    evidence = Evidence(
        map_item_id=payload.map_item_id,
        file_name=payload.file_name,
        summary=payload.summary,
        validation_status=status,
        confidence_score=confidence,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    append_audit_record(
        db,
        action_type="EVIDENCE_VALIDATE",
        resource_type="EVIDENCE",
        resource_id=str(evidence.id),
        payload={"status": status, "confidence": confidence},
    )

    return EvidenceValidationResponse(
        evidence_id=evidence.id,
        status=status,
        confidence_score=confidence,
        reasoning=reasoning,
    )
