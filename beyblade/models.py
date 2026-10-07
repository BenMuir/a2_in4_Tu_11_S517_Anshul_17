from datetime import datetime
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    # Only the hashed password is ever stored, never the plain text
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Used wherever we show who someone is (navbar, comments, bookings)
    @property
    def full_name(self):
        return f"{self.first_name} {self.surname}"

    def __repr__(self):
        return f"<User {self.email}>"
