from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# Hosting an event and viewing registrations require an account
@bp.route('/create-event')
@login_required
def create_event():
    return render_template('create-event.html')

@bp.route('/booking-history')
@login_required
def booking_history():
    return render_template('booking-history.html')

@bp.route('/event-details')
def event_details():
    return render_template('event-details.html')
