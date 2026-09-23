from __future__ import annotations

from typing import Any


# รองรับ: IF-IDP-01

def is_identity_verified(headers: dict[str, Any] | None = None) -> bool:
    if not headers:
        return False

    normalized = {str(key).lower(): str(value) for key, value in headers.items()}
    return normalized.get("x-verified-identity", "").lower() == "true"
