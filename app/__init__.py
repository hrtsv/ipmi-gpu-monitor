from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder=os.path.abspath('app/templates'))
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app