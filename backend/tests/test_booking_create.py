from datetime import date, datetime, time, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Base, Booking, Slot
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
    assert payload["queue_no"] == "01"

    with SessionLocal() as session:
        slot = session.get(Slot, 1)
        assert slot is not None
        assert slot.remaining == 0


def create_booking_client(session_factory):
    # รองรับ: FR-BKG-04, IF-IDP-01
    def override_get_db():
        with session_factory() as db:
            yield db

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_AC_BKG_01_queue_numbers_share_package_sequence_and_reset_by_slot_date():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(bind=engine)
    slot_date = date.today()
    next_slot_date = slot_date + timedelta(days=1)

    with testing_session_local() as db:
        slots = [
            Slot(slot_date=slot_date, start_time=time(9, 0), package_code="STD", capacity=1, remaining=1),
            Slot(slot_date=slot_date, start_time=time(10, 0), package_code="VIP", capacity=1, remaining=1),
            Slot(slot_date=next_slot_date, start_time=time(9, 0), package_code="STD", capacity=1, remaining=1),
        ]
        db.add_all(slots)
        db.commit()
        for slot in slots:
            db.refresh(slot)
        slot_ids = [slot.id for slot in slots]

    client = create_booking_client(testing_session_local)
    responses = [
        client.post(
            "/bookings",
            json={"slot_id": slot_id, "hn": f"HN-{index:03d}"},
            headers={"X-Verified-Identity": "true"},
        )
        for index, slot_id in enumerate(slot_ids, start=1)
    ]

    assert [response.status_code for response in responses] == [200, 200, 200]
    assert [response.json()["queue_no"] for response in responses] == ["01", "02", "01"]


def test_AC_BKG_01_queue_number_expands_after_99_without_truncation():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(bind=engine)
    slot_date = date.today()

    with testing_session_local() as db:
        slots = [
            Slot(
                slot_date=slot_date,
                start_time=(datetime.combine(slot_date, time(9, 0)) + timedelta(minutes=index)).time(),
                package_code="STD" if index % 2 == 0 else "VIP",
                capacity=1,
                remaining=1 if index == 99 else 0,
            )
            for index in range(100)
        ]
        db.add_all(slots)
        db.flush()
        db.add_all(
            [
                Booking(
                    hn=f"HN-{index:03d}",
                    slot_id=slots[index - 1].id,
                    booking_date=datetime.now(),
                    queue_no=f"{index:02d}",
                    status="confirmed",
                )
                for index in range(1, 100)
            ]
        )
        target_slot_id = slots[99].id
        db.commit()

    client = create_booking_client(testing_session_local)
    response = client.post(
        "/bookings",
        json={"slot_id": target_slot_id, "hn": "HN-100"},
        headers={"X-Verified-Identity": "true"},
    )

    assert response.status_code == 200
    assert response.json()["queue_no"] == "100"
