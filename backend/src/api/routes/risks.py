from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_MANAGEMENT
from src.models.entities import Risk
from src.schemas.api import RiskResponse

router = APIRouter(prefix="/risks", tags=["risks"])


@router.get("", response_model=list[RiskResponse])
def list_risks(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> list[RiskResponse]:
    rows = db.execute(select(Risk).order_by(Risk.score.desc())).scalars().all()
    return [
        RiskResponse(
            id=row.id,
            map_item_id=row.map_item_id,
            score=row.score,
            severity=row.severity,
            assigned_department=row.assigned_department,
        )
        for row in rows
    ]
