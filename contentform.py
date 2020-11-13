from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,SubmitField
from wtforms.validators import DataRequired


class takinginputforcontent(FlaskForm):
    movie_name = StringField("movie_name",validators=[DataRequired()])
    user_rating = IntegerField("user_rating", validators=[DataRequired()])
    submit = SubmitField("Search")