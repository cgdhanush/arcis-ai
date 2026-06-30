from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

SCHEMA_UPDATES: dict[str, dict[str, str]] = {
    "regulations": {
        "external_id": "VARCHAR(128)",
        "title": "VARCHAR(512)",
        "source": "VARCHAR(64)",
        "content": "TEXT",
        "status": "VARCHAR(32)",
        "created_at": "TIMESTAMP",
    },
    "departments": {
        "name": "VARCHAR(128)",
        "pending_tasks": "INTEGER",
        "capacity_limit": "INTEGER",
    },
    "maps": {
        "regulation_id": "INTEGER",
        "title": "VARCHAR(512)",
        "description": "TEXT",
        "department": "VARCHAR(128)",
        "deadline": "INTEGER",
        "risk_level": "VARCHAR(32)",
        "priority_score": "INTEGER",
        "status": "VARCHAR(32)",
        "created_at": "TIMESTAMP",
    },
    "evidence": {
        "map_id": "INTEGER",
        "file_name": "VARCHAR(256)",
        "file_path": "VARCHAR(512)",
        "validation_score": "INTEGER",
        "validation_reason": "TEXT",
        "uploaded_at": "TIMESTAMP",
    },
    "risks": {
        "map_id": "INTEGER",
        "score": "INTEGER",
        "severity": "VARCHAR(32)",
        "assigned_department": "VARCHAR(128)",
    },
    "audit_logs": {
        "timestamp": "TIMESTAMP",
        "event": "VARCHAR(128)",
        "event_data": "TEXT",
        "previous_hash": "VARCHAR(128)",
        "current_hash": "VARCHAR(128)",
    },
}


def ensure_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        for table_name, columns in SCHEMA_UPDATES.items():
            if table_name not in existing_tables:
                continue

            existing_columns = {
                column["name"] for column in inspector.get_columns(table_name)
            }
            for column_name, ddl_type in columns.items():
                if column_name not in existing_columns:
                    connection.execute(
                        text(
                            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {ddl_type}"
                        )
                    )
