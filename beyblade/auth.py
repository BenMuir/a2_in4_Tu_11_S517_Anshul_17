from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        # Each email can only be used for one account
        if db.session.scalar(db.select(User).where(User.email == email)):
            form.email.errors.append('An account with that email already exists')
        else:
            user = User(first_name=form.first_name.data.strip(),
                        surname=form.surname.data.strip(),
                        email=email,
                        password_hash=generate_password_hash(form.password.data),
                        contact_number=form.contact_number.data.strip(),
                        street_address=form.street_address.data.strip())
            db.session.add(user)
            db.session.commit()
            # Log the new user straight in, then redirect (PRG pattern)
            login_user(user)
            flash(f'Welcome to X-Burst, {user.first_name}!', 'success')
            return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = db.session.scalar(db.select(User).where(User.email == email))
        # Same message for wrong email or password so we don't leak which accounts exist
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Incorrect email or password', 'danger')
        else:
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.first_name}!', 'success')
            # Send the user back to the page that required login, if it is on our site
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
                next_page = url_for('main.index')
            return redirect(next_page)

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
