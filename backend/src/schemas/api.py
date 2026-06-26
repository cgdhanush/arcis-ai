from pydantic import BaseModel, Field


class RegulationUploadResponse(BaseModel):
    regulation_id: int
    status: str


class ConflictItem(BaseModel):
    policy: str
    regulation: str
    severity: str


class ConflictResponse(BaseModel):
    conflicts: list[ConflictItem]


class MAPItem(BaseModel):
    title: str
    description: str
    department: str
    deadline_days: int
    risk_level: str


class MAPResponse(BaseModel):
    items: list[MAPItem]


class DashboardResponse(BaseModel):
    total_regulations: int
    pending_maps: int
    compliance_score: float
    high_risk_alerts: int
    department_compliance: dict[str, int]
    map_status: dict[str, int]
    risk_exposure: dict[str, int]


class AuditLogResponse(BaseModel):
    id: int
    timestamp: str
    event: str
    event_data: str
    previous_hash: str
    current_hash: str


from pydantic import BaseModel, Field


class IngestNotificationRequest(BaseModel):
    source: str = Field(examples=["RBI"])
    external_id: str
    title: str
    content: str


class NotificationResponse(BaseModel):
    id: int
    source: str
    external_id: str
    title: str
    status: str


class MapResponse(BaseModel):
    id: int
    title: str
    owner_department: str
    deadline_days: int
    risk_level: str
    status: str


class RiskResponse(BaseModel):
    id: int
    map_item_id: int
    score: int
    severity: str
    assigned_department: str


class EvidenceValidationResponse(BaseModel):
    evidence_id: int
    status: str
    confidence_score: int
    reasoning: str


class DashboardMetricsResponse(BaseModel):
    pending_maps: int
    overdue_maps: int
    high_risk_items: int
