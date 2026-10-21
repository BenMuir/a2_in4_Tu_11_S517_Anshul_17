from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TelField, SelectField, TextAreaField, IntegerField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, Regexp, NumberRange, ValidationError
from wtforms.fields import DateTimeLocalField
from datetime import date

# --- AI SEARCH FORM ---
class AISearchForm(FlaskForm):
    search_query = StringField('What kind of tournament are you looking for?', validators=[DataRequired()])
    submit = SubmitField('Search with AI')

# --- AUTHENTICATION FORMS ---
# Login form - users sign in with their email and password
class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired('Enter your email address')])
    password = PasswordField('Password', validators=[InputRequired('Enter your password')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=50)])
    surname = StringField('Surname', validators=[InputRequired(), Length(max=50)])
    email = EmailField('Email Address', validators=[
        InputRequired(),
        Email('Please enter a valid email address'),
        Length(max=120)])
    contact_number = TelField('Contact Number', validators=[
        InputRequired(),
        Regexp(r'^\+?[0-9 ]{8,15}$', message='Enter a valid phone number (digits and spaces only)')])
    street_address = StringField('Street Address', validators=[InputRequired(), Length(max=200)])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message='Password must be at least 8 characters')])
    confirm = PasswordField('Confirm Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Account')

# --- TOURNAMENT FORM ---
class TournamentForm(FlaskForm):
    title = StringField('Tournament Title', validators=[DataRequired(), Length(max=120)])
    category = SelectField('Tournament Category', choices=[
        ('', 'Select format category...'), 
        ('deck3v3', '3v3 Deck'),
        ('swiss1v1', '1v1 Swiss'), 
        ('limited', 'Limited Format'), 
        ('freeplay', 'Casual Free-Play')
    ], validators=[DataRequired()])
    
    start_time = DateTimeLocalField('Date & Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired(), Length(max=200)])
    
    image = SelectField('Banner Image', choices=[
        ('event-deck3v3.jpg', 'Preset: 3v3 Team Stadium Setup'),
        ('event-swiss.jpg', 'Preset: 1v1 Swiss'),
        ('event-freeplay.jpg', 'Preset: Casual Free-Play')
    ], validators=[DataRequired()])
        
    description = TextAreaField('Description', validators=[DataRequired()])
    capacity = IntegerField('Capacity', default=32, validators=[DataRequired(), NumberRange(min=1)])
    price = DecimalField('Registration Fee', places=2, default=15.00, validators=[DataRequired(), NumberRange(min=0)])
    
    submit = SubmitField('Publish Tournament')

    def validate_start_time(self, field): 
        if field.data and field.data.date() < date.today():
            raise ValidationError("The tournament date can't be in the past.")