from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from . import db
from .models import Tournament, Comment
from .forms import AISearchForm, TournamentForm
from google import genai
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load the hidden variables from your .env file
load_dotenv()

# Set up the AI Client safely using the environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
            host_id=current_user.id  # Automatically links to the logged-in user
        )
        
        db.session.add(new_tournament)
        db.session.commit()
        
        flash(f'Successfully created tournament: {new_tournament.title}', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('create-event.html', form=form)

# --- NEW AI SEARCH ROUTE ---
@bp.route('/search', methods=['GET', 'POST'])
def ai_search():
    form = AISearchForm()
    results = []
    ai_explanation = ""

    if request.method == 'POST':
        print("--- FORM SUBMITTED ---")

    if form.validate_on_submit():
        user_text = form.search_query.data
        print(f"SUCCESS: Form passed! User searched for: {user_text}")
        
        try:
            prompt = f"""
            The user is searching for a Beyblade X tournament. 
            User query: "{user_text}"
            Extract 1 to 3 core search keywords (like location, style, or format). 
            Return ONLY the keywords separated by spaces, nothing else.
            """
            
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt
            )
            
            keywords = response.text.strip().split()
            print(f"SUCCESS: AI Extracted Keywords: {keywords}")
            ai_explanation = f"AI understood your search as: {', '.join(keywords)}"

        except Exception as e:
            print(f"API OVERLOADED (503). Using fallback search. Error: {str(e)}")
            # Fallback: If AI fails, manually split the sentence so the site doesn't break
            keywords = user_text.strip().split()
            ai_explanation = f"AI servers busy. Using standard keyword fallback: {', '.join(keywords)}"
            flash("AI is currently experiencing high demand. Used standard search instead.", "warning")

        # --- REAL DATABASE SEARCH ---
        # Start by looking only at open tournaments
        query = Tournament.query.filter(Tournament.status == 'open')
        
        # Chain filters so the tournament must match every AI keyword extracted
        for kw in keywords:
            search_term = f"%{kw}%"
            # The keyword can be found in the title, category, venue, OR description (case-insensitive)
            query = query.filter(
                or_(
                    Tournament.title.ilike(search_term),
                    Tournament.category.ilike(search_term),
                    Tournament.venue.ilike(search_term),
                    Tournament.description.ilike(search_term)
                )
            )
            
        # Execute the query and store the actual Tournament objects
        results = query.all()

    return render_template('search.html', form=form, results=results, ai_explanation=ai_explanation)