import { useState, useEffect } from 'react';
import Auth from './components/Auth';
import Events from './components/Events';
import Bookings from './components/Bookings';
import FacilitatorDashboard from './components/FacilitatorDashboard';
import { getToken, logout } from './api';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('events');
  const [loginTime, setLoginTime] = useState(Date.now());

  useEffect(() => {
    // Check if user is already logged in
    const token = getToken();
    if (token) {
      setUser({ username: 'User' });
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentPage('events');
    setLoginTime(Date.now()); // Force remount of Events
  };

  const handleLogout = () => {
    logout();
    setUser(null);
  };

  if (!user) {
    return (
      <div className="app">
        <nav className="navbar">
          <h1>🧘 Wellness Booking</h1>
          <div className="nav-links">
            <button
              className={currentPage !== 'facilitator' ? 'active' : ''}
              onClick={() => setCurrentPage('login')}
            >
              User Login
            </button>
            <button
              className={currentPage === 'facilitator' ? 'active' : ''}
              onClick={() => setCurrentPage('facilitator')}
            >
              Facilitator
            </button>
          </div>
        </nav>
        {currentPage === 'facilitator' ? (
          <FacilitatorDashboard />
        ) : (
          <Auth onLogin={handleLogin} />
        )}
      </div>
    );
  }

  return (
    <div className="app">
      <nav className="navbar">
        <h1>🧘 Wellness Booking</h1>
        <div className="nav-links">
          <button
            className={currentPage === 'events' ? 'active' : ''}
            onClick={() => setCurrentPage('events')}
          >
            Events
          </button>
          <button
            className={currentPage === 'bookings' ? 'active' : ''}
            onClick={() => setCurrentPage('bookings')}
          >
            My Bookings
          </button>
          <button
            className={currentPage === 'facilitator' ? 'active' : ''}
            onClick={() => setCurrentPage('facilitator')}
          >
            Facilitator
          </button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {currentPage === 'events' && <Events key={loginTime} />}
      {currentPage === 'bookings' && <Bookings key={loginTime} />}
      {currentPage === 'facilitator' && <FacilitatorDashboard />}
    </div>
  );
}

export default App;

