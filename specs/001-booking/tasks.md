# Tasks: จองคิวตรวจสุขภาพ (Booking)
- Feature: จองคิวตรวจสุขภาพ
- Spec ID: SPEC-BKG-001
- อ้างอิง plan.md: specs/001-booking/plan.md
- วันที่: 2569-09-23

## สรุป
- ทำทั้งหมด: 11 task
- รอ Open Questions: 1 task (Q-02)

### T-01 สร้างโครงข้อมูลและ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง slots, bookings และ audit_logs ใน PostgreSQL และ bookings เก็บเฉพาะ hn ไม่เก็บ national_id
- สถานะ: พร้อมทำ

### T-02 สร้าง API ดึงช่วงว่างและคำนวณที่นั่งคงเหลือ
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01, IF-IDP-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/auth/idp.py, backend/tests/test_slots.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots คืนข้อมูลช่วงเวลาว่าง 30 วันข้างหน้า พร้อมที่นั่งคงเหลือและสามารถคำนวณใหม่เมื่อเปลี่ยนแพ็กเกจได้
- สถานะ: พร้อมทำ

### T-03 สร้างการจองพื้นฐานและตัดจำนวนที่นั่ง
- รองรับ: FR-BKG-04, IF-IDP-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/tests/test_booking_create.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: POST /bookings บันทึกการจองได้สำเร็จ ตัด remaining ของ slot ลง 1 และส่งกลับข้อมูล booking พร้อมหมายเลขคิวที่มีค่าจากระบบ
- สถานะ: พร้อมทำ

### T-04 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/tests/test_booking_duplicate.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบปฏิเสธการจองใหม่และส่งกลับ booking เดิม พร้อมหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-05 จัดการช่วงเวลาเต็มและเสนอ 3 ตัวเลือกที่ใกล้ที่สุด
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py, backend/tests/test_booking_full_slot.py
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: เมื่อ slot ที่เลือกเต็มระหว่างยืนยัน ระบบส่ง 409 พร้อม 3 ช่วงที่ว่างใกล้สุดภายในวันเดียวกันและวันถัดไป และไม่สร้างการจองซ้อน
- สถานะ: พร้อมทำ

### T-06 สร้างคิวส่งข้อความยืนยันและระบบส่งซ้ำ
- รองรับ: FR-BKG-05, NFR-REL-02, IF-NOT-01
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/tests/test_notification_retry.py
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: การจองยังบันทึกได้ แม้ส่งข้อความยืนยันไม่สำเร็จ และมีรายการค้างส่งที่กำหนดให้ retry ภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-07 บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/db/models.py, backend/tests/test_audit_log.py
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ทุก request ที่เข้าถึงข้อมูลการจองบันทึก actor_id, accessed_at, hn และมีข้อมูลเพียงพอให้ตรวจสอบการเข้าถึงใน 1 ปี
- สถานะ: พร้อมทำ

### T-08 เชื่อมต่อกับ HIS เพื่อค้น HN จากเลขบัตรประชาชน
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/booking/service.py, backend/tests/test_his_lookup.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบค้นข้อมูลผู้รับบริการจาก HIS ด้วยเลขบัตร และเก็บเฉพาะ HN ในตารางการจอง โดยไม่เก็บเลขบัตรประชาชนในฐานข้อมูล
- สถานะ: พร้อมทำ

### T-09 สร้างหน้าจอเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/__tests__/SlotPicker.test.jsx
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอแสดงแพ็กเกจ วัน และช่วงเวลาที่ว่าง พร้อมจำนวนที่นั่งคงเหลือ และโหลดช่วงเวลาใหม่เมื่อเปลี่ยนแพ็กเกจ
- สถานะ: พร้อมทำ

### T-10 สร้างหน้้ายืนยันและแสดง 3 ตัวเลือกเมื่อช่วงเวลาเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/App.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-09, T-05
- เสร็จเมื่อ: เมื่อ API ตอบ 409 พร้อม 3 ช่วงที่ใกล้ที่สุด หน้าจอแสดงข้อความ “ช่วงเวลาเต็ม” และมี 3 ปุ่ม/ตัวเลือกให้ผู้ใช้เลือกใหม่
- สถานะ: พร้อมทำ

### T-11 สร้างหน้าผลลัพธ์การจองและรอคำตอบ Q-02
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/src/App.jsx, frontend/src/__tests__/BookingResult.test.jsx
- ต้องทำหลัง: T-03, T-06, T-10
- เสร็จเมื่อ: หน้าจอแสดงหมายเลขคิวและข้อความยืนยันได้อย่างถูกต้องเมื่อรูปแบบเลขคิวได้รับคำตอบจาก Q-02
- สถานะ: รอ Q-02

## ตารางตรวจความครบ AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-10 |
| AC-BKG-04 | T-06 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-07 |

## ตารางตรวจความครบ Constraint
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | T-02, T-03 |
| IF-HIS-01 | T-01, T-08 |
| IF-NOT-01 | T-06 |

## สิ่งที่ยังไม่ทำ
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)?
  -> ถามเจ้าหน้าที่เวชระเบียน (ยังไม่ได้คำตอบ)
  -> รอ task: T-11
