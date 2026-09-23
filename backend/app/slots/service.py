from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.db.models import Slot


# รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01

def get_slots_for_period(db: Session, date_from: date, package_code: str | None = None) -> list[dict[str, Any]]:
    query = db.query(Slot).filter(Slot.slot_date >= date_from)
    query = query.filter(Slot.slot_date <= date_from + timedelta(days=30))

    if package_code:
        query = query.filter(Slot.package_code == package_code)

    rows = query.order_by(Slot.slot_date.asc(), Slot.start_time.asc()).all()

    return [
        {
            "id": row.id,
            "slot_date": row.slot_date.isoformat(),
            "start_time": row.start_time.isoformat(),
            "package_code": row.package_code,
            "capacity": row.capacity,
            "remaining": row.remaining,
        }
        for row in rows
    ]
