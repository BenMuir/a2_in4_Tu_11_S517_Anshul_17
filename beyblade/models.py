from datetime import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)
    # Only the hashed password is ever stored, never the plain text
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    # one-to-many: a user can make many bookings
    bookings = db.relationship('Booking', backref='user', cascade='all, delete-orphan')
    # one-to-many: a user can post many comments
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')
    # one-to-many: a user can host many tournaments
    tournaments_hosted = db.relationship('Tournament', backref='host')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User {self.id} {self.username!r}>"