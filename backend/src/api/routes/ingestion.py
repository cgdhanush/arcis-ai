from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.agents.ingestion import clean_text, extract_pdf_text, ensure_storage_path
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE
from src.models.entities import Regulation
from src.schemas.api import RegulationUploadResponse
from src.services.audit_service import append_audit_record

router = APIRouter(tags=["ingestion"])


@router.post("/upload-regulation", response_model=RegulationUploadResponse)
async def upload_regulation(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> RegulationUploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    storage_path = ensure_storage_path(file.filename or "regulation-upload")
    contents = await file.read()
    storage_path.write_bytes(contents)

    if suffix == ".pdf":
        content = extract_pdf_text(str(storage_path))
    else:
        content = clean_text(contents.decode("utf-8", errors="ignore"))

    regulation = Regulation(
        title=(file.filename or "Uploaded Regulation").replace(".pdf", ""),
        source="Uploaded",
        content=content,
    )
    db.add(regulation)
    db.commit()
    db.refresh(regulation)

    append_audit_record(
        db,
        action_type="REGULATION_UPLOADED",
        resource_type="REGULATION",
        resource_id=str(regulation.id),
        payload={"file_name": file.filename, "path": str(storage_path)},
    )

    return RegulationUploadResponse(regulation_id=regulation.id, status="uploaded")
