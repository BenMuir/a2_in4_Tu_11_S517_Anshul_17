from datetime import datetime
from flask_login import UserMixin
from . import db

# User

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # relationships
    bookings = db.relationship('Booking', backref='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')
    tournaments_hosted = db.relationship('Tournament', backref='host')
    
    def __repr__(self):
        return f'<User {self.id} {self.username!r}>'
    
    
    
    
    