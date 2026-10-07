import { fireEvent, render, screen } from '@testing-library/react'

import App from '../App.jsx'

// รองรับ: FR-BKG-03
test('test_AC_BKG_03 แสดงสามช่วงเวลาใกล้เคียงเมื่อ slot เต็มระหว่างยืนยัน', async () => {
  const selectedSlot = {
    id: 8,
    slot_date: '2026-10-01',
    start_time: '09:00:00',
    package_code: 'STD',
    capacity: 1,
    remaining: 1,
  }
  const alternatives = [
    { id: 9, slot_date: '2026-10-01', start_time: '09:05:00', package_code: 'STD', remaining: 1 },
    { id: 10, slot_date: '2026-10-01', start_time: '09:15:00', package_code: 'STD', remaining: 1 },
    { id: 11, slot_date: '2026-10-02', start_time: '08:45:00', package_code: 'STD', remaining: 1 },
  ]
  const client = {
    getSlots: vi.fn().mockResolvedValue({ slots: [selectedSlot] }),
    createBooking: vi.fn().mockResolvedValue({
      status: 409,
      body: { detail: 'ช่วงเวลาเต็ม', alternatives },
    }),
  }

  render(<App client={client} />)

  fireEvent.click(await screen.findByRole('radio', { name: /2026-10-01 · 09:00 น\. STD คงเหลือ 1 ที่/ }))
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันการจอง' }))

  expect((await screen.findByRole('alert')).textContent).toContain('ช่วงเวลาเต็ม')
  expect(screen.getByRole('button', { name: 'เลือก 2026-10-01 · 09:05 น.' })).toBeTruthy()
  expect(screen.getByRole('button', { name: 'เลือก 2026-10-01 · 09:15 น.' })).toBeTruthy()
  expect(screen.getByRole('button', { name: 'เลือก 2026-10-02 · 08:45 น.' })).toBeTruthy()
  expect(client.createBooking).toHaveBeenCalledWith({ slotId: 8 })
})