from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Booking, Slot


# รองรับ: FR-BKG-02, FR-BKG-04, IF-IDP-01

class DuplicateBookingError(ValueError):
    def __init__(self, existing_booking: Booking):
        self.existing_booking = existing_booking
        super().__init__("You already have a booking for this day")


def find_existing_same_day_booking(db: Session, hn: str, slot_date: object) -> Booking | None:
    return (
        db.query(Booking)
        .join(Slot, Booking.slot_id == Slot.id)
        .filter(Booking.hn == hn, Slot.slot_date == slot_date, Booking.status == "confirmed")
        .order_by(Booking.created_at.asc())
        .first()
    )


def create_booking_record(db: Session, slot_id: int, hn: str) -> Booking:
    slot = db.query(Slot).filter(Slot.id == slot_id).one_or_none()
    if slot is None:
        raise ValueError("Slot not found")

    if slot.remaining <= 0:
        raise ValueError("Selected slot is full")

    existing_booking = find_existing_same_day_booking(db, hn, slot.slot_date)
    if existing_booking is not None:
        raise DuplicateBookingError(existing_booking)

    booking = Booking(hn=hn, slot_id=slot.id, booking_date=datetime.utcnow())
    db.add(booking)
    db.flush()

    booking.queue_no = f"Q-{booking.id:04d}"
    slot.remaining -= 1
    db.commit()
    db.refresh(booking)

    return booking
