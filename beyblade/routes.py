from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/create-event')
def create_event():
    return render_template('create-event.html')

@bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

@bp.route('/event-details')
def event_details():
    return render_template('event-details.html')