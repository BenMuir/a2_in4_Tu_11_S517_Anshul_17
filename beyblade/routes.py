from flask import Blueprint, render_template

# Define the blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/events/create')
def create_event():
    # Lauren will eventually attach her WTF form logic here
    return render_template('create-event.html')

@main_bp.route('/events/<int:event_id>')
def event_details(event_id):
    # The event_id parameter pre-empts Eric's database queries
    return render_template('event-details.html')

@main_bp.route('/history')
def booking_history():
    return render_template('booking-history.html')