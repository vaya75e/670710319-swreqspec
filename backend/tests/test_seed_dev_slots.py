from datetime import date

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.slots.router import get_db, router
from scripts.seed_dev_slots import add_dev_slot


# รองรับ: FR-BKG-01, FR-BKG-04

def test_seeded_slot_is_discoverable_from_get_slots(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'booking.db'}")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    slot_date = date.today()

    with TestingSessionLocal() as db:
        seeded_slot = add_dev_slot(db, slot_date, "STD")
        seeded_slot_id = seeded_slot.id

    def override_get_db():
        with TestingSessionLocal() as db:
            yield db

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    response = client.get(
        "/slots",
        params={"date_from": slot_date.isoformat(), "package_code": "STD"},
        headers={"X-Verified-Identity": "true"},
    )

    assert response.status_code == 200
    slots = response.json()["slots"]
    assert len(slots) == 1
    assert slots[0]["id"] == seeded_slot_id
    assert slots[0]["start_time"] == "09:00:00"
    assert slots[0]["capacity"] == 1
    assert slots[0]["remaining"] == 1


def test_seed_rejects_a_date_outside_the_booking_window(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'booking.db'}")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)

    with TestingSessionLocal() as db:
        try:
            add_dev_slot(db, date.today().replace(year=date.today().year - 1), "STD")
        except ValueError as exc:
            assert str(exc) == "slot date must be within the next 30 days"
        else:
            raise AssertionError("an out-of-window slot date must be rejected")
