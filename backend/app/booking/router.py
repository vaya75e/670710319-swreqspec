from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.idp import is_identity_verified
from app.booking.service import DuplicateBookingError, SlotFullError, create_booking_record
from app.db.session import SessionLocal


# รองรับ: FR-BKG-02, FR-BKG-03, FR-BKG-04, IF-IDP-01
router = APIRouter()


class BookingCreateRequest(BaseModel):
    slot_id: int
    hn: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/bookings")
def create_booking(
    payload: BookingCreateRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    headers = dict(request.headers)
    if not is_identity_verified(headers):
        raise HTTPException(status_code=401, detail="Identity not verified")

    try:
        booking = create_booking_record(db, payload.slot_id, payload.hn)
    except SlotFullError as exc:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc), "alternatives": exc.alternatives},
        )
    except DuplicateBookingError as exc:
        existing = exc.existing_booking
        return JSONResponse(
            status_code=409,
            content={
                "detail": "คุณมีคิวที่ยังไม่ได้ใช้ในวันเดียวกันแล้ว ไม่สามารถจองซ้ำได้",
                "queue_no": existing.queue_no,
                "booking_id": existing.id,
                "slot_id": existing.slot_id,
                "hn": existing.hn,
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {
        "id": booking.id,
        "slot_id": booking.slot_id,
        "hn": booking.hn,
        "queue_no": booking.queue_no,
        "status": booking.status,
        "booking_date": booking.booking_date.isoformat(),
    }
