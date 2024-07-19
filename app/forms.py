from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
  city_name = StringField('Введите город', validators=[DataRequired()])
  submit = SubmitField('Посмотреть')