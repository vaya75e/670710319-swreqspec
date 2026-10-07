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

---

## 2026-09-30 คำสั่ง: แก้หน้าเว็บให้ส่งคำขอจองได้จริง

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/main.py, backend/tests/test_booking_create.py, frontend/src/api/client.js, frontend/src/pages/SlotPicker.jsx, frontend/src/__tests__/SlotPicker.test.jsx
- ผล test: backend `pytest tests/test_booking_create.py tests/test_booking_duplicate.py -q` -> 2 passed; frontend `npm test -- src/__tests__/SlotPicker.test.jsx` -> 5 passed
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี; spec ระบุการยืนยันตัวตนก่อนเข้าถึงข้อมูล (IF-IDP-01) และการจองสำเร็จ (FR-BKG-04) ชัดเจน
- ผลลัพธ์: พบและแก้การไม่ลงทะเบียน POST /bookings ใน app จริง และเพิ่ม verified identity header ตอนโหลด slots; UI แสดง error และปลดปุ่มเมื่อ request จองล้มเหลว

---

## 2026-09-30 คำสั่ง: จัดการข้อผิดพลาดเมื่อโหลดช่วงเวลาไม่ได้

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่แก้: frontend/src/pages/SlotPicker.jsx, frontend/src/__tests__/setup.test.jsx
- ผล test: `cd frontend && npm test` -> 6 passed; `npm run build` -> สำเร็จ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เป็นการแสดงข้อผิดพลาดเมื่อ API ที่กำหนดในหน้าเว็บติดต่อไม่ได้
- ผลลัพธ์: UI แสดงข้อความเมื่อโหลด slots ล้มเหลว และไม่มี unhandled rejection ในการเปิดหน้าโดย backend ไม่พร้อม

---

## 2026-09-30 คำสั่ง: ปรับ Plan และ Tasks เพื่อให้ทดสอบการจองผ่านเว็บได้

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่แก้: specs/001-booking/plan.md, specs/001-booking/tasks.md
- ผลลัพธ์: ระบุการเตรียม slot สำหรับ dev/test โดยไม่เพิ่มการจัดการตารางคิวในระบบจริง เพิ่ม T-12 สำหรับ seed ข้อมูลทดสอบที่รับ package_code และวันที่จากผู้ทดสอบ และเพิ่ม T-13 สำหรับทดสอบ flow ผ่านเว็บกับ API จริง
- การเปลี่ยน task: ปรับเกณฑ์เสร็จของ T-09 ให้ใช้ slot id จาก API และรองรับรายการว่าง; ปรับจำนวนเป็น 13 tasks โดย T-12 พร้อมทำและ T-13 รอ Q-02
- สิ่งที่ไม่ได้เดา: ไม่กำหนด package_code ตัวอย่างแทนทีม และไม่แก้ spec หรือสร้าง requirement ID ใหม่
- ผล test: ไม่ได้รัน เนื่องจากรอบนี้แก้เอกสารเท่านั้น

---

## 2026-09-30 คำสั่ง: /implement T-12

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/scripts/seed_dev_slots.py, backend/tests/test_seed_dev_slots.py
- ผล test: `cd backend && pytest tests/test_seed_dev_slots.py -q` -> 2 passed, 1 warning; smoke test `python -m scripts.seed_dev_slots --date 2026-09-30 --package-code STD` กับ SQLite file database -> สร้าง slot id=1 เวลา 09:00 และ remaining=1
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่กำหนด package_code เริ่มต้น; ต้องระบุ `--package-code` และ `--date` ทุกครั้ง โดย STD เป็นค่าที่ส่งให้ใน test/คำสั่ง smoke test เท่านั้น
- ผลลัพธ์: เพิ่มเครื่องมือ seed slot สำหรับฐานข้อมูล dev/test แบบ persistent โดยไม่ seed อัตโนมัติ และทดสอบว่า GET /slots ค้นพบ slot ที่เพิ่มได้

---

## 2026-09-30 คำสั่ง: /implement T-09

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/__tests__/SlotPicker.test.jsx
- ผล test: `cd frontend && npm test -- src/__tests__/SlotPicker.test.jsx src/__tests__/setup.test.jsx` -> 3 passed; `npm run build` -> สำเร็จ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่สร้างรายการ package code เอง; หน้าจออ่านตัวเลือกจากผล GET /slots และใช้ slot id ที่ API คืนมา
- ผลลัพธ์: เพิ่มหน้าเลือกแพ็กเกจ วัน และช่วงเวลาว่าง โดยโหลดใหม่เมื่อเปลี่ยนแพ็กเกจ กรอง slot เต็มออก และแสดงสถานะเมื่อไม่มีช่วงว่าง ตาม FR-BKG-01 และ FR-BKG-06

---

## 2026-09-30 คำสั่ง: /implement T-05

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/slots/service.py, backend/app/booking/service.py, backend/app/booking/router.py, backend/tests/test_booking_full_slot.py
- ผล test: `cd backend && pytest tests/test_booking_full_slot.py tests/test_booking_create.py tests/test_booking_duplicate.py -q` -> 3 passed, 6 warnings
- คำตอบทีมก่อน implement: จัดอันดับด้วยความต่างของเวลาบนนาฬิกา ไม่คิดข้ามวัน; ถ้าระยะเท่ากันให้วันปัจจุบันมาก่อน; ตัวเลือกต้องเป็น package_code เดียวกับ slot ที่เต็ม
- ขอบเขตไฟล์: เพิ่ม `backend/app/booking/router.py` จากรายการเดิมของ T-05 โดยได้รับอนุญาตจากทีม เพราะ router ต้องแปลงผลเป็น HTTP 409 พร้อมรายการ alternatives
- ผลลัพธ์: เมื่อ slot เต็ม API คืน 409 พร้อมสูงสุด 3 slot ว่างที่ใกล้ที่สุดในแพ็กเกจเดิมภายในวันเดียวกัน/วันถัดไป และไม่สร้าง booking เพิ่ม

---

## 2026-09-30 คำสั่ง: /implement T-10

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: frontend/src/pages/ConfirmBooking.jsx, frontend/src/App.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx, frontend/src/pages/SlotPicker.jsx
- ผล test: `cd frontend && npm test` -> 4 passed; `npm run build` -> สำเร็จ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: คงการแสดงหมายเลขคิวไว้กับ T-11 ซึ่งรอ Q-02; หน้าจอ T-10 แสดงเพียงสถานะบันทึกสำเร็จและไม่กำหนดรูปแบบคิว
- ขอบเขตไฟล์: เพิ่ม `frontend/src/pages/SlotPicker.jsx` จากรายการเดิมของ T-10 โดยได้รับอนุญาตจากทีม เพื่อส่ง slot id ที่เลือกเข้า App และ POST /bookings
- ผลลัพธ์: เพิ่มปุ่มยืนยันที่ส่ง slot id จาก API; เมื่อ API ตอบ 409 จะแสดง "ช่วงเวลาเต็ม" และตัวเลือก 3 ช่วงตาม AC-BKG-03

---

## 2026-09-30 คำสั่ง: ปิด Q-02

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่แก้: specs/001-booking/spec.md, specs/001-booking/plan.md, specs/001-booking/tasks.md
- คำตอบของทีม: หมายเลขคิวรีเซ็ตตามวันตรวจ (`slot_date`), ใช้ลำดับร่วมกันทุกแพ็กเกจ, ไม่มี prefix, เริ่ม `01` และแสดงอย่างน้อยสองหลัก; หลัง `99` ต่อเป็น `100` ขึ้นไป
- ผลลัพธ์: ปรับ spec เป็น Draft v3 โดยคง FR-BKG-04 เดิม, ปรับ plan ให้สะท้อนกติกา, เอาสถานะรอ Q-02 ออกจาก T-11/T-13 และเพิ่ม T-14 เพื่อแก้ implementation ที่ปัจจุบันสร้าง `Q-{booking.id:04d}` ซึ่งไม่ตรงกับคำตัดสินใหม่
- สิ่งที่ไม่ได้ทำ: ไม่แก้โค้ดหรือรันทดสอบในรอบปิดคำถามนี้; การแก้หมายเลขคิวถูกแยกเป็น T-14

---

## 2026-09-30 คำสั่ง: /implement T-14

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/booking/service.py, backend/tests/test_booking_create.py
- ผล test: `cd backend && pytest tests/test_booking_create.py tests/test_booking_duplicate.py tests/test_booking_full_slot.py -q` -> 5 passed, 113 warnings
- ผลยืนยัน: คิวแรกเป็น `01`, ลำดับใช้ร่วมกันข้าม package_code และรีเซ็ตตาม `slot_date`; หลัง 99 ออก `100` โดยไม่ตัดหลัก
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี; วันที่รีเซ็ต, ขอบเขตแพ็กเกจ, prefix และ overflow ถูกระบุในคำตอบทีมต่อ Q-02
- ผลลัพธ์: เปลี่ยนการออก queue_no จาก booking ID แบบ `Q-0001` เป็นลำดับตามวันตรวจตาม FR-BKG-04

---

## 2026-09-30 คำสั่ง: /implement T-06

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/notify/queue.py, backend/app/booking/service.py, backend/tests/test_notification_retry.py, backend/requirements.txt
- ผล test: `cd backend && pytest tests/test_notification_retry.py tests/test_booking_create.py tests/test_booking_duplicate.py tests/test_booking_full_slot.py -q` -> 7 passed, 115 warnings
- ผลลัพธ์: หลัง commit การจอง วาง notification เข้า Redis เมื่อกำหนด `REDIS_URL`; ใน test/dev ที่ไม่มี `REDIS_URL` ใช้คิวในหน่วยความจำตาม Plan; เมื่อ sender ล้มเหลว กำหนด retry ทุก 5 นาทีสูงสุด 3 ครั้ง แล้วส่งไป pending
- ขอบเขตไฟล์: เพิ่ม `backend/requirements.txt` จากรายการเดิมของ T-06 โดยได้รับอนุญาตจากทีม; เพิ่ม `redis>=5.0` และติดตั้ง Redis client เพื่อรันทดสอบ
- ข้อสังเกต: ไม่ได้ระบุผู้ให้บริการ SMS/LINE จริง เนื่องจากไม่มี endpoint หรือ credential ใน plan; worker รับ sender callback เพื่อเชื่อม provider ตามสัญญาที่ทีมกำหนดภายหลัง

---

## 2026-09-30 คำสั่ง: /implement T-11

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: frontend/src/pages/BookingResult.jsx, frontend/src/App.jsx, frontend/src/__tests__/BookingResult.test.jsx
- ผล test: `cd frontend && npm test` -> 5 passed; `npm run build` -> สำเร็จ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่แปลงหรือจัดรูปแบบ `queue_no`; หน้าจอแสดงค่าจาก API ตาม FR-BKG-04 และแสดงผลการจองจาก response ที่ commit สำเร็จ โดยไม่ขึ้นกับผลส่ง notification ภายหลัง
- ผลลัพธ์: เพิ่มหน้าผลการจองที่แสดงหมายเลขคิวและสถานะเมื่อ POST /bookings สำเร็จ

---

## 2026-10-01 คำสั่ง: /implement T-07

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/audit/middleware.py, backend/app/db/models.py, backend/tests/test_audit_log.py
- ผล test: `cd backend && pytest tests/test_audit_log.py tests/test_booking_create.py tests/test_booking_duplicate.py tests/test_booking_full_slot.py tests/test_notification_retry.py -q` -> 8 passed
- ผลลัพธ์: เพิ่ม `AuditMiddleware` ที่จับทุก request ไป `/bookings` และบันทึก `actor_id`, `accessed_at`, `hn`, `action` ลง `audit_logs` พร้อม validate ผ่าน AC-BKG-06
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี; task ระบุชัดว่า log ต้องมี actor_id, accessed_at, hn และ schema ให้มี `audit_logs` แล้วอยู่ใน model ก่อนหน้า
- ข้อควรตรวจด้วยตาก่อน commit: ด้าน production ต้องแน่ใจว่า middleware ถูกลงใน `app.main` จริง เพื่อให้ request จริงผ่านเข้าสู่ middleware อย่างเดียวกับ test ที่ใช้ `add_middleware` โดยตรง

---

## 2026-10-01 คำสั่ง: /implement T-08

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/app/his/client.py, backend/app/booking/service.py, backend/tests/test_his_lookup.py
- ผล test: `cd backend && pytest tests/test_his_lookup.py -q` -> 2 passed
- ผลลัพธ์: เพิ่ม `lookup_hn_by_national_id` ที่เรียก HIS endpoint `/patients/lookup` ด้วย `national_id` และคืนค่า `hn` อย่างเดียว; `resolve_hn_for_booking` ใน booking service เรียก helper นี้ เพื่อแปลงเลขบัตรให้เป็น HN ก่อนบันทึกในตารางการจองและไม่เก็บ `national_id`
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี; spec ระบุชัดว่าต้องค้นจาก HIS ด้วยเลขบัตรและไม่เก็บเลขบัตรในตารางการจอง
- ข้อควรตรวจด้วยตาก่อน commit: ต้องต่อกับ HIS จริงและตรวจว่า ticket/credential ส่งผ่านถูกต้อง รวมถึงแน่ใจว่าสงวนเฉพาะ HN ใน booking record เท่านั้น

---

## 2026-10-01 คำสั่ง: /implement T-12

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: backend/scripts/seed_dev_slots.py, backend/tests/test_seed_dev_slots.py
- ผล test: `cd backend && pytest tests/test_seed_dev_slots.py -q` -> 2 passed
- ผลลัพธ์: เพิ่มสคริปต์ seed slot สำหรับ dev/test ที่รับ `--date` และ `--package-code`, สร้าง slot 09:00 ที่เหลือ 1 ที่ภายใน 30 วันข้างหน้า และตรวจได้ผ่าน `GET /slots`
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี; spec ระบุชัดว่าต้องระบุ package_code และวันที่จากผู้ทดสอบ และต้องไม่ seed อัตโนมัติเมื่อเริ่มระบบ
- ข้อควรตรวจด้วยตาก่อน commit: รันบนฐานข้อมูล dev/test จริงที่มี `DATABASE_URL` เป็น persistent DB; ห้ามใช้ SQLite in-memory สำหรับ seed จริง เพราะ task ระบุให้ใช้ฐานข้อมูลที่กำหนดสำหรับทดสอบเท่านั้น

---

## 2026-10-01 คำสั่ง: /implement T-13

- เครื่องมือ: Copilot in Codespaces
- ไฟล์ที่สร้างหรือแก้: frontend/src/__tests__/AC-BKG-01.test.jsx, frontend/src/App.jsx, frontend/src/pages/ConfirmBooking.jsx
- ผล test: `cd frontend && npm test -- src/__tests__/AC-BKG-01.test.jsx src/__tests__/BookingResult.test.jsx src/__tests__/AC-BKG-03.test.jsx src/__tests__/SlotPicker.test.jsx src/__tests__/setup.test.jsx` -> 5 files passed, 6 tests passed; `cd frontend && npm run build` -> สำเร็จ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: API จริงให้ POST /bookings คืน JSON ตรงแบบคาดไว้ และ `App` ต้องสลับจากหน้ายืนยันไปหน้าผลสำเร็จทันทีหลัง 200
- ผลลัพธ์: ปรับ flow ให้เลือก slot -> ยืนยัน -> สลับไปหน้า BookingResult ที่แสดง `queue_no` และสถานะจาก response จริง โดยไม่แสดง success alert ซ้ำ
