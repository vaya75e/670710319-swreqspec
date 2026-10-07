import { fireEvent, render, screen } from '@testing-library/react'

import App from '../App.jsx'

// รองรับ: FR-BKG-01, FR-BKG-04
test('test_AC_BKG_01_จองสำเร็จจาก slot ที่เลือกแล้วแสดง queue_no และสถานะ', async () => {
  const selectedSlot = {
    id: 7,
    slot_date: '2026-10-01',
    start_time: '09:00:00',
    package_code: 'STD',
    capacity: 1,
    remaining: 1,
  }
  const fetchMock = vi.fn((input, init) => {
    const url = String(input)
    if (url.includes('/slots') && init?.method !== 'POST') {
      return Promise.resolve({
        ok: true,
        json: async () => ({ slots: [selectedSlot] }),
      })
    }

    if (url.includes('/bookings') && init?.method === 'POST') {
      return Promise.resolve({
        ok: true,
        json: async () => ({
          id: 99,
          slot_id: 7,
          hn: 'HN-001',
          queue_no: '01',
          status: 'confirmed',
          booking_date: '2026-10-01T09:00:00',
        }),
      })
    }

    return Promise.reject(new Error('unexpected request'))
  })

  global.fetch = fetchMock

  render(<App />)

  fireEvent.click(await screen.findByRole('radio', { name: /2026-10-01 · 09:00 น\. STD คงเหลือ 1 ที่/ }))
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันการจอง' }))

  expect(await screen.findByRole('heading', { name: 'บันทึกการจองแล้ว' })).toBeTruthy()
  expect(screen.getByText('01')).toBeTruthy()
  expect(screen.getByText('สถานะ: ยืนยันแล้ว')).toBeTruthy()
  expect(fetchMock).toHaveBeenCalledWith(
    expect.stringMatching(/\/bookings$/),
    expect.objectContaining({
      method: 'POST',
      headers: expect.objectContaining({
        'Content-Type': 'application/json',
      }),
    }),
  )
})
