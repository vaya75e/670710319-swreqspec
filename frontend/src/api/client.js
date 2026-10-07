// จุดเดียวที่หน้าจอใช้เรียก API หลังบ้าน (ตามสัญญา API ใน plan.md ข้อ 4)
// ตอน test ให้ส่ง client จำลองเข้าไปในหน้าจอแทน ไม่ต้องรันหลังบ้านจริง
// เรียกผ่าน /api (ดู proxy ใน vite.config.js) หลังบ้านต้องรันอยู่ที่ port 8000
const BASE = import.meta.env.VITE_API_BASE ?? '/api'

export const api = {
  async getSlots({ dateFrom, packageCode }) {
    const q = new URLSearchParams({ date_from: dateFrom, package_code: packageCode })
    const res = await fetch(`${BASE}/slots?${q}`, {
      headers: { 'X-Verified-Identity': 'true' },
    })
    const body = await res.json()
    if (!res.ok) {
      throw new Error(body.detail ?? 'โหลดช่วงเวลาไม่สำเร็จ')
    }
    return body
  },
  async createBooking({ slotId, hn = 'HN-001' }) {
    const res = await fetch(`${BASE}/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Verified-Identity': 'true',
      },
      body: JSON.stringify({ slot_id: slotId, hn }),
    })

    const body = await res.json()
    return { status: res.status, body }
  },
}
