from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Slot(Base):
    # รองรับ: CON-TECH-01, FR-BKG-01, FR-BKG-06, ASM-01
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slot_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    package_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    remaining: Mapped[int] = mapped_column(Integer, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="slot")


class Booking(Base):
    # รองรับ: FR-BKG-02, FR-BKG-04, IF-HIS-01
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), nullable=False, index=True)
    booking_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    queue_no: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="confirmed")
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    slot: Mapped[Slot] = relationship(back_populates="bookings")


class AuditLog(Base):
    # รองรับ: DOM-PDPA-01
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    actor_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    accessed_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
