export default function BookingResult({ booking }) {
  return (
    <div>
      <h1>ผลการจอง</h1>
      <p>หมายเลขคิว: {booking.queue_no}</p>
      <p>{booking.status}</p>
    </div>
  )
}