from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from . import db
from .models import Tournament, Comment, Booking
from .forms import AISearchForm, TournamentForm
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import random
from datetime import timedelta

# Load the hidden variables from your .env file
load_dotenv()

# Set up the Hugging Face Client safely using the environment variable
client = InferenceClient(api_key=os.getenv("HUGGINGFACE_API_KEY"))
# TEMPORARY TEST
client = InferenceClient(api_key="hf_your_actual_token_string_here")

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Fetch both open and sold-out tournaments, ordered by start time
    tournaments = Tournament.query.filter(Tournament.status.in_(['open', 'sold_out'])).order_by(Tournament.start_time).all()
    return render_template('index.html', tournaments=tournaments)

@bp.route('/booking-history')
@login_required
def booking_history():
    return render_template('booking-history.html')

# --- DYNAMIC EVENT DETAILS ROUTE ---
@bp.route('/event/<int:id>')
def event_details(id):
    # Fetch the specific tournament by its ID, or return a 404 error if it doesn't exist
    tournament = Tournament.query.get_or_404(id)
    return render_template('event-details.html', tournament=tournament)

# --- ADD COMMENT ROUTE ---
@bp.route('/event/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    tournament = Tournament.query.get_or_404(id)
    
    # Grab the text from the standard HTML form
    body = request.form.get('body')
    
    if body:
        new_comment = Comment(
            body=body,
            user_id=current_user.id,
            tournament_id=tournament.id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        
    return redirect(url_for('main.event_details', id=tournament.id))

# --- EVENT CREATION ROUTE ---
@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = TournamentForm()
    
    if form.validate_on_submit():
        # Handle the image upload
        image_filename = form.default_image.data
        if form.custom_image.data and hasattr(form.custom_image.data, 'filename') and form.custom_image.data.filename:
            f = form.custom_image.data
            image_filename = secure_filename(f.filename)
            # Ensure the static/img directory exists
            upload_dir = os.path.join(current_app.root_path, 'static', 'img')
            os.makedirs(upload_dir, exist_ok=True)
            # Save the physical file
            f.save(os.path.join(upload_dir, image_filename))

        # Create the new tournament record
        new_tournament = Tournament(
            title=form.title.data,
            category=form.category.data,
            start_time=form.start_time.data,
            end_time=form.start_time.data + timedelta(hours=4),
            venue=form.venue.data,
            image=image_filename,
            description=form.description.data,
            capacity=form.capacity.data,
            price=form.price.data,
            host_id=current_user.id,  # Automatically links to the logged-in user
            ack_statement=form.ack_statement.data,
            custom_ack_text=form.custom_ack_text.data,
        )
        
        db.session.add(new_tournament)
        db.session.commit()
        
        flash(f'Successfully created tournament: {new_tournament.title}', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('create-event.html', form=form)

# --- BOOKING ROUTE ---
@bp.route('/event/<int:id>/book', methods=['POST'])
@login_required
def book_event(id):
    tournament = Tournament.query.get_or_404(id)
    
    # Grab the quantity the user selected from the dropdown
    quantity = int(request.form.get('quantity', 1))
    
    # Security check: