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
              <li key={slot.id} className="flex items-center justify-between rounded-lg border border-slate-200 p-3">
                <div>
                  <div className="text-sm text-slate-500">{slot.slot_date}</div>
                  <div className="text-lg font-semibold text-slate-800">{formatTime(slot.start_time)}</div>
                </div>
                <div className="text-right text-sm text-slate-600">
                  <div>ที่นั่งคงเหลือ: {slot.remaining}</div>
                  <div className="text-xs text-slate-500">{slot.package_code}</div>
                </div>
              </li>
            ))
          )}
        </ul>
      )}
    </section>
  )
}