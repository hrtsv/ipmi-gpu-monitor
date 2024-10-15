from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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

class SensorData(db.Model):
    # ... (rest of the SensorData model remains unchanged)