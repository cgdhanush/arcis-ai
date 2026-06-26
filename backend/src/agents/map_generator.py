from __future__ import annotations


def generate_measurable_action_points(regulation_text: str) -> list[dict]:
    lowered = regulation_text.lower()
    maps: list[dict] = []

    if "vapt" in lowered or "cyber" in lowered or "security" in lowered:
        maps.append(
            {
                "title": "Conduct annual VAPT audit",
                "description": "Perform an annual vulnerability assessment and penetration test and submit the report.",
                "department": "IT Security",
                "deadline_days": 30,
                "risk_level": "High",
            }
        )

    maps.append(
        {
            "title": "Appoint Chief Information Security Officer",
            "description": "Designate a CISO with formal responsibilities for information security governance.",
            "department": "HR",
            "deadline_days": 60,
            "risk_level": "High",
        }
    )
    maps.append(
        {
            "title": "Update IT risk policy",
            "description": "Review and update IT risk policy to align with the regulation.",
            "department": "Legal",
            "deadline_days": 45,
            "risk_level": "Medium",
        }
    )
    return maps
