from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from . import db
from .models import Tournament, Comment, Booking
from .forms import AISearchForm, TournamentForm
# REMOVED FOR DEPLOYMENT: from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
import os
import random
from datetime import timedelta

# Load the hidden variables from the .env file
load_dotenv()

# REMOVED FOR DEPLOYMENT: model = SentenceTransformer('all-MiniLM-L6-v2')

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Fetch all open tournaments, ordered by start time
    tournaments = Tournament.query.filter_by(status='open').order_by(Tournament.start_time).all()
    return render_template('index.html', tournaments=tournaments)

@bp.route('/booking-history')
@login_required
def booking_history():
    return render_template('booking-history.html')

# --- EVENT DETAILS ROUTE ---
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
        # Create the new tournament record
        new_tournament = Tournament(
            title=form.title.data,
            category=form.category.data,
            start_time=form.start_time.data,
            # Database constraint requires end_time > start_time. 
            # Defaulting to 4 hours later since it is not in the form yet.
            end_time=form.start_time.data + timedelta(hours=4),
            venue=form.venue.data,
            image=form.image.data,
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
    # Send them to their dashboard so they can see their new ticket
    return redirect(url_for('main.booking_history'))

# --- FALLBACK SEARCH ROUTE (LITE VERSION) ---
@bp.route('/search', methods=['GET', 'POST'])
def ai_search():
    form = AISearchForm()
    results = []
    ai_explanation = ""

    if form.validate_on_submit():
        user_text = form.search_query.data
        print(f"SUCCESS: Form passed! User searched for: {user_text}")
        
        try:
            # FORCE FALLBACK FOR PYTHONANYWHERE DEPLOYMENT
            raise Exception("AI Search disabled for cloud deployment. Forcing fallback.")

        except Exception as e:
            print(f"Embedding disabled. Using fallback search. Error: {str(e)}")
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
            ai_explanation = f"Cloud deployment active. Using standard keyword match for: {', '.join(keywords)}"

    return render_template('search.html', form=form, results=results, ai_explanation=ai_explanation)

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
        tournament.image = form.image.data
        tournament.description = form.description.data
        tournament.capacity = form.capacity.data
        tournament.price = form.price.data
        
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

# --- ERROR HANDLERS ---
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500