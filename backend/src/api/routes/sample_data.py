from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.sample_data import seed_demo_data
from src.core.security import ROLE_COMPLIANCE

router = APIRouter(prefix="/sample-data", tags=["sample-data"])


@router.post("/seed")
def seed_sample_data(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE)),
) -> dict:
    return seed_demo_data(db)
