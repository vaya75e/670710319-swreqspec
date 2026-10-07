from __future__ import annotations

import argparse
import os
from datetime import date, time, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import Slot


# รองรับ: FR-BKG-01, FR-BKG-04

def add_dev_slot(db: Session, slot_date: date, package_code: str) -> Slot:
    today = date.today()
    if slot_date < today or slot_date > today + timedelta(days=30):
        raise ValueError("slot date must be within the next 30 days")
    if not package_code.strip():
        raise ValueError("package code must not be empty")

    slot = Slot(
        slot_date=slot_date,
        start_time=time(9, 0),
        package_code=package_code.strip(),
        capacity=1,
        remaining=1,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add one 09:00 slot to an explicitly configured dev/test database."
    )
    parser.add_argument("--date", required=True, help="Slot date in YYYY-MM-DD format")
    parser.add_argument("--package-code", required=True, help="Team-selected test package code")
    args = parser.parse_args()

    database_url = os.getenv("DATABASE_URL")
    if not database_url or database_url in {"sqlite://", "sqlite:///:memory:"}:
        parser.error("set DATABASE_URL to a persistent dev/test database")

    try:
        slot_date = date.fromisoformat(args.date)
    except ValueError:
        parser.error("--date must use YYYY-MM-DD format")

    engine_options = {}
    if database_url.startswith("sqlite"):
        engine_options["connect_args"] = {"check_same_thread": False}
    engine = create_engine(database_url, **engine_options)
    session_factory = sessionmaker(bind=engine)

    try:
        with session_factory() as db:
            slot = add_dev_slot(db, slot_date, args.package_code)
            print(
                f"Created test slot id={slot.id} date={slot.slot_date.isoformat()} "
                f"time={slot.start_time.isoformat()} package={slot.package_code} "
                f"remaining={slot.remaining}"
            )
    except ValueError as exc:
        parser.error(str(exc))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
