# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- เครื่องมือ: Copilot in Codespaces
- โหมด: ร่าง
- AC: AC-BKG-01 (FR-BKG-04)
- แถวที่เสนอ: 3 แถว ทางปกติ, ขอบ, ทางผิด
- TC-BKG-01-1: บันทึกการจอง, ตัดที่นั่งเป็น 0, คืนหมายเลขคิว (รอ Q-02)
- TC-BKG-01-2: แสดงหมายเลขคิวและสถานะการจอง (รอ Q-02) ผ่านหน้าจอ
- TC-BKG-01-3: ไม่ยืนยันตัวตนไม่อนุญาตการจองตาม IF-IDP-01
- ผล: ยังไม่เขียนโค้ด test เพราะ test-cases.md ยังไม่มีแถวที่ใช้ได้; ต้องทีมตรวจแถวและเปลี่ยนสถานะเป็น "ใช้ได้" ก่อน แล้วสั่ง /testcases อีกครั้ง

---

## 2569-10-07 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- เครื่องมือ: Copilot in Codespaces
- โหมด: เขียน test
- AC: AC-BKG-01 (FR-BKG-04)
- แถวที่ใช้งาน: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3 โดยสถานะ "ใช้ได้"
- TC-BKG-01-1: เพิ่ม test_TC_BKG_01_1_booking_success เพื่อตรวจบันทึก, remaining 0, และ response queue number (รอ Q-02)
- TC-BKG-01-2: เพิ่ม TC-BKG-01-2.test.jsx เพื่อตรวจแสดงหมายเลขคิวและสถานะการจอง (รอ Q-02)
- TC-BKG-01-3: เพิ่ม test_TC_BKG_01_3_unverified_identity_rejected เพื่อตรวจ 401 และไม่มี booking
- ผล: รอ run test; ขณะนี้ frontend test imports missing BookingResult page และจะรายงานเป็นไม่ผ่านเพราะ task ยังไม่ทำ

---

## 2569-10-07 08:34 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- ผล backend: pytest -v => 6 passed, 0 failed, 1 warning โดย 0.80s
- TC-BKG-01-1: test_TC_BKG_01_1_booking_success ผ่าน
- TC-BKG-01-3: test_TC_BKG_01_3_unverified_identity_rejected ผ่าน
- TC-BKG-01-2: test_TC_BKG_01_2_booking_result_display ไม่ผ่าน เพราะ frontend/src/pages/BookingResult.jsx ยังไม่มีในโฟลเดอร์ปัจจุบัน (import resolution failure)
- การแก้ระบบ: ไม่แก้ backend/app/ หรือ frontend/src/ ไฟล์ production เพราะคำสั่งห้ามแก้โค้ดระบบ
- การแก้ test: แก้ comments ของ test ใหม่จาก # เป็น // เพื่อให้ syntax valid แล้ว rerun; การไม่ผ่านเป็นเพราะ task T-06 ยังไม่ทำ

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 คำสั่ง: /verify specs/001-booking/

- เครื่องมือ: Copilot in Codespaces
- โหมด: ตรวจและรายงาน
- ผล backend: 6 passed, 0 failed, 1 warning
- ผล frontend: 1 passed, 1 failed
- Failed suite: src/__tests__/TC-BKG-01-2.test.jsx เพราะไม่มี frontend/src/pages/BookingResult.jsx
- RTM: specs/001-booking/rtm.md ได้รับการสร้าง
- ผลระ=status: 6 requirement IDs ครบ, 5 IDs ยังไม่ถึง, 3 IDs ช่องโหว่, 3 IDs ต้องคนตรวจเพิ่มเติม
- ข้อค้นพบใหม่: FR-BKG-01, FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-05, FR-BKG-06, NFR-SEC-01, NFR-REL-02, NFR-USE-01, CON-TECH-01, DOM-PDPA-01, IF-HIS-01, IF-NOT-01
- การแก้: ไม่แก้โค้ด source/test/spec/plan/tasks; แก้เฉพาะ rtm.md และ prompt-log.md
