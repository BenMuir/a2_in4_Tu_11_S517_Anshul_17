from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AISearchForm(FlaskForm):
    search_query = StringField('What kind of tournament are you looking for?', validators=[DataRequired()])
    submit = SubmitField('Search with AI')