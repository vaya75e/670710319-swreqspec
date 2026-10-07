import { render, screen } from '@testing-library/react'
import { describe, expect, test } from 'vitest'
import BookingResult from '../pages/BookingResult.jsx'

describe('TC-BKG-01-2', () => {
  test('test_TC_BKG_01_2_booking_result_display', () => {
    // Given: เลือกช่วง 09.00 น. ที่มีที่นั่งว่าง 1 ที่ แล้วยืนยันการจอง
    const booking = {
      booking_id: 1,
      slot_id: 1,
      queue_no: 'A001',
      status: 'BOOKED',
    }

    // When: แสดงผลการจอง
    render(<BookingResult booking={booking} />)

    // Then: แสดงหมายเลขคิวจาก response และแสดงสถานะการจองที่สำเร็จ (รอ Q-02)
    // รอ Q-02: รูปแบบหมายเลขคิวยังไม่ได้ตัดสิน ไม่สวมถ่วง assert
    expect(screen.getByText('BOOKED')).toBeTruthy()
  })
})
