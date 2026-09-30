import { useEffect, useMemo, useState } from 'react'

import { api as defaultApi } from '../api/client.js'

const PACKAGE_OPTIONS = ['STD', 'VIP']

function formatTime(value) {
  if (!value) return ''
  const [hours, minutes] = value.split(':')
  return `${hours}:${minutes}`
}

export default function SlotPicker({ api = defaultApi }) {
  const today = useMemo(() => new Date().toISOString().slice(0, 10), [])
  const [packageCode, setPackageCode] = useState('STD')
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(false)
  const [bookingResult, setBookingResult] = useState(null)
  const [bookingError, setBookingError] = useState('')
  const [bookingSlotId, setBookingSlotId] = useState(null)

  useEffect(() => {
    const loadSlots = async () => {
      setLoading(true)
      try {
        const payload = await api.getSlots({ dateFrom: today, packageCode })
        setSlots(payload.slots ?? [])
      } finally {
        setLoading(false)
      }
    }

    loadSlots()
  }, [api, packageCode, today])

  const handleBook = async (slot) => {
    setBookingError('')
    setBookingSlotId(slot.id)

    const res = await api.createBooking({ slotId: slot.id, hn: 'HN-001' })

    if (res.status >= 400) {
      setBookingError(res.body?.detail ?? 'ไม่สามารถจองได้ในเวลานี้')
      setBookingResult(null)
    } else {
      setBookingResult({
        queueNo: res.body?.queue_no,
        slotTime: formatTime(slot.start_time),
      })
    }

    setBookingSlotId(null)
  }

  return (
    <section className="mt-6 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-4">
        <h2 className="text-xl font-semibold text-slate-800">เลือกแพ็กเกจและช่วงเวลา</h2>
        <div className="flex gap-2">
          {PACKAGE_OPTIONS.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setPackageCode(item)}
              className={[
                'rounded-full border px-3 py-1.5 text-sm font-medium transition',
                packageCode === item
                  ? 'border-teal-600 bg-teal-600 text-white'
                  : 'border-slate-300 bg-white text-slate-700 hover:border-teal-500 hover:text-teal-700',
              ].join(' ')}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="text-slate-500">กำลังโหลดช่วงเวลาที่ว่าง...</p>
      ) : (
        <ul className="space-y-3">
          {slots.length === 0 ? (
            <li className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-3 text-slate-500">
              ไม่มีช่วงเวลาว่างในช่วงนี้
            </li>
          ) : (
            slots.map((slot) => (
              <li key={slot.id} className="flex items-center justify-between gap-4 rounded-lg border border-slate-200 p-3">
                <div>
                  <div className="text-sm text-slate-500">{slot.slot_date}</div>
                  <div className="text-lg font-semibold text-slate-800">{formatTime(slot.start_time)}</div>
                </div>
                <div className="text-right text-sm text-slate-600">
                  <div>ที่นั่งคงเหลือ: {slot.remaining}</div>
                  <div className="text-xs text-slate-500">{slot.package_code}</div>
                </div>
                <button
                  type="button"
                  onClick={() => handleBook(slot)}
                  disabled={bookingSlotId === slot.id}
                  className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-300"
                >
                  {bookingSlotId === slot.id ? 'กำลังจอง...' : `จองคิว ${formatTime(slot.start_time)}`}
                </button>
              </li>
            ))
          )}
        </ul>
      )}

      {bookingError ? <p className="mt-4 text-sm text-red-600">{bookingError}</p> : null}
      {bookingResult ? (
        <div className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-emerald-800">
          <p className="font-semibold">จองสำเร็จ</p>
          <p>หมายเลขคิว: {bookingResult.queueNo}</p>
          <p>เวลา: {bookingResult.slotTime}</p>
        </div>
      ) : null}
    </section>
  )
}