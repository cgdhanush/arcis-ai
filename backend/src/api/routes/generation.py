from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.agents.map_generator import generate_measurable_action_points
from src.agents.prioritizer import calculate_priority_score
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE
from src.models.entities import MapItem, Regulation
from src.schemas.api import MAPResponse
from src.services.audit_service import append_audit_record

router = APIRouter(tags=["maps"])


class GenerateMapsInput(BaseModel):
    regulation_id: int | None = None
    regulation_text: str | None = None


@router.post("/generate-maps", response_model=MAPResponse)
def generate_maps(
    payload: GenerateMapsInput,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE)),
) -> MAPResponse:
    if payload.regulation_text:
        regulation_text = payload.regulation_text
        regulation_id = payload.regulation_id or 1
    else:
        regulation = db.scalar(
            select(Regulation).where(Regulation.id == payload.regulation_id)
        )
        regulation_text = regulation.content if regulation else ""
        regulation_id = regulation.id if regulation else 1

    items = []
    for map_data in generate_measurable_action_points(regulation_text):
        score_info = calculate_priority_score(
            deadline_weight=max(0, 40 - map_data["deadline_days"]),
            risk_weight=50 if map_data["risk_level"] == "High" else 30,
            department_workload=3,
        )
        map_item = MapItem(
            regulation_id=regulation_id,
            title=map_data["title"],
            description=map_data["description"],
            department=map_data["department"],
            deadline=map_data["deadline_days"],
            risk_level=map_data["risk_level"],
            priority_score=score_info["score"],
            status="Pending",
        )
        db.add(map_item)
        db.flush()
        items.append(map_data)

    db.commit()

    append_audit_record(
        db,
        action_type="MAP_GENERATED",
        resource_type="REGULATION",
        resource_id=str(regulation_id),
        payload={"maps_created": len(items)},
    )

    return MAPResponse(items=items)


@router.get("/maps")
def list_maps(db: Session = Depends(get_db)) -> list[dict]:
    rows = (
        db.execute(select(MapItem).order_by(MapItem.created_at.desc())).scalars().all()
    )
    return [
        {
            "id": row.id,
            "regulation_id": row.regulation_id,
            "title": row.title,
            "description": row.description,
            "department": row.department,
            "deadline": row.deadline,
            "risk_level": row.risk_level,
            "priority_score": row.priority_score,
            "status": row.status,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]
