from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import requests
from models import db, Booking, Event, User
from config import Config

bookings_bp = Blueprint('bookings', __name__)


def notify_crm(booking, user, event):
    """Send notification to CRM/Facilitator system"""
    try:
        payload = {
            'booking_id': booking.id,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'event': {
                'id': event.id,
                'title': event.title,
                'event_type': event.event_type,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat()
            },
            'facilitator_id': event.facilitator_id,
            'booked_at': booking.booked_at.isoformat()
        }
        
        headers = {
            'Authorization': f'Bearer {Config.CRM_BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{Config.CRM_URL}/notify',
            json=payload,
            headers=headers,
            timeout=5
        )
        
        return response.status_code == 200
    except Exception as e:
        print(f'CRM notification failed: {e}')
        return False


@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or 'event_id' not in data:
        return jsonify({'error': 'event_id is required'}), 400
    
    event_id = data.get('event_id')
    
    # Get event
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    if not event.is_active:
        return jsonify({'error': 'Event is no longer available'}), 400
    
    # Check if already booked
    existing_booking = Booking.query.filter_by(
        user_id=user_id,
        event_id=event_id,
        status='confirmed'
    ).first()
    
    if existing_booking:
        return jsonify({'error': 'You have already booked this event'}), 409
    
    # Check capacity
    confirmed_bookings = Booking.query.filter_by(
        event_id=event_id,
        status='confirmed'
    ).count()
    
    if confirmed_bookings >= event.max_participants:
        return jsonify({'error': 'Event is fully booked'}), 400
    
    # Create booking
    booking = Booking(user_id=user_id, event_id=event_id)
    db.session.add(booking)
    db.session.commit()
    
    # Notify CRM
    user = User.query.get(user_id)
    crm_notified = notify_crm(booking, user, event)
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking': booking.to_dict(),
        'crm_notified': crm_notified
    }), 201


@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """Get all bookings for the current user"""
    user_id = int(get_jwt_identity())
    
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    now = datetime.utcnow()
    upcoming = []
    past = []
    
    for booking in bookings:
        if booking.event.start_time > now:
            upcoming.append(booking.to_dict())
        else:
            past.append(booking.to_dict())
    
    return jsonify({
        'upcoming': upcoming,
        'past': past,
        'total': len(bookings)
    }), 200


@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking"""
    user_id = int(get_jwt_identity())
    
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.status == 'cancelled':
        return jsonify({'error': 'Booking is already cancelled'}), 400
    
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({
        'message': 'Booking cancelled successfully',
        'booking': booking.to_dict()
    }), 200
