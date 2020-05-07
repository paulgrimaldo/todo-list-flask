from flask_wtf import FlaskForm
from wtforms import SubmitField


class UpdateTodoStatusForm(FlaskForm):
    submit = SubmitField('Update')
