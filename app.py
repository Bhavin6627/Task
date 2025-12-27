from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from config import Config
from models import db

# Create Flask app
app = Flask(__name__)

# Enable CORS for frontend
CORS(app)

# Load configuration
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Import and register blueprints
from auth import auth_bp
from events import events_bp
from bookings import bookings_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(events_bp, url_prefix='/api/events')
app.register_blueprint(bookings_bp, url_prefix='/api/bookings')


@app.route('/')
def index():
    return {
        'name': 'Booking System API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'events': '/api/events',
            'bookings': '/api/bookings'
        }
    }


# Create tables and seed data on startup
with app.app_context():
    db.create_all()
    
    # Seed if empty
    from models import Facilitator
    if Facilitator.query.count() == 0:
        from seed_data import seed_database
        seed_database()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
