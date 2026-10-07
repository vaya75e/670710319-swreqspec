// test ตรวจว่าโครงหน้าจอพร้อมใช้ (ไม่ใช่ test ของ AC ใด)
import { render, screen } from '@testing-library/react'
import App from '../App.jsx'

test('โครงหน้าจอเปิดได้แม้โหลดช่วงเวลาไม่สำเร็จ', async () => {
  render(<App />)
  expect(screen.getByText('ระบบจองคิวตรวจสุขภาพ')).toBeTruthy()
  expect(await screen.findByRole('alert')).toBeTruthy()
})
