from flask_wtf import FlaskForm
from wtforms import SubmitField


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Delete')
