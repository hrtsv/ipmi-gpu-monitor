from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    from flask_jwt_extended import JWTManager
    jwt = JWTManager()
    logger.info("JWT extension loaded successfully")
except ImportError as e:
    logger.error(f"Failed to import JWT: {e}")
    jwt = None

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Initialize extensions
    db.init_app(app)
    
    if jwt:
        app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
        jwt.init_app(app)
    
    with app.app_context():
        db.create_all()
        logger.info("Database initialized successfully")
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app