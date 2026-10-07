from datetime import date, time, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.booking.router import get_db, router
from app.db.models import Base, Booking, Slot


# รองรับ: FR-BKG-03
def test_AC_BKG_03_full_slot_returns_three_nearest_same_package_slots_without_duplicate_booking():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    slot_date = date.today()

    with TestingSessionLocal() as db:
        selected_slot = Slot(
            slot_date=slot_date,
            start_time=time(9, 0),
            package_code="STD",
            capacity=1,
            remaining=1,
        )
        slots = [
            selected_slot,
            Slot(slot_date=slot_date, start_time=time(9, 15), package_code="STD", capacity=1, remaining=1),
            Slot(slot_date=slot_date, start_time=time(8, 50), package_code="STD", capacity=1, remaining=1),
            Slot(
                slot_date=slot_date + timedelta(days=1),
                start_time=time(9, 5),
                package_code="STD",
                capacity=1,
                remaining=1,
            ),
            Slot(
                slot_date=slot_date + timedelta(days=1),
                start_time=time(8, 45),
                package_code="STD",
                capacity=1,
                remaining=1,
            ),
            Slot(slot_date=slot_date, start_time=time(9, 1), package_code="VIP", capacity=1, remaining=1),
            Slot(
                slot_date=slot_date + timedelta(days=2),
                start_time=time(9, 1),
                package_code="STD",
                capacity=1,
                remaining=1,
            ),
            Slot(slot_date=slot_date, start_time=time(9, 1), package_code="STD", capacity=1, remaining=0),
        ]
        db.add_all(slots)
        db.commit()
        db.refresh(selected_slot)
        selected_slot_id = selected_slot.id

    def override_get_db():
        with TestingSessionLocal() as db:
            yield db

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    headers = {"X-Verified-Identity": "true"}

    first_booking = client.post(
        "/bookings",
        json={"slot_id": selected_slot_id, "hn": "HN-FIRST"},
        headers=headers,
    )
    assert first_booking.status_code == 200

    second_booking = client.post(
        "/bookings",
        json={"slot_id": selected_slot_id, "hn": "HN-SECOND"},
        headers=headers,
    )

    assert second_booking.status_code == 409
    payload = second_booking.json()
    assert payload["detail"] == "ช่วงเวลาเต็ม"
    assert [slot["start_time"] for slot in payload["alternatives"]] == [
        "09:05:00",
        "08:50:00",
        "09:15:00",
    ]
    assert [slot["slot_date"] for slot in payload["alternatives"]] == [
        (slot_date + timedelta(days=1)).isoformat(),
        slot_date.isoformat(),
        slot_date.isoformat(),
    ]
    assert all(slot["package_code"] == "STD" for slot in payload["alternatives"])

    with TestingSessionLocal() as db:
        assert db.query(Booking).count() == 1
        assert db.get(Slot, selected_slot_id).remaining == 0