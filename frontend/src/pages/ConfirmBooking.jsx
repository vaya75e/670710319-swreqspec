import { useEffect, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ: FR-BKG-03
export default function ConfirmBooking({ client = api, selectedSlot, onSelectAlternative, onBookingSuccess }) {
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [alternatives, setAlternatives] = useState([])

  useEffect(() => {
    setMessage('')
    setAlternatives([])
  }, [selectedSlot?.id])

  async function confirmBooking() {
    if (!selectedSlot || submitting) return

    setSubmitting(true)
    setMessage('')
    setAlternatives([])

    try {
      const result = await client.createBooking({ slotId: selectedSlot.id })
      if (result.status === 409) {
        setMessage(result.body.detail ?? 'ช่วงเวลาเต็ม')
        setAlternatives(Array.isArray(result.body.alternatives) ? result.body.alternatives : [])
      } else if (result.status >= 400) {
        setMessage(result.body.detail ?? 'ยืนยันการจองไม่สำเร็จ กรุณาลองอีกครั้ง')
      } else {
        onBookingSuccess?.(result.body)
      }
    } catch {
      setMessage('ยืนยันการจองไม่สำเร็จ กรุณาลองอีกครั้ง')
    } finally {
      setSubmitting(false)
    }
  }

  function chooseAlternative(slot) {
    onSelectAlternative?.(slot)
    setMessage('')
    setAlternatives([])
  }

  return (
    <section aria-label="ยืนยันการจอง" className="mx-auto max-w-5xl px-5 pb-10 sm:px-8">
      {selectedSlot && (
        <p className="mb-3 text-sm text-slate-700">
          เลือกแล้ว: {selectedSlot.slot_date} · {selectedSlot.start_time.slice(0, 5)} น. · {selectedSlot.package_code}
        </p>
      )}
      <button
        type="button"
        onClick={confirmBooking}
        disabled={!selectedSlot || submitting}
        className="min-h-11 rounded bg-teal-800 px-5 font-semibold text-white hover:bg-teal-900 disabled:cursor-not-allowed disabled:bg-slate-400"
      >
        {submitting ? 'กำลังยืนยัน...' : 'ยืนยันการจอง'}
      </button>

      {message && (
        <div role={alternatives.length > 0 ? 'alert' : 'status'} className="mt-5 border-y border-slate-200 py-4">
          <p className="font-semibold">{message}</p>
          {alternatives.length > 0 && (
            <div className="mt-3 grid gap-2 sm:grid-cols-3">
              {alternatives.map((slot) => (
                <button
                  key={slot.id}
                  type="button"
                  onClick={() => chooseAlternative(slot)}
                  className="min-h-16 rounded border border-slate-300 bg-white px-3 py-2 text-left hover:border-teal-800"
                >
                  เลือก {slot.slot_date} · {slot.start_time.slice(0, 5)} น.
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  )
}