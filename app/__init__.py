from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        logger.info("Database initialized successfully")
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app