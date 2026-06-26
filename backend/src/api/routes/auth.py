from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.core.security import ALLOWED_ROLES, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    role: str


@router.post("/token")
def issue_token(payload: LoginRequest) -> dict[str, str]:
    if payload.role not in ALLOWED_ROLES:
        allowed = ", ".join(sorted(ALLOWED_ROLES))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"role must be one of: {allowed}",
        )
    token = create_access_token(payload.username, payload.role)
    return {"access_token": token, "token_type": "bearer"}
