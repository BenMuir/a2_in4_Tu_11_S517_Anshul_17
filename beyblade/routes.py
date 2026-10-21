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
            host_id=current_user.id  # Automatically links to the logged-in user
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
    
    # Security check: Does the event have enough capacity?
    if tournament.capacity < quantity:
        flash('Sorry, there are not enough slots left for this event.', 'danger')
        return redirect(url_for('main.event_details', id=tournament.id))
        
    # Calculate total price
    total_paid = quantity * tournament.price
    
    # Generate a random 5-digit order reference (e.g., XB-84920)
    order_ref = f"XB-{random.randint(10000, 99999)}"
    
    # Create the booking record in the database
    new_booking = Booking(
        order_ref=order_ref,
        quantity=quantity,
        total_paid=total_paid,
        status='confirmed',
        user_id=current_user.id,
        tournament_id=tournament.id
    )
    
    # Deduct the tickets from the tournament's capacity
    tournament.capacity -= quantity
    
    # Automatically mark as sold out if capacity hits zero
    if tournament.capacity <= 0:
        tournament.status = 'sold_out'
        
    db.session.add(new_booking)
    db.session.commit()
    
    flash(f'Successfully booked {quantity} ticket(s)! Your order reference is {order_ref}.', 'success')
    return redirect(url_for('main.booking_history'))

# --- EDIT EVENT ROUTE ---
@bp.route('/edit-event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    tournament = Tournament.query.get_or_404(id)
    
    # Security check: Only the host can edit their own event
    if tournament.host_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('main.event_details', id=tournament.id))
        
    # Populate the form with the existing database data
    form = TournamentForm(obj=tournament)
    
    if form.validate_on_submit():
        tournament.title = form.title.data
        tournament.category = form.category.data
        tournament.start_time = form.start_time.data
        tournament.end_time = form.start_time.data + timedelta(hours=4)
        tournament.venue = form.venue.data
        tournament.description = form.description.data
        tournament.capacity = form.capacity.data
        tournament.price = form.price.data
        
        # Handle image upload if a new file was provided
        if form.custom_image.data and hasattr(form.custom_image.data, 'filename') and form.custom_image.data.filename:
            f = form.custom_image.data
            filename = secure_filename(f.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'img')
            os.makedirs(upload_dir, exist_ok=True)
            f.save(os.path.join(upload_dir, filename))
            tournament.image = filename
        else:
            tournament.image = form.default_image.data
        
        db.session.commit()
        flash(f'Successfully updated {tournament.title}!', 'success')
        return redirect(url_for('main.event_details', id=tournament.id))
        
    return render_template('edit-event.html', form=form, tournament=tournament)

# --- CANCEL EVENT ROUTE ---
@bp.route('/event/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_event(id):
    tournament = Tournament.query.get_or_404(id)
    
    # Security check: Only the host can cancel their own event
    if tournament.host_id != current_user.id:
        flash('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('main.event_details', id=tournament.id))
        
    # We change the status rather than deleting it so user booking histories don't break
    tournament.status = 'cancelled'
    db.session.commit()
    
    flash(f'Event "{tournament.title}" has been cancelled.', 'warning')
    return redirect(url_for('main.index'))

# --- NEW AI SEARCH ROUTE ---
@bp.route('/search', methods=['GET', 'POST'])
def ai_search():
    form = AISearchForm()
    results = []
    ai_explanation = ""

    if form.validate_on_submit():
        user_text = form.search_query.data
        print(f"SUCCESS: Form passed! User searched for: {user_text}")
        
        try:
            # Using flan-t5-large via standard text generation bypasses the provider routing errors
            prompt = f"Extract 1 to 3 core search keywords (like location, style, or format) from this query. Return ONLY the keywords separated by spaces.\n\nQuery: '{user_text}'\nKeywords:"
            
            response = client.text_generation(
                prompt,
                model="google/flan-t5-large",
                max_new_tokens=15
            )
            
            # Extract the text from the Hugging Face response
            keywords = response.strip().split()
            print(f"SUCCESS: AI Extracted Keywords: {keywords}")
            ai_explanation = f"AI understood your search as: {', '.join(keywords)}"

        except Exception as e:
            print(f"API ERROR OR MISSING KEY. Using fallback search. Error: {str(e)}")
            # Fallback: If AI fails, manually split the sentence so the site doesn't break
            keywords = user_text.strip().split()
            query = Tournament.query.filter(Tournament.status == 'open')
            for kw in keywords:
                search_term = f"%{kw}%"
                query = query.filter(
                    or_(
                        Tournament.title.ilike(search_term),
                        Tournament.category.ilike(search_term),
                        Tournament.venue.ilike(search_term),
                        Tournament.description.ilike(search_term)
                    )
                )
            results = query.all()
            ai_explanation = f"AI processing error. Using standard keyword fallback: {', '.join(keywords)}"

    return render_template('search.html', form=form, results=results, ai_explanation=ai_explanation)

# --- ERROR HANDLERS ---
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500