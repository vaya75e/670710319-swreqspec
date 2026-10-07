from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import AuditLog, Base
from app.db.session import SessionLocal


# รองรับ: DOM-PDPA-01

def test_AC_BKG_06_records_actor_and_hn_for_booking_access():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    from app.audit.middleware import AuditMiddleware

    app = FastAPI()

    @app.post("/bookings")
    async def create_booking():
        return {"id": 1, "hn": "HN-001", "status": "confirmed"}

    app.add_middleware(AuditMiddleware, db_session_factory=SessionLocal)
    client = TestClient(app)

    response = client.post(
        "/bookings",
        json={"slot_id": 9, "hn": "HN-001"},
        headers={"X-Actor-Id": "nurse-19"},
    )

    assert response.status_code == 200

    with SessionLocal() as db:
        log = db.query(AuditLog).first()
        assert log is not None
        assert log.actor_id == "nurse-19"
        assert log.hn == "HN-001"
        assert log.action == "booking_access"
        assert log.accessed_at is not None
