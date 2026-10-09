from datetime import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)
    # Only the hashed password is ever stored, never the plain text
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # relationships
    # one-to-many: a user can make many bookings
    bookings = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')
    # one-to-many: a user can post many comments
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    # one-to-many: a user can host many tournaments
    tournaments_hosted = db.relationship('Tournament', back_populates='host', cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User {self.id} {self.email!r}>"
    
    
class Tournament(db.Model):
    __tablename__ = 'tournaments'
    __table_args__ = (
        db.CheckConstraint('end_time > start_time', name='ck_end_after_start'),
    )
        
    id = db.Column(db.Integer, primary_key=True)
        
    # General info (create-event.html: eventTitle / eventCategory / eventDateTime / eventVenue)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)   # e.g. '3v3 Deck Format', '1v1 Swiss'
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
        
    # Technical regulations (matchPoints / gearLegality / stadiumType)
    match_points = db.Column(db.Integer, default=4)
    gear_legality = db.Column(db.String(100), nullable=True)
    stadium_type = db.Column(db.String(100), nullable=True)
        
    # Capacity & ticketing (ticketCapacity / ticketPrice)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False, default=0)
        
    # Cultural protocol (none | generic | enhanced)
    ack_statement = db.Column(
        db.Enum('none', 'generic', 'enhanced',
            name='ack_statement',
            create_constraint=True,
            validate_strings=True),
            default='none',
            nullable=False,
            )
    
    custom_ack_text = db.Column(db.String(255), nullable=True)
        
    # Tournament status (open | sold_out | inactive | cancelled)
    status = db.Column(
        db.Enum('open', 'sold_out', 'inactive', 'cancelled',
            name='tournament_status',
            create_constraint=True,   # adds a CHECK constraint in the database
            validate_strings=True),   # rejects bad values in Python before the insert
            default='open',
            nullable=False,
            )
        
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)    
    
    host = db.relationship('User', back_populates='tournaments_hosted')
    
    bookings = db.relationship(
        'Booking',
        back_populates='tournament',
        lazy=True,
        cascade='all, delete-orphan',
    )

    comments = db.relationship(
        'Comment',
        back_populates='tournament',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='Comment.created_at',
    )
    
    def __repr__(self):
        return f'<Tournament {self.id} {self.title!r}>'
    
    
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    order_ref = db.Column(db.String(20), unique=True, nullable=False)  # e.g. 'XB-84920'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_paid = db.Column(db.Numeric(6, 2), nullable=False)
    
    status = db.Column(
    db.Enum('confirmed', 'attended', 'cancelled',
            name='booking_status',
            create_constraint=True,
            validate_strings=True),
    default='confirmed',
    nullable=False,
    )
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User', back_populates='bookings')
    tournament = db.relationship('Tournament', back_populates='bookings')

    def __repr__(self):
        return f'<Booking {self.order_ref} user={self.user_id} tournament={self.tournament_id}>'
   
    
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    body = db.Column(db.Text, nullable=False)
    is_host_reply = db.Column(db.Boolean, default=False)   # "Host" badge in event-details.html
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User', back_populates='comments')
    tournament = db.relationship('Tournament', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.id} by user={self.user_id} on tournament={self.tournament_id}>'
