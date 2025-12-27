import { useState, useEffect } from 'react';

const CRM_URL = 'http://localhost:5001';
const CRM_TOKEN = 'crm-secret-token-12345';

function FacilitatorDashboard({ onLogout }) {
  const [facilitator, setFacilitator] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [editingEvent, setEditingEvent] = useState(null);
  
  // Login state
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);

  useEffect(() => {
    // Check for saved facilitator
    const saved = localStorage.getItem('facilitator');
    if (saved) {
      setFacilitator(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    if (facilitator) {
      fetchBookings();
      fetchEvents();
    }
  }, [facilitator]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await fetch(`${CRM_URL}/api/facilitator/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();

      if (response.ok) {
        setFacilitator(data.facilitator);
        localStorage.setItem('facilitator', JSON.stringify(data.facilitator));
        setMessage({ type: 'success', text: 'Login successful!' });
      } else {
        setMessage({ type: 'error', text: data.error || 'Login failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to connect to CRM server' });
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    setFacilitator(null);
    localStorage.removeItem('facilitator');
    setBookings([]);
    setEvents([]);
  };

  const fetchBookings = async () => {
    try {
      const response = await fetch(`${CRM_URL}/api/facilitator/${facilitator.id}/bookings`, {
        headers: { 'Authorization': `Bearer ${CRM_TOKEN}` },
      });
      const data = await response.json();
      if (response.ok) {
        setBookings(data.bookings || []);
      }
    } catch (error) {
      console.error('Failed to fetch bookings:', error);
    }
  };

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${CRM_URL}/api/facilitator/${facilitator.id}/events`, {
        headers: { 'Authorization': `Bearer ${CRM_TOKEN}` },
      });
      const data = await response.json();
      if (response.ok) {
        setEvents(data.events || []);
      }
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateEvent = async (eventId, updates) => {
    setMessage({ type: '', text: '' });
    try {
      const response = await fetch(`${CRM_URL}/api/facilitator/${facilitator.id}/events/${eventId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${CRM_TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      });
      const data = await response.json();

      if (response.ok) {
        setMessage({ type: 'success', text: 'Event updated successfully!' });
        setEditingEvent(null);
        fetchEvents();
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to update event' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to connect to CRM server' });
    }
  };

  const handleCancelEvent = async (eventId) => {
    if (!confirm('Are you sure you want to cancel this event?')) return;
    
    setMessage({ type: '', text: '' });
    try {
      const response = await fetch(`${CRM_URL}/api/facilitator/${facilitator.id}/events/${eventId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${CRM_TOKEN}` },
      });
      const data = await response.json();

      if (response.ok) {
        setMessage({ type: 'success', text: 'Event cancelled successfully!' });
        fetchEvents();
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to cancel event' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to connect to CRM server' });
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
    });
  };

  // Login Form
  if (!facilitator) {
    return (
      <div className="auth-container">
        <div className="card auth-card">
          <h2>Facilitator Login</h2>
          
          {message.text && (
            <div className={`message ${message.type}`}>{message.text}</div>
          )}

          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loginLoading}>
              {loginLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div style={{ marginTop: '1.5rem', padding: '1rem', background: '#f0f7ff', borderRadius: '8px' }}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 0 }}>
              <strong>Demo Accounts:</strong><br />
              priya / priya123<br />
              arjun / arjun123<br />
              kavya / kavya123
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard
  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ color: 'var(--primary-blue)', marginBottom: '0.25rem' }}>
            🧘 Facilitator Dashboard
          </h2>
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            Welcome, {facilitator.name}
          </p>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>{message.text}</div>
      )}

      {/* Bookings Section */}
      <div className="bookings-section">
        <h3>Registered Users ({bookings.length})</h3>
        {bookings.length === 0 ? (
          <div className="empty-state">No bookings yet.</div>
        ) : (
          bookings.map((booking) => (
            <div key={booking.id} className="card booking-card">
              <div className="booking-info">
                <h4>{booking.event?.title}</h4>
                <p>👤 {booking.user?.username} ({booking.user?.email})</p>
                <p>📅 {formatDate(booking.event?.start_time)}</p>
              </div>
              <span className="booking-status confirmed">Registered</span>
            </div>
          ))
        )}
      </div>

      {/* Events Section */}
      <div className="bookings-section" style={{ marginTop: '2rem' }}>
        <h3>My Sessions ({events.length})</h3>
        {loading ? (
          <div className="loading">Loading...</div>
        ) : events.length === 0 ? (
          <div className="empty-state">No sessions found.</div>
        ) : (
          events.map((event) => (
            <div key={event.id} className="card" style={{ marginBottom: '1rem' }}>
              {editingEvent === event.id ? (
                <EditEventForm
                  event={event}
                  onSave={(updates) => handleUpdateEvent(event.id, updates)}
                  onCancel={() => setEditingEvent(null)}
                />
              ) : (
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h4 style={{ margin: '0 0 0.5rem 0' }}>{event.title}</h4>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                      {event.event_type} | ₹{event.price} | Max: {event.max_participants}
                    </p>
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => setEditingEvent(event.id)}
                    >
                      Edit
                    </button>
                    {event.is_active && (
                      <button
                        className="btn btn-sm"
                        style={{ background: '#ef4444', color: 'white' }}
                        onClick={() => handleCancelEvent(event.id)}
                      >
                        Cancel
                      </button>
                    )}
                    {!event.is_active && (
                      <span style={{ color: '#ef4444', fontWeight: 500 }}>Cancelled</span>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function EditEventForm({ event, onSave, onCancel }) {
  const [title, setTitle] = useState(event.title);
  const [description, setDescription] = useState(event.description || '');
  const [maxParticipants, setMaxParticipants] = useState(event.max_participants);
  const [price, setPrice] = useState(event.price);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ title, description, max_participants: maxParticipants, price });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Title</label>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
      </div>
      <div className="form-group">
        <label>Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          style={{ width: '100%', padding: '0.5rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}
        />
      </div>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <div className="form-group" style={{ flex: 1 }}>
          <label>Max Participants</label>
          <input
            type="number"
            value={maxParticipants}
            onChange={(e) => setMaxParticipants(parseInt(e.target.value))}
            min={1}
          />
        </div>
        <div className="form-group" style={{ flex: 1 }}>
          <label>Price (₹)</label>
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(parseFloat(e.target.value))}
            min={0}
            step={0.01}
          />
        </div>
      </div>
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <button type="submit" className="btn btn-primary btn-sm">Save</button>
        <button type="button" className="btn btn-secondary btn-sm" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
}

export default FacilitatorDashboard;
