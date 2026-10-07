from datetime import date, datetime, time, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.booking.router import get_db, router
from app.db.models import Base, Booking, Slot
from app.notify.queue import InMemoryNotificationQueue


# รองรับ: FR-BKG-05, NFR-REL-02, IF-NOT-01

def test_AC_BKG_04_booking_persists_and_failed_notification_retries_within_five_minutes(monkeypatch):
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(bind=engine)
    slot_date = date.today()

    with testing_session_local() as db:
        db.add(
            Slot(
                slot_date=slot_date,
                start_time=time(9, 0),
                package_code="STD",
                capacity=1,
                remaining=1,
            )
        )
        db.commit()

    queue = InMemoryNotificationQueue()
    monkeypatch.setattr("app.booking.service.get_notification_queue", lambda: queue)

    def override_get_db():
        with testing_session_local() as db:
            yield db

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
    booking_response = response.json()
    assert booking_response["queue_no"] == "01"
    assert len(queue.jobs) == 1

    with testing_session_local() as db:
        assert db.query(Booking).count() == 1
        assert db.get(Slot, 1).remaining == 0

    first_attempt_at = datetime.fromisoformat(str(queue.jobs[0]["scheduled_at"]))
    result = queue.process_due(lambda notification: False, now=first_attempt_at)

    assert result == {"sent": 0, "rescheduled": 1, "pending": 0}
    assert queue.jobs[0]["retry_count"] == 1
    assert datetime.fromisoformat(str(queue.jobs[0]["scheduled_at"])) == first_attempt_at + timedelta(minutes=5)

    for expected_retry_count in (2, 3):
        retry_at = datetime.fromisoformat(str(queue.jobs[0]["scheduled_at"]))
        result = queue.process_due(lambda notification: False, now=retry_at)
        assert result == {"sent": 0, "rescheduled": 1, "pending": 0}
        assert queue.jobs[0]["retry_count"] == expected_retry_count
        assert datetime.fromisoformat(str(queue.jobs[0]["scheduled_at"])) == retry_at + timedelta(minutes=5)

    last_retry_at = datetime.fromisoformat(str(queue.jobs[0]["scheduled_at"]))
    result = queue.process_due(lambda notification: False, now=last_retry_at)

    assert result == {"sent": 0, "rescheduled": 0, "pending": 1}
    assert queue.jobs == []
    assert queue.pending[0]["retry_count"] == 4

    with testing_session_local() as db:
        assert db.query(Booking).count() == 1
        assert db.get(Slot, 1).remaining == 0


def test_notification_queue_removes_a_successfully_sent_message():
    queue = InMemoryNotificationQueue()
    queue.enqueue(booking_id=1, hn="HN-001", queue_no="01")
    scheduled_at = datetime.fromisoformat(str(queue.jobs[0]["scheduled_at"]))

    result = queue.process_due(lambda notification: True, now=scheduled_at)

    assert result == {"sent": 1, "rescheduled": 0, "pending": 0}
    assert queue.jobs == []
    assert queue.pending == []
