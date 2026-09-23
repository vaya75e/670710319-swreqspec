from sqlalchemy import inspect

from app.db.models import Base
from app.db.session import build_engine


# รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01

def test_db_schema_has_required_tables_and_no_national_id_column():
    engine = build_engine()
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "slots" in tables
    assert "bookings" in tables
    assert "audit_logs" in tables

    booking_columns = {column["name"] for column in inspector.get_columns("bookings")}
    assert "hn" in booking_columns
    assert "slot_id" in booking_columns
    assert "queue_no" in booking_columns
    assert "national_id" not in booking_columns
