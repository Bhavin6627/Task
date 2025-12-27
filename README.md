# Booking System for Sessions & Retreats

## Requirements

- Python 3.8+
- Node.js 18+

## Setup

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

## Run

**Terminal 1 - Main API (Port 5000):**
```bash
python app.py
```

**Terminal 2 - CRM API (Port 5001):**
```bash
python crm_app.py
```

**Terminal 3 - Frontend (Port 5173):**
```bash
cd frontend
npm run dev
```

## Usage

Open http://localhost:5173

### User Login
Register a new account or login to:
- Browse available events
- Book sessions and retreats
- View your bookings

### Facilitator Login
Click "Facilitator" in the navbar and use these demo accounts:

| Username | Password | Name |
|----------|----------|------|
| priya | priya123 | Dr. Priya Sharma |
| arjun | arjun123 | Arjun Patel |
| kavya | kavya123 | Kavya Reddy |

Facilitators can:
- View registered users
- Edit session details
- Cancel sessions


Project Overview

This project implements a booking system for sessions and retreats with a separate CRM service for facilitators.
It allows users to browse events, book sessions, and view bookings, while facilitators can manage events and view registered users.

The system is built using Flask (Python) for backend services and a React-based frontend for user interaction.

🧱 System Architecture

The application follows a multi-service architecture:

Service	Port	Description
Main Backend API	5000	User authentication, events, bookings
CRM / Facilitator API	5001	Facilitator operations & booking notifications
Frontend	5173	User & facilitator interface
🛠 Tech Stack

Backend: Python, Flask, Flask-JWT-Extended

Frontend: React, Vite

Authentication: JWT

Inter-service Security: Bearer Token

Database: Logical relational models (SQLite / in-memory for demo)

⚙️ Setup Instructions
Backend Setup
python -m venv env
env\Scripts\activate
pip install -r task/requirements.txt

Run Services
# Terminal 1
python task/app.py

# Terminal 2
python task/crm_app.py

Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:
👉 http://localhost:5173

🔐 Authentication
JWT Authentication

Used for user login

JWT token is passed in headers

Authorization: Bearer <JWT_TOKEN>

The Diagram Of :

```markdown
![System Architecture Diagram](Diagram/ER.png)
```

This will embed the ER diagram image at the placeholder location. Make sure the `Diagram/ER.png` file path is correct relative to your README.md location.

1.   CRM Notification Logic

When a user books a session:

Booking is stored in the main backend

Backend sends a POST request to CRM

CRM validates and logs the booking

CRM responds with success or error

CRM Notify Endpoint
POST /notify

Sample Payload
{
  "booking_id": 101,
  "user": "Bhavin",
  "event": "Meditation Retreat",
  "facilitator_id": 2
}




🔐 Secure Communication Between Services

CRM endpoints are protected using a static Bearer Token.

Authorization Header
Authorization: Bearer CRM_SECRET_123

Security Behavior

Missing/invalid token → 401 Unauthorized

Valid token → Request processed



📘 API Documentation
Base URLs

Main API: http://127.0.0.1:5000

CRM API: http://127.0.0.1:5001




🔵 Main Backend API (Port 5000)
Method	Endpoint	Description
POST	/auth/register	Register user
POST	/auth/login	Login user (JWT)
GET	/events	List all events
POST	/book	Book a session
GET	/bookings	View user bookings




🟢 CRM / Facilitator API (Port 5001)
Method	Endpoint	Description
POST	/notify	Receive booking notification
GET	/api/facilitator/<id>/events	View facilitator events
GET	/api/facilitator/<id>/bookings	View facilitator bookings
PUT	/api/facilitator/<id>/events/<event_id>	Modify event
DELETE	/api/facilitator/<id>/events/<event_id>	Cancel event



💳Bonus: Payments & Refund Roadmap (Detailed)

This section outlines a future-ready plan to integrate online payments and refunds into the booking system in a secure and scalable manner.

🔹 Phase 1: Payment Integration
🎯 Goal

Ensure that bookings are confirmed only after successful payment.

🧩 Payment Gateway Selection

The system can integrate with industry-standard gateways such as:

Stripe (International)

Razorpay (India)

Both provide:

Secure card & UPI payments

Webhooks for payment confirmation

Automated refund APIs

🛠 Payment Flow (Step-by-Step)

User initiates booking

User selects a session or retreat

Clicks “Book & Pay”

Payment Order Creation

Backend creates a payment order via gateway API

Order ID is returned to frontend

User Completes Payment

Payment UI opens (Stripe Checkout / Razorpay Modal)

User completes payment securely

Payment Verification

Gateway sends payment success response

Backend verifies signature / webhook

Booking Confirmation

Only after successful payment:

Booking is marked as confirmed

Booking is stored in database

CRM is notified






 Booking Table Enhancement


Additional fields to support payments:

payment_id

payment_status (pending, success, failed)

payment_provider (stripe, razorpay)

amount_paid

currency

🔹 Phase 2: Refund Process (Session Cancellation)




Goal

Automatically refund users if a session is cancelled by the facilitator.




 Refund Flow (Step-by-Step)

Facilitator Cancels Session

Facilitator cancels an event via CRM

Event status changes to cancelled

Identify Affected Bookings

System finds all bookings for that event

Filters only payment_status = success

Initiate Refund

Backend calls gateway refund API

Refund is linked to original payment ID

Update Booking Status

Booking status → refunded

Refund ID stored for reference

User Notification

User receives notification (email / in-app)

Refund confirmation shared



 Refund Tracking Fields

Additional fields:

refund_id

refund_status (initiated, processed, failed)

refunded_at



 Security Practices Used

JWT-based authentication

Role-based access control

Bearer token for inter-service security

Payload validation

Proper HTTP status codes

CORS enabled safely



 Deployment Status

Local deployment completed

Cloud deployment planned (Render / Railway / Vercel)




 Project Structure
task/
├── app.py
├── crm_app.py
├── task/requirements.txt
├── env/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md




 Conclusion

This project implements a complete booking system with secure CRM integration, clean API architecture, and scalable design.
It satisfies all required deliverables and includes a roadmap for future enhancements like payments and deployment.
