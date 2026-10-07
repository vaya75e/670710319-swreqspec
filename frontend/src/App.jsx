import { useCallback, useState } from 'react'

import { api } from './api/client.js'
import BookingResult from './pages/BookingResult.jsx'
import ConfirmBooking from './pages/ConfirmBooking.jsx'
import SlotPicker from './pages/SlotPicker.jsx'

// รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-06
export default function App({ client = api }) {
  const [selectedSlot, setSelectedSlot] = useState(null)
  const [bookingResult, setBookingResult] = useState(null)

  const handleSelectSlot = useCallback((slot) => {
    setSelectedSlot(slot)
    setBookingResult(null)
  }, [])

  return (
    <>
      <SlotPicker
        client={client}
        selectedSlot={selectedSlot}
        onSelectSlot={handleSelectSlot}
      />
      {bookingResult ? (
        <BookingResult booking={bookingResult} />
      ) : (
        <ConfirmBooking
          client={client}
          selectedSlot={selectedSlot}
          onSelectAlternative={handleSelectSlot}
          onBookingSuccess={setBookingResult}
        />
      )}
    </>
  )
}
