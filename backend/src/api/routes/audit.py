from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_MANAGEMENT
from src.models.entities import AuditTrail

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/trail")
def list_audit_trail(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> list[dict[str, str]]:
    rows = db.execute(select(AuditTrail).order_by(AuditTrail.id.asc())).scalars().all()
    return [
        {
            "id": str(row.id),
            "action_type": row.action_type,
            "resource_type": row.resource_type,
            "resource_id": row.resource_id,
            "previous_hash": row.previous_hash,
            "current_hash": row.current_hash,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]


@router.get("/verify")
def verify_chain(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> dict[str, str | int]:
    rows = db.execute(select(AuditTrail).order_by(AuditTrail.id.asc())).scalars().all()
    if not rows:
        return {"status": "ok", "records": 0}

    prev = "GENESIS"
    for row in rows:
        if row.previous_hash != prev:
            return {"status": "broken", "record_id": row.id}
        prev = row.current_hash

    return {"status": "ok", "records": len(rows)}
