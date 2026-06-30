from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Regulation(Base):
    __tablename__ = "regulations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[str] = mapped_column(
        String(128), unique=True, index=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(512), index=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="Draft", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    pending_tasks: Mapped[int] = mapped_column(Integer, default=0)
    capacity_limit: Mapped[int] = mapped_column(Integer, default=5)


class MapItem(Base):
    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    regulation_id: Mapped[int] = mapped_column(ForeignKey("regulations.id"), index=True)
    title: Mapped[str] = mapped_column(String(512), index=True)
    description: Mapped[str] = mapped_column(Text)
    department: Mapped[str] = mapped_column(String(128), index=True)
    deadline: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(32), index=True)
    priority_score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    status: Mapped[str] = mapped_column(String(32), default="Pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), index=True)
    file_name: Mapped[str] = mapped_column(String(256))
    file_path: Mapped[str] = mapped_column(String(512))
    validation_score: Mapped[int] = mapped_column(Integer, default=0)
    validation_reason: Mapped[str] = mapped_column(Text, default="")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), index=True)
    score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    severity: Mapped[str] = mapped_column(String(32), index=True)
    assigned_department: Mapped[str] = mapped_column(String(128), index=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    event: Mapped[str] = mapped_column(String(128), index=True)
    event_data: Mapped[str] = mapped_column(Text)
    previous_hash: Mapped[str] = mapped_column(String(128), default="GENESIS")
    current_hash: Mapped[str] = mapped_column(String(128), index=True)


# Compatibility aliases for earlier scaffold code.
Notification = Regulation
Map = MapItem
AuditTrail = AuditLog
