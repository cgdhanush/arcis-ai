from __future__ import annotations


def detect_conflicts_with_policies(regulation_text: str, policies: list[str]) -> dict:
    lowered = regulation_text.lower()
    conflicts = []
    for policy in policies:
        policy_lower = policy.lower()
        if policy_lower in lowered or any(
            token in lowered for token in policy_lower.split()[:2]
        ):
            conflicts.append(
                {
                    "policy": policy,
                    "regulation": regulation_text[:280],
                    "severity": "High",
                }
            )
    return {"conflicts": conflicts}
