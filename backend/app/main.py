from fastapi import FastAPI

from app.booking.router import router as booking_router
from app.slots.router import router as slots_router


# รองรับ: FR-BKG-01, IF-IDP-01
app = FastAPI(title="Booking API")
app.include_router(slots_router)
app.include_router(booking_router)
