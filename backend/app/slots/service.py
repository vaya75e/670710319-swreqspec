from __future__ import annotations

from datetime import date, datetime, timedelta
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


# รองรับ: FR-BKG-03
def get_nearest_available_slots(db: Session, selected_slot: Slot, limit: int = 3) -> list[dict[str, Any]]:
    next_day = selected_slot.slot_date + timedelta(days=1)
    candidates = (
        db.query(Slot)
        .filter(
            Slot.slot_date >= selected_slot.slot_date,
            Slot.slot_date <= next_day,
            Slot.package_code == selected_slot.package_code,
            Slot.remaining > 0,
        )
        .all()
    )
    selected_minutes = selected_slot.start_time.hour * 60 + selected_slot.start_time.minute
    candidates.sort(
        key=lambda candidate: (
            abs(candidate.start_time.hour * 60 + candidate.start_time.minute - selected_minutes),
            candidate.slot_date,
            candidate.start_time,
            candidate.id,
        )
    )

    return [
        {
            "id": candidate.id,
            "slot_date": candidate.slot_date.isoformat(),
            "start_time": candidate.start_time.isoformat(),
            "package_code": candidate.package_code,
            "remaining": candidate.remaining,
        }
        for candidate in candidates[:limit]
    ]
