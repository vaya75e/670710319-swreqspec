from datetime import date, datetime, time

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.booking.router import get_db, router
from app.db.models import Base, Booking, Slot
from app.db.session import SessionLocal


# รองรับ: FR-BKG-02

def test_AC_BKG_02_duplicate_booking_same_day_is_rejected_with_original_queue_number():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        slot = Slot(
            slot_date=date(2026, 9, 23),
            start_time=time(9, 0),
            package_code="STD",
            capacity=2,
            remaining=2,
        )
        session.add(slot)
        session.commit()
        session.refresh(slot)

        original_booking = Booking(
            hn="HN-001",
            slot_id=slot.id,
            booking_date=datetime(2026, 9, 23, 8, 0, 0),
            queue_no="Q-0001",
            status="confirmed",
        )
        session.add(original_booking)
        session.commit()
        session.refresh(original_booking)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    response = client.post(
        "/bookings",
        json={"slot_id": 1, "hn": "HN-001"},
        headers={"X-Verified-Identity": "true"},
    )

    assert response.status_code == 409
    payload = response.json()
    assert payload["queue_no"] == "Q-0001"
    assert "จองซ้ำ" in payload["detail"] or "ไม่สามารถจองซ้ำ" in payload["detail"]
