from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class CRMFacilitator(db.Model):
    """Facilitator model for CRM authentication"""
    __tablename__ = 'crm_facilitators'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialization = db.Column(db.String(200))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'specialization': self.specialization
        }


class Notification(db.Model):
    """Model to store booking notifications received from main API"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer)
    user_username = db.Column(db.String(80))
    user_email = db.Column(db.String(120))
    event_id = db.Column(db.Integer)
    event_title = db.Column(db.String(200))
    event_type = db.Column(db.String(50))
    event_start_time = db.Column(db.String(50))
    event_end_time = db.Column(db.String(50))
    facilitator_id = db.Column(db.Integer, nullable=False)
    booked_at = db.Column(db.String(50))
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'user': {
                'id': self.user_id,
                'username': self.user_username,
                'email': self.user_email
            },
            'event': {
                'id': self.event_id,
                'title': self.event_title,
                'event_type': self.event_type,
                'start_time': self.event_start_time,
                'end_time': self.event_end_time
            },
            'facilitator_id': self.facilitator_id,
            'booked_at': self.booked_at,
            'received_at': self.received_at.isoformat()
        }


class CRMEvent(db.Model):
    """Mirror of events for facilitator management"""
    __tablename__ = 'crm_events'
    
    id = db.Column(db.Integer, primary_key=True)
    original_event_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    max_participants = db.Column(db.Integer, default=20)
    price = db.Column(db.Float, default=0.0)
    facilitator_id = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'original_event_id': self.original_event_id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'max_participants': self.max_participants,
            'price': self.price,
            'facilitator_id': self.facilitator_id,
            'is_active': self.is_active
        }

