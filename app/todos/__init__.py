from flask import Blueprint

todos = Blueprint('todos', __name__, url_prefix='/todos')

from . import views
