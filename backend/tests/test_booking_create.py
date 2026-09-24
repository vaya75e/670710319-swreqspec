from datetime import date, time

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Base, Slot
from app.db.session import SessionLocal
from app.booking.router import get_db, router


# รองรับ: FR-BKG-04, IF-IDP-01

def test_AC_BKG_01_booking_success_creates_record_and_reduces_remaining():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        session.add(
            Slot(
                slot_date=date(2026, 9, 23),
                start_time=time(9, 0),
                package_code="STD",
                capacity=1,
                remaining=1,
            )
        )
        session.commit()

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

    assert response.status_code == 200
    payload = response.json()
    assert payload["slot_id"] == 1
    assert payload["hn"] == "HN-001"
    assert payload["queue_no"]

    with SessionLocal() as session:
        slot = session.get(Slot, 1)
        assert slot is not None
        assert slot.remaining == 0
