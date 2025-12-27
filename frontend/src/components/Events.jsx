import { useState, useEffect } from 'react';
import { getEvents, createBooking } from '../api';

function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const data = await getEvents();
      setEvents(data.events);
    } catch (error) {
      setMessage({ type: 'error', text: error.message });
    } finally {
      setLoading(false);
    }
  };

  const handleBook = async (eventId) => {
    setMessage({ type: '', text: '' });
    try {
      await createBooking(eventId);
      setMessage({ type: 'success', text: 'Booking created successfully!' });
      fetchEvents(); // Refresh to update participant count
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
    return <div className="loading">Loading events...</div>;
  }

  return (
    <div className="container">
      <div className="events-header">
        <h2>Available Events</h2>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>{message.text}</div>
      )}

      {events.length === 0 ? (
        <div className="empty-state">No events available at the moment.</div>
      ) : (
        <div className="events-grid">
          {events.map((event) => (
            <div key={event.id} className="card event-card">
              <span className={`event-type ${event.event_type}`}>
                {event.event_type}
              </span>
              <h3 className="event-title">{event.title}</h3>
              <p className="event-description">{event.description}</p>

              <div className="event-meta">
                <span>📅 {formatDate(event.start_time)}</span>
                <span>
                  👥 {event.current_participants}/{event.max_participants}
                </span>
              </div>

              <p className="event-facilitator">
                🧘 {event.facilitator?.name} - {event.facilitator?.specialization}
              </p>

              <div className="event-footer">
                <span className="event-price">₹{event.price.toFixed(0)}</span>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => handleBook(event.id)}
                  disabled={event.current_participants >= event.max_participants}
                >
                  {event.current_participants >= event.max_participants
                    ? 'Fully Booked'
                    : 'Book Now'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Events;
