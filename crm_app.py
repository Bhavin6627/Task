from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from config import CRMConfig
from crm_models import db, Notification, CRMEvent

# Create Flask app
app = Flask(__name__)

# Enable CORS for frontend
CORS(app)

# Load configuration
app.config['SQLALCHEMY_DATABASE_URI'] = CRMConfig.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CRMConfig.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize database
db.init_app(app)


def require_bearer_token(f):
    """Decorator to require Bearer token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401
        
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        token = parts[1]
        
        if token != CRMConfig.BEARER_TOKEN:
            return jsonify({'error': 'Invalid token'}), 403
        
        return f(*args, **kwargs)
    
    return decorated


@app.route('/')
def index():
    return {
        'name': 'CRM/Facilitator API',
        'version': '1.0.0',
        'endpoints': {
            'notify': 'POST /notify',
            'facilitator_bookings': 'GET /api/facilitator/<id>/bookings',
            'facilitator_events': 'GET /api/facilitator/<id>/events',
            'modify_event': 'PUT /api/facilitator/<id>/events/<event_id>',
            'cancel_event': 'DELETE /api/facilitator/<id>/events/<event_id>'
        }
    }


@app.route('/notify', methods=['POST'])
@require_bearer_token
def receive_notification():
    """Receive booking notifications from the main booking system"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    required_fields = ['booking_id', 'user', 'event', 'facilitator_id']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing': missing_fields
        }), 400
    
    # Create notification record
    user_data = data.get('user', {})
    event_data = data.get('event', {})
    
    notification = Notification(
        booking_id=data['booking_id'],
        user_id=user_data.get('id'),
        user_username=user_data.get('username'),
        user_email=user_data.get('email'),
        event_id=event_data.get('id'),
        event_title=event_data.get('title'),
        event_type=event_data.get('event_type'),
        event_start_time=event_data.get('start_time'),
        event_end_time=event_data.get('end_time'),
        facilitator_id=data['facilitator_id'],
        booked_at=data.get('booked_at')
    )
    
    db.session.add(notification)
    db.session.commit()
    
    print(f'[CRM] Received booking notification: Booking #{notification.booking_id} for {notification.event_title}')
    
    return jsonify({
        'message': 'Notification received successfully',
        'notification_id': notification.id
    }), 200


@app.route('/api/facilitator/<int:facilitator_id>/bookings', methods=['GET'])
@require_bearer_token
def get_facilitator_bookings(facilitator_id):
    """Get all bookings (notifications) for a specific facilitator"""
    notifications = Notification.query.filter_by(facilitator_id=facilitator_id).all()
    
    return jsonify({
        'facilitator_id': facilitator_id,
        'bookings': [n.to_dict() for n in notifications],
        'total': len(notifications)
    }), 200


@app.route('/api/facilitator/<int:facilitator_id>/events', methods=['GET'])
@require_bearer_token
def get_facilitator_events(facilitator_id):
    """Get all events for a specific facilitator"""
    events = CRMEvent.query.filter_by(facilitator_id=facilitator_id).all()
    
    return jsonify({
        'facilitator_id': facilitator_id,
        'events': [e.to_dict() for e in events],
        'total': len(events)
    }), 200


@app.route('/api/facilitator/<int:facilitator_id>/events/<int:event_id>', methods=['PUT'])
@require_bearer_token
def modify_event(facilitator_id, event_id):
    """Modify an event's details"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    event = CRMEvent.query.filter_by(id=event_id, facilitator_id=facilitator_id).first()
    
    if not event:
        return jsonify({'error': 'Event not found or not authorized'}), 404
    
    # Update allowed fields
    allowed_fields = ['title', 'description', 'max_participants', 'price']
    
    for field in allowed_fields:
        if field in data:
            setattr(event, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Event updated successfully',
        'event': event.to_dict()
    }), 200


@app.route('/api/facilitator/<int:facilitator_id>/events/<int:event_id>', methods=['DELETE'])
@require_bearer_token
def cancel_event(facilitator_id, event_id):
    """Cancel an event"""
    event = CRMEvent.query.filter_by(id=event_id, facilitator_id=facilitator_id).first()
    
    if not event:
        return jsonify({'error': 'Event not found or not authorized'}), 404
    
    event.is_active = False
    db.session.commit()
    
    return jsonify({
        'message': 'Event cancelled successfully',
        'event': event.to_dict()
    }), 200


@app.route('/api/facilitator/login', methods=['POST'])
def facilitator_login():
    """Facilitator login endpoint"""
    from crm_models import CRMFacilitator
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'error': 'Missing username or password'}), 400
    
    facilitator = CRMFacilitator.query.filter_by(username=username).first()
    
    if not facilitator or not facilitator.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'message': 'Login successful',
        'facilitator': facilitator.to_dict()
    }), 200


def seed_facilitators():
    """Seed demo facilitators"""
    from crm_models import CRMFacilitator
    
    facilitators_data = [
        {
            'username': 'priya',
            'password': 'priya123',
            'name': 'Dr. Priya Sharma',
            'email': 'priya@wellness.in',
            'specialization': 'Mindfulness & Meditation'
        },
        {
            'username': 'arjun',
            'password': 'arjun123',
            'name': 'Arjun Patel',
            'email': 'arjun@wellness.in',
            'specialization': 'Yoga & Pranayama'
        },
        {
            'username': 'kavya',
            'password': 'kavya123',
            'name': 'Kavya Reddy',
            'email': 'kavya@wellness.in',
            'specialization': 'Sound Healing & Therapy'
        }
    ]
    
    for data in facilitators_data:
        existing = CRMFacilitator.query.filter_by(username=data['username']).first()
        if not existing:
            f = CRMFacilitator(
                username=data['username'],
                name=data['name'],
                email=data['email'],
                specialization=data['specialization']
            )
            f.set_password(data['password'])
            db.session.add(f)
    
    db.session.commit()
    print(f'[CRM] Facilitators seeded: {CRMFacilitator.query.count()} total')


# Create tables and seed data on startup
with app.app_context():
    db.create_all()
    seed_facilitators()


if __name__ == '__main__':
    print('Starting CRM/Facilitator API on port 5001...')
    app.run(debug=True, port=5001)

