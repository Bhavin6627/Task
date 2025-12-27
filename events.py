from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import Event

events_bp = Blueprint('events', __name__)


@events_bp.route('', methods=['GET'])
@jwt_required()
def get_all_events():
    """Get all bookable events"""
    events = Event.query.filter_by(is_active=True).all()
    return jsonify({
        'events': [event.to_dict() for event in events],
        'total': len(events)
    }), 200


@events_bp.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    """Get a specific event by ID"""
    event = Event.query.get(event_id)
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    return jsonify({'event': event.to_dict()}), 200
