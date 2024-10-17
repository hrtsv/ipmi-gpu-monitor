from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
import os
import logging

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    with app.app_context():
        # Import models here to ensure they are registered with SQLAlchemy
        from app.models import SensorData
        db.create_all()
        app.logger.info("Database initialized")

    from app.routes import main
    app.register_blueprint(main)

    @app.route('/health')
    def health_check():
        return "OK", 200

    return app