from __future__ import annotations

from unittest.mock import Mock

import pytest

from app.his.client import HISLookupError, lookup_hn_by_national_id


# รองรับ: IF-HIS-01

def test_lookup_hn_by_national_id_returns_hn_from_his_response():
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "hn": "HN-9001",
        "national_id": "1234567890123",
    }

    client = Mock()
    client.get.return_value = response

    hn = lookup_hn_by_national_id("1234567890123", client=client, base_url="https://his.example")

    assert hn == "HN-9001"
    client.get.assert_called_once_with(
        "https://his.example/patients/lookup",
        params={"national_id": "1234567890123"},
        timeout=5.0,
    )


def test_lookup_hn_by_national_id_raises_when_his_has_no_hn():
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"message": "not found"}

    client = Mock()
    client.get.return_value = response

    with pytest.raises(HISLookupError):
        lookup_hn_by_national_id("0000000000000", client=client, base_url="https://his.example")
