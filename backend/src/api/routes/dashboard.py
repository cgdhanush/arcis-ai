from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.authz import require_roles
from src.core.database import get_db
from src.core.security import ROLE_COMPLIANCE, ROLE_MANAGEMENT
from src.models.entities import Evidence, MapItem, Regulation, Risk
from src.schemas.api import DashboardResponse, DashboardMetricsResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetricsResponse)
def get_metrics(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> DashboardMetricsResponse:
    pending_maps = (
        db.scalar(
            select(func.count()).select_from(MapItem).where(MapItem.status == "PENDING")
        )
        or 0
    )
    overdue_maps = (
        db.scalar(
            select(func.count()).select_from(MapItem).where(MapItem.deadline_days <= 30)
        )
        or 0
    )
    high_risk_items = (
        db.scalar(select(func.count()).select_from(Risk).where(Risk.severity == "HIGH"))
        or 0
    )
    return DashboardMetricsResponse(
        pending_maps=int(pending_maps),
        overdue_maps=int(overdue_maps),
        high_risk_items=int(high_risk_items),
    )


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles(ROLE_COMPLIANCE, ROLE_MANAGEMENT)),
) -> DashboardResponse:
    total_regulations = db.scalar(select(func.count()).select_from(Regulation)) or 0
    total_maps = db.scalar(select(func.count()).select_from(MapItem)) or 0
    verified_maps = (
        db.scalar(
            select(func.count())
            .select_from(Evidence)
            .where(Evidence.validation_score >= 80)
        )
        or 0
    )
    pending_maps = (
        db.scalar(
            select(func.count()).select_from(MapItem).where(MapItem.status == "Pending")
        )
        or 0
    )
    high_risk_alerts = (
        db.scalar(
            select(func.count())
            .select_from(MapItem)
            .where(MapItem.risk_level == "High")
        )
        or 0
    )

    department_compliance = {
        row[0]: int(row[1])
        for row in db.execute(
            select(MapItem.department, func.count()).group_by(MapItem.department)
        ).all()
    }
    map_status = {
        row[0]: int(row[1])
        for row in db.execute(
            select(MapItem.status, func.count()).group_by(MapItem.status)
        ).all()
    }
    risk_exposure = {
        row[0]: int(row[1])
        for row in db.execute(
            select(MapItem.risk_level, func.count()).group_by(MapItem.risk_level)
        ).all()
    }

    compliance_score = round(verified_maps / total_maps, 2) if total_maps else 0.0

    return DashboardResponse(
        total_regulations=int(total_regulations),
        pending_maps=int(pending_maps),
        compliance_score=compliance_score,
        high_risk_alerts=int(high_risk_alerts),
        department_compliance=department_compliance,
        map_status=map_status,
        risk_exposure=risk_exposure,
    )
