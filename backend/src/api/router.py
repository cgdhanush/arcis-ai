from fastapi import APIRouter

from src.api.routes import (
    audit,
    auth,
    audit_log,
    assignment,
    conflicts,
    dashboard,
    evidence,
    generation,
    health,
    ingestion,
    maps,
    notifications,
    risks,
    validation,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(ingestion.router)
api_router.include_router(conflicts.router)
api_router.include_router(generation.router)
api_router.include_router(assignment.router)
api_router.include_router(validation.router)
api_router.include_router(audit_log.router)
api_router.include_router(evidence.router)
api_router.include_router(audit.router)
api_router.include_router(maps.router)
api_router.include_router(notifications.router)
api_router.include_router(risks.router)
api_router.include_router(dashboard.router)