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
