from __future__ import annotations

DEPARTMENTS = ["IT Security", "Legal", "HR", "Operations", "Risk"]


def assign_map(map_item: dict, department_state: dict[str, dict[str, int]]) -> dict:
    department_name = map_item.get("department", "Operations")
    current = department_state.get(
        department_name, {"pending_tasks": 0, "capacity_limit": 5}
    )
    overloaded = current["pending_tasks"] > current["capacity_limit"]
    return {
        "department": department_name,
        "overloaded": overloaded,
        "pending_tasks": current["pending_tasks"],
        "capacity_limit": current["capacity_limit"],
    }
