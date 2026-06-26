from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from src.core.config import settings

ROLE_COMPLIANCE = "compliance_officer"
ROLE_DEPARTMENT = "department_owner"
ROLE_MANAGEMENT = "management_viewer"
ALLOWED_ROLES = {ROLE_COMPLIANCE, ROLE_DEPARTMENT, ROLE_MANAGEMENT}


def create_access_token(subject: str, role: str) -> str:
    if role not in ALLOWED_ROLES:
        raise ValueError(f"Unsupported role: {role}")
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload: dict[str, Any] = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
