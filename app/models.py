from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_default_user(cls):
        default_user = cls.query.filter_by(username='admin').first()
        if not default_user:
            default_user = cls(username='admin')
            default_user.set_password('changeme')
            db.session.add(default_user)
            db.session.commit()

# SensorData model for storing temperature and fan readings
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensor_type = db.Column(db.String(64), nullable=False)  # Temperature or Fan
    sensor_name = db.Column(db.String(64), nullable=False)  # Name of the sensor (e.g., CPU, GPU)
    value = db.Column(db.Float, nullable=False)  # The value of the sensor (temperature or fan speed)

    def __repr__(self):
        return f'<SensorData {self.sensor_type} {self.sensor_name}: {self.value}>'

# SensorThreshold model to store acceptable temperature ranges for sensors
class SensorThreshold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_name = db.Column(db.String(64), nullable=False)  # Sensor name (e.g., CPU, GPU)
    min_value = db.Column(db.Float, nullable=False)  # Minimum acceptable temperature
    max_value = db.Column(db.Float, nullable=False)  # Maximum acceptable temperature

    def __repr__(self):
        return f'<SensorThreshold {self.sensor_name}: {self.min_value}-{self.max_value}>'
