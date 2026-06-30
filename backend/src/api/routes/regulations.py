from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_DEPARTMENT, ROLE_MANAGEMENT
from src.models.entities import Regulation
from src.schemas.api import RegulationResponse

router = APIRouter(prefix="/regulations", tags=["regulations"])


@router.get("", response_model=list[RegulationResponse])
def list_regulations(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_DEPARTMENT, ROLE_MANAGEMENT)),
) -> list[RegulationResponse]:
    rows = (
        db.execute(select(Regulation).order_by(Regulation.created_at.desc()))
        .scalars()
        .all()
    )
    return [
        RegulationResponse(
            id=row.id,
            external_id=row.external_id,
            title=row.title,
            source=row.source,
            content=row.content,
            status=row.status,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]
