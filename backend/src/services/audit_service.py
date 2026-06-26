import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.entities import AuditLog


def _hash_payload(event: str, event_data: dict, previous_hash: str) -> str:
    raw = f"{event}|{json.dumps(event_data, sort_keys=True)}|{previous_hash}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def append_audit_record(
    db: Session,
    *,
    action_type: str,
    resource_type: str,
    resource_id: str,
    payload: dict,
) -> AuditLog:
    event = f"{action_type}:{resource_type}:{resource_id}"
    last_record = (
        db.execute(select(AuditLog).order_by(AuditLog.id.desc())).scalars().first()
    )
    previous_hash = last_record.current_hash if last_record else "GENESIS"
    event_data = {
        "action_type": action_type,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "payload": payload,
    }
    current_hash = _hash_payload(event, event_data, previous_hash)

    record = AuditLog(
        event=event,
        event_data=json.dumps(event_data),
        previous_hash=previous_hash,
        current_hash=current_hash,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
