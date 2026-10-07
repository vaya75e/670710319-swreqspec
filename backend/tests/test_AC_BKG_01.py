# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH

# Given / When / Then
from app.db.models import Booking


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_booking_success(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    response = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกการจองสำเร็จ ตัดที่นั่งของช่วงนั้นเป็น 0 และคืนหมายเลขคิว (รอ Q-02)
    assert response.status_code == 201
    assert response.json()["booking_id"] is not None
    # รอ Q-02: รูปแบบหมายเลขคิวยังไม่ได้ตัดสิน ไม่สวมถ่วง assert
    assert slot.remaining == 0
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1


def test_TC_BKG_01_3_unverified_identity_rejected(client, db, make_slot):
    # Given: ยังไม่ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    response = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ไม่บันทึกการจอง และไม่ยอมรับ request ตาม IF-IDP-01
    assert response.status_code == 401
    assert response.json()["detail"] == "ยังไม่ได้ยืนยันตัวตน"
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 0
    assert slot.remaining == 1
