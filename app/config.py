import os
import json
from datetime import timedelta

class Config:
    @staticmethod
    def load_secrets():
        secrets_file = '/app/secrets.json'
        if os.path.exists(secrets_file):
            with open(secrets_file, 'r') as f:
                return json.load(f)
        return {}

    secrets = load_secrets()
    
    SECRET_KEY = secrets.get('SECRET_KEY') or os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    JWT_SECRET_KEY = secrets.get('JWT_SECRET_KEY') or os.environ.get('JWT_SECRET_KEY') or 'fallback-jwt-secret-key'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    IPMI_HOST = os.environ.get('IPMI_HOST')
    IPMI_USERNAME = os.environ.get('IPMI_USERNAME')
    IPMI_PASSWORD = os.environ.get('IPMI_PASSWORD')