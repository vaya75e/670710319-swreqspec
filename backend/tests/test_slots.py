from datetime import date, time, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Base, Slot
from app.db.session import SessionLocal
from app.slots.router import get_db, router


# รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01, IF-IDP-01

def test_AC_BKG_05_search_slots_returns_available_slots_with_remaining_capacity():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    today = date.today()

    with SessionLocal() as session:
        session.add_all(
            [
                Slot(
                    slot_date=today,
                    start_time=time(9, 0),
                    package_code="STD",
                    capacity=5,
                    remaining=4,
                ),
                Slot(
                    slot_date=today + timedelta(days=1),
                    start_time=time(10, 0),
                    package_code="STD",
                    capacity=3,
                    remaining=2,
                ),
                Slot(
                    slot_date=today + timedelta(days=10),
                    start_time=time(11, 0),
                    package_code="VIP",
                    capacity=2,
                    remaining=1,
                ),
            ]
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

    response = client.get(
        "/slots",
        params={"date_from": today.isoformat(), "package_code": "STD"},
        headers={"X-Verified-Identity": "true"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "slots" in payload
    assert len(payload["slots"]) == 2
    assert payload["slots"][0]["package_code"] == "STD"
    assert payload["slots"][0]["remaining"] >= 0
    assert all(slot["package_code"] == "STD" for slot in payload["slots"])
