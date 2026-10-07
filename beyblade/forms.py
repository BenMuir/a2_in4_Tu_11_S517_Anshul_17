from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, EmailField, TelField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp


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
