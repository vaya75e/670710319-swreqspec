# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md SPEC-BKG-001 Draft v2 | tasks.md | test-cases.md | plan.md
สร้างด้วย /verify เมื่อ 2569-10-07 | test: backend 6 passed, frontend 1 passed 1 failed

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | test_AC_BKG_05 ผ่าน | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | backend/app/booking/service.py: create_booking | ไม่มี test ของ AC-BKG-02 | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05 | backend/app/booking/router.py: create_booking; backend/app/booking/service.py: create_booking | ไม่มี test ของ AC-BKG-03 | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/router.py: create_booking; backend/app/booking/service.py: create_booking, next_queue_no | test_TC_BKG_01_1 ผ่าน; TC-BKG-01-2 ไม่ผ่านเพราะหน้าไม่มี | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มี implementation สำหรับ queue/retry | ไม่มี test ของ AC-BKG-04 | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-10 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | ไม่มี test สำหรับ package change | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | test_AC_BKG_05 ผ่าน | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มี implementation สำหรับ TLS 1.2 | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มี implementation สำหรับ retry | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี test สำหรับผู้ใช้ใหม่ 8/10 | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL; backend/app/db/session.py: engine | test_T01_schema ผ่านแต่ใช้ SQLite เป็น fixture | ช่องโหว่ |
| DOM-PDPA-01 | AC-BKG-06 | T-01, T-08 | backend/app/db/models.py: AuditLog; backend/app/db/migrations/001_init.py: upgrade | ไม่มี test ของ AC-BKG-06 | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 | T-03 | backend/app/auth/idp.py: get_verified_hn; backend/app/booking/router.py: create_booking | test_TC_BKG_01_3 ผ่าน | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | ไม่มี HIS client หรือ lookup | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ไม่มี notification queue หรือ asynchronous sending | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
1. แถวต่อ 1 endpoint หรือฟังก์ชันหลัก
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/router.py: get_slots | FR-BKG-01, FR-BKG-06 | ประมาณ 60% ตรง | คืนช่วงเวลาและ remaining แต่ระยะเวลา 14 วัน ไม่ตรง 30 วัน และไม่มี UI |
| backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ประมาณ 60% ตรง | ใช้ package_code และ remaining > 0 แต่ date window คือ 14 วัน ไม่ใช่ 30 วัน |
| backend/app/booking/router.py: create_booking | FR-BKG-04, IF-IDP-01 | ประมาณ 70% ตรง | ตรวจ identity, save booking, return queue_no, แต่ไม่ส่ง notification |
| backend/app/booking/service.py: create_booking | FR-BKG-04 | ประมาณ 70% ตรง | ตัด remaining อีกครั้งแล้วบันทึกอีกครั้ง แต่ไม่ตรวจ remaining == 0 และไม่มี duplicate guard |
| backend/app/booking/service.py: next_queue_no | FR-BKG-04, Q-02 | ไม่ตรงสมบูรณ์ | ใช้ A001 ใน code แต่ Q-02 ยังไม่ตอบรูปแบบหมายเลขคิว |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ตรง | ระบบตอบ 401 ถ้าขาดหรือไม่ใช่ Bearer verified: |
| backend/app/db/models.py: Slot, Booking, AuditLog | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | ประมาณ 70% ตรง | ตารางและ column ใส่ correct แต่ no national_id is complete; audit log only model, no write |
| backend/app/config.py: DATABASE_URL | CON-TECH-01 | ไม่ตรงสมบูรณ์ | default คือ SQLite โดยตรง แต่ constraint นี้กำหนด PostgreSQL |
| frontend/src/api/client.js: getSlots, createBooking | FR-BKG-01, FR-BKG-04 | ประมาณ 50% ตรง | API client exists แต่ไม่มี pages หรือ wiring to UI |
| frontend/src/__tests__/TC-BKG-01-2.test.jsx | FR-BKG-04 | ไม่ตรง | test imports missing BookingResult page |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| FR-BKG-01 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py | spec กำหนด 30 วัน | code ใช้ DAYS_AHEAD = 14 วัน |  |
| FR-BKG-02 | code lacks FR | backend/app/booking/service.py | AC-BKG-02, FR-BKG-02 | no duplicate booking guard for same day; no corresponding test |  |
| FR-BKG-03 | code lacks FR | backend/app/booking/service.py | AC-BKG-03, FR-BKG-03 | remaining == 0 still decrements to -1 and no near-slot alternatives |  |
| FR-BKG-04 | AC ไม่มี test | frontend/src/__tests__/TC-BKG-01-2.test.jsx | AC-BKG-01 | UI test cannot resolve BookingResult page; queue display not implemented |  |
| FR-BKG-04 | เดา Q-xx | backend/app/booking/service.py: next_queue_no | Q-02 | code chooses A001 despite Q-02 still unresolved |  |
| FR-BKG-05 | code lacks FR | backend/app | AC-BKG-04, FR-BKG-05 | no retry queue or notification failure handling |  |
| FR-BKG-06 | FR ไม่มี AC | backend/app/slots/service.py | spec requirement | API filters by package but no UI or AC verifies changing package |  |
| NFR-SEC-01 | ยังไม่ตรวจ | backend/app | spec constraint | no TLS 1.2 enforcement or test |  |
| NFR-REL-02 | code lacks FR | backend/app | AC-BKG-04 | no retry queue within 5 minutes |  |
| NFR-USE-01 | ไม่มี test | backend/tests / frontend/src/__tests__ | spec quality requirement | no 8 in 10 user test or 3-minute success test |  |
| CON-TECH-01 | ละเมิด Constraint | backend/app/config.py | spec constraint | default database is SQLite, not PostgreSQL |  |
| DOM-PDPA-01 | code lacks FR | backend/app | AC-BKG-06 | AuditLog model exists but no middleware writes audit log |  |
| IF-HIS-01 | code lacks FR | backend/app | IF-HIS-01 | no HIS lookup or national ID validation; request national_id is unused |  |
| IF-NOT-01 | code lacks FR | backend/app | IF-NOT-01 | no asynchronous notification request queue |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| NFR-PERF-01 | test_AC_BKG_05 ผ่าน | 200 requests, p95 <= 2.0 seconds |
| IF-IDP-01 | test_TC_BKG_01_3 ผ่าน | 401, no booking, remaining unchanged |
| FR-BKG-04 (backend part) | test_TC_BKG_01_1 ผ่าน | 201, booking record, remaining 0 |
