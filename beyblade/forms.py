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

