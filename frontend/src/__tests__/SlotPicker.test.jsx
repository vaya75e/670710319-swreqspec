import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import SlotPicker from '../pages/SlotPicker.jsx'

function getTodayDate() {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// รองรับ: FR-BKG-01, FR-BKG-06
test('แสดงช่วงเวลาว่างและโหลดข้อมูลใหม่เมื่อเปลี่ยนแพ็กเกจ', async () => {
  const stdSlot = {
    id: 41,
    slot_date: '2026-10-01',
    start_time: '09:00:00',
    package_code: 'STD',
    capacity: 1,
    remaining: 1,
  }
  const vipSlot = {
    id: 42,
    slot_date: '2026-10-01',
    start_time: '10:00:00',
    package_code: 'VIP',
    capacity: 3,
    remaining: 2,
  }
  const client = {
    getSlots: vi.fn()
      .mockResolvedValueOnce({ slots: [stdSlot, vipSlot] })
      .mockResolvedValueOnce({ slots: [vipSlot] }),
  }

  render(<SlotPicker client={client} />)

  expect(await screen.findByText('2026-10-01 · 09:00 น.')).toBeTruthy()
  expect(screen.getByText('คงเหลือ 1 ที่')).toBeTruthy()
  expect(screen.getByRole('radio', { name: /2026-10-01 · 09:00 น\. STD คงเหลือ 1 ที่/ })).toHaveProperty('value', '41')

  fireEvent.change(screen.getByLabelText('แพ็กเกจ'), { target: { value: 'VIP' } })

  await waitFor(() => {
    expect(client.getSlots).toHaveBeenNthCalledWith(2, {
      dateFrom: getTodayDate(),
      packageCode: 'VIP',
    })
  })
  expect(await screen.findByText('2026-10-01 · 10:00 น.')).toBeTruthy()
  expect(screen.queryByText('2026-10-01 · 09:00 น.')).toBeNull()
})

test('แสดงสถานะไม่มีช่วงเวลาว่างเมื่อ API ไม่พบ slot', async () => {
  const client = { getSlots: vi.fn().mockResolvedValue({ slots: [] }) }

  render(<SlotPicker client={client} />)

  expect(await screen.findByText('ไม่มีช่วงเวลาว่างสำหรับเงื่อนไขที่เลือก')).toBeTruthy()
})