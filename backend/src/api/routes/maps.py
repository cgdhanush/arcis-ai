from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_DEPARTMENT, ROLE_MANAGEMENT
from src.models.entities import MapItem
from src.schemas.api import MapResponse

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("", response_model=list[MapResponse])
def list_maps(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_DEPARTMENT, ROLE_MANAGEMENT)),
) -> list[MapResponse]:
    rows = db.execute(select(MapItem).order_by(MapItem.id.desc())).scalars().all()
    return [
        MapResponse(
            id=row.id,
            title=row.title,
            owner_department=row.owner_department,
            deadline_days=row.deadline_days,
            risk_level=row.risk_level,
            status=row.status,
        )
        for row in rows
    ]
