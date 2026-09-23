from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.auth.idp import is_identity_verified
from app.db.session import SessionLocal
from app.slots.service import get_slots_for_period


# รองรับ: FR-BKG-01, FR-BKG-06, IF-IDP-01
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/slots")
def list_slots(
    request: Request,
    date_from: date = Query(...),
    package_code: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    headers = dict(request.headers)
    if not is_identity_verified(headers):
        raise HTTPException(status_code=401, detail="Identity not verified")

    slots = get_slots_for_period(db, date_from, package_code)
    return {"slots": slots}
