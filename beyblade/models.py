
#PLACEHOLDER COLUMNS FOR DB

from datetime import datetime
from . import db
 
 
class User(db.Model):
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
 
    events = db.relationship("Event", backref="creator", lazy=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)
 
    def __repr__(self):
        return f"<User {self.username}>"
 
 
class Tournament(db.Model): #note this is Event 
    __tablename__ = "tournaments"

    #id = db.Column(db.Integer, primary_key=True)
    tourney_title = db.Column(db.String(120), nullable=False)
    tourney_category = db.Column(db.String(30), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_addy_hall = db.Column(db.String(200), nullable=False)
    tb_banner_image = db.Column(db.String(100), nullable=False)
    description_rules = db.Column(db.Text, nullable=False)


    point_cap = db.Column(db.Integer, default=4)
    gear_compliance = db.Column(db.String(100))
    stadium = db.Column(db.String(100))
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    #id = db.Column(db.Integer, primary_key=True)

    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    acknowledgement = db.Column(db.String(50), nullable=False, default='generic')
    acknowledgement_details = db.Column(db.String(300), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
    #user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rego = db.relationship("Registration", backref="tournament", lazy=True)
 
    def __repr__(self):
        return f"<Tournament {self.tourney_title}>"
 
 
class Booking(db.Model):
    __tablename__ = "bookings"
 
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
 
    username = db.Column(db.String(100), db.ForeignKey("users.username"), nullable=False) #idk if this is how we want to do registration though. for now using username, but might want reg to have user id too
    tournament_name = db.Column(db.String(150), db.ForeignKey("tournaments.title"), nullable=False) #rule: open events can't have the same name. might want tournament id though - tbc
 
    def __repr__(self):
        return f"<Booking {self.id}>"


#tbc - comments 

