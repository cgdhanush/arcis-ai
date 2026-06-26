from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_MANAGEMENT
from src.models.entities import AuditLog

router = APIRouter(tags=["audit"])


@router.get("/audit-log")
def get_audit_log(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> list[dict]:
    rows = db.execute(select(AuditLog).order_by(AuditLog.id.asc())).scalars().all()
    return [
        {
            "id": row.id,
            "timestamp": row.timestamp.isoformat(),
            "event": row.event,
            "event_data": row.event_data,
            "previous_hash": row.previous_hash,
            "current_hash": row.current_hash,
        }
        for row in rows
    ]


@router.get("/audit-log/verify")
def verify_audit_chain(db: Session = Depends(get_db)) -> dict:
    rows = db.execute(select(AuditLog).order_by(AuditLog.id.asc())).scalars().all()
    previous_hash = "GENESIS"
    for row in rows:
        if row.previous_hash != previous_hash:
            return {"status": "broken", "record_id": row.id}
        previous_hash = row.current_hash
    return {"status": "ok", "records": len(rows)}
