from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.agents.validator import extract_evidence_text, validate_evidence_against_map
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_DEPARTMENT
from src.models.entities import Evidence, MapItem
from src.services.audit_service import append_audit_record

router = APIRouter(tags=["validation"])


@router.post("/upload-evidence")
async def upload_evidence(
    map_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_DEPARTMENT)),
) -> dict:
    map_item = db.scalar(select(MapItem).where(MapItem.id == map_id))
    if not map_item:
        raise HTTPException(status_code=404, detail="MAP not found")

    uploads = Path("uploads")
    uploads.mkdir(exist_ok=True)
    file_path = uploads / file.filename
    file_path.write_bytes(await file.read())

    evidence = Evidence(
        map_id=map_id,
        file_name=file.filename,
        file_path=str(file_path),
        validation_score=0,
        validation_reason="Uploaded for validation",
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    append_audit_record(
        db,
        action_type="EVIDENCE_UPLOADED",
        resource_type="EVIDENCE",
        resource_id=str(evidence.id),
        payload={"map_id": map_id, "file_name": file.filename},
    )

    return {"evidence_id": evidence.id, "status": "uploaded"}


@router.post("/validate-evidence")
def validate_evidence(
    evidence_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_DEPARTMENT)),
) -> dict:
    evidence = db.scalar(select(Evidence).where(Evidence.id == evidence_id))
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    map_item = db.scalar(select(MapItem).where(MapItem.id == evidence.map_id))
    if not map_item:
        raise HTTPException(status_code=404, detail="MAP not found")

    evidence_text = extract_evidence_text(evidence.file_path)
    verdict = validate_evidence_against_map(map_item.description, evidence_text)
    evidence.validation_score = verdict["confidence"]
    evidence.validation_reason = verdict["reasoning"]
    db.commit()

    append_audit_record(
        db,
        action_type="EVIDENCE_VALIDATED",
        resource_type="EVIDENCE",
        resource_id=str(evidence.id),
        payload=verdict,
    )

    return verdict
