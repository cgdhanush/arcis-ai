from dataclasses import dataclass

from src.agents.assignment import assign_map
from src.agents.conflict_detector import detect_conflicts_with_policies
from src.agents.hash_chain import hash_event
from src.agents.map_generator import generate_measurable_action_points
from src.agents.prioritizer import calculate_priority_score
from src.agents.validator import validate_evidence_against_map


@dataclass
class MapDraft:
    title: str
    owner_department: str
    deadline_days: int
    risk_level: str


def detect_conflicts(content: str) -> list[str]:
    return detect_conflicts_with_policies(
        content, ["timeline", "overlap", "conflict"]
    ).get("conflicts", [])


def generate_maps_from_notification(title: str, content: str) -> list[MapDraft]:
    maps = []
    for item in generate_measurable_action_points(content):
        maps.append(
            MapDraft(
                title=item["title"],
                owner_department=item["department"],
                deadline_days=item["deadline_days"],
                risk_level=item["risk_level"].upper(),
            )
        )
    return maps


def score_risk(deadline_days: int, risk_level: str) -> int:
    deadline_weight = max(0, 40 - deadline_days)
    risk_weight = (
        50
        if risk_level.upper() == "HIGH"
        else 30 if risk_level.upper() == "MEDIUM" else 10
    )
    return calculate_priority_score(deadline_weight, risk_weight, 3)["score"]


def validate_evidence(summary: str, map_title: str) -> tuple[str, int, str]:
    verdict = validate_evidence_against_map(map_title, summary)
    return (
        "VALID" if verdict["verified"] else "REVIEW_REQUIRED",
        verdict["confidence"],
        verdict["reasoning"],
    )


def build_audit_hash(event_data: dict, previous_hash: str) -> str:
    return hash_event(event_data, previous_hash)
