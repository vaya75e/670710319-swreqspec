from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Booking, Slot


# รองรับ: FR-BKG-04, IF-IDP-01

def create_booking_record(db: Session, slot_id: int, hn: str) -> Booking:
    slot = db.query(Slot).filter(Slot.id == slot_id).one_or_none()
    if slot is None:
        raise ValueError("Slot not found")

    if slot.remaining <= 0:
        raise ValueError("Selected slot is full")

    booking = Booking(hn=hn, slot_id=slot.id, booking_date=datetime.utcnow())
    db.add(booking)
    db.flush()

    booking.queue_no = f"Q-{booking.id:04d}"
    slot.remaining -= 1
    db.commit()
    db.refresh(booking)

    return booking
