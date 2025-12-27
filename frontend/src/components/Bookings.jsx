import { useState, useEffect } from 'react';
import { getBookings, cancelBooking } from '../api';

function Bookings() {
  const [bookings, setBookings] = useState({ upcoming: [], past: [] });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const data = await getBookings();
      setBookings({ upcoming: data.upcoming, past: data.past });
    } catch (error) {
      setMessage({ type: 'error', text: error.message });
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (bookingId) => {
    setMessage({ type: '', text: '' });
    try {
      await cancelBooking(bookingId);
      setMessage({ type: 'success', text: 'Booking cancelled successfully!' });
      fetchBookings();
    } catch (error) {
      setMessage({ type: 'error', text: error.message });
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return <div className="loading">Loading your bookings...</div>;
  }

  return (
    <div className="container">
      <h2 style={{ color: 'var(--primary-blue)', marginBottom: '1.5rem' }}>
        My Bookings
      </h2>

      {message.text && (
        <div className={`message ${message.type}`}>{message.text}</div>
      )}

      <div className="bookings-section">
        <h3>Upcoming Bookings</h3>
        {bookings.upcoming.length === 0 ? (
          <div className="empty-state">No upcoming bookings.</div>
        ) : (
          bookings.upcoming.map((booking) => (
            <div key={booking.id} className="card booking-card">
              <div className="booking-info">
                <h4>{booking.event.title}</h4>
                <p>📅 {formatDate(booking.event.start_time)}</p>
                <p>Booked on: {formatDate(booking.booked_at)}</p>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span className={`booking-status ${booking.status}`}>
                  {booking.status}
                </span>
                {booking.status === 'confirmed' && (
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => handleCancel(booking.id)}
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="bookings-section">
        <h3>Past Bookings</h3>
        {bookings.past.length === 0 ? (
          <div className="empty-state">No past bookings.</div>
        ) : (
          bookings.past.map((booking) => (
            <div key={booking.id} className="card booking-card">
              <div className="booking-info">
                <h4>{booking.event.title}</h4>
                <p>📅 {formatDate(booking.event.start_time)}</p>
              </div>
              <span className={`booking-status ${booking.status}`}>
                {booking.status}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Bookings;
