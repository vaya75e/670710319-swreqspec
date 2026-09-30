import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import SlotPicker from '../pages/SlotPicker.jsx'

test('โหลดช่วงเวลาว่างตามแพ็กเกจที่เลือก', async () => {
  const api = {
    getSlots: vi.fn().mockResolvedValue({
      slots: [
        {
          id: 101,
          slot_date: '2026-09-23',
          start_time: '09:00:00',
          package_code: 'STD',
          capacity: 5,
          remaining: 2,
        },
      ],
    }),
  }

  render(<SlotPicker api={api} />)

  await waitFor(() => {
    expect(api.getSlots).toHaveBeenCalledWith({
      dateFrom: expect.any(String),
      packageCode: 'STD',
    })
  })

  expect(screen.getByText('เลือกแพ็กเกจและช่วงเวลา')).toBeTruthy()
  expect(screen.getByText('09:00')).toBeTruthy()
  expect(screen.getByText('ที่นั่งคงเหลือ: 2')).toBeTruthy()

  fireEvent.click(screen.getByRole('button', { name: 'VIP' }))

  await waitFor(() => {
    expect(api.getSlots).toHaveBeenLastCalledWith({
      dateFrom: expect.any(String),
      packageCode: 'VIP',
    })
  })
})

test('เมื่อผู้ใช้กดจองแล้วต้องเรียก API และแสดงหมายเลขคิวที่ตอบกลับ', async () => {
  const api = {
    getSlots: vi.fn().mockResolvedValue({
      slots: [
        {
          id: 101,
          slot_date: '2026-09-23',
          start_time: '09:00:00',
          package_code: 'STD',
          capacity: 5,
          remaining: 2,
        },
      ],
    }),
    createBooking: vi.fn().mockResolvedValue({
      status: 200,
      body: { id: 1, queue_no: 'Q-0001', hn: 'HN-001', slot_id: 101 },
    }),
  }

  render(<SlotPicker api={api} />)

  await waitFor(() => {
    expect(screen.getByText('09:00')).toBeTruthy()
  })

  fireEvent.click(screen.getByRole('button', { name: 'จองคิว 09:00' }))

  await waitFor(() => {
    expect(api.createBooking).toHaveBeenCalledWith({
      slotId: 101,
      hn: 'HN-001',
    })
  })

  expect(await screen.findByText('หมายเลขคิว: Q-0001')).toBeTruthy()
})

test('ถ้าจองซ้ำวันเดียวกันต้องแสดงข้อความปฏิเสธ', async () => {
  const api = {
    getSlots: vi.fn().mockResolvedValue({
      slots: [
        {
          id: 101,
          slot_date: '2026-09-23',
          start_time: '09:00:00',
          package_code: 'STD',
          capacity: 5,
          remaining: 2,
        },
      ],
    }),
    createBooking: vi.fn().mockResolvedValue({
      status: 409,
      body: {
        detail: 'คุณมีคิวที่ยังไม่ได้ใช้ในวันเดียวกันแล้ว ไม่สามารถจองซ้ำได้',
        queue_no: 'Q-0001',
      },
    }),
  }

  render(<SlotPicker api={api} />)

  await waitFor(() => {
    expect(screen.getByText('09:00')).toBeTruthy()
  })

  fireEvent.click(screen.getByRole('button', { name: 'จองคิว 09:00' }))

  await waitFor(() => {
    expect(api.createBooking).toHaveBeenCalledWith({
      slotId: 101,
      hn: 'HN-001',
    })
  })

  expect(await screen.findByText('คุณมีคิวที่ยังไม่ได้ใช้ในวันเดียวกันแล้ว ไม่สามารถจองซ้ำได้')).toBeTruthy()
})
