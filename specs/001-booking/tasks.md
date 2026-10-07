# Tasks: จองคิวตรวจสุขภาพ (Booking)
- Feature: จองคิวตรวจสุขภาพ
- Spec ID: SPEC-BKG-001
- อ้างอิง plan.md: specs/001-booking/plan.md
- วันที่: 2569-09-23

## สรุป
- ทำทั้งหมด: 14 task
- รอ Open Questions: 0 task

### T-01 สร้างโครงข้อมูลและ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง slots, bookings และ audit_logs ใน PostgreSQL และ bookings เก็บเฉพาะ hn ไม่เก็บ national_id
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้าง API ดึงช่วงว่างและคำนวณที่นั่งคงเหลือ
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01, IF-IDP-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/auth/idp.py, backend/tests/test_slots.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots คืนข้อมูลช่วงเวลาว่าง 30 วันข้างหน้า พร้อมที่นั่งคงเหลือและสามารถคำนวณใหม่เมื่อเปลี่ยนแพ็กเกจได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 สร้างการจองพื้นฐานและตัดจำนวนที่นั่ง
- รองรับ: FR-BKG-04, IF-IDP-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/tests/test_booking_create.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: POST /bookings บันทึกการจองได้สำเร็จ ตัด remaining ของ slot ลง 1 และส่งกลับข้อมูล booking พร้อมหมายเลขคิวที่มีค่าจากระบบ
- สถานะ: เสร็จ รอทีมตรวจ

### T-04 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/tests/test_booking_duplicate.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบปฏิเสธการจองใหม่และส่งกลับ booking เดิม พร้อมหมายเลขคิวเดิม
- สถานะ: เสร็จ รอทีมตรวจ

### T-05 จัดการช่วงเวลาเต็มและเสนอ 3 ตัวเลือกที่ใกล้ที่สุด
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py, backend/tests/test_booking_full_slot.py
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: เมื่อ slot ที่เลือกเต็มระหว่างยืนยัน ระบบส่ง 409 พร้อม 3 ช่วงที่ว่างใกล้สุดภายในวันเดียวกันและวันถัดไป และไม่สร้างการจองซ้อน
- สถานะ: เสร็จ รอทีมตรวจ

### T-06 สร้างคิวส่งข้อความยืนยันและระบบส่งซ้ำ
- รองรับ: FR-BKG-05, NFR-REL-02, IF-NOT-01
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/tests/test_notification_retry.py, backend/requirements.txt
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: การจองยังบันทึกได้ แม้ส่งข้อความยืนยันไม่สำเร็จ และมีรายการค้างส่งที่กำหนดให้ retry ภายใน 5 นาที
- สถานะ: เสร็จ รอทีมตรวจ

### T-07 บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/db/models.py, backend/tests/test_audit_log.py
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ทุก request ที่เข้าถึงข้อมูลการจองบันทึก actor_id, accessed_at, hn และมีข้อมูลเพียงพอให้ตรวจสอบการเข้าถึงใน 1 ปี
- สถานะ: เสร็จ รอทีมตรวจ

### T-08 เชื่อมต่อกับ HIS เพื่อค้น HN จากเลขบัตรประชาชน
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/booking/service.py, backend/tests/test_his_lookup.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบค้นข้อมูลผู้รับบริการจาก HIS ด้วยเลขบัตร และเก็บเฉพาะ HN ในตารางการจอง โดยไม่เก็บเลขบัตรประชาชนในฐานข้อมูล
- สถานะ: เสร็จ รอทีมตรวจ

### T-09 สร้างหน้าจอเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/__tests__/SlotPicker.test.jsx
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอแสดงแพ็กเกจ วัน และช่วงเวลาที่ API คืนมาพร้อมจำนวนที่นั่งคงเหลือ ใช้ slot id จากผล API เมื่อเลือก และแสดงสถานะไม่มีช่วงเวลาว่างเมื่อรายการเป็นค่าว่าง
- สถานะ: เสร็จ รอทีมตรวจ

### T-10 สร้างหน้้ายืนยันและแสดง 3 ตัวเลือกเมื่อช่วงเวลาเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/App.jsx, frontend/src/pages/SlotPicker.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-09, T-05
- เสร็จเมื่อ: เมื่อ API ตอบ 409 พร้อม 3 ช่วงที่ใกล้ที่สุด หน้าจอแสดงข้อความ “ช่วงเวลาเต็ม” และมี 3 ปุ่ม/ตัวเลือกให้ผู้ใช้เลือกใหม่
- สถานะ: เสร็จ รอทีมตรวจ

### T-11 แสดงผลการจองและหมายเลขคิว
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/src/App.jsx, frontend/src/__tests__/BookingResult.test.jsx
- ต้องทำหลัง: T-03, T-06, T-10, T-14
- เสร็จเมื่อ: หน้าจอแสดงหมายเลขคิวตามค่าที่ API ส่งกลับโดยไม่เปลี่ยนรูปแบบ และแสดงสถานะการจองได้แม้ส่งข้อความยืนยันไม่สำเร็จ
- สถานะ: เสร็จ รอทีมตรวจ

### T-12 เตรียมข้อมูลช่วงเวลาสำหรับทดสอบเว็บ
- รองรับ: FR-BKG-01, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-12
- ไฟล์ที่แตะ: backend/scripts/seed_dev_slots.py, backend/tests/test_seed_dev_slots.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ผู้ทดสอบระบุ package_code และวันที่ภายใน 30 วันเพื่อเพิ่ม slot ทดสอบ 09.00 น. ที่เหลือ 1 ที่ลงฐานข้อมูล dev/test ที่กำหนด และเรียก GET /slots แล้วพบ slot นั้นได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-13 ทดสอบการจองผ่านเว็บกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-04
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/pages/SlotPicker.jsx, frontend/src/pages/ConfirmBooking.jsx, frontend/src/pages/BookingResult.jsx, frontend/src/__tests__/AC-BKG-01.test.jsx
- ต้องทำหลัง: T-03, T-09, T-10, T-11, T-12, T-14
- เสร็จเมื่อ: ในเว็บเลือก slot id ที่ได้จาก GET /slots แล้วยืนยันการจองสำเร็จ แสดงผลที่ได้จาก API และตรวจได้ว่า remaining ของ slot ลดจาก 1 เป็น 0
- สถานะ: เสร็จ รอทีมตรวจ

### T-14 ปรับการออกหมายเลขคิวตามคำตอบ Q-02
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/tests/test_booking_create.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: หมายเลขคิวเริ่ม `01` ใหม่ตาม `slot_date` ใช้ลำดับเดียวกันทุกแพ็กเกจ ไม่มี prefix แสดงอย่างน้อย 2 หลัก และใช้ `100` ขึ้นไปหลัง `99`; test ยืนยันการใช้ลำดับร่วมกันและการเริ่มใหม่ในวันตรวจถัดไป
- สถานะ: เสร็จ รอทีมตรวจ

## ตารางตรวจความครบ AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03, T-13, T-14 |
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
- ไม่มี Open Questions ที่ยังรอคำตอบสำหรับ feature นี้
- Q-02 ปิดแล้ว: รีเซ็ตตามวันตรวจ (`slot_date`), ใช้ลำดับร่วมกันทุกแพ็กเกจ, ไม่มี prefix, เริ่ม `01` และหลัง `99` ต่อเป็น `100` ขึ้นไป
