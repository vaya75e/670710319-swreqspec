import { fireEvent, render, screen } from '@testing-library/react'

import App from '../App.jsx'

// รองรับ: FR-BKG-04, FR-BKG-05
test('แสดงหมายเลขคิวและสถานะตามผล API หลังบันทึกการจอง', async () => {
  const selectedSlot = {
    id: 23,
    slot_date: '2026-10-01',
    start_time: '09:00:00',
    package_code: 'STD',
    capacity: 1,
    remaining: 1,
  }
  const client = {
    getSlots: vi.fn().mockResolvedValue({ slots: [selectedSlot] }),
    createBooking: vi.fn().mockResolvedValue({
      status: 200,
      body: {
        id: 3,
        slot_id: 23,
        hn: 'HN-001',
        queue_no: '01',
        status: 'confirmed',
      },
    }),
  }

  render(<App client={client} />)

  fireEvent.click(await screen.findByRole('radio', { name: /2026-10-01 · 09:00 น\. STD คงเหลือ 1 ที่/ }))
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันการจอง' }))

  expect(await screen.findByRole('heading', { name: 'บันทึกการจองแล้ว' })).toBeTruthy()
  expect(screen.getByText('01')).toBeTruthy()
  expect(screen.getByText('สถานะ: ยืนยันแล้ว')).toBeTruthy()
  expect(client.createBooking).toHaveBeenCalledWith({ slotId: 23 })
})