from __future__ import annotations


def calculate_priority_score(
    deadline_weight: int, risk_weight: int, department_workload: int
) -> dict:
    workload_score = max(0, 20 - department_workload * 2)
    score = min(100, deadline_weight + risk_weight + workload_score)
    if score <= 40:
        priority = "Low"
    elif score <= 70:
        priority = "Medium"
    else:
        priority = "Critical"
    return {"priority": priority, "score": score}
