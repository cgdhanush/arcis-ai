from __future__ import annotations

import hashlib
import json


def hash_event(event_data: dict, previous_hash: str) -> str:
    payload = json.dumps(event_data, sort_keys=True)
    return hashlib.sha256(f"{payload}{previous_hash}".encode("utf-8")).hexdigest()
