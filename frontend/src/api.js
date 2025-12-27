const API_URL = 'http://localhost:5000';

// Store token in localStorage
export const setToken = (token) => {
  localStorage.setItem('token', token);
};

export const getToken = () => {
  return localStorage.getItem('token');
};

export const removeToken = () => {
  localStorage.removeItem('token');
};

// API helper with auth header
const apiRequest = async (endpoint, options = {}) => {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || data.msg || 'Something went wrong');
  }

  return data;
};

// Auth API
export const register = async (username, email, password) => {
  return apiRequest('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  });
};

export const login = async (username, password) => {
  const data = await apiRequest('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  if (data.access_token) {
    setToken(data.access_token);
  }
  return data;
};

export const logout = () => {
  removeToken();
};

// Events API
export const getEvents = async () => {
  return apiRequest('/api/events');
};

export const getEvent = async (eventId) => {
  return apiRequest(`/api/events/${eventId}`);
};

// Bookings API
export const createBooking = async (eventId) => {
  return apiRequest('/api/bookings', {
    method: 'POST',
    body: JSON.stringify({ event_id: eventId }),
  });
};

export const getBookings = async () => {
  return apiRequest('/api/bookings');
};

export const cancelBooking = async (bookingId) => {
  return apiRequest(`/api/bookings/${bookingId}`, {
    method: 'DELETE',
  });
};
