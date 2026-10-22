from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, EmailField, TelField, SelectField, TextAreaField, IntegerField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, Regexp, NumberRange, ValidationError
from wtforms.fields import DateTimeLocalField
from datetime import date
import re

# SEARCH FORM
# Submitted with GET (?search_query=...&mode=...) so a search can be linked to or bookmarked.
# Searching doesn't change any data, so it doesn't need a CSRF token.
class AISearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_query = StringField('What kind of tournament are you looking for?', validators=[DataRequired()])
    mode = RadioField('Search type', choices=[
        ('ai', 'Smart search (AI) - matches the meaning of your words'),
        ('keyword', 'Keyword search - matches the exact words')
    ], default='ai')
    submit = SubmitField('Search')

# AUTHENTICATION FORMS
# Login form - users sign in with their email and password
class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired('Enter your email address')])
    password = PasswordField('Password', validators=[InputRequired('Enter your password')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

# Registration form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=50)])
    email = EmailField('Email Address', validators=[
        InputRequired(),
        Email('Please enter a valid email address'),
        Length(max=120)])
    contact_number = TelField('Contact Number', validators=[
        InputRequired(),
        Regexp(r'^\+?[0-9 ]{8,15}$', message='Enter a valid phone number (digits and spaces only)')])
    street_address = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message='Password must be at least 8 characters')])
    confirm = PasswordField('Confirm Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Account')

# TOURNAMENT FORM
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
    
    default_image = SelectField('Default Event Image', choices=[
        ('event-deck3v3.jpg', 'Preset: 3v3 Team Stadium Setup'),
        ('event-swiss.jpg', 'Preset: 1v1 Swiss'),
        ('event-freeplay.jpg', 'Preset: Casual Free-Play')
    ], default='event-deck3v3.jpg')
    
    custom_image = FileField('Or Upload a Custom Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

    ack_statement = SelectField('Acknowledgement of Country', choices=[
        ('none', 'No Acknowledgement'),
        ('generic', 'Use Generic Acknowledgement (Recommended)'),
        ('enhanced', 'Write a Custom/Enhanced Acknowledgement')
    ], default='none')
    
    custom_ack_text = TextAreaField('Your Acknowledgement', validators=[Length(max=500)], render_kw={"placeholder": "Name the Traditional Owners of your venue, recognise their continuing connection to Country, and pay your respects in your own words..."})

    description = TextAreaField('Description', validators=[DataRequired()])
    capacity = IntegerField('Capacity', default=32, validators=[DataRequired(), NumberRange(min=1)])
    # InputRequired allows a price of 0 for free events
    price = DecimalField('Registration Fee', places=2, default=15.00, validators=[InputRequired(), NumberRange(min=0)])

    submit = SubmitField('Publish Tournament')

    def validate_start_time(self, field):
        if field.data and field.data.date() < date.today():
            raise ValidationError("The tournament date can't be in the past.")

    def validate_custom_ack_text(self, field):
        if self.ack_statement.data != 'enhanced':
            return
        text = (field.data or '').strip()
        if not text:
            raise ValidationError("Write your acknowledgement, or choose a different option.")
        if len(text) < 50:
            raise ValidationError("Your acknowledgement is very short. Name the Traditional Owners of your "
                                  "venue and pay your respects (at least 50 characters).")
        # Only Traditional Owners can give a Welcome to Country, so an event page shouldn't claim to
        if re.search(r'welcome\s+(\w+\s+){0,3}to\s+(this\s+)?country', text, re.IGNORECASE):
            raise ValidationError("Only Traditional Owners can give a Welcome to Country. Please word this as "
                                  "an acknowledgement instead.")