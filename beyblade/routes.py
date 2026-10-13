from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from sqlalchemy import or_
from .models import Tournament
from .forms import AISearchForm
from google import genai
from dotenv import load_dotenv
import os

# Load the hidden variables from your .env file
load_dotenv()

# Set up the AI Client safely using the environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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