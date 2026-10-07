from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from app.db.models import Booking, Slot
from app.his.client import lookup_hn_by_national_id
from app.notify.queue import get_notification_queue
from app.slots.service import get_nearest_available_slots


# รองรับ: FR-BKG-02, FR-BKG-03, FR-BKG-04, IF-IDP-01

def resolve_hn_for_booking(national_id: str, client=None, base_url: str = "https://his.example") -> str:
    # รองรับ: IF-HIS-01
    return lookup_hn_by_national_id(national_id, client=client, base_url=base_url)

def get_next_queue_number(db: Session, slot_date: date) -> str:
    # รองรับ: FR-BKG-04
    db.query(Slot.id).filter(Slot.slot_date == slot_date).order_by(Slot.id).with_for_update().all()
    daily_booking_count = (
        db.query(Booking.id)
        .join(Slot, Booking.slot_id == Slot.id)
        .filter(Slot.slot_date == slot_date)
        .count()
    )
    return f"{daily_booking_count + 1:02d}"

class SlotFullError(ValueError):
    # รองรับ: FR-BKG-03
    def __init__(self, alternatives: list[dict[str, object]]):
        self.alternatives = alternatives
        super().__init__("ช่วงเวลาเต็ม")

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
        raise SlotFullError(get_nearest_available_slots(db, slot))

    existing_booking = find_existing_same_day_booking(db, hn, slot.slot_date)
    if existing_booking is not None:
        raise DuplicateBookingError(existing_booking)

    queue_no = get_next_queue_number(db, slot.slot_date)
    booking = Booking(hn=hn, slot_id=slot.id, booking_date=datetime.utcnow())
    db.add(booking)
    db.flush()

    booking.queue_no = queue_no
    slot.remaining -= 1
    db.commit()
    db.refresh(booking)
    get_notification_queue().enqueue(booking.id, booking.hn, booking.queue_no)

    return booking
