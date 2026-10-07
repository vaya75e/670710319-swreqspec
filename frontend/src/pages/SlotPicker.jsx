import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

function getTodayDate() {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// รองรับ: FR-BKG-01, FR-BKG-06
export default function SlotPicker({ client = api, selectedSlot, onSelectSlot }) {
  const [dateFrom] = useState(getTodayDate)
  const [packageCode, setPackageCode] = useState('')
  const [selectedDate, setSelectedDate] = useState('')
  const [packageOptions, setPackageOptions] = useState([])
  const [slots, setSlots] = useState([])
  const [selectedSlotId, setSelectedSlotId] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')

    client
      .getSlots({ dateFrom, packageCode })
      .then((result) => {
        if (!active) return
        const loadedSlots = Array.isArray(result?.slots) ? result.slots : []
        setSlots(loadedSlots)
        setSelectedSlotId('')
        onSelectSlot?.(null)
        if (!packageCode) {
          setPackageOptions(
            [...new Set(loadedSlots.filter((slot) => slot.remaining > 0).map((slot) => slot.package_code))].sort(),
          )
        }
      })
      .catch(() => {
        if (!active) return
        setSlots([])
        setError('โหลดช่วงเวลาว่างไม่สำเร็จ กรุณาลองใหม่อีกครั้ง')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [client, dateFrom, onSelectSlot, packageCode])

  const availableDates = [...new Set(slots.filter((slot) => slot.remaining > 0).map((slot) => slot.slot_date))].sort()
  const currentSelectedSlotId = typeof onSelectSlot === 'function' ? selectedSlot?.id ?? '' : selectedSlotId
  const visibleSlots = slots.filter(
    (slot) => slot.remaining > 0 && (!selectedDate || slot.slot_date === selectedDate),
  )

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-5 py-10 text-slate-900 sm:px-8">
      <header className="mb-8 border-b border-slate-200 pb-5">
        <p className="text-sm font-semibold uppercase tracking-wide text-teal-800">ระบบจองคิวตรวจสุขภาพ</p>
        <h1 className="mt-2 text-3xl font-bold">เลือกแพ็กเกจและช่วงเวลา</h1>
        <p className="mt-2 text-sm text-slate-600">แสดงช่วงเวลาที่มีที่นั่งว่างตั้งแต่ {dateFrom}</p>
      </header>

      <section aria-label="ตัวกรองช่วงเวลา" className="mb-8 grid gap-4 sm:grid-cols-2">
        <label className="grid gap-2 text-sm font-medium" htmlFor="package-code">
          แพ็กเกจ
          <select
            id="package-code"
            value={packageCode}
            onChange={(event) => {
              setPackageCode(event.target.value)
              setSelectedDate('')
              setSelectedSlotId('')
              onSelectSlot?.(null)
            }}
            className="min-h-11 rounded border border-slate-300 bg-white px-3"
          >
            <option value="">ทุกแพ็กเกจ</option>
            {packageOptions.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </label>

        <label className="grid gap-2 text-sm font-medium" htmlFor="slot-date">
          วันที่
          <select
            id="slot-date"
            value={selectedDate}
            onChange={(event) => {
              setSelectedDate(event.target.value)
              setSelectedSlotId('')
              onSelectSlot?.(null)
            }}
            className="min-h-11 rounded border border-slate-300 bg-white px-3"
          >
            <option value="">ทุกวัน</option>
            {availableDates.map((slotDate) => (
              <option key={slotDate} value={slotDate}>{slotDate}</option>
            ))}
          </select>
        </label>
      </section>

      {loading && <p role="status" className="py-8 text-center text-slate-600">กำลังโหลดช่วงเวลาว่าง...</p>}
      {error && <p role="alert" className="py-8 text-center text-red-700">{error}</p>}

      {!loading && !error && visibleSlots.length === 0 && (
        <p role="status" className="border-y border-slate-200 py-8 text-center text-slate-600">
          ไม่มีช่วงเวลาว่างสำหรับเงื่อนไขที่เลือก
        </p>
      )}

      {!loading && !error && visibleSlots.length > 0 && (
        <fieldset>
          <legend className="mb-3 text-lg font-semibold">ช่วงเวลาที่ว่าง</legend>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {visibleSlots.map((slot) => (
              <label
                key={slot.id}
                className={`flex min-h-24 cursor-pointer items-start gap-3 rounded border p-4 ${
                  String(currentSelectedSlotId) === String(slot.id)
                    ? 'border-teal-800 bg-teal-50'
                    : 'border-slate-300 bg-white'
                }`}
              >
                <input
                  type="radio"
                  name="slot"
                  value={slot.id}
                  checked={String(currentSelectedSlotId) === String(slot.id)}
                  onChange={() => {
                    setSelectedSlotId(slot.id)
                    onSelectSlot?.(slot)
                  }}
                  className="mt-1 accent-teal-800"
                />
                <span className="grid gap-1">
                  <span className="font-semibold">{slot.slot_date} · {slot.start_time.slice(0, 5)} น.</span>
                  <span className="text-sm text-slate-600">{slot.package_code}</span>
                  <span className="text-sm text-slate-700">คงเหลือ {slot.remaining} ที่</span>
                </span>
              </label>
            ))}
          </div>
        </fieldset>
      )}
    </main>
  )
}