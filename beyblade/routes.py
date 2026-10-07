
from flask import Blueprint, render_template, redirect, url_for, flash

from . import db
from .models import Tournament
from .forms import TournamentForm


bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")


@bp.route('/tournament/create', methods=['GET', 'POST'])
def create_tournament():
    form = TournamentForm()
    if form.validate_on_submit():
        tournament = Tournament()
        form.populate_obj(tournament)
        db.session.add(tournament)
        db.session.commit()
        flash(f'"{tournament.tourney_title}" has been published', 'success')
        return redirect(url_for('main.tournament_details', id=tournament.id))
    #return render_template('create-tournament.html', form=form)

@bp.route('/tournament/<int:id>') #Only if there's a tourney ID
def tournament_details(id):
    tournament = db.get_or_404(Tournament, id)
    return render_template('tournament-details.html', tournament=tournament)

#note that i'll have to swap <inputs> for form fields into html create-event with same classes

@bp.route("/booking")
def booking_history():
    return render_template("booking-history.html")