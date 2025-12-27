from datetime import datetime, timedelta
from models import db, User, Facilitator, Event


def seed_database():
    """Seed the database with sample data"""
    
    # Create sample facilitators (Indian names)
    facilitators = [
        Facilitator(
            name='Dr. Priya Sharma',
            email='priya@wellness.in',
            specialization='Mindfulness & Meditation'
        ),
        Facilitator(
            name='Arjun Patel',
            email='arjun@wellness.in',
            specialization='Yoga & Pranayama'
        ),
        Facilitator(
            name='Kavya Reddy',
            email='kavya@wellness.in',
            specialization='Sound Healing & Therapy'
        )
    ]
    
    for f in facilitators:
        existing = Facilitator.query.filter_by(email=f.email).first()
        if not existing:
            db.session.add(f)
    
    db.session.commit()
    
    # Get facilitators
    priya = Facilitator.query.filter_by(email='priya@wellness.in').first()
    arjun = Facilitator.query.filter_by(email='arjun@wellness.in').first()
    kavya = Facilitator.query.filter_by(email='kavya@wellness.in').first()
    
    # Create sample events (Indian context)
    now = datetime.utcnow()
    
    events = [
        Event(
            title='Morning Meditation Session',
            description='Start your day with a peaceful guided meditation session at our Rishikesh center. Perfect for beginners and experienced practitioners alike.',
            event_type='session',
            start_time=now + timedelta(days=1, hours=8),
            end_time=now + timedelta(days=1, hours=9),
            max_participants=15,
            price=500.00,
            facilitator_id=priya.id
        ),
        Event(
            title='Weekend Yoga Retreat - Coorg',
            description='A transformative 2-day yoga retreat in the hills of Coorg, Karnataka. Includes sattvic meals, accommodation, and multiple yoga sessions.',
            event_type='retreat',
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=9),
            max_participants=20,
            price=8500.00,
            facilitator_id=arjun.id
        ),
        Event(
            title='Sound Bath Healing',
            description='Experience deep relaxation through the healing vibrations of Tibetan singing bowls and traditional Indian instruments.',
            event_type='session',
            start_time=now + timedelta(days=3, hours=18),
            end_time=now + timedelta(days=3, hours=19, minutes=30),
            max_participants=12,
            price=800.00,
            facilitator_id=kavya.id
        ),
        Event(
            title='Pranayama Workshop',
            description='Learn powerful breathing techniques from ancient Indian traditions for stress relief, energy, and emotional balance.',
            event_type='session',
            start_time=now + timedelta(days=5, hours=10),
            end_time=now + timedelta(days=5, hours=12),
            max_participants=10,
            price=1200.00,
            facilitator_id=arjun.id
        ),
        Event(
            title='Silent Meditation Retreat - Dharamsala',
            description='A 3-day silent retreat in the serene mountains of Dharamsala. Includes guided Vipassana sessions and mindful meals.',
            event_type='retreat',
            start_time=now + timedelta(days=14),
            end_time=now + timedelta(days=17),
            max_participants=8,
            price=12000.00,
            facilitator_id=priya.id
        )
    ]
    
    for e in events:
        existing = Event.query.filter_by(title=e.title).first()
        if not existing:
            db.session.add(e)
    
    db.session.commit()
    
    print('Database seeded successfully!')
    print(f'  - Facilitators: {Facilitator.query.count()}')
    print(f'  - Events: {Event.query.count()}')


if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_database()
