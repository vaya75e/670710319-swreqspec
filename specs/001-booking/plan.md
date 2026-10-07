# Plan: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md SPEC-BKG-001 Draft v3 | Updated: 2569-09-30 | สร้างด้วย /plan แล้วทีมตรวจแล้ว (plan v1)

## 1. สรุปแนวทาง
- ผู้รับบริการที่ยืนยันตัวตนแล้ว ค้นช่วงเวลาว่าง เลือก แล้วยืนยันการจอง ได้หมายเลขคิวกลับทันที
- หลังบ้านเป็น API (Python FastAPI) เก็บข้อมูลใน PostgreSQL ตาม CON-TECH-01 ผ่าน SQLAlchemy
- การส่งข้อความยืนยันไม่รอผล (IF-NOT-01): API แค่วางงานลงคิว แล้วตัวส่งแยกทำงานเบื้องหลัง
- ทุกการเข้าถึงข้อมูลการจองถูกบันทึก audit log (DOM-PDPA-01) และเก็บเฉพาะ HN ไม่เก็บเลขบัตรประชาชน (IF-HIS-01)
- Q-02 ปิดแล้ว: หมายเลขคิวรีเซ็ตตามวันตรวจ (`slot_date`), ใช้ลำดับเดียวร่วมกันทุกแพ็กเกจ, ไม่มี prefix, เริ่ม `01` และหลัง `99` ใช้ `100` ขึ้นไป; T-14 ปรับ implementation ให้ตรงกับคำตัดสินนี้

## 2. เทคโนโลยีที่ใช้
| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| PostgreSQL 16 | CON-TECH-01 | บังคับโดยฝ่าย IT โรงพยาบาล ใช้ในระบบจริง |
| Python 3.12 + FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ค่าเริ่มต้นของรายวิชา |
| SQLAlchemy 2 | ทีมเลือกเอง ไม่ได้มาจาก spec | ต่อฐานข้อมูลผ่านตัวแปร `DATABASE_URL` สลับฐานข้อมูลได้โดยไม่แก้โค้ด |
| pytest | ทีมเลือกเอง ไม่ได้มาจาก spec | ตอน test ใช้ SQLite ในหน่วยความจำ (`sqlite:///:memory:`) แทน PostgreSQL เพราะ Codespace ไม่มีเครื่องฐานข้อมูลรันอยู่ ไม่ต้องติดตั้งอะไรเพิ่ม |
| React (Vite) + Tailwind CSS | ทีมเลือกเอง ไม่ได้มาจาก spec | ค่าเริ่มต้นของรายวิชา โครงเริ่มต้นอยู่ใน `frontend/` แล้ว |
| Vitest + React Testing Library | ทีมเลือกเอง ไม่ได้มาจาก spec | test หน้าจอ ใช้ API จำลอง ไม่ต้องรันหลังบ้านจริง |
| Redis (คิวส่งข้อความ) | ทีมเลือกเอง ไม่ได้มาจาก spec | รองรับ IF-NOT-01 แบบ async ตอน test ใช้คิวจำลองในหน่วยความจำ ไม่ต้องมี Redis จริง |

library ทั้งหมดอยู่ใน `backend/requirements.txt` (Codespace ติดตั้งให้ตอนสร้างเครื่อง)
รัน test หลังบ้านด้วยคำสั่ง `cd backend && pytest` (ตั้งค่าไว้แล้วใน `backend/pytest.ini`)
เปิดหลังบ้านให้หน้าจอเรียกได้ด้วยคำสั่ง `cd backend && uvicorn app.main:app --reload --port 8000` (หน้าจอเรียกผ่าน `/api` ซึ่ง Vite ส่งต่อไปให้)
รัน test หน้าจอด้วยคำสั่ง `cd frontend && npm test` และเปิดดูหน้าจอด้วย `cd frontend && npm run dev` (Codespace ติดตั้ง library ของหน้าจอให้ตอนสร้างเครื่อง)

### ข้อมูลสำหรับทดสอบผ่านเว็บ
- `GET /slots` อ่านช่วงเวลาจากตาราง `slots` ซึ่งเป็นข้อมูลที่ UC-09 จัดเตรียมไว้ ระบบจองคิวนี้ไม่สร้างตารางหรือโควตาจริงเอง
- เมื่อฐานข้อมูลทดสอบยังไม่มี slot ให้ใช้ `backend/scripts/seed_dev_slots.py` เพิ่มข้อมูลทดสอบลงในฐานข้อมูลที่กำหนดด้วย `DATABASE_URL` เท่านั้น ไม่ seed อัตโนมัติเมื่อเริ่มระบบ
- ผู้ทดสอบต้องระบุวันที่ภายใน 30 วันและ `package_code` ที่ทีมเลือกสำหรับการทดสอบเอง ไม่มีค่า package code เริ่มต้นที่อนุมานจาก spec; เวลา 09.00 น. และจำนวน 1 ที่ใช้ตาม AC-BKG-01
- หน้าจอใช้ `id` ที่ได้จาก `GET /slots` เป็น `slot_id` ในคำขอจอง ห้ามกำหนด `slot_id` ล่วงหน้า หาก API คืนรายการว่าง ให้แสดงสถานะว่าไม่มีช่วงเวลาว่าง แทนการส่งคำขอจองด้วย ID ที่ไม่มีอยู่
- การทดสอบหลังบ้านอัตโนมัติยังใช้ SQLite ในหน่วยความจำตามแผน ส่วนการทดสอบเว็บเชื่อมฐานข้อมูลจริงต้องใช้ PostgreSQL ผ่าน `DATABASE_URL` ที่ตรงกันทั้งตอน seed และตอนรัน API
- ขั้นทดสอบเว็บ: เริ่ม API ด้วยฐานข้อมูลทดสอบ, seed slot, ตรวจ `GET /slots` ว่ามี slot, เริ่ม Vite, เลือก slot ที่แสดง แล้วจอง; ตรวจผลสำเร็จและจำนวน `remaining` ที่ลดลง

### โครงไฟล์
```
backend/
  requirements.txt
  pytest.ini                   ตั้งค่า pytest ให้หา app/ เจอ
  app/
    main.py                    สร้าง FastAPI app และรวม router
    config.py                  อ่าน DATABASE_URL
    db/
      models.py                ตาราง slots, bookings, audit_logs (SQLAlchemy)
      session.py               สร้าง engine และ session
      migrations/
        001_init.py            ฟังก์ชัน upgrade(engine) สร้างทุกตาราง
    auth/
      idp.py                   ตรวจผลยืนยันตัวตนจากระบบยืนยันตัวตน (IF-IDP-01)
    his/
      client.py                ค้น HN จาก HIS ด้วยเลขบัตร (IF-HIS-01)
    audit/
      middleware.py            บันทึก audit log ทุก request ที่แตะข้อมูลการจอง (DOM-PDPA-01)
    slots/
      router.py                GET /slots
      service.py               คำนวณช่วงว่าง และหาช่วงใกล้เคียง
    booking/
      router.py                POST /bookings, GET /bookings/{id}
      service.py               กันจองซ้ำ ตัดที่นั่ง บันทึกการจอง
    notify/
      queue.py                 วางงานส่งข้อความลงคิว และส่งซ้ำตาม ASM-03
  scripts/
    seed_dev_slots.py          เพิ่ม slot สำหรับฐานข้อมูล dev/test ตามค่าที่ผู้ทดสอบระบุ
  tests/
    conftest.py                เตรียมฐานข้อมูล SQLite ในหน่วยความจำให้ทุก test
    test_*.py                  1 ไฟล์ต่อ 1 task หรือ 1 AC
    test_seed_dev_slots.py     ตรวจการเพิ่ม slot ในฐานข้อมูลทดสอบ
frontend/                      React (Vite) + Tailwind CSS มีโครงเริ่มต้นให้แล้ว
  package.json                 คำสั่ง npm run dev, npm test
  vite.config.js               ตั้งค่า Vite, Tailwind และ Vitest
  src/
    App.jsx                    หน้าแรก ใส่หน้าจอของแต่ละ task เข้ามาที่นี่
    index.css                  เปิดใช้ Tailwind
    api/client.js              เรียก API หลังบ้านผ่าน /api (Vite ส่งต่อไป port 8000) ตอน test ส่ง client จำลองเข้าหน้าจอแทน
    pages/SlotPicker.jsx       หน้าเลือกแพ็กเกจและช่วงเวลา
    pages/ConfirmBooking.jsx   หน้ายืนยัน และแจ้ง "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือก
    pages/BookingResult.jsx    หน้าแสดงผลการจองและหมายเลขคิว
    __tests__/                 test หน้าจอ ตั้งชื่อไฟล์ตาม AC เช่น AC-BKG-03.test.jsx
```

## 3. โมเดลข้อมูล
| ตาราง | ฟิลด์หลัก | รองรับ |
|---|---|---|
| slots | id, slot_date, start_time, package_code, capacity, remaining | FR-BKG-01, FR-BKG-06, ASM-01 |
| bookings | id, hn, slot_id, booking_date, queue_no, status, created_at | FR-BKG-02, FR-BKG-04, IF-HIS-01 |
| audit_logs | id, actor_id, action, hn, accessed_at | DOM-PDPA-01 |

- ตาราง bookings เก็บเฉพาะ `hn` **ไม่มีคอลัมน์เลขบัตรประชาชน (national_id)** ตาม IF-HIS-01
- `queue_no` ใช้ลำดับรายวันตาม `slots.slot_date` ร่วมกันทุกแพ็กเกจ; รูปแบบไม่มี prefix, อย่างน้อย 2 หลัก (`01`-`99`) และไม่ตัดหลักเมื่อเกิน 99
- รายการค้างส่งข้อความ (ASM-03) เก็บในคิว Redis ไม่ใช่ตารางใน PostgreSQL

## 4. API / หน้าจอ
| รายการ | input / output หลัก | รองรับ |
|---|---|---|
| GET /slots | in: date_from, package_code / out: รายการช่วงเวลา + ที่นั่งคงเหลือ | FR-BKG-01, FR-BKG-06 |
| POST /bookings | in: slot_id / out: booking id, queue_no หรือ 409 พร้อมช่วงใกล้เคียง 3 ช่วง | FR-BKG-02, FR-BKG-03, FR-BKG-04 |
| GET /bookings/{id} | out: รายละเอียดการจอง + queue_no | FR-BKG-05 |
| GET /patients/lookup | in: เลขบัตร (ส่งต่อไป HIS ไม่เก็บ) / out: hn | IF-HIS-01 |
| หน้าเลือกแพ็กเกจและเวลา (SlotPicker) | เรียก GET /slots เปลี่ยนแพ็กเกจแล้วโหลดช่วงเวลาใหม่ | FR-BKG-01, FR-BKG-06 |
| หน้ายืนยัน (ConfirmBooking) | เรียก POST /bookings ถ้าได้ 409 แสดง "ช่วงเวลาเต็ม" และ 3 ตัวเลือก | FR-BKG-03, FR-BKG-04 |
| หน้าแสดงผลการจอง (BookingResult) | แสดงหมายเลขคิว แม้ส่งข้อความไม่สำเร็จ | FR-BKG-04, FR-BKG-05 |

## 5. ตารางตรวจ Constraints
| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | ข้อ 2 และข้อ 3 (ตารางทั้งหมดอยู่ใน PostgreSQL ในระบบจริง) | ใช้แล้ว |
| DOM-PDPA-01 | ตาราง audit_logs และ audit/middleware.py | ใช้แล้ว |
| IF-IDP-01 | auth/idp.py ทุก endpoint ตรวจผลยืนยันตัวตนก่อน | ใช้แล้ว |
| IF-HIS-01 | GET /patients/lookup และ bookings เก็บเฉพาะ hn | ใช้แล้ว |
| IF-NOT-01 | notify/queue.py POST /bookings ไม่รอผลการส่งข้อความ | ใช้แล้ว ตาม ASM-03 |

## 6. แผนทดสอบจาก Acceptance Criteria
| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01 | สร้างช่วง 09.00 ที่เหลือ 1 ที่ จองผ่าน API แล้วตรวจว่าบันทึกสำเร็จ มีหมายเลขคิว และ remaining เป็น 0; T-14 ตรวจการจัดลำดับคิวตามวันตรวจ |
| AC-BKG-02 | test_AC_BKG_02 | สร้างการจองวันเดียวกันไว้ 1 รายการ จองซ้ำ แล้วตรวจว่าถูกปฏิเสธและได้ booking เดิมกลับ |
| AC-BKG-03 | test_AC_BKG_03 | ทำให้ช่วง 09.00 เต็มก่อนยืนยัน แล้วตรวจว่าได้ 409 พร้อม 3 ช่วงที่ใกล้ที่สุดในวันเดียวกันและวันถัดไป และไม่มีการจองซ้อน |
| AC-BKG-04 | test_AC_BKG_04 | ใช้คิวจำลองที่ส่งไม่สำเร็จ ตรวจว่าการจองยังถูกบันทึก และมีงานส่งซ้ำกำหนดภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05 | ยิง GET /slots พร้อมกัน 200 ครั้งแบบย่อส่วนใน Codespace แล้ววัด p95 (ผลจริงต้องวัดบนเครื่องทดสอบ) |
| AC-BKG-06 | test_AC_BKG_06 | เปิดดูการจอง 1 ครั้ง แล้วตรวจว่ามี audit log ที่มี actor_id, accessed_at และ hn |
| AC-BKG-03 (หน้าจอ) | AC-BKG-03.test.jsx | ให้ API จำลองตอบ 409 พร้อม 3 ช่วง แล้วตรวจว่าหน้าจอแสดง "ช่วงเวลาเต็ม" และปุ่ม 3 ตัวเลือก |

หลักแยกง่าย ๆ: AC ที่ Then บอกว่า "บันทึก" ตรวจที่หลังบ้าน AC ที่ Then บอกว่า "แสดง" หรือ "แจ้ง" ต้องมี test หน้าจอด้วย
FR-BKG-06 ยังไม่มี AC ใน spec จึงยังไม่มี test ที่ตรวจการเปลี่ยนแพ็กเกจ (ควรเสนอทีมเพิ่ม AC)

## 7. ลำดับงาน
หลังบ้าน
1. สร้างตารางและ migration (CON-TECH-01, DOM-PDPA-01, IF-HIS-01)
2. GET /slots และการคำนวณช่วงว่างตามแพ็กเกจ (FR-BKG-01, FR-BKG-06, AC-BKG-05)
3. POST /bookings พื้นฐาน ตัดที่นั่งและบันทึก (FR-BKG-04, AC-BKG-01)
4. กันจองซ้ำวันเดียวกัน (FR-BKG-02, AC-BKG-02)
5. เสนอช่วงใกล้เคียงเมื่อเต็ม (FR-BKG-03, AC-BKG-03)
6. คิวส่งข้อความและการส่งซ้ำ (FR-BKG-05, IF-NOT-01, AC-BKG-04)
7. audit log middleware (DOM-PDPA-01, AC-BKG-06)
8. ค้น HN จาก HIS (IF-HIS-01)
9. ปรับการออกหมายเลขคิวตาม `slot_date` และรูปแบบที่ทีมกำหนดใน Q-02 (FR-BKG-04, AC-BKG-01) ทำใน T-14

หน้าจอ (ใช้ API จำลองตามสัญญาในข้อ 4 จึงเริ่มพร้อมหลังบ้านได้)
10. หน้าเลือกแพ็กเกจและช่วงเวลา (FR-BKG-01, FR-BKG-06) เริ่มได้เลย
11. หน้ายืนยัน และแจ้ง "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือก (FR-BKG-03, AC-BKG-03) ทำหลังข้อ 10
12. ต่อหน้าจอกับ API จริง (FR-BKG-01, FR-BKG-03) ทำหลังข้อ 2, ข้อ 5 และข้อ 11
13. เพิ่มข้อมูล slot dev/test โดยระบุ package_code และวันทดสอบเอง; ใช้เฉพาะฐานข้อมูลที่กำหนดสำหรับทดสอบ ไม่เพิ่ม API จัดการโควตา
14. แสดงผลการจองและหมายเลขคิวที่ API ส่งกลับ (FR-BKG-04, FR-BKG-05) ทำหลังข้อ 6, ข้อ 9 และข้อ 11
15. ทดสอบ flow ผ่านเว็บกับ API จริง โดยใช้ slot id จาก GET /slots; ทำหลังข้อ 3 และข้อ 9-14

## 8. สิ่งที่ยังไม่ทำ
- Q-02 ปิดแล้วตามคำตัดสินทีมใน spec v3; ไม่มี Open Question ค้างสำหรับฟีเจอร์นี้
- การปรับ implementation หมายเลขคิวและการแสดงหมายเลขคิวเป็นงาน T-14 และ T-11 ตามลำดับ
