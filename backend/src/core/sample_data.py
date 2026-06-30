from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.entities import Department, Evidence, MapItem, Regulation, Risk
from src.services.audit_service import append_audit_record


def seed_demo_data(db: Session) -> dict:
    existing_sample = db.scalar(select(Regulation).limit(1))
    if existing_sample:
        return {
            "status": "skipped",
            "message": "Sample data already exists in the database.",
        }

    departments = [
        Department(name="IT Security", pending_tasks=2, capacity_limit=8),
        Department(name="Risk Management", pending_tasks=1, capacity_limit=6),
        Department(name="Compliance Team", pending_tasks=1, capacity_limit=7),
        Department(name="Operations", pending_tasks=3, capacity_limit=10),
    ]
    db.add_all(departments)
    db.commit()

    regulations = [
        Regulation(
            title="RBI Master Direction on IT Governance",
            source="RBI",
            content=(
                "All scheduled commercial banks must conduct VAPT, implement robust incident "
                "response controls, and report cyber control maturity to the central compliance "
                "team within 60 days."
            ),
        ),
        Regulation(
            title="RBI Circular on Data Localization and Resilience",
            source="RBI",
            content=(
                "Banking data must remain within the country, with encrypted backups, disaster "
                "recovery plans, and quarterly resilience testing for all third-party hosted systems."
            ),
        ),
        Regulation(
            title="SEBI Notification on AML/KYC Technology Controls",
            source="SEBI",
            content=(
                "Firms must deploy automated KYC validation, monitor suspicious transaction patterns, "
                "and escalate 100% of high-risk alerts to the compliance review board."
            ),
        ),
    ]
    db.add_all(regulations)
    db.commit()

    db.refresh(regulations[0])
    db.refresh(regulations[1])
    db.refresh(regulations[2])

    maps = [
        MapItem(
            regulation_id=regulations[0].id,
            title="Conduct 60-day VAPT and remediate findings",
            description="Perform a vulnerability assessment and penetration test across internet-facing banking systems.",
            department="IT Security",
            deadline=30,
            risk_level="High",
            priority_score=95,
            status="Pending",
        ),
        MapItem(
            regulation_id=regulations[0].id,
            title="Implement incident response escalation matrices",
            description="Define roles, timelines, and notification procedures for cyber incidents.",
            department="Risk Management",
            deadline=45,
            risk_level="Medium",
            priority_score=65,
            status="Pending",
        ),
        MapItem(
            regulation_id=regulations[1].id,
            title="Encrypt localized banking datasets",
            description="Ensure all sensitive customer data and backups are encrypted at rest within the jurisdiction.",
            department="Compliance Team",
            deadline=60,
            risk_level="High",
            priority_score=88,
            status="Pending",
        ),
        MapItem(
            regulation_id=regulations[2].id,
            title="Deploy automated AML/KYC validation workflows",
            description="Integrate transaction monitoring with customer KYC profiles and alert generation for high-risk cases.",
            department="Operations",
            deadline=50,
            risk_level="Medium",
            priority_score=72,
            status="Pending",
        ),
    ]
    db.add_all(maps)
    db.commit()

    db.refresh(maps[0])
    db.refresh(maps[1])
    db.refresh(maps[2])
    db.refresh(maps[3])

    risks = [
        Risk(
            map_id=maps[0].id,
            score=92,
            severity="HIGH",
            assigned_department="IT Security",
        ),
        Risk(
            map_id=maps[1].id,
            score=70,
            severity="MEDIUM",
            assigned_department="Risk Management",
        ),
        Risk(
            map_id=maps[2].id,
            score=88,
            severity="HIGH",
            assigned_department="Compliance Team",
        ),
        Risk(
            map_id=maps[3].id,
            score=74,
            severity="MEDIUM",
            assigned_department="Operations",
        ),
    ]
    db.add_all(risks)
    db.commit()

    evidence = Evidence(
        map_id=maps[0].id,
        file_name="VAPT_Report_Q2.pdf",
        file_path="uploads/VAPT_Report_Q2.pdf",
        validation_score=90,
        validation_reason="Evidence confirms remediation of critical findings and documented security controls.",
    )
    db.add(evidence)
    db.commit()

    append_audit_record(
        db,
        action_type="DEMO_SEED",
        resource_type="SYSTEM",
        resource_id="demo-data",
        payload={
            "departments": len(departments),
            "regulations": len(regulations),
            "maps": len(maps),
            "risks": len(risks),
            "evidence": 1,
        },
    )

    return {
        "status": "seeded",
        "departments": len(departments),
        "regulations": len(regulations),
        "maps": len(maps),
        "risks": len(risks),
        "evidence": 1,
    }


if __name__ == "__main__":
    from src.core.database import SessionLocal

    with SessionLocal() as db:
        result = seed_demo_data(db)
        print(result)
