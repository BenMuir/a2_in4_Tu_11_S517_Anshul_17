<<<<<<< HEAD
from wtforms import Form, BooleanField, StringField, PasswordField,DecimalField, validators, StringField, SelectField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError,InputRequired, Length, NumberRange, Optional
from wtforms.fields import DateTimeLocalField

#note login is compulsory to create a tournament, since this hasn't been created yet this is my placeholder:
class UserLoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])


class TournamentForm(Form):
    title = StringField('Tournament Title', validators=[InputRequired(), Length(max=120)])
    category = SelectField('Tournament Category', choices=[
        ('', 'Select format category...'), ('deck3v3', '3v3 Deck'),
        ('swiss1v1', '1v1 Swiss'), ('limited', 'Limited Format'), ('freeplay', 'Casual Free-Play')],
        validators=[InputRequired()])
    start_time = DateTimeLocalField('Date & Start Time', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired(), Length(max=200)])
    image = SelectField('Banner Image', choices=[
        ('event-deck3v3.jpg', 'Preset: 3v3 Team Stadium Setup'),
        ('event-swiss.jpg', 'Preset: 1v1 Swiss'),
        ('event-freeplay.jpg', 'Preset: Casual Free-Play')])
    description = TextAreaField('Description', validators=[InputRequired()])
    point_cap = IntegerField('Match Point Cap', default=4, validators=[NumberRange(min=1)])
    gear_compliance = StringField('Gear Compliance', default='Official TT & Hasbro Legal')
    stadium = StringField('Arena Model', default='Xtreme Dash Stadium (BX-10)')
    capacity = IntegerField('Capacity', default=32, validators=[InputRequired(), NumberRange(min=1)])
    price = DecimalField('Registration Fee', places=2, default=15.00, validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Publish Tournament')

    country_acknowledgement = SelectField('Acknowledgement of Country Statement', choices=[
        ('generic', 'Acknowledgement of Country: Generic'),
        ('brisbane', 'Acknowledgement of Country: Turrbal & Jagera (Brisbane)')],
        validators=[InputRequired()])
    acknowledgement_details = StringField('Enhanced Statement Details (Optional)',
        validators=[Optional(), Length(max=300)])
    
    ACKNOWLEDGEMENTS = {
    'generic': 'We acknowledge the Traditional Owners of the land on which this event is held, and pay our respects to Elders past and present.',
    'brisbane': 'We acknowledge the Turrbal and Jagera peoples, the Traditional Owners of the land on which this event is held, and pay our respects to Elders past and present.',
    }

    def validate_date(self, field): #confirming that the date is not in the past
        if field.data < TournamentForm.date.today():
            raise ValidationError("The tournament date can't be in the past.")

=======
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

    ack_statement = SelectField('Acknowledgement of Country', choices=[
        ('none', 'No Acknowledgement'),
        ('generic', 'Use Generic Acknowledgement (Recommended)'),
        ('enhanced', 'Write a Custom/Enhanced Acknowledgement')
    ], default='none')
    
    custom_ack_text = TextAreaField('Custom Acknowledgement', render_kw={"placeholder": "E.g., We acknowledge the Turrbal and Yuggera peoples as the First Nations owners of the lands where this tournament takes place..."})

        
    description = TextAreaField('Description', validators=[DataRequired()])
    capacity = IntegerField('Capacity', default=32, validators=[DataRequired(), NumberRange(min=1)])
    price = DecimalField('Registration Fee', places=2, default=15.00, validators=[DataRequired(), NumberRange(min=0)])
    
    submit = SubmitField('Publish Tournament')

    def validate_start_time(self, field): 
        if field.data and field.data.date() < date.today():
            raise ValidationError("The tournament date can't be in the past.")
>>>>>>> 17910eb77816b19ac1557ed54c38289a13a7315e
