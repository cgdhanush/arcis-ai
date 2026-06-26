from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.agents.assignment import assign_map
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE
from src.models.entities import Department, MapItem
from src.services.audit_service import append_audit_record

router = APIRouter(tags=["assignment"])


@router.post("/assign-maps")
def assign_maps(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE)),
) -> dict:
    departments = db.execute(select(Department)).scalars().all()
    department_state = {
        department.name: {
            "pending_tasks": department.pending_tasks,
            "capacity_limit": department.capacity_limit,
        }
        for department in departments
    }

    maps = (
        db.execute(select(MapItem).where(MapItem.status == "Pending")).scalars().all()
    )
    alerts = []

    for map_item in maps:
        assignment = assign_map(
            {"department": map_item.department},
            department_state,
        )
        if assignment["overloaded"]:
            alerts.append(
                {
                    "map_id": map_item.id,
                    "department": assignment["department"],
                    "alert": "Department overloaded",
                }
            )
        map_item.status = "Assigned"

    db.commit()

    append_audit_record(
        db,
        action_type="TASK_ASSIGNED",
        resource_type="MAP",
        resource_id="bulk",
        payload={"alerts": alerts, "assigned_count": len(maps)},
    )

    return {"assigned": len(maps), "alerts": alerts}
