from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.agents.orchestrator import (
    detect_conflicts,
    generate_maps_from_notification,
    score_risk,
)
from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_MANAGEMENT
from src.models.entities import MapItem, Notification, Risk
from src.schemas.api import IngestNotificationRequest, NotificationResponse
from src.services.audit_service import append_audit_record

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/ingest", response_model=NotificationResponse)
def ingest_notification(
    payload: IngestNotificationRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE)),
) -> NotificationResponse:
    existing = (
        db.execute(
            select(Notification).where(Notification.external_id == payload.external_id)
        )
        .scalars()
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Notification already exists")

    notification = Notification(
        source=payload.source,
        external_id=payload.external_id,
        title=payload.title,
        content=payload.content,
        status="Ingested",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    conflicts = detect_conflicts(payload.content)
    maps = generate_maps_from_notification(payload.title, payload.content)

    for m in maps:
        map_item = MapItem(
            regulation_id=notification.id,
            title=m.title,
            description=m.title,
            department=m.owner_department,
            deadline=m.deadline_days,
            risk_level=m.risk_level,
            priority_score=score_risk(m.deadline_days, m.risk_level),
            status="Pending",
        )
        db.add(map_item)
        db.flush()

        risk_score = score_risk(m.deadline_days, m.risk_level)
        risk = Risk(
            map_id=map_item.id,
            score=risk_score,
            severity="HIGH" if risk_score >= 80 else "MEDIUM",
            assigned_department=m.owner_department,
        )
        db.add(risk)

    db.commit()

    append_audit_record(
        db,
        action_type="INGEST",
        resource_type="REGULATION",
        resource_id=str(notification.id),
        payload={
            "source": payload.source,
            "conflicts": conflicts,
            "generated_maps": len(maps),
        },
    )

    return NotificationResponse(
        id=notification.id,
        source=notification.source,
        external_id=notification.external_id,
        title=notification.title,
        status=notification.status,
    )


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> list[NotificationResponse]:
    records = (
        db.execute(select(Notification).order_by(Notification.id.desc()))
        .scalars()
        .all()
    )
    return [
        NotificationResponse(
            id=n.id,
            source=n.source,
            external_id=n.external_id,
            title=n.title,
            status=n.status,
        )
        for n in records
    ]
