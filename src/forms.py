from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    Buscar = StringField('Buscar', validators=[DataRequired()])
    submit = SubmitField('Buscar')
