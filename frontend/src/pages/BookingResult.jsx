// รองรับ: FR-BKG-04, FR-BKG-05
export default function BookingResult({ booking }) {
  if (!booking) return null

  return (
    <section
      aria-label="ผลการจอง"
      role="status"
      className="mx-auto mt-6 max-w-5xl border-y border-teal-800 px-5 py-6 sm:px-8"
    >
      <h2 className="text-xl font-bold">บันทึกการจองแล้ว</h2>
      <p className="mt-3 text-sm text-slate-600">หมายเลขคิว</p>
      <p className="mt-1 text-3xl font-semibold text-teal-900">{booking.queue_no}</p>
      <p className="mt-3 text-sm text-slate-700">
        สถานะ: {booking.status === 'confirmed' ? 'ยืนยันแล้ว' : booking.status}
      </p>
    </section>
  )
}