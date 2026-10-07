from __future__ import annotations

from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.db.models import AuditLog


# รองรับ: DOM-PDPA-01
class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, db_session_factory: Callable | None = None):
        super().__init__(app)
        self.db_session_factory = db_session_factory

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if not self.db_session_factory:
            return response

        if request.url.path.startswith("/bookings"):
            actor_id = request.headers.get("X-Actor-Id") or "system"
            payload = getattr(request, "state", None)
            booking_hn = None
            if payload is not None:
                booking_hn = getattr(payload, "hn", None)
            if not booking_hn and request.method == "POST":
                try:
                    booking_hn = (await request.json()).get("hn")
                except Exception:
                    booking_hn = None

            if booking_hn:
                db = self.db_session_factory()
                try:
                    db.add(
                        AuditLog(
                            actor_id=actor_id,
                            action="booking_access",
                            hn=booking_hn,
                        )
                    )
                    db.commit()
                finally:
                    db.close()

        return response
