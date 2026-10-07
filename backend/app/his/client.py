from __future__ import annotations

from typing import Any

import requests


# รองรับ: IF-HIS-01

class HISLookupError(RuntimeError):
    pass


def lookup_hn_by_national_id(national_id: str, client: Any | None = None, base_url: str = "https://his.example") -> str:
    if not national_id:
        raise HISLookupError("national_id is required")

    http_client = client or requests
    response = http_client.get(
        f"{base_url.rstrip('/')}/patients/lookup",
        params={"national_id": national_id},
        timeout=5.0,
    )
    response.raise_for_status()

    payload = response.json()
    hn = payload.get("hn")
    if not hn:
        raise HISLookupError("HIS did not return an HN")

    return str(hn)
