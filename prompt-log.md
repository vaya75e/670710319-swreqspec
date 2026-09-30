# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2026-09-16 08:13 คำสั่ง: /clarify

- เครื่องมือ: Copilot in Codespaces
- ไฟล์: specs/001-booking/spec.md (v1)

### คำถามที่ AI ถาม (ทั้งหมด)

1. การปฏิเสธการจองเมื่อมีคิวค้างในวันเดียวกันควรปฏิเสธเฉพาะผู้รับบริการคนเดิมตาม HN หรือปฏิเสธทุกการจองในวันนั้น?
2. “ช่วงเวลาใกล้เคียง 3 ตัวเลือก” ควรคำนวณจากช่วงเวลาใกล้ที่สุดในวันเดียวกันหรือสามารถข้ามวันได้?
3. ใน audit log ควรใช้ HN หรือรหัสภายในระบบเป็น “รหัสผู้รับบริการ” ?
4. จำนวนที่นั่งคงเหลือควรคำนวณจากโควตาของแพ็กเกจหรือโควตาของช่วงเวลาโดยรวม?
5. “ยืนยันภายใน 3 นาที” เริ่มนับเมื่อไรในกระบวนการจอง?
6. “ข้อความไม่สำเร็จ” หมายถึงกรณีใด และ retry ควรเริ่มภายในกี่นาที?
7. โควตาที่นั่งต่อช่วงเวลาควรยึดจากข้อมูลที่มีอยู่หรือคำนวณจากการจองจริงทันที?
8. “ยังไม่ได้ใช้” หมายถึงคิวที่ยังไม่ถึงเวลาเข้าตรวจหรือรวมถึงคิวที่ไม่ผ่านการตรวจด้วย?

### คำตอบของทีมและเหตุผล

1. ยังไม่มีคำตอบจากทีม จึงยังไม่สามารถปิด Open Questions ได้
2. ตอบไม่ได้ ย้ายไป Open Questions (ต้องถามทีม product / ทีม A / เจ้าหน้าที่เวชระเบียน)

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- ยังไม่ได้แก้ spec.md เนื่องจากยังรอคำตอบจากทีมเพื่อยืนยันข้อกำกวมก่อนปรับ Draft v2

---

## 2026-09-23 09:30 คำสั่ง: /tasks

- เครื่องมือ: Copilot in Codespaces
- ไฟล์: specs/001-booking/tasks.md
- ผลลัพธ์: สร้างไฟล์ tasks.md ในโฟลเดอร์ spec ของ feature นี้ โดยเรียง task ตาม dependency และเชื่อมกลับไปยัง FR / AC / Constraint ใน spec
- รายงานสรุป: ทำทั้งหมด 11 task, มี 1 task ที่รอ Q-02 (T-11) และทุก AC ใน spec ถูกครอบคลุมอย่างน้อย 1 task โดยมีตารางตรวจความครบ AC และ Constraint ท้ายไฟล์
- ข้อสังเกต: task ที่รอคำตอบจาก Open Question เป็น T-11 เนื่องจาก Q-02 ว่าด้วยรูปแบบหมายเลขคิวที่ยังไม่เคยได้รับคำตอบจากเจ้าหน้าที่เวชระเบียน

---

## 2026-09-23 09:41 คำสั่ง: /implement T-01

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_db_schema.py
- ผล test: `cd backend && pytest tests/test_db_schema.py -q` -> 1 passed in 0.47s
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เพราะ task นี้ไม่ติด Open Question และระบุไฟล์/เงื่อนไขชัดเจนจาก spec + plan
- ผลลัพธ์: สร้าง schema ฐานข้อมูลเริ่มต้นสำหรับ slots, bookings, audit_logs ตาม CON-TECH-01, DOM-PDPA-01 และ IF-HIS-01 โดย bookings เก็บเฉพาะ hn และไม่มี national_id

---

## 2026-09-23 09:52 คำสั่ง: /implement T-02

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/auth/idp.py, backend/tests/test_slots.py
- ผล test: `cd backend && pytest tests/test_slots.py -q` -> 1 passed, 1 warning in 0.85s
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เพราะ task นี้มี spec/plan ครอบคลุมและไม่มี Open Question ที่บล็อก
- ผลลัพธ์: สร้าง API GET /slots ที่ตรวจยืนยันตัวตนก่อน, กรองช่วงเวลา 30 วัน และคืนข้อมูลที่นั่งคงเหลือพร้อม package_code ตาม FR-BKG-01, FR-BKG-06 และ IF-IDP-01

---

## 2026-09-30 15:20 คำสั่ง: /implement T-03

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/booking/router.py, backend/app/booking/service.py, backend/tests/test_booking_create.py
- ผล test: `cd backend && pytest tests/test_booking_create.py -q` -> 1 passed in 0.73s
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เพราะ task นี้มี spec/plan ครอบคลุมและยังไม่มี Open Question ที่บล็อกงาน
- ผลลัพธ์: สร้าง POST /bookings ที่ตรวจ identity ก่อน, บันทึก Booking, ลด remaining ของ slot ลง 1, และส่งกลับ queue_no ที่มีค่าจากระบบตาม FR-BKG-04 และ IF-IDP-01

---

## 2026-09-30 15:40 คำสั่ง: /implement T-04

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/booking/service.py, backend/tests/test_booking_duplicate.py
- ผล test: `cd backend && pytest tests/test_booking_create.py tests/test_booking_duplicate.py -q` -> 2 passed in 0.68s
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เพราะ task นี้มีข้อกำหนดชัดเจนจาก FR-BKG-02 และ AC-BKG-02 ว่า “มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ต้องปฏิเสธและส่งกลับหมายเลขคิวเดิม”
- ผลลัพธ์: เพิ่มตรวจสอบการจองซ้ำในวันเดียวกันที่ service layer เพื่อคืน booking เดิมและป้องกันการสร้างคิวใหม่สำหรับผู้รับบริการคนเดิมในวันเดียวกันตาม FR-BKG-02

---

## 2026-09-16 08:17 คำสั่ง: /plan

- เครื่องมือ: Copilot in Codespaces
- ผลลัพธ์: specs/001-booking/plan.md
- Constraint ที่ AI ยังไม่ได้ใช้: ทุก Constraint ใน spec ได้ถูกนำไปใช้ในแผนแล้ว แต่มีรายละเอียดเชิงธุรกิจบางประเด็นที่ยังต้องรอคำตอบจากทีมก่อนปิด Open Questions อย่างสมบูรณ์
- สิ่งที่ AI บอกว่าอยากเดาแต่ไม่ได้เดา: กติกาการปฏิเสธการจองซ้ำในวันเดียวกัน, การคำนวณ 3 ตัวเลือกที่ใกล้ที่สุด, การกำหนด HN เป็นรหัสผู้รับบริการใน audit log, และเงื่อนไข retry ของข้อความแจ้งเตือน

---

## 2026-09-30 คำสั่ง: commit

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่ตรวจและเตรียม commit: frontend/src/__tests__/SlotPicker.test.jsx, specs/001-booking/tasks.md, prompt-log.md
- ผล test: `cd frontend && npm test -- src/__tests__/SlotPicker.test.jsx` -> 3 passed
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เป็นการ commit การเปลี่ยนแปลงที่มีอยู่ใน working tree ตามคำสั่งของทีม
- ผลลัพธ์: เพิ่ม test การจองสำเร็จและการปฏิเสธการจองซ้ำ พร้อมระบุ T-04 ว่าเสร็จรอทีมตรวจ ตาม FR-BKG-02 และ AC-BKG-02
