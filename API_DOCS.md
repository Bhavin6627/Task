# Booking System API Documentation

## Overview

Two Flask applications:
1. **Main Booking API** (Port 5000) - User authentication, events, bookings
2. **CRM/Facilitator API** (Port 5001) - Booking notifications, facilitator management

---

## Main Booking API (Port 5000)

### Authentication

#### Register User
```
POST /api/auth/register
```
```json
{
    "username": "rahul",
    "email": "rahul@gmail.com",
    "password": "password123"
}
```

#### Login
```
POST /api/auth/login
```
```json
{
    "username": "rahul",
    "password": "password123"
}
```
Returns `access_token` for authenticated requests.

---

### Events (Requires JWT)

Header: `Authorization: Bearer <access_token>`

#### Get All Events
```
GET /api/events
```

#### Get Event by ID
```
GET /api/events/<event_id>
```

---

### Bookings (Requires JWT)

Header: `Authorization: Bearer <access_token>`

#### Create Booking
```
POST /api/bookings
```
```json
{
    "event_id": 1
}
```

#### Get User Bookings
```
GET /api/bookings
```

#### Cancel Booking
```
DELETE /api/bookings/<booking_id>
```

---

## CRM/Facilitator API (Port 5001)

### Facilitator Login
```
POST /api/facilitator/login
```
```json
{
    "username": "priya",
    "password": "priya123"
}
```

### Get Facilitator Bookings
```
GET /api/facilitator/<facilitator_id>/bookings
```
Header: `Authorization: Bearer crm-secret-token-12345`

### Notify Endpoint (Internal)
```
POST /notify
```
Receives booking notifications from main API.

---

## Data Models

| Model | Fields |
|-------|--------|
| User | id, username, email, password_hash, created_at |
| Facilitator | id, name, email, specialization |
| Event | id, title, description, event_type, start_time, end_time, max_participants, price, facilitator_id |
| Booking | id, user_id, event_id, booked_at, status |
